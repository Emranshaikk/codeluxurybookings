$gaCode = @"
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-J56D1LJLFM"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-J56D1LJLFM');
    </script>
"@

$htmlFiles = Get-ChildItem -Path . -Filter *.html -Recurse

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    if ($content -notlike "*G-J56D1LJLFM*") {
        # Inject after <head> tag
        $newContent = $content -replace '<head>', "<head>`n$gaCode"
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
        Write-Host "Injected GA into $($file.FullName)"
    } else {
        Write-Host "GA already present in $($file.FullName)"
    }
}
