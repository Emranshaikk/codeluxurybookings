$htmlFiles = Get-ChildItem -Path . -Filter "*.html" -Recurse
$actions = @{}

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    $allMatches = [regex]::Matches($content, 'action=["'']([^"''#\s?]+)["'']')
    foreach ($match in $allMatches) {
        $action = $match.Groups[1].Value
        if ($actions.ContainsKey($action)) {
            $actions[$action] += 1
        } else {
            $actions[$action] = 1
        }
    }
}

$actions | Out-String | Write-Host
