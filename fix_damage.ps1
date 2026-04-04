# Repair and Sanity Fix Script
$files = Get-ChildItem "route*.html"

foreach ($file in $files) {
    Write-Host "Checking integrity of $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    $originalLength = $content.Length
    
    # 1. Fix Mangled Footer (Screenshot issue)
    # Search for the class string starting with a space (indicating missing <footer)
    $mangledFooter = ' class="section-padding" style="background: #000; border-top: 1px solid rgba(255,255,255,0.05); text-align: center;">'
    $fixedFooter = '<footer' + $mangledFooter
    
    if ($content -match [regex]::Escape($mangledFooter) -and $content -notmatch [regex]::Escape($fixedFooter)) {
        $content = $content -replace [regex]::Escape($mangledFooter), $fixedFooter
        Write-Host "  - Restored missing <footer tag."
    }

    # 2. Fix Missing Departure Label
    $depGroupNoLabel = '(?s)(<div class="form-group">)\s*(<select[^>]*id="departure")'
    $depLabel = '<label class="form-label" for="departure">Departure Airport</label>'
    
    if ($content -match $depGroupNoLabel) {
        $content = $content -replace $depGroupNoLabel, ('$1' + "`n                                " + $depLabel + "`n                                " + '$2')
        Write-Host "  - Restored missing Departure Label."
    }
    
    # 3. Cleanup Duplicate Script comments if any
    $content = $content -replace '(?s)<!-- TRIP INTEGRATION SCRIPT -->\s+<!-- TRIP INTEGRATION SCRIPT -->', '<!-- TRIP INTEGRATION SCRIPT -->'

    if ($content.Length -ne $originalLength) {
        Set-Content $file.FullName $content -NoNewline
        Write-Host "  - Saved repairs to $($file.Name)."
    }
}

Write-Host "Integrity Repair Complete."
