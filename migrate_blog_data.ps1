$blogIndex = Get-Content 'blog_index.html' -Raw
$blogMain = Get-Content 'blog.html' -Raw

# 1. Extract the cards container from blog_index.html
if ($blogIndex -match '(?s)<div class="blog-grid" id="blogGrid">(.*?)</div>\s*</div>\s*</section>|(?s)<div class="blog-grid" id="blogGrid">(.*?)</div>') {
    # We take the content inside blogGrid
    $cardsContent = $matches[1]
    if (-not $cardsContent) { $cardsContent = $matches[2] }

    # 2. Fix the .html.html bug
    $cardsContent = $cardsContent -replace '\.html\.html', '.html'

    # 3. Fix the {{HERO_IMAGE}} placeholder
    $cardsContent = $cardsContent -replace '\{\{HERO_IMAGE\}\}', 'jet_master.png'

    # 4. Strip excessive whitespace and newlines for a cleaner file
    $cardsContent = $cardsContent -replace '\n\s*\n', "`n"

    # 5. Inject into blog.html
    if ($blogMain -match '(?s)<div class="blog-grid" id="blogGrid">.*?</div>') {
        $blogMain = $blogMain -replace '(?s)<div class="blog-grid" id="blogGrid">.*?</div>', "<div class=\"blog-grid\" id=\"blogGrid\">`n$cardsContent`n        </div>"
        
        Set-Content 'blog.html' $blogMain -NoNewline
        Write-Host "Success: Migrated and optimized cards to blog.html"
    } else {
        Write-Host "Error: Could not find blogGrid target in blog.html"
    }
} else {
    Write-Host "Error: Could not find cards in blog_index.html"
}
