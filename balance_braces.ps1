$files = Get-ChildItem route*.html | Where-Object { $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    Write-Host "Balancing Braces in $($file.Name)..."
    $content = Get-Content $file.FullName -Raw

    # Find all <style> blocks
    $styleRegex = '(?s)<style>(.*?)</style>'
    $matches = [regex]::Matches($content, $styleRegex)
    
    foreach ($m in $matches) {
        $styleContent = $m.Groups[1].Value
        
        # Count braces
        $openCount = ([regex]::Matches($styleContent, '\{')).Count
        $closeCount = ([regex]::Matches($styleContent, '\}')).Count
        
        if ($openCount -gt $closeCount) {
            $diff = $openCount - $closeCount
            Write-Host "  - Adding $diff missing closing braces."
            $padding = "`n" + ("    }" * $diff) + "`n"
            # Insert the padding before the closing </style> of THIS specific match
            # To be safe, we just replace this specific style block in the main content
            $newStyleContent = $styleContent + $padding
            $content = $content.Replace("<style>$styleContent</style>", "<style>$newStyleContent</style>")
        }
    }
    
    Set-Content $file.FullName $content -NoNewline
}

Write-Host "Brace Balancing Complete."
