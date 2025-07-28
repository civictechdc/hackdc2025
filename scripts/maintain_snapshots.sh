#!/bin/bash

# Civic Hack DC 2025 - Project Snapshot Maintenance Script
# This script helps maintain both subtree snapshots and submodule links

set -e

PROJECT_NAME=$1
REPO_URL=$2
TEAM_SLUG=$3

if [ -z "$PROJECT_NAME" ] || [ -z "$REPO_URL" ] || [ -z "$TEAM_SLUG" ]; then
    echo "Usage: $0 <project_name> <repo_url> <team_slug>"
    echo "Example: $0 'Smart Transit App' 'https://github.com/team/repo' 'smart_transit'"
    exit 1
fi

PROJECT_DIR="projects/$TEAM_SLUG"

echo "Setting up project: $PROJECT_NAME"
echo "Team slug: $TEAM_SLUG"
echo "Repository: $REPO_URL"

# Create project directory if it doesn't exist
mkdir -p "$PROJECT_DIR"

# Add subtree snapshot (squashed to keep repo size manageable)
echo "Creating subtree snapshot..."
git subtree add --prefix="$PROJECT_DIR/snapshot" "$REPO_URL" main --squash || \
    git subtree add --prefix="$PROJECT_DIR/snapshot" "$REPO_URL" master --squash

# Optionally add as submodule for tracking continued development
read -p "Add as submodule for tracking continued development? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Adding submodule..."
    git submodule add "$REPO_URL" "$PROJECT_DIR/upstream"
fi

# Create/update project metadata
cat > "$PROJECT_DIR/links.txt" << EOF
Original Repository: $REPO_URL
Added: $(date +%Y-%m-%d)
Snapshot Method: git subtree (squashed)
EOF

echo "✅ Project snapshot created successfully!"
echo "Next steps:"
echo "1. Update $PROJECT_DIR/README.md with project details"
echo "2. Add any demo files or data samples to $PROJECT_DIR/data/"
echo "3. Commit and push changes" 