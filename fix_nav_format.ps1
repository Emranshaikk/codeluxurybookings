Get-ChildItem -Path "$PSScriptRoot" -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # Correct the literal \n injected by the previous script
    $content = $content -replace '\\n', "`n"

    Set-Content $_.FullName $content
}
