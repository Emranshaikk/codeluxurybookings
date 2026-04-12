
$htmlFiles = Get-ChildItem -Path . -Filter "*.html" -Recurse
$report = @()

foreach ($file in $htmlFiles) {
    if ($file.Name -match "audit_") { continue }
    $content = Get-Content $file.FullName -Raw
    
    $hasCanonical = $content -match '<link rel=["'']canonical["'']'
    $images = [regex]::Matches($content, '<img[^>]+>')
    $missingAlt = 0
    foreach ($img in $images) {
        if ($img.Value -notmatch 'alt=["'']') {
            $missingAlt++
        }
    }

    $report += [PSCustomObject]@{
        Page = $file.Name
        HasCanonical = $hasCanonical
        ImagesCount = $images.Count
        ImagesMissingAlt = $missingAlt
    }
}

$report | Export-Csv -Path "seo_audit.csv" -NoTypeInformation
$report | Group-Object HasCanonical | Select-Object Name, Count | Write-Host
$report | Where-Object { $_.ImagesMissingAlt -gt 0 } | Select-Object Page, ImagesMissingAlt | Write-Host
