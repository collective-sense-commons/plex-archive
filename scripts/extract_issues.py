#!/usr/bin/env python3
"""
Extract issues from Ghost export JSON and create individual HTML files.
Handle duplicates by adding sequence numbers.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

def extract_issues():
    # Find the Ghost export file
    ghost_files = list(Path('.').glob('biweekly-plex-dispatch.ghost*.json'))
    if not ghost_files:
        print("No Ghost export file found")
        return

    ghost_file = ghost_files[0]
    print(f"Processing {ghost_file}")

    # Load and parse JSON
    with open(ghost_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    issues = data['db'][0]['data']['posts']
    print(f"Found {len(issues)} total issues")

    # Filter out pages, keep only issues
    actual_issues = [p for p in issues if p.get('type') != 'page']
    print(f"Found {len(actual_issues)} actual issues (excluding pages)")

    # Create output directory
    output_dir = Path('issues')
    output_dir.mkdir(exist_ok=True)

    # Track filenames to handle duplicates
    filename_counter = defaultdict(int)

    # Identify oddball issues to skip
    oddball_titles = {
        'Updates for Plex: 1 March 2023',
        'Midjourney Wrangler',
        'test issue',
        'test post',
        'automation testing'
    }

    for issue in actual_issues:
        title = issue.get('title', 'Untitled')

        # Skip oddball issues
        if title in oddball_titles:
            print(f"Skipping oddball issue: {title}")
            continue

        # Extract date from published_at or created_at
        date_str = issue.get('published_at') or issue.get('created_at')
        if date_str:
            # Parse ISO date string
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            base_filename = date_obj.strftime('%Y-%m-%d')
        else:
            # Fallback to slug if no date
            base_filename = issue.get('slug', 'untitled')

        # Handle duplicate filenames
        filename_counter[base_filename] += 1
        if filename_counter[base_filename] > 1:
            filename = f"{base_filename}-{filename_counter[base_filename]}.html"
        else:
            filename = f"{base_filename}.html"

        # Create HTML content
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Georgia, serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .meta {{
            color: #666;
            font-style: italic;
            margin-bottom: 20px;
        }}
        .content {{
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="meta">
        <p>Published: {date_obj.strftime('%B %d, %Y') if date_str else 'Unknown'}</p>
        {f'<p>Slug: {issue.get("slug")}</p>' if issue.get('slug') else ''}
        {f'<p>Excerpt: {issue.get("custom_excerpt")}</p>' if issue.get('custom_excerpt') else ''}
        {f'<p>Status: {issue.get("status")}</p>' if issue.get('status') else ''}
    </div>
    <div class="content">
{issue.get('html', '<p>No content available</p>')}
    </div>
</body>
</html>"""

        # Write file
        output_path = output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Created: {output_path}")

    print(f"\nSummary:")
    print(f"- Total issues processed: {len(actual_issues)}")
    print(f"- Oddball issues skipped: {len(oddball_titles)}")
    print(f"- HTML files created: {len(list(output_dir.glob('*.html')))}")

if __name__ == '__main__':
    extract_issues()
