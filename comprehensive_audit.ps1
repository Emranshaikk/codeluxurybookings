# Comprehensive audit of all HTML pages for correct Formspree lead forms
$htmlFiles = Get-ChildItem -Filter *.html
$missingFormspree = @()
$containsValens = @()
$formspreeID = "formspree.io/f/xwvwanlj"

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Check for Formspree
    if ($content -notmatch $formspreeID) {
        $missingFormspree += $file.Name
    }
    
    # Check for legacy Valens widget comments/scripts
    if ($content -match "ELB_VALENS_WIDGET_START" -or $content -match "valens_api_bridge.js") {
        $containsValens += $file.Name
    }
}

Write-Host "--- Audit Results ---"
if ($missingFormspree.Count -eq 0) {
    Write-Host "Success: All $($htmlFiles.Count) pages have the correct Formspree lead form."
} else {
    Write-Host "Warning: $($missingFormspree.Count) pages are missing Formspree:"
    $missingFormspree | ForEach-Object { Write-Host " - $_" }
}

if ($containsValens.Count -eq 0) {
    Write-Host "Success: No pages contain legacy Valens references."
} else {
    Write-Host "Warning: $($containsValens.Count) pages still contain legacy Valens references:"
    $containsValens | ForEach-Object { Write-Host " - $_" }
}
