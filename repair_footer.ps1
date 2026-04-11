# Repair script to fix broken footer div structure
$brokenPattern = '(?s)</ul>\s*</div>\s*<div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center;'
$repairText = "</ul>`n                </div>`n            </div>`n            <div style=""display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center;"

Get-ChildItem -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -match $brokenPattern) {
        Write-Host "Repairing $($_.Name)..."
        # $matches[0] contains the matched text
        $content = $content.Replace($matches[0], $repairText)
        Set-Content $_.FullName $content
    }
}
