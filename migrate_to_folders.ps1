# Elite Luxury Bookings - Pure Folder Architecture Migration
# This script transforms 150+ Authority pages into a 100% reliable directory structure.

# 1. Setup Home Page
if (Test-Path "homepagesilo.html") {
    Write-Host "Setting up Master Home Page: index.html"
    if (Test-Path "index.html") { Remove-Item "index.html" -Force }
    Rename-Item "homepagesilo.html" "index.html"
}

# 2. Iterate through all Landing Pages
$files = Get-ChildItem -Path "*.html" -Exclude "index.html", "_template_*.html", "authority-triad-snippet.html"

foreach ($file in $files) {
    # Skip the templates and other internal snippets if they weren't caught by exclude
    if ($file.Name -like "_template_*") { continue }
    
    $folderName = $file.BaseName
    Write-Host "Migrating: $($file.Name) -> $folderName/index.html"
    
    # Create the Authority Directory
    if (-not (Test-Path $folderName)) {
        New-Item -ItemType Directory -Path $folderName
    }
    
    # Move the page in as the directory index
    $targetPath = Join-Path $folderName "index.html"
    Move-Item -Path $file.FullName -Destination $targetPath -Force
}

Write-Host "Pure Folder Architecture Migration Complete."
