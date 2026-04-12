# Elite Luxury Bookings - Authority Route Renamer
# This script migrates 80+ jet route files to their premium, SEO-optimized URL names.

$files = Get-ChildItem -Path "route*.html"

foreach ($file in $files) {
    $oldName = $file.Name
    # Transform: routebeijingtoseoul.html -> beijing-to-seoul-private-jet-cost.html
    $baseName = $oldName -replace "^route", "" -replace "\.html$", ""
    
    # Split by 'to' to ensure hyphenation
    # Handle cases like "abudhabi" vs "abu-dhabi" if necessary, 
    # but for now we follow the user's direct request pattern.
    if ($baseName -match "(.+)to(.+)") {
        $from = $matches[1]
        $to = $matches[2]
        $newName = "$from-to-$to-private-jet-cost.html"
        
        Write-Host "Renaming: $oldName -> $newName"
        Rename-Item -Path $file.FullName -NewName $newName
    }
}

Write-Host "Elite Jet Network Renaming Complete."
