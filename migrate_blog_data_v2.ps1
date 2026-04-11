$blogIndexContent = [System.IO.File]::ReadAllText("$(System.AppDomain::CurrentDomain.BaseDirectory)\blog_index.html")
$blogMainContent = [System.IO.File]::ReadAllText("$(System.AppDomain::CurrentDomain.BaseDirectory)\blog.html")

# Fix path for local run
$blogIndexContent = [System.IO.File]::ReadAllText("c:\Users\imran\OneDrive\Desktop\ELB code\blog_index.html")
$blogMainContent = [System.IO.File]::ReadAllText("c:\Users\imran\OneDrive\Desktop\ELB code\blog.html")

# Pattern to find the grid content in index
$pattern = '(?s)<div class="blog-grid" id="blogGrid">(.*?)</div>'
if ($blogIndexContent -match $pattern) {
    $cards = $matches[1]
    
    # 1. Cleaning
    $cards = $cards -replace '\.html\.html', '.html'
    $cards = $cards -replace '\{\{HERO_IMAGE\}\}', 'jet_master.png'
    
    # 2. Re-Injection
    $newBlogContent = $blogMainContent -replace '(?s)<div class="blog-grid" id="blogGrid">.*?</div>', "<div class=`"blog-grid`" id=`"blogGrid`">`n$cards`n</div>"
    
    [System.IO.File]::WriteAllText("c:\Users\imran\OneDrive\Desktop\ELB code\blog.html", $newBlogContent)
    Write-Host "Restoration Complete: 5000+ Lines Organized and Cleaned."
} else {
    Write-Host "Grid Not Found"
}
