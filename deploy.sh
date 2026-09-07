#!/bin/bash
# Build the site for deployment. Run from anywhere:  ./deploy.sh
set -e
cd "$(dirname "$0")"

if pgrep -f "hugo server" >/dev/null 2>&1; then
    echo "A 'hugo server' preview is running. Stop it first (Ctrl+C in its terminal):"
    echo "the preview writes development files with localhost links into public/."
    exit 1
fi

if grep -Eq '^baseURL *= *""' hugo.toml; then
    echo "Warning: baseURL is empty in hugo.toml. Set it to the site's public address"
    echo "(for example https://example.uci.edu/) so that the sitemap and RSS feed carry full links."
    echo
fi

find static content -name .DS_Store -delete 2>/dev/null
echo "Building Hugo site (stale files in public/ are removed)..."
hugo --cleanDestinationDir

echo
echo "Build successful. The site is in public/."
echo "Upload its contents to the web server, for example:"
echo "  rsync -avz --delete public/ username@server.university.edu:/path/to/public_html/"
