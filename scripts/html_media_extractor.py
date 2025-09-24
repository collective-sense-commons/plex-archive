#!/usr/bin/env python3
"""
HTML Media URL Extractor and Archiver

This script scans HTML files in a directory for media URLs (images, videos, etc.)
and can optionally download them while preserving directory structure.
"""

import os
import re
import requests
import argparse
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time


def extract_media_urls(html_content, base_url=None):
    """
    Extract media URLs from HTML content.
    
    Args:
        html_content (str): HTML content to parse
        base_url (str): Base URL to resolve relative URLs and replace __GHOST_URL__
    
    Returns:
        set: Set of unique media URLs found
    """
    # Replace __GHOST_URL__ placeholder with base_url if provided
    if base_url and '__GHOST_URL__' in html_content:
        html_content = html_content.replace('__GHOST_URL__', base_url.rstrip('/'))
        print(f"  Replaced __GHOST_URL__ with {base_url}")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    urls = set()
    
    # Find img src attributes
    for img in soup.find_all('img', src=True):
        urls.add(img['src'])
    
    # Find video src attributes
    for video in soup.find_all('video', src=True):
        urls.add(video['src'])
    
    # Find source elements (for video/audio)
    for source in soup.find_all('source', src=True):
        urls.add(source['src'])
    
    # Find poster attributes in video tags
    for video in soup.find_all('video', poster=True):
        urls.add(video['poster'])
    
    # Find srcset attributes (responsive images)
    for element in soup.find_all(attrs={'srcset': True}):
        srcset = element['srcset']
        # Parse srcset format: "url1 descriptor, url2 descriptor, ..."
        for src_desc in srcset.split(','):
            url = src_desc.strip().split()[0]
            urls.add(url)
    
    # Find data-src attributes (lazy loading)
    for element in soup.find_all(attrs={'data-src': True}):
        urls.add(element['data-src'])
    
    # Find CSS url() references in style attributes and style tags
    css_url_pattern = r'url\([\'"]?([^\'"\)]+)[\'"]?\)'
    
    # Check style attributes
    for element in soup.find_all(style=True):
        matches = re.findall(css_url_pattern, element['style'])
        urls.update(matches)
    
    # Check style tags
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            matches = re.findall(css_url_pattern, style_tag.string)
            urls.update(matches)
    
    # Find background-image in CSS
    bg_pattern = r'background(?:-image)?\s*:\s*url\([\'"]?([^\'"\)]+)[\'"]?\)'
    for element in soup.find_all(style=True):
        matches = re.findall(bg_pattern, element['style'])
        urls.update(matches)
    
    # Convert relative URLs to absolute if base_url provided
    if base_url:
        absolute_urls = set()
        for url in urls:
            absolute_url = urljoin(base_url, url)
            absolute_urls.add(absolute_url)
        urls = absolute_urls
    
    # Filter out data URLs and other non-http(s) schemes
    filtered_urls = set()
    for url in urls:
        if url.startswith(('http://', 'https://', '//', '/')):
            filtered_urls.add(url)
        elif not url.startswith(('data:', 'javascript:', 'mailto:')):
            # Relative URLs without base_url
            filtered_urls.add(url)
    
    return filtered_urls


def sanitize_filename(filename):
    """
    Sanitize filename for safe filesystem storage.
    """
    # Replace problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple consecutive underscores
    filename = re.sub(r'_+', '_', filename)
    return filename


def get_file_extension_from_url(url):
    """
    Extract file extension from URL, handling query parameters.
    """
    parsed = urlparse(url)
    path = parsed.path
    if '.' in path:
        return os.path.splitext(path)[1]
    return ''


def download_file(url, local_path, session=None):
    """
    Download a file from URL to local path.
    
    Args:
        url (str): URL to download
        local_path (Path): Local path to save file
        session (requests.Session): Optional session for connection pooling
    
    Returns:
        bool: True if download successful, False otherwise
    """
    if session is None:
        session = requests
    
    try:
        # Create directory if it doesn't exist
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Skip if file already exists
        if local_path.exists():
            print(f"  Already exists: {local_path}")
            return True
        
        print(f"  Downloading: {url} -> {local_path}")
        
        response = session.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
        
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        return False


def process_html_files(directory, output_file, download_dir=None, base_url=None):
    """
    Process all HTML files in directory and extract media URLs.
    
    Args:
        directory (str): Directory containing HTML files
        output_file (str): Output text file for URLs
        download_dir (str): Optional directory to download files to
        base_url (str): Base URL for resolving relative URLs
    """
    html_dir = Path(directory)
    all_urls = set()
    
    if not html_dir.exists():
        print(f"Error: Directory {directory} does not exist")
        return
    
    # Find all HTML files
    html_files = list(html_dir.glob('*.html')) + list(html_dir.glob('*.htm'))
    
    if not html_files:
        print(f"No HTML files found in {directory}")
        return
    
    print(f"Found {len(html_files)} HTML files to process")
    
    # Process each HTML file
    for html_file in html_files:
        print(f"\nProcessing: {html_file.name}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            urls = extract_media_urls(content, base_url)
            print(f"  Found {len(urls)} media URLs")
            all_urls.update(urls)
            
        except Exception as e:
            print(f"  Error reading {html_file}: {e}")
    
    # Write URLs to output file
    print(f"\nWriting {len(all_urls)} unique URLs to {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        for url in sorted(all_urls):
            f.write(url + '\n')
    
    # Download files if requested
    if download_dir:
        download_path = Path(download_dir)
        download_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\nDownloading files to {download_dir}")
        
        # Use session for connection pooling
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        downloaded = 0
        failed = 0
        
        for i, url in enumerate(sorted(all_urls), 1):
            print(f"\n[{i}/{len(all_urls)}] Processing: {url}")
            
            # Parse URL to create local path
            parsed = urlparse(url)
            
            # Handle different URL formats
            if url.startswith('//'):
                url = 'https:' + url
            elif url.startswith('/'):
                if base_url:
                    url = urljoin(base_url.rstrip('/'), url)
                else:
                    print(f"  Skipping relative URL (no base_url): {url}")
                    continue
            
            # Create local file path
            if parsed.path:
                # Preserve directory structure
                local_path = download_path / parsed.netloc / parsed.path.lstrip('/')
                
                # Ensure we have a filename
                if local_path.is_dir() or not local_path.suffix:
                    # Generate filename from URL
                    filename = parsed.path.split('/')[-1] or 'index'
                    if not get_file_extension_from_url(url):
                        # Try to guess extension from URL or use generic
                        filename += '.bin'
                    local_path = local_path / filename
            else:
                # No path in URL, create filename from domain and query
                filename = f"{parsed.netloc}_{hash(url)}{get_file_extension_from_url(url) or '.bin'}"
                filename = sanitize_filename(filename)
                local_path = download_path / filename
            
            # Sanitize the final path
            local_path = Path(str(local_path).replace('..', '_'))
            
            # Download the file
            if download_file(url, local_path, session):
                downloaded += 1
            else:
                failed += 1
            
            # Small delay to be respectful to servers
            time.sleep(0.1)
        
        print(f"\nDownload complete: {downloaded} successful, {failed} failed")


def main():
    parser = argparse.ArgumentParser(
        description="Extract media URLs from HTML files and optionally download them"
    )
    parser.add_argument(
        'directory',
        help="Directory containing HTML files"
    )
    parser.add_argument(
        '-o', '--output',
        default='media_urls.txt',
        help="Output file for URLs (default: media_urls.txt)"
    )
    parser.add_argument(
        '-d', '--download',
        help="Download directory (optional)"
    )
    parser.add_argument(
        '-b', '--base-url',
        help="Base URL for resolving relative URLs"
    )
    
    args = parser.parse_args()
    
    process_html_files(
        args.directory,
        args.output,
        args.download,
        args.base_url
    )


if __name__ == '__main__':
    main()
