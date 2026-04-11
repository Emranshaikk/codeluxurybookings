$path = "c:\Users\imran\OneDrive\Desktop\ELB code\blog.html"
$content = [System.IO.File]::ReadAllText($path)

# 1. Fix broken comments
$content = $content -replace '< !--', '<!--'
$content = $content -replace '-- >', '-->'

# 2. Fix duplicate classes
$content = $content -replace 'class="blog-grid" id="blogGrid" class="blog-grid"', 'class="blog-grid" id="blogGrid"'

# 3. Fix the Filter logic (Make sure it's crisp)
# The user's snippet had some weird spacing in the script
$content = $content -replace '(?s)<script>.*?function filterPosts\(category\).*?</script>', @"
<script>
function filterPosts(category) {
    const cards = document.querySelectorAll('.blog-card');
    const btns = document.querySelectorAll('.filter-btn');

    btns.forEach(btn => {
        const btnText = btn.innerText.toLowerCase();
        if (btnText === category.toLowerCase() || (category === 'all' && btnText === 'all articles')) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    cards.forEach(card => {
        const cardCat = card.getAttribute('data-category').toLowerCase();
        const isRoute = card.classList.contains('route-card');

        if (category === 'all') {
            // Initially show only main articles, hide 100+ route pages for better UX
            card.style.display = isRoute ? 'none' : 'block';
        } else if (cardCat === category.toLowerCase()) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // Initial display
    filterPosts('all');
});
</script>
"@

# 4. Final Cleanup of any double spaces or broken formatting in the cards
$content = $content -replace '\n\s*\n', "`n"

[System.IO.File]::WriteAllText($path, $content)
Write-Host "Success: Blog page sanitized and optimized."

$blogPath = "c:\Users\imran\OneDrive\Desktop\ELB code\blog.html"
$content = [System.IO.File]::ReadAllText($blogPath)

# 1. Purge all card-img-wrap blocks
$content = $content -replace '(?s)<div class="card-img-wrap">.*?</div>', ''

# 2. Inject high-end editorial excerpts
$excerptHtml = '<p class="card-excerpt">Comprehensive technical analysis of aircraft availability, landing permits, and peak-season cost projections for this elite corridor.</p>'
$content = $content -replace '</h3>', "</h3>`n                    $excerptHtml"

[System.IO.File]::WriteAllText($blogPath, $content)
Write-Host "Success: Blog transformed to premium editorial text layout."
