$backupPath = "c:\Users\imran\OneDrive\Desktop\ELB code\blog_index.html"
$mainPath = "c:\Users\imran\OneDrive\Desktop\ELB code\blog.html"

# Direct Read
$content = [System.IO.File]::ReadAllText($backupPath)

# 1. Global Link Fixes
$content = $content -replace '\.html\.html', '.html'
$content = $content -replace '\{\{HERO_IMAGE\}\}', 'jet_master.png'

# 2. Fix the Filter logic to show EVERYTHING by default
$content = $content -replace "(?s)if \(category==='all'\).*?else \{", "if (category==='all') {
                            card.style.display='block';
                        } else if ("

# 3. Direct Write
[System.IO.File]::WriteAllText($mainPath, $content)

Write-Host "Restoration Successful: All articles are now live and visible by default."
