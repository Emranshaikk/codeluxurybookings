# Elite Luxury Bookings - Master Authority Harmonizer
# This script ensures every folder and every link across 150+ pages is perfectly synchronized in the premium format.

# 1. Harmonize Folders (The Directories)
$dirs = Get-ChildItem -Directory
foreach ($dir in $dirs) {
    # If it's a 'routeCITYtoCITY' folder, rename it to 'CITY-to-CITY-private-jet-cost'
    if ($dir.Name -match '^route([a-z]+)to([a-z]+)$') {
        $from = $Matches[1]
        $to = $Matches[2]
        $newName = "$from-to-$to-private-jet-cost"
        Write-Host "Harmonizing Directory: $($dir.Name) -> $newName"
        if (-not (Test-Path $newName)) {
            Rename-Item $dir.FullName $newName
        } else {
            # Merge if necessary, though it shouldn't happen
            Move-Item "$($dir.FullName)/*" $newName -Force
            Remove-Item $dir.FullName -Force
        }
    }
}

# 2. Harmonize Links (The Content)
$allIndices = Get-ChildItem -Path "**/index.html" -Recurse
$templates = Get-ChildItem -Path "_template_*.html"
$allFiles = $allIndices + $templates + (Get-ChildItem -Path "index.html")

foreach ($file in $allFiles) {
    Write-Host "Harmonizing Links in: $($file.FullName)"
    $content = Get-Content $file.FullName -Raw
    
    # Pattern A: "/routeCITYtoCITY/" -> "/CITY-to-CITY-private-jet-cost/"
    $newContent = $content -replace '/route([a-z]+)to([a-z]+)/', '/$1-to-$2-private-jet-cost/'
    
    # Pattern B: "/CITYtoCITY/" -> "/CITY-to-CITY-private-jet-cost/"
    # Captures cases where route prefix was already missing but no dashes
    $newContent = $newContent -replace '/([a-z]{3,15})to([a-z]{3,15})/', '/$1-to-$2-private-jet-cost/'
    
    # Pattern C: Ensure all internal route links end with a trailing slash
    # Matches href="/whatever" (no trailing slash) and adds it
    $newContent = $newContent -replace 'href="/([a-z-]+)"', 'href="/$1/"'
    
    # Clean up any double slashes
    $newContent = $newContent -replace '"//', '"/'
    $newContent = $newContent -replace '/+"', '/"'

    Set-Content $file.FullName $newContent -NoNewline
}

Write-Host "Master Harmonization Complete."
