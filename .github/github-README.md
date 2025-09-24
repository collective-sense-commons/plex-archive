# GitHub Configuration for Plex Archive

This directory contains GitHub-specific configuration files for the Plex Archive Massive Wiki.

## Files

### `workflows/deploy.yml`
GitHub Actions workflow that:
- Runs on pushes to main branch
- Sets up Python environment
- Verifies archive structure and content counts
- Provides deployment information for Netlify

The workflow serves as both a CI check and deployment preparation step.

## Usage

When changes are pushed to the main branch, GitHub Actions will automatically:
1. Check out the repository
2. Set up the Python environment
3. Install dependencies from `scripts/requirements.txt`
4. Verify the archive structure (count posts, authors, topics)
5. Prepare for deployment

This ensures the archive is always in a deployable state and provides visibility into content statistics.