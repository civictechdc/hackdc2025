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
    echo ""
    echo "Available team slugs:"
    ls -1 projects/ | grep -v README.md | grep -v example_team || true
    exit 1
fi

PROJECT_DIR="projects/$TEAM_SLUG"

echo "Setting up project: $PROJECT_NAME"
echo "Team slug: $TEAM_SLUG"
echo "Repository: $REPO_URL"

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Project directory $PROJECT_DIR does not exist!"
    echo "Available projects:"
    ls -1 projects/ | grep -v README.md | grep -v example_team || true
    exit 1
fi

# Create standard subdirectories if they don't exist
echo "Ensuring standard directory structure..."
mkdir -p "$PROJECT_DIR"/{snapshot,upstream}

# Check if snapshot already exists
if [ -d "$PROJECT_DIR/snapshot" ] && [ "$(ls -A $PROJECT_DIR/snapshot)" ]; then
    echo "⚠️  Snapshot directory already contains files."
    read -p "Update existing snapshot? This will replace current contents. (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing snapshot..."
        rm -rf "$PROJECT_DIR/snapshot"
        mkdir -p "$PROJECT_DIR/snapshot"
    else
        echo "Skipping snapshot creation."
        SKIP_SNAPSHOT=true
    fi
fi

# Add subtree snapshot (squashed to keep repo size manageable)
if [ "$SKIP_SNAPSHOT" != "true" ]; then
    echo "Creating subtree snapshot..."
    
    # Try main branch first, then master
    if git subtree add --prefix="$PROJECT_DIR/snapshot" "$REPO_URL" main --squash 2>/dev/null; then
        echo "✅ Snapshot created from 'main' branch"
        SNAPSHOT_BRANCH="main"
    elif git subtree add --prefix="$PROJECT_DIR/snapshot" "$REPO_URL" master --squash 2>/dev/null; then
        echo "✅ Snapshot created from 'master' branch"
        SNAPSHOT_BRANCH="master"
    else
        echo "❌ Failed to create snapshot. Please check the repository URL and branch."
        exit 1
    fi
fi

# Handle submodule
if [ -d "$PROJECT_DIR/upstream" ] && [ "$(ls -A $PROJECT_DIR/upstream)" ]; then
    echo "⚠️  Upstream directory already contains files."
    read -p "Replace with submodule? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$PROJECT_DIR/upstream"
        git submodule add "$REPO_URL" "$PROJECT_DIR/upstream"
    fi
else
    read -p "Add as submodule for tracking continued development? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Adding submodule..."
        git submodule add "$REPO_URL" "$PROJECT_DIR/upstream"
    fi
fi

# Update links.txt while preserving existing content
echo "Updating project metadata..."
LINKS_FILE="$PROJECT_DIR/links.txt"
TEMP_LINKS=$(mktemp)

if [ -f "$LINKS_FILE" ]; then
    # Preserve existing content but update repository info
    sed "s|^Original Repository:.*|Original Repository: $REPO_URL|" "$LINKS_FILE" > "$TEMP_LINKS"
    
    # Add snapshot info if not present
    if ! grep -q "Snapshot Method:" "$TEMP_LINKS"; then
        echo "Snapshot Method: git subtree (squashed)" >> "$TEMP_LINKS"
    fi
    
    # Add/update snapshot date
    if grep -q "Snapshot Added:" "$TEMP_LINKS"; then
        sed -i.bak "s|^Snapshot Added:.*|Snapshot Added: $(date +%Y-%m-%d)|" "$TEMP_LINKS"
    else
        echo "Snapshot Added: $(date +%Y-%m-%d)" >> "$TEMP_LINKS"
    fi
    
    # Add branch info if snapshot was created
    if [ "$SKIP_SNAPSHOT" != "true" ] && [ -n "$SNAPSHOT_BRANCH" ]; then
        if grep -q "Snapshot Branch:" "$TEMP_LINKS"; then
            sed -i.bak "s|^Snapshot Branch:.*|Snapshot Branch: $SNAPSHOT_BRANCH|" "$TEMP_LINKS"
        else
            echo "Snapshot Branch: $SNAPSHOT_BRANCH" >> "$TEMP_LINKS"
        fi
    fi
    
    mv "$TEMP_LINKS" "$LINKS_FILE"
    rm -f "$LINKS_FILE.bak" 2>/dev/null || true
else
    # Create basic links.txt if it doesn't exist
    cat > "$LINKS_FILE" << EOF
Original Repository: $REPO_URL
Demo Video: [To be added]
Presentation Slides: [To be added]
Live Demo: [To be added]
Team Contact: [To be added]
Snapshot Added: $(date +%Y-%m-%d)
Snapshot Method: git subtree (squashed)
EOF
    [ -n "$SNAPSHOT_BRANCH" ] && echo "Snapshot Branch: $SNAPSHOT_BRANCH" >> "$LINKS_FILE"
fi

rm -f "$TEMP_LINKS" 2>/dev/null || true

echo ""
echo "✅ Project snapshot setup completed successfully!"
echo ""
echo "📂 Project structure:"
echo "   $PROJECT_DIR/"
echo "   ├── README.md           (project documentation)"
echo "   ├── links.txt           (updated with snapshot info)"
echo "   ├── snapshot/           $([ "$SKIP_SNAPSHOT" = "true" ] && echo "(existing files preserved)" || echo "(fresh code snapshot)")"
echo "   └── upstream/          $([ -d "$PROJECT_DIR/upstream/.git" ] && echo "(submodule tracking)" || echo "(available for submodule)")"
echo ""
echo "🔄 To update an existing snapshot later:"
echo "   git subtree pull --prefix=\"$PROJECT_DIR/snapshot\" \"$REPO_URL\" ${SNAPSHOT_BRANCH:-main} --squash"
echo ""
echo "📝 Next steps:"
echo "1. Review and update $PROJECT_DIR/README.md if needed"
echo "2. Add demo files or data samples to $PROJECT_DIR/data/"
echo "3. Add additional documentation to $PROJECT_DIR/docs/"
echo "4. Commit and push changes" 