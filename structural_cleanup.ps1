$files = Get-ChildItem route*.html | Where-Object { $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    Write-Host "Structural Cleanup in $($file.Name)..."
    $content = Get-Content $file.FullName -Raw

    # 1. Remove the broken `"n` sequences left by previous run
    $content = $content -replace '"n', ""
    $content = $content -replace '}n', "}"

    # 2. Extract and fix ALL style blocks
    $styleRegex = '(?s)<style>(.*?)</style>'
    $allMatches = [regex]::Matches($content, $styleRegex)
    
    foreach ($m in $allMatches) {
        $origFull = $m.Value
        $styleInner = $m.Groups[1].Value
        
        # Clean up any duplicated '}' at the very end of the block
        # (Heuristic: trailing whitespace then multiple braces)
        $cleanInner = $styleInner -replace '(?s)\s+\}\s+\}\s+$', "`n    }`n"
        
        # Count braces to ensure balance
        $openCount = ([regex]::Matches($cleanInner, '\{')).Count
        $closeCount = ([regex]::Matches($cleanInner, '\}')).Count
        
        if ($openCount -gt $closeCount) {
            $diff = $openCount - $closeCount
            Write-Host "  - Adding $diff missing closing braces."
            for ($i = 0; $i -lt $diff; $i++) {
                $cleanInner += "`n    }"
            }
            $cleanInner += "`n"
        }
        
        $newFull = "<style>$cleanInner</style>"
        $content = $content.Replace($origFull, $newFull)
    }
    
    # 3. Final sanity: check for any `}` that are right before `</style>` but missing a newline
    $content = $content -replace '\}</style>', "}`n</style>"

    Set-Content $file.FullName $content -NoNewline
}

Write-Host "Final Network Repair Complete."
