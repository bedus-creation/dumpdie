#!/bin/bash
set -e

# 1. Validation
if [[ ! "$1" =~ ^(patch|minor|major)$ ]]; then
  echo "Usage: ./release.sh [patch|minor|major]"
  exit 1
fi

# 2. Ensure we are on main and up to date
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "Error: You must be on the main branch to release."
  exit 1
fi

# 3. Bump version (This creates the commit and tag locally)
echo "Bumping version and tagging..."
uv run bump-my-version bump "$1"

# 4. Push to GitHub
echo "Pushing code and tags to GitHub..."
git push origin main --follow-tags

# 5. Build and Upload
echo "Cleaning 'dist' and building package..."
rm -rf dist/*
uv build

echo "Uploading to PyPI..."
uv run twine upload dist/*

echo "🚀 Release v$(uv run python -c 'import dumpdie; print(dumpdie.__version__)' 2>/dev/null || echo 'updated') is live!"