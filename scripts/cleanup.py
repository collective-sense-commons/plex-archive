#!/usr/bin/env python3
"""
Cleanup script for Plex Archive regeneration.

Removes generated content directories while preserving source files and scripts.
Safe to run before regenerating the archive.
"""

import shutil
from pathlib import Path

def cleanup_generated_content():
    """Remove generated content directories, preserving source files."""

    # Change to project root (script runs from scripts/ directory)
    project_root = Path(__file__).parent.parent

    # Directories to remove (generated content)
    generated_dirs = ['posts', 'authors', 'topics', 'years']

    # Files to remove at root level (generated)
    generated_files = ['README.md']

    # Directories/files to preserve
    preserve = ['issues', 'scripts', 'venv', '.git', '.gitignore', 'CLAUDE.md',
               'Project.md', 'biweekly-plex-dispatch.ghost.*.json', '__pycache__',
               'Sidebar.md', 'netlify.toml', '.markpub', '.github', 'Contact Peter Kaminski.md']

    print("🧹 Cleaning generated content...")

    # Remove generated directories
    for dir_name in generated_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"  Removing directory: {dir_name}/")
            shutil.rmtree(dir_path)
        else:
            print(f"  Directory not found: {dir_name}/")

    # Remove generated files at root
    for file_name in generated_files:
        file_path = project_root / file_name
        if file_path.exists() and file_path.is_file():
            print(f"  Removing file: {file_name}")
            file_path.unlink()
        else:
            print(f"  File not found: {file_name}")

    print("✅ Cleanup complete!")
    print("\nPreserved directories:")
    for item in sorted(project_root.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            print(f"  📁 {item.name}/")

    print("\nTo regenerate archive:")
    print("  python3 scripts/extract_posts.py")

if __name__ == '__main__':
    cleanup_generated_content()