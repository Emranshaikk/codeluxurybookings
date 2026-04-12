$c = Get-Content 'blog.html' -Raw

# 1. Clean the Grid Container
$c = $c -replace 'id="blogGrid"[^>]*style="[^"]*"', 'id="blogGrid" class="blog-grid"'

# 2. Clean the Cards (Removing inline background, border, transition etc)
$c = $c -replace 'class="blog-card route-card"[^>]*style="[^"]*"', 'class="blog-card route-card"'
$c = $c -replace 'class="card-img-container"[^>]*style="[^"]*"', 'class="card-img-container"'
$c = $c -replace 'class="card-content"[^>]*style="[^"]*"', 'class="card-content"'
$c = $c -replace 'class="card-meta"[^>]*style="[^"]*"', 'class="card-meta"'

# 3. Fix the duplicated head issues (cleaning up to ELB_STYLE_END)
$startTag = "<style>"
$endTag = "/* ELB_STYLE_END */"
$newCss = "
        /* ELB_CORE_THEME_INJECT */
        :root {
            --primary-gold: #D4AF37;
            --deep-black: #050505;
            --graphene: #1A1A1A;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(212, 175, 55, 0.15);
            --text-main: #FFFFFF;
            --text-muted: rgba(255, 255, 255, 0.6);
        }

        body {
            background: var(--deep-black) !important;
            color: var(--text-main) !important;
            margin: 0;
            font-family: 'Inter', sans-serif;
            padding-top: 72px !important;
        }

        /* --- ELITE MODULAR GRID RESTORATION --- */
        .blog-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2.5rem;
            margin: 4rem 0;
        }

        .blog-card {
            display: flex;
            flex-direction: column;
            background: var(--graphene) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 20px !important;
            overflow: hidden;
            text-decoration: none !important;
            transition: all 0.4s ease !important;
        }

        .blog-card:hover {
            transform: translateY(-10px);
            border-color: var(--primary-gold) !important;
        }

        .card-img-container {
            height: 220px;
            overflow: hidden;
            background: #000;
        }

        .card-img-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: 0.6s ease;
        }

        .blog-card:hover img {
            transform: scale(1.05);
        }

        .card-content {
            padding: 2rem;
            flex-grow: 1;
        }

        .card-meta {
            color: var(--primary-gold);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 1rem;
            display: block;
        }

        .card-content h3 {
            color: #fff;
            font-size: 1.4rem;
            line-height: 1.3;
            font-family: 'Cormorant Garamond', serif;
            margin-bottom: 1rem;
        }

        .card-content p {
            color: var(--text-muted);
            font-size: 0.95rem;
            line-height: 1.6;
        }

        /* Floating WhatsApp Button */
        .wa-float {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 54px;
            height: 54px;
            background: linear-gradient(135deg, #25D366, #128C7E);
            color: #fff !important;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            z-index: 999999;
        }

        @media (max-width: 768px) {
            .blog-grid { grid-template-columns: 1fr; gap: 1.5rem; }
            .wa-float { width: 48px; height: 48px; bottom: 20px; right: 20px; }
        }"

# Inject clean CSS
if ($c -match '<style>.*?\/\* ELB_STYLE_END \*\/') {
    $c = $c -replace '(?s)<style>.*?\/\* ELB_STYLE_END \*\/', "<style>$newCss`n        $endTag"
}

Set-Content 'blog.html' $c -NoNewline
