# HTML Media Extractor and Archiver

A Python script for extracting media URLs from HTML files and optionally downloading them while preserving directory structure.

## Features

- **Comprehensive URL Detection**: Finds media URLs from multiple sources including:
  - `<img src="">` attributes
  - `<video src="">` and `poster=""` attributes
  - `<source src="">` elements (for audio/video)
  - `srcset` attributes (responsive images)
  - `data-src` attributes (lazy loading)
  - CSS `url()` references in style attributes and tags
  - CSS background-image properties
  
- **Template Placeholder Support**: Automatically replaces `__GHOST_URL__` placeholders with your base URL

- **Smart File Organization**: When downloading files:
  - Preserves directory structure based on URL paths
  - Creates folder hierarchy mimicking source domains
  - Sanitizes filenames for safe filesystem storage
  - Handles relative URLs when base URL is provided

- **Robust Downloading**:
  - Connection pooling for improved performance
  - Comprehensive error handling
  - Progress reporting with detailed output
  - Skips already downloaded files
  - Respectful delays between requests

## Installation

### Prerequisites

- Python 3.6 or higher
- Required packages:

```bash
pip3 install beautifulsoup4 requests
```

### Download

Save the script as `html_media_extractor.py` and make it executable:

```bash
chmod +x html_media_extractor.py
```

## Usage

### Basic Syntax

```bash
python3 html_media_extractor.py [directory] [options]
```

### Arguments

- `directory`: Directory containing HTML files (required)
- `-o, --output`: Output file for URLs (default: `media_urls.txt`)
- `-d, --download`: Download directory (optional)
- `-b, --base-url`: Base URL for resolving relative URLs and replacing `__GHOST_URL__`

### Examples

#### 1. Extract URLs Only

Extract all media URLs from HTML files and save to text file:

```bash
python3 html_media_extractor.py /path/to/html/files
```

This creates `media_urls.txt` with all found URLs.

#### 2. Extract and Download

Extract URLs and download all media files:

```bash
python3 html_media_extractor.py /path/to/html/files -d ./media_archive
```

#### 3. With Base URL (Recommended)

Handle relative URLs and `__GHOST_URL__` placeholders:

```bash
python3 html_media_extractor.py /path/to/html/files \
  -b https://example.com \
  -d ./archive \
  -o extracted_urls.txt
```

#### 4. For Ghost CMS / Plex Files

Specifically for Ghost CMS exports or similar:

```bash
python3 html_media_extractor.py issues \
  -d ./plex_media_archive \
  -b https://plex.collectivesensecommons.org \
  -o plex_urls.txt
```

## Output

### URL List File

The script creates a text file containing all unique URLs found, sorted alphabetically:

```
https://example.com/content/images/2025/09/image1.jpg
https://example.com/content/media/2025/09/video1.mp4
/content/images/local-image.png
```

### Download Directory Structure

When downloading, files are organized by domain and path:

```
media_archive/
├── example.com/
│   ├── content/
│   │   ├── images/
│   │   │   └── 2025/
│   │   │       └── 09/
│   │   │           └── image1.jpg
│   │   └── media/
│   │       └── 2025/
│   │           └── 09/
│   │               └── video1.mp4
│   └── static/
│       └── style.css
```

### Console Output

The script provides detailed progress information:

```
Found 3 HTML files to process

Processing: article1.html
  Replaced __GHOST_URL__ with https://example.com
  Found 12 media URLs

Processing: article2.html
  Found 8 media URLs

Writing 18 unique URLs to media_urls.txt

Downloading files to ./archive

[1/18] Processing: https://example.com/image1.jpg
  Downloading: https://example.com/image1.jpg -> archive/example.com/image1.jpg

[2/18] Processing: https://example.com/video1.mp4
  Already exists: archive/example.com/video1.mp4
```

## Supported URL Types

### Image Formats
- Standard img tags: `<img src="image.jpg">`
- Responsive images: `<img srcset="image-small.jpg 480w, image-large.jpg 800w">`
- Lazy loading: `<img data-src="image.jpg">`

### Video/Audio Formats
- Video sources: `<video src="video.mp4">`
- Video posters: `<video poster="thumbnail.jpg">`
- Source elements: `<source src="audio.mp3">`

### CSS References
- Style attributes: `<div style="background-image: url('bg.jpg')">`
- Style tags: `<style>.class { background: url('bg.jpg'); }</style>`

### Template Placeholders
- Ghost CMS: `__GHOST_URL__/content/images/image.jpg`

## Error Handling

The script handles various error conditions gracefully:

- **Missing directories**: Clear error message if HTML directory doesn't exist
- **Unreadable files**: Continues processing other files if one fails
- **Download failures**: Reports errors but continues with remaining files
- **Network issues**: Timeout handling and retry logic
- **Invalid URLs**: Filters out malformed URLs and data URIs

## Performance Notes

- Uses connection pooling to improve download performance
- Includes small delays between requests to be respectful to servers
- Skips files that already exist locally
- Processes files in batches for memory efficiency

## Troubleshooting

### No URLs Found
- Check that HTML files contain media references
- Verify the base URL is correct for relative links
- Ensure HTML files are valid and parseable

### Download Failures
- Check internet connection
- Verify URLs are accessible (not behind authentication)
- Some servers may block automated requests

### Permission Errors
- Ensure write permissions in output directory
- Check that filenames don't contain invalid characters

## License

This script is provided as-is for archival and backup purposes. Respect copyright and terms of service when downloading content.
