$files = Get-ChildItem -Path "$PSScriptRoot" -Filter *.html
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    if ($content -notlike "*formspree.io/f/xwvwanlj*") {
        Write-Output $file.Name
    }
}
