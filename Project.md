# Plex Archive Project

This project extracts individual posts from the Biweekly Plex Dispatch HTML archives and creates a Massive Wiki for easy navigation and cross-referencing.

Note: There's a tension between tweaking the extract script and re-running it vs. making edits in the extraction output files. At some point this will be resolved by better automation or deciding never to run the extract script again. Until then, check diffs carefully when making changes to either automation or output files.

The extraction script only generates these files/directories:
- posts/ directory and all markdown files within it
- authors/ directory and all files within it
- topics/ directory and all files within it
- years/ directory and all files within it
- issues/index.html

## Project Structure

```
/
├── posts/           # Individual post markdown files (614 posts)
├── authors/         # Author index pages (53 authors)
├── topics/          # Topic index pages (30 topics)
├── years/           # Year index pages (2022-2025)
├── issues/          # Original HTML source files (87 issues)
├── scripts/         # Python extraction and utility scripts
├── venv/           # Python virtual environment
├── README.md        # Main archive navigation (Massive Wiki entry point)
└── Project.md       # This technical documentation
```

## Scripts

### Main Scripts
- `scripts/extract_posts.py` - Main extraction script with topic detection and author consolidation
- `scripts/cleanup.py` - Removes generated content for clean regeneration

### Requirements
- Python 3.x
- BeautifulSoup4 for HTML parsing
- See `scripts/requirements.txt` for full dependencies

## Usage

### Setup
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r scripts/requirements.txt
```

### Generate Archive
```bash
source venv/bin/activate
python3 scripts/cleanup.py    # Clean previous run
python3 scripts/extract_posts.py
```

## Features

### Content Organization
- **614 posts** from 87 HTML issues (2022-2025)
- **53 authors** with name consolidation and individual index pages
- **30 topic categories** with improved keyword detection accuracy
- **Cross-referencing** between posts, authors, topics, and years

### Topic Detection
Uses confidence-based scoring with:
- Multi-word phrase matching for specificity
- Occurrence counting to reduce false positives
- 30 categories from general (AI, Climate) to specific (Web3, Bioregionalism)

### Author Management
- Hardcoded author list from "Kith and Kin" section
- Name consolidation (Pete → Peter Kaminski, George P → George Pór)
- Proper Unicode handling for international characters

### Linking
- **People links**: `[[Author Name]]` using spaces in filenames
- **Issue links**: `[2022-04-07](https://plex.collectivesensecommons.org/2022-04-07/)` to original Plex website
- **Topic links**: `[[Topic Name]]` to topic index pages
- **Year links**: `[[2022]]` to year index pages

## Data Sources

- **Original HTML**: 87 issue files in `/issues` directory
- **Ghost Export**: `biweekly-plex-dispatch.ghost.2025-09-17-17-08-49.json` (backup)
- **Known Authors**: Extracted from 2025-09-04 "Kith and Kin" post

## Development

### Adding New Topics
Edit `COMMON_TOPICS` dictionary in `scripts/extract_posts.py` and regenerate.

### Author Name Changes
Update `AUTHOR_CONSOLIDATION` mapping and `KNOWN_AUTHORS` set.

### Regeneration
Always run `scripts/cleanup.py` first to remove generated content while preserving source files and scripts.