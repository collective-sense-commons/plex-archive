# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains the Plex Archive - a Massive Wiki containing posts from the Biweekly Plex Dispatch published by Pete from 2022 to 2025. The archive has been created from original HTML files by Python scripts written by Claude Code.

## File Structure

- `issues/` - Original HTML files from the Biweekly Plex Dispatch archives (87 issues)
- `posts/` - Individual markdown posts extracted from HTML (614 posts)
- `authors/` - Author pages and index (53 contributors)
- `topics/` - Topic category pages and index (30 categories)
- `years/` - Year-based organization (2022-2025)
- `scripts/` - Python extraction and processing scripts
- `README.md` - Main archive overview and navigation
- `Sidebar.md` - Wiki sidebar navigation
- `Project.md` - Project documentation and structure
- `netlify.toml` - Netlify deployment configuration

## Key Scripts

### `/scripts/extract_posts.py`
Main extraction script that processes HTML files and generates the Massive Wiki structure:
- Extracts individual posts from HTML files using BeautifulSoup
- Uses slug metadata (preferred) or filename parsing for post naming
- Generates markdown files with YAML frontmatter
- Creates index files for authors, topics, years, and issues
- Links to original Plex website: `https://plex.collectivesensecommons.org/{slug}/`

### `/scripts/cleanup.py`
Utility script to clean generated content while preserving important files:
- Removes generated directories: posts, authors, topics, years
- Preserves "Contact Peter Kaminski.md"

## Content Structure

Posts are organized with:
- **Slug-based naming**: Uses slug from HTML meta (e.g., `2022-06-15`)
- **Cross-linking**: Authors and topics are linked using wiki-style `[[Author Name]]` syntax
- **YAML frontmatter**: Contains title, author, issue_slug, and tags
- **Issue linking**: Links to original posts on Plex website

## Common Commands

- **Regenerate archive**: `python scripts/extract_posts.py`
- **Clean generated content**: `python scripts/cleanup.py`
- **View structure**: Check README.md for current stats and navigation

## Archive Statistics

- **Total Posts:** 614
- **Authors:** 53
- **Topics:** 30
- **Years Covered:** 2022-2025
- **Issues:** 87

## Notes

- Archive uses slug-based dating instead of published dates for consistency
- All posts link back to original Plex website for reference
- Massive Wiki format enables cross-referencing and navigation
- HTML extraction may have occasional conversion errors - watch for updates