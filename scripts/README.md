# Scripts Directory

This directory contains Python scripts for processing the Biweekly Plex Dispatch archive.

## Scripts

### `extract_posts.py`
**Main extraction script** - Converts HTML issue files into an Obsidian-compatible markdown wiki.

**Features:**
- Extracts individual posts from HTML files (each containing multiple posts)
- Generates author index pages with post lists
- Categorizes posts into 30 topic areas using confidence-based detection
- Creates year-based navigation
- Handles author name consolidation and Unicode characters
- Produces cross-linked markdown files with proper wikilink syntax

**Input:** HTML files in `/issues` directory
**Output:** Markdown files in `/posts`, `/people`, `/topics`, `/years` directories

### `cleanup.py`
**Regeneration helper script** - Safely removes generated content while preserving source files.

**Features:**
- Removes generated directories: `posts/`, `people/`, `topics/`, `years/`
- Removes generated `README.md` at project root
- Preserves source files and directories: `issues/`, `scripts/`, `venv/`, `.git/`
- Shows summary of remaining files after cleanup

**Usage:** Always run before regenerating the archive to ensure clean output.

### `requirements.txt`
**Python dependencies** - Required packages for running the extraction scripts.

**Key dependencies:**
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML parser backend
- Standard library modules (no additional installation needed)

## Usage Workflow

1. **Setup environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Generate archive:**
   ```bash
   # From project root
   python3 scripts/cleanup.py      # Remove previous output
   python3 scripts/extract_posts.py  # Generate new archive
   ```

3. **Expected output:**
   ```
   ✅ Archive created successfully!
   📊 Extracted 614 posts from 52 authors across 4 years
   🏷️ Identified 30 topics across all posts
   ```

## Development

### Modifying Topic Detection
Edit the `COMMON_TOPICS` dictionary in `extract_posts.py` to add new categories or adjust keywords.

### Author Management
Update `AUTHOR_CONSOLIDATION` mapping and `KNOWN_AUTHORS` set in `extract_posts.py` for name changes or additions.

### File Structure
The scripts expect this project structure:
```
/
├── issues/          # HTML source files (input)
├── posts/           # Generated post files (output)
├── people/          # Generated author pages (output)
├── topics/          # Generated topic pages (output)
├── years/           # Generated year pages (output)
└── scripts/         # This directory
```

## Troubleshooting

**"No HTML files found"** - Ensure HTML files are in `/issues` directory with `.html` extension

**"Module not found"** - Run `pip install -r requirements.txt` in activated virtual environment

**"Permission denied"** - Check file permissions and that no files are open in other applications

**Incomplete extraction** - Run `cleanup.py` first to remove partial output, then re-run `extract_posts.py`