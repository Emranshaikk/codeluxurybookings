# Elite Luxury Bookings - Global Link Synchronizer
# This script ensures every internal link across 150+ folders uses the premium, folder-based URL structure.

# 1. Get all index.html files (Root and Subfolders)
$files = Get-ChildItem -Path "**/index.html" -Recurse
# Also catch the template files
$templates = Get-ChildItem -Path "_template_*.html"
$allFiles = $files + $templates

foreach ($file in $allFiles) {
    Write-Host "Synchronizing Links in: $($file.FullName)"
    $content = Get-Content $file.FullName -Raw
    
    # Transformation 1: Change "page.html" to "/page/"
    # Matches href="slug.html" and href="slug.html"
    $newContent = $content -replace 'href="([a-zA-Z0-9-]+)\.html"', 'href="/$1/"'
    
    # Transformation 2: Handle Home Page links
    $newContent = $newContent -replace 'href="/index/"', 'href="/"'
    $newContent = $newContent -replace 'href="/homepagesilo/"', 'href="/"'
    
    # Transformation 3: Fix trailing slashes for jet routes (already renamed)
    # If they are already folder names without slashes, add the slashing
    # Matches href="ibiza-to-london-private-jet-cost" (no extension)
    # We use a negative lookahead to avoid double slashing if already present.
    $newContent = $newContent -replace 'href="([a-zA-Z0-9-]{10,})"(?!\/)', 'href="/$1/"'
    
    Set-Content $file.FullName $newContent -NoNewline
}

Write-Host "Global Link Synchronization Complete."
