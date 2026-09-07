#!/bin/bash
# Publish the site: commit every change and push it to GitHub, which rebuilds
# and deploys the site automatically.   Usage: ./publish.sh "what changed"
set -e
cd "$(dirname "$0")"
message="${1:-Update site}"
git add -A
if git diff --cached --quiet; then
    echo "Nothing to publish: no changes since the last publish."
    exit 0
fi
git commit -m "$message"
git push
echo "Pushed. GitHub publishes the site in a minute or two; the Actions tab of the repository shows progress."
