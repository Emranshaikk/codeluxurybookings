import os
import re

files_data = {
    "all-inclusive-private-island-rental.html": {
        "canonical": "https://eliteluxurybookings.com/all-inclusive-private-island-rental",
        "hero_img": "assets/all_inclusive_private_island_hero.png"
    },
    "bahamas-private-island-rental.html": {
        "canonical": "https://eliteluxurybookings.com/bahamas-private-island-rental",
        "hero_img": "assets/bahamas_island_aerial.png"
    },
    "caribbean-private-island-rental.html": {
        "canonical": "https://eliteluxurybookings.com/caribbean-private-island-rental",
        "hero_img": "assets/caribbean_island_aerial_2.jpg"
    },
    "exclusive-private-island-rental.html": {
        "canonical": "https://eliteluxurybookings.com/exclusive-private-island-rental",
        "hero_img": "assets/exclusive_island_hero.png"
    },
    "luxury-private-island-rental.html": {
        "canonical": "https://eliteluxurybookings.com/luxury-private-island-rental",
        "hero_img": "assets/private_island_aerial.jpg"
    },
    "maldives-private-island-rental.html": {
        "canonical": "https://eliteluxurybookings.com/maldives-private-island-rental",
        "hero_img": "assets/maldives_island_aerial.png"
    },
    "private-island-for-rent.html": {
        "canonical": "https://eliteluxurybookings.com/private-island-for-rent",
        "hero_img": "assets/private_island_hero.jpg"
    }
}

directory = r"c:\Users\imran\OneDrive\Desktop\ELB code"

for filename, info in files_data.items():
    path = os.path.join(directory, filename)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(path, 'r', encoding='latin-1') as f:
                content = f.read()

        # Skip if OG tags already exist on the page
        if "og:title" in content:
            print(f"{filename}: SEO tags already present.")
            continue

        # Extract Title
        title_match = re.search(r"<title>(.*?)</title>", content)
        title = title_match.group(1).strip() if title_match else "Elite Luxury Bookings"
        
        # Extract Description
        desc_match = re.search(r'name="description"\s+content="([^"]+)"', content)
        if not desc_match:
            desc_match = re.search(r"name='description'\s+content='([^']+)'", content)
        desc = desc_match.group(1).strip() if desc_match else ""

        # Construct Meta Tags Block
        seo_meta = f"""
    <!-- Open Graph / Facebook Meta Tags -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{info['canonical']}">
    <meta property="og:image" content="https://eliteluxurybookings.com/{info['hero_img']}">
    <meta property="og:site_name" content="Elite Luxury Bookings">

    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="@eliteluxuryb">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="https://eliteluxurybookings.com/{info['hero_img']}">"""

        # 1. Inject SEO Metadata right after Canonical Link
        canonical_str = f'href="{info["canonical"]}"'
        canonical_pattern = re.compile(r'<link\s+rel="canonical"\s+href="[^"]+"\s*/?>')
        
        if canonical_pattern.search(content):
            content = canonical_pattern.sub(f'<link rel="canonical" href="{info["canonical"]}">\n{seo_meta}', content)
        else:
            # Fallback if pattern matches slightly differently
            content = content.replace("</head>", f"{seo_meta}\n</head>")

        # 2. Remove the duplicated relative style.css link to eliminate 404 requests
        # keeping the absolute "/style.css" which is correct
        content = re.sub(r'^\s*<link\s+rel="stylesheet"\s+href="style.css"\s*/?>\s*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*<link\s+rel="stylesheet"\s+href=\'style.css\'\s*/?>\s*\n', '', content, flags=re.MULTILINE)
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        except UnicodeEncodeError:
            with open(path, 'w', encoding='latin-1') as f:
                f.write(content)
                
        print(f"SEO successfully upgraded on: {filename}")
    else:
        print(f"File not found: {filename}")
