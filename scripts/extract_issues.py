#!/usr/bin/env python3
import json
import re
import os

# Load the JSON file
with open('biweekly-plex-dispatch.ghost.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract posts
issues = data['db'][0]['data']['posts']
print(f"Found {len(issues)} issues")

# Create posts directory
os.makedirs('issues', exist_ok=True)

for i, issue in enumerate(issues):
    title = issue.get('title', f'Post_{i}')
    slug = issue.get('slug', f'issue_{i}')
    html_content = issue.get('html', '')
    
    # Clean title for filename (remove problematic characters)
    safe_title = re.sub(r'[^\w\s-]', '', title).strip()
    safe_title = re.sub(r'[-\s]+', '-', safe_title)
    
    filename = f"issues/{slug}_{safe_title}.html"
    
    # Write HTML file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>{title}</title>\n</head>\n<body>\n")
        f.write(f"<h1>{title}</h1>\n")
        f.write(html_content)
        f.write("\n</body>\n</html>")
    
print(f"Extracted {len(issues)} HTML files")

print("Done! Check 'issues/' directory for HTML files.")
