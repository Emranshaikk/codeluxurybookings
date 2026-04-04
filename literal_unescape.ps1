$files = Get-ChildItem route*.html | Where-Object { $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    Write-Host "Un-escaping Network in $($file.Name)..."
    $content = Get-Content -Path $file.FullName -Raw
    
    # Replace literal backtick-n string with a real newline
    # In PowerShell double quotes, `` ` is a literal backtick.
    $brokenSeq = "``n"
    $content = $content.Replace($brokenSeq, "`n")
    
    # Also fix some other potential escapes
    $content = $content.Replace("`"n", "") 

    # Now let's balance correctly
    $content = $content -replace '(?s)\}\s+\}\s+</style>', "}`n    }`n    </style>"
    
    Set-Content $file.FullName $content -NoNewline
}

Write-Host "Real Cleanup Complete."
