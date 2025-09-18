#!/usr/bin/env python3
"""
Extract individual posts from Plex HTML issues and create a Massive Wiki.
Fixed version 2: Properly handle HR-based post splitting.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from collections import defaultdict
import unicodedata

def slugify(text, max_length=50):
    """Convert text to a valid filename."""
    if not text:
        return "Unknown"

    # Remove HTML tags if any
    text = re.sub(r'<[^>]+>', '', text)
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    # Remove non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Replace spaces and special chars with hyphens
    text = re.sub(r'[^\w\s\-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    text = text.strip('-')

    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length].rsplit('-', 1)[0]  # Break at word boundary

    return text or "Unknown"

def clean_html_to_markdown(html_content):
    """Convert HTML content to markdown with simpler approach."""

    # Simple regex-based conversion to avoid BeautifulSoup tree issues
    content = html_content

    # Convert headers
    for i in range(1, 7):
        content = re.sub(f'<h{i}[^>]*>(.*?)</h{i}>', f"{'#' * i} \\1\n", content, flags=re.DOTALL)

    # Convert common HTML tags to markdown
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
    content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.DOTALL)
    content = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL)
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
    content = re.sub(r'<br[^>]*/?>', '\n', content)
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', content, flags=re.DOTALL)
    content = re.sub(r'<ul[^>]*>', '', content)
    content = re.sub(r'</ul>', '\n', content)
    content = re.sub(r'<ol[^>]*>', '', content)
    content = re.sub(r'</ol>', '\n', content)

    # Handle images - replace with placeholder notice
    img_placeholder = "\n*[Image not included in the current archive. Images may be included in the future.]*\n\n"
    content = re.sub(r'<img[^>]*>', img_placeholder, content, flags=re.DOTALL)

    # Handle figure tags that often contain images
    content = re.sub(r'<figure[^>]*>.*?</figure>', img_placeholder, content, flags=re.DOTALL)

    # Remove remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)

    # Clean up whitespace and entities
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    content = re.sub(r'&nbsp;', ' ', content)
    content = re.sub(r'&amp;', '&', content)
    content = re.sub(r'&lt;', '<', content)
    content = re.sub(r'&gt;', '>', content)
    content = re.sub(r'&quot;', '"', content)

    return content.strip()

# Author name consolidation mapping
AUTHOR_CONSOLIDATION = {
    'George P': 'George Pór',
    'George Pór': 'George Pór',
    'Doug Carmichael': 'Douglass Carmichael',
    'Gil': 'Gil Friend',
    'Jack': 'Jack Park',
    'Jerry': 'Jerry Michalski',
    'Jordan Nicholas': 'Jordan Sukut',
    'Jordan Nicholas One': 'Jordan Sukut',
    'Marianne': 'Marianne Wyne',
    'Pete': 'Peter Kaminski',
    'Wendy E.': 'Wendy Elford',
    'Wendy E': 'Wendy Elford',
}

# Common topics that appear frequently in Plex posts
COMMON_TOPICS = {
    # Original 18 topics with improved keyword matching
    'AI and Technology': ['artificial intelligence', 'machine learning', 'generative AI', 'AI systems', 'digital transformation', 'automation', 'algorithms'],
    'Collective Intelligence': ['collective intelligence', 'collective wisdom', 'group intelligence', 'distributed cognition', 'swarm intelligence'],
    'Climate and Environment': ['climate change', 'environmental', 'carbon', 'greenhouse gas', 'biodiversity', 'extinction', 'global warming'],
    'Community Building': ['community building', 'social network', 'relationship building', 'trust building', 'social capital', 'belonging'],
    'Economics and Finance': ['doughnut economics', 'regenerative economics', 'economic justice', 'financial systems', 'wealth distribution', 'economic inequality'],
    'Education and Learning': ['education system', 'pedagogy', 'curriculum', 'student learning', 'educational reform', 'lifelong learning'],
    'Events and Gatherings': ['conference', 'summit', 'workshop', 'symposium', 'gathering', 'convening', 'meetup'],
    'Governance and Democracy': ['democratic governance', 'participatory democracy', 'civic engagement', 'policy making', 'political systems'],
    'Health and Wellbeing': ['mental health', 'wellbeing', 'wellness', 'healthcare', 'public health', 'healing'],
    'Identity and Self': ['personal identity', 'self-development', 'individual growth', 'self-awareness', 'personal transformation'],
    'Innovation and Creativity': ['creative process', 'design thinking', 'innovation systems', 'entrepreneurship', 'creative collaboration'],
    'Media and Communication': ['journalism', 'media literacy', 'communication theory', 'storytelling', 'information systems'],
    'Philosophy and Spirituality': ['philosophical inquiry', 'spiritual practice', 'contemplative', 'wisdom tradition', 'sacred', 'meaning-making'],
    'Science and Research': ['scientific research', 'empirical study', 'data analysis', 'methodology', 'evidence-based'],
    'Social Change': ['social transformation', 'social movement', 'activism', 'social justice', 'systemic change'],
    'Systems Thinking': ['systems theory', 'complex systems', 'systems design', 'holistic thinking', 'systemic approach'],
    'Tools and Platforms': ['software platform', 'digital tools', 'collaborative tools', 'wiki', 'mattermost', 'obsidian', 'technology stack'],
    'Work and Organizations': ['organizational design', 'workplace culture', 'leadership', 'team dynamics', 'organizational change'],

    # New 12 topic categories
    'Regenerative Systems and Agriculture': ['regenerative agriculture', 'permaculture', 'soil health', 'carbon sequestration', 'ecological restoration', 'regenerative farming', 'food systems'],
    'Wisdom Traditions and Ancient Knowledge': ['indigenous wisdom', 'traditional knowledge', 'ancestral practices', 'elder wisdom', 'ceremony', 'ritual', 'cultural preservation'],
    'Narrative and Storytelling': ['narrative change', 'storytelling', 'myth', 'cultural stories', 'shared stories', 'vision', 'futures thinking'],
    'Emergence and Complexity': ['emergence theory', 'complexity science', 'adaptive systems', 'self-organization', 'complex adaptive systems', 'emergent properties'],
    'Protocols and Coordination': ['coordination protocols', 'governance protocols', 'decision-making processes', 'organizational protocols', 'coordination mechanisms'],
    'Web3, DAOs, and Distributed Governance': ['web3', 'blockchain', 'DAOs', 'decentralized governance', 'distributed organizations', 'crypto', 'digital commons', 'token economics'],
    'Bioregionalism and Place-Based Practice': ['bioregion', 'place-based', 'local ecosystems', 'watershed', 'local governance', 'regional networks', 'geographic communities'],
    'Metamodern and Integral Approaches': ['metamodern', 'integral', 'developmental stages', 'spiral dynamics', 'post-postmodern', 'liminal', 'both/and thinking'],
    'Network Weaving and Connecting': ['network weaving', 'connector', 'boundary spanning', 'cross-pollination', 'bridge building', 'relationship weaving', 'network effects'],
    'Sensemaking and Collective Intelligence': ['sensemaking', 'collective sensemaking', 'shared understanding', 'distributed cognition', 'group intelligence'],
    'Future Visioning and Scenario Planning': ['future visioning', 'scenario planning', 'alternative futures', 'visionary thinking', 'long-term thinking'],
    'Hosting and Facilitation': ['hosting', 'facilitation', 'convening', 'stewardship', 'holding space', 'process design', 'dialogue facilitation']
}

# Hardcoded list of known Plex community authors
# Based on "Kith and Kin" section from 2025-09-04 issue and "Name Key" from 2022-02-03
KNOWN_AUTHORS = {
    # Complete list from "Kith and Kin" (2025-09-04)
    'John Abbe', 'Vincent Arena', 'Bill Anderson', 'Judith Benham', 'Mark Bernstein',
    'Charles Blass', 'David Bovill', 'Douglass Carmichael', 'Patti Cobian', 'Joe Corneli',
    'Brad deGraf', 'Stacey Druss', 'Wendy Elford', 'Chris Felstead', 'Pete Forsyth',
    'Gil Friend', 'Kylie Stedman Gomes', 'Julian Gómez', 'Michael Grossman', 'Cody Harrison',
    'Ken Homer', 'Todd Hoskins', 'Kaliya Identity Woman', 'Chochi Iturralde', 'Kevin Jones',
    'John Kelly', 'Hank Kune', 'Jon Lebkowsky', 'Jose Leal', 'Stewart Levine',
    'Michael Lennon', 'Boris Mann', 'Klaus Mager', 'Wendy McLean', 'Jerry Michalski',
    'Scott Moehring', 'Jack Park', 'Linda Park', 'George Pór', 'Grace Rachmany',
    'Jonathan Sand', 'Killu Sanborn', 'Doc Searls', 'Sam Schikowitz', 'Jordan Sukut',
    'Shaun Swanson', 'Jamaica Stevens', 'Tibet Sprague', 'Jessie Upp', 'David Witzel',
    'Marianne Wyne', 'Peter Kaminski',

    # Additional from Name Key and other sources
    'Bentley Davis', 'Marc-Antoine Parent', 'Rob O\'Keefe', 'Sam Rose', 'Jordan Nicholas',
    'Nora Bateson', 'Forrist Lytehaause',

    # Alternative name formats and nicknames
    'Pete', 'Jerry', 'Ken', 'Charles', 'Gil', 'Todd', 'Klaus', 'Brad', 'Jack',
    'Wendy E.', 'Wendy M.', 'Jordan Nicholas One', 'Doug Carmichael', 'Marianne',
    'Holly', 'Wendy Ed', 'George P', 'George Pór',

    # Organization/project names that might appear as authors
    'Collective Sense Commons', 'The Meta Project', 'Unknown'
}

def find_best_author_match(text):
    """Find the best matching author from our known list with consolidation."""
    text = text.lower()

    # First check for exact consolidation matches (case-insensitive)
    for old_name, new_name in AUTHOR_CONSOLIDATION.items():
        if old_name.lower() in text:
            return new_name

    # Try exact matches first (longer names first to avoid partial matches)
    for author in sorted(KNOWN_AUTHORS, key=len, reverse=True):
        if author.lower() in text:
            return author

    # Try partial matches for compound names
    words = text.split()
    for author in KNOWN_AUTHORS:
        author_words = author.lower().split()
        if len(author_words) >= 2 and all(word in words for word in author_words):
            return author

    return "Unknown"

def extract_author_from_content(content_soup, raw_content):
    """Extract author name from post content using hardcoded known authors."""

    # Get all text content
    full_text = content_soup.get_text()

    # Method 1: Look for "by **Author Name**" pattern
    author_matches = re.findall(r'by\s+\*\*([^*]+)\*\*', full_text, re.IGNORECASE)
    for match in author_matches:
        author = find_best_author_match(match)
        if author != "Unknown":
            return author

    # Method 2: Look for "by Author Name" pattern (prioritize full names)
    author_matches = re.findall(r'by\s+([A-Z][a-zA-Z\s\u00C0-\u024F]+)', full_text)
    for match in author_matches:
        author = find_best_author_match(match)
        # Prioritize full names (2+ words) to avoid short name false positives like "Brad"
        if author != "Unknown" and len(author.split()) >= 2:
            return author

    # Method 2b: Single name patterns from "by Author Name" (lower priority)
    for match in author_matches:
        author = find_best_author_match(match)
        if author != "Unknown":
            return author

    # Method 3: Look for known full names anywhere in the content (avoid single-word matches)
    for author in sorted(KNOWN_AUTHORS, key=len, reverse=True):
        if len(author.split()) >= 2 and author.lower() in full_text.lower():
            return author

    # Method 4: Look for any known author names anywhere in the content (last resort)
    author = find_best_author_match(full_text)
    if author != "Unknown":
        return author

    # Method 5: Check for h3 tags that might contain author info
    for h3 in content_soup.find_all('h3'):
        author = find_best_author_match(h3.get_text())
        if author != "Unknown":
            return author

    return "Unknown"

def detect_topics(content_text):
    """Detect topics based on keywords in content with improved accuracy."""
    content_lower = content_text.lower()
    detected_topics = []

    for topic, keywords in COMMON_TOPICS.items():
        topic_score = 0
        matches = []

        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in content_lower:
                # Count occurrences for better confidence
                count = content_lower.count(keyword_lower)
                topic_score += count
                matches.append((keyword, count))

        # Only add topic if we have sufficient confidence
        # Require either multiple matches or strong single match
        if topic_score >= 2 or (topic_score == 1 and any(count > 1 for _, count in matches)):
            detected_topics.append(topic)
        # Special case for very specific multi-word phrases
        elif any(len(keyword.split()) >= 2 and keyword.lower() in content_lower for keyword in keywords):
            detected_topics.append(topic)

    return detected_topics

def extract_posts_from_issue(html_file_path):
    """Extract individual posts from an HTML issue file using proper HTML splitting."""
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Extract slug from meta information (preferred) or fallback to filename
    slug = None
    meta_div = soup.find('div', class_='meta')
    if meta_div:
        # Look for paragraph containing "Slug:"
        for p in meta_div.find_all('p'):
            if 'Slug:' in p.get_text():
                slug = p.get_text().replace('Slug:', '').strip()
                break

    # Fallback to extracting date from filename if slug not found
    if not slug:
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', str(html_file_path))
        slug = date_match.group(1) if date_match else '1970-01-01'

    issue_slug = slug

    # Find the content div
    content_div = soup.find('div', class_='content')
    if not content_div:
        print(f"No content div found in {html_file_path}")
        return []

    # Convert to string to work with regex splitting
    content_html = str(content_div)

    # Split by HR tags using regex
    sections = re.split(r'<hr[^>]*/?>', content_html)

    posts = []

    for i, section in enumerate(sections):
        if not section.strip():
            continue

        # Parse each section
        section_soup = BeautifulSoup(section, 'html.parser')

        # Find the first h2 as post title
        h2 = section_soup.find('h2')
        if not h2:
            continue

        title = h2.get_text().strip()

        # Skip common non-post sections
        skip_titles = ['in this issue', 'thank you', 'special thanks', 'name key', 'welcome to']
        if any(skip in title.lower() for skip in skip_titles):
            continue

        # Extract author
        author = extract_author_from_content(section_soup, section)

        # Convert to markdown
        markdown_content = clean_html_to_markdown(section)

        # Detect topics
        full_content = title + " " + markdown_content
        detected_topics = detect_topics(full_content)

        # Clean up the title
        clean_title = re.sub(r'[^\w\s\-.,!?]', '', title).strip()

        posts.append({
            'title': clean_title,
            'author': author,
            'content': markdown_content,
            'issue_slug': issue_slug,
            'raw_title': title,
            'topics': detected_topics
        })

        print(f"  Found post: '{clean_title}' by {author}")

    return posts

def create_wiki_structure():
    """Create the Massive Wiki structure."""

    # Determine paths based on current working directory
    if Path.cwd().name == 'scripts':
        base_dir = Path('..')  # Run from scripts/
        issues_dir = Path('../issues')
    else:
        base_dir = Path('.')   # Run from project root
        issues_dir = Path('issues')

    # Create directory structure
    dirs = ['posts', 'authors', 'topics', 'years']

    for dir_name in dirs:
        (base_dir / dir_name).mkdir(parents=True, exist_ok=True)

    # Track data for indexes
    all_posts = []
    authors = defaultdict(list)
    years = defaultdict(list)
    topics = defaultdict(list)

    # Process each HTML file
    html_files = list(issues_dir.glob('*.html'))

    print(f"Processing {len(html_files)} HTML files...")

    for html_file in sorted(html_files):
        print(f"Processing {html_file}")

        posts = extract_posts_from_issue(html_file)

        for post in posts:
            # Create filename: YYYY-MM-DD_Post-Author-Name_Title.md
            author_slug = slugify(post['author'], max_length=30)
            title_slug = slugify(post['title'], max_length=40)
            filename = f"{post['issue_slug']}_Post-{author_slug}_{title_slug}.md"

            # Create post content with metadata
            topics_list = [f"'{topic}'" for topic in post['topics']]
            topics_str = '[' + ', '.join(topics_list) + ']'

            post_content = f"""---
title: "{post['title']}"
author: "{post['author']}"
issue_slug: "{post['issue_slug']}"
tags: {topics_str}
---

# {post['title']}

**Author:** [[{post['author']}]]
**Issue:** [{post['issue_slug']}](https://plex.collectivesensecommons.org/{post['issue_slug']}/)

---

{post['content']}

---

**Related:**
- [[{post['author']}]] (author)
- [[{post['issue_slug'][:4]}]] (year)
- Topics: {', '.join(f"[[{topic}]]" for topic in post['topics'])}

"""

            # Write post file
            post_path = base_dir / 'posts' / filename
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(post_content)

            # Track for indexes
            post['filename'] = filename
            all_posts.append(post)
            authors[post['author']].append(post)
            years[post['issue_slug'][:4]].append(post)

            # Add to topic lists
            for topic in post['topics']:
                topics[topic].append(post)

            print(f"  Created: {filename}")

    # Create author index pages
    print("Creating author index pages...")
    for author, author_posts in authors.items():
        # Use author name with spaces for filename (no slugification for authors)
        author_filename = author + ".md"
        author_content = f"""---
title: "{author}"
type: "author"
---

# {author}

**Posts by {author}:**

"""
        for post in sorted(author_posts, key=lambda x: x['issue_slug']):
            author_content += f"- [[{post['filename'][:-3]}|{post['title']}]] ({post['issue_slug']})\n"

        author_content += f"\n**Total posts:** {len(author_posts)}\n"

        author_path = base_dir / 'authors' / author_filename
        with open(author_path, 'w', encoding='utf-8') as f:
            f.write(author_content)

    # Create year index pages
    print("Creating year index pages...")
    for year, year_posts in years.items():
        year_content = f"""---
title: "{year}"
type: "year"
---

# {year}

**Posts from {year}:**

"""
        for post in sorted(year_posts, key=lambda x: x['issue_slug']):
            year_content += f"- [[{post['filename'][:-3]}|{post['title']}]] by [[{post['author']}]] ({post['issue_slug']})\n"

        year_content += f"\n**Total posts:** {len(year_posts)}\n"

        year_path = base_dir / 'years' / f"{year}.md"
        with open(year_path, 'w', encoding='utf-8') as f:
            f.write(year_content)

    # Create topic index pages
    print("Creating topic index pages...")
    for topic, topic_posts in topics.items():
        topic_filename = topic + ".md"
        topic_content = f"""---
title: "{topic}"
type: "topic"
---

# {topic}

**Posts about {topic}:**

"""
        for post in sorted(topic_posts, key=lambda x: x['issue_slug']):
            topic_content += f"- [[{post['filename'][:-3]}|{post['title']}]] by [[{post['author']}]] ({post['issue_slug']})\n"

        topic_content += f"\n**Total posts:** {len(topic_posts)}\n"

        topic_path = base_dir / 'topics' / topic_filename
        with open(topic_path, 'w', encoding='utf-8') as f:
            f.write(topic_content)

    # Create main README
    print("Creating main README...")
    year_range = f"{min(years.keys())}-{max(years.keys())}" if years else "No years found"

    readme_content = f"""# Plex Archive

Welcome to the Plex Archive - a Massive Wiki containing posts from the [Biweekly Plex Dispatch](https://plex.collectivesensecommons.org/) published by Pete from 2022 to 2025.

This is a work in progress. The archive has been created from the original HTML pages by a Python script written by Claude Code, directed by Peter Kaminski. There are extraction / conversion errors, including attribution errors. Watch for updates to this wiki, and feel free to [email Pete](mailto:kaminski@istori.com) with comments or suggestions.

There is a [zip of all posts](/plex-archive-posts.zip) in Markdown format, useful for archiving or processing with AI.

## Overview

- **Total Posts:** {len(all_posts)}
- **Authors:** {len(authors)}
- **Topics:** {len(topics)}
- **Years Covered:** {year_range}

## Navigation

### TODO: where we have ` posts)\n"`, add code to say ` post)\n` instead if the count is 1

### By Author
"""

    for author in sorted(authors.keys()):
        readme_content += f"- [[{author}|{author}]] ({len(authors[author])} posts)\n"

    readme_content += "\n### By Topic\n"
    for topic in sorted(topics.keys()):
        readme_content += f"- [[{topic}|{topic}]] ({len(topics[topic])} posts)\n"

    readme_content += "\n### By Year\n"
    for year in sorted(years.keys()):
        readme_content += f"- [[{year}]] ({len(years[year])} posts)\n"

    readme_content += f"""

### Recent Posts

"""

    # Show last 10 posts
    recent_posts = sorted(all_posts, key=lambda x: x['issue_slug'], reverse=True)[:10]
    for post in recent_posts:
        readme_content += f"- [[{post['filename'][:-3]}|{post['title']}]] by [[{post['author']}]] ({post['issue_slug']})\n"

    readme_path = base_dir / 'README.md'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    # Create index files
    print("Creating index files...")

    # Create Authors.md index
    authors_index_content = f"""---
title: "Authors"
type: "index"
---

# Authors

All {len(authors)} contributors to the Plex Archive.

"""
    for author in sorted(authors.keys()):
        authors_index_content += f"- [[{author}]] ({len(authors[author])} posts)\n"

    authors_index_path = base_dir / 'authors' / 'Authors.md'
    with open(authors_index_path, 'w', encoding='utf-8') as f:
        f.write(authors_index_content)

    # Create Topics.md index
    topics_index_content = f"""---
title: "Topics"
type: "index"
---

# Topics

All {len(topics)} topic categories in the Plex Archive.

"""
    for topic in sorted(topics.keys()):
        topics_index_content += f"- [[{topic}]] ({len(topics[topic])} posts)\n"

    topics_index_path = base_dir / 'topics' / 'Topics.md'
    with open(topics_index_path, 'w', encoding='utf-8') as f:
        f.write(topics_index_content)

    # Create Years.md index
    years_index_content = f"""---
title: "Years"
type: "index"
---

# Years

All {len(years)} years covered in the Plex Archive ({year_range}).

"""
    for year in sorted(years.keys()):
        years_index_content += f"- [[{year}]] ({len(years[year])} posts)\n"

    years_index_path = base_dir / 'years' / 'Years.md'
    with open(years_index_path, 'w', encoding='utf-8') as f:
        f.write(years_index_content)

    # Create issues/index.html
    issues_index_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plex Archive - Original HTML Issues</title>
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
        .file-list {{
            list-style: none;
            padding: 0;
        }}
        .file-list li {{
            margin: 10px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
        }}
        .file-list a {{
            color: #2c3e50;
            text-decoration: none;
            font-weight: bold;
        }}
        .file-list a:hover {{
            text-decoration: underline;
        }}
        .back-link {{
            margin: 20px 0;
            font-size: 16px;
        }}
    </style>
</head>
<body>
    <h1>Original HTML Issues</h1>

    <div class="back-link">
        <a href="../README.md">← Back to Plex Archive</a>
    </div>

    <p>These are the original HTML files extracted from the Biweekly Plex Dispatch archives. Each file contains multiple posts from a single issue.</p>

    <p><strong>Total Issues:</strong> {len(list(issues_dir.glob('*.html'))) if issues_dir.exists() else 0}</p>

    <ul class="file-list">"""

    # Add HTML files in reverse chronological order
    html_files = []
    if issues_dir.exists():
        html_files = sorted(list(issues_dir.glob('*.html')), reverse=True)

    for html_file in html_files:
        # Extract date from filename for display
        date_str = html_file.stem  # Gets filename without .html
        issues_index_content += f"""
        <li>
            <a href="{html_file.name}">{date_str}</a>
        </li>"""

    issues_index_content += f"""
    </ul>

    <div class="back-link">
        <a href="../README.md">← Back to Plex Archive</a>
    </div>

    <hr>
    <p style="text-align: center; color: #666; font-size: 14px;">
        Generated by Claude Code • Plex Archive
    </p>
</body>
</html>"""

    issues_index_path = issues_dir / 'index.html'
    with open(issues_index_path, 'w', encoding='utf-8') as f:
        f.write(issues_index_content)

    print(f"\n✅ Archive created successfully!")
    print(f"📁 Location: {base_dir.absolute()}")
    print(f"📊 Extracted {len(all_posts)} posts from {len(authors)} authors across {len(years)} years")
    print(f"🏷️  Identified {len(topics)} topics across all posts")

if __name__ == '__main__':
    create_wiki_structure()
