# Script to remove the redundant "Company" footer block site-wide
$companyBlockPattern = '(?s)<div style="min-width:140px; margin-bottom:2rem;">\s*<div[^>]*>Company</div>.*?</ul>\s*</div>'

Get-ChildItem -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -match $companyBlockPattern) {
        Write-Host "Updating $($_.Name)..."
        $content = [regex]::Replace($content, $companyBlockPattern, "")
        
        # Cleanup extra whitespace/newlines created by removal
        $content = $content -replace '(?s)\s*</div>\s*</div>\s*<div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center;', "`n            </div>`n            <div style=""display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center;"
        
        Set-Content $_.FullName $content
    }
}
