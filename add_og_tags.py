import os
import re

def add_og_tags():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    print(f"Processing {len(html_files)} HTML files for OG tags...")
    
    files_changed = 0
    default_image = "https://eliteluxurybookings.com/assets/elite_jet_master_hero.png"

    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        old_content = content
        
        # Check if OG tags already exist (prevent duplicates)
        if 'property="og:title"' in content or 'property="og:image"' in content:
            continue
            
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Elite Luxury Bookings"
        
        # Extract description
        desc_match = re.search(r'<meta name="description"[^>]*content="([^"]*)"', content, re.IGNORECASE)
        description = desc_match.group(1).strip() if desc_match else "We curate world-class luxury experiences: Private Jets, Luxury Yachts, and Exclusive Villas."
        
        # Build URL
        slug = filename.replace('.html', '')
        url = "https://eliteluxurybookings.com/" if slug == 'index' else f"https://eliteluxurybookings.com/{slug}/"
        
        og_tags = f"""
    <!-- Open Graph / Social Sharing -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{default_image}">
    <meta property="og:site_name" content="Elite Luxury Bookings">
"""

        # Inject before </head>
        content = content.replace('</head>', og_tags + '</head>')
        
        if content != old_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            files_changed += 1

    print(f"OG tags added to {files_changed} files.")

if __name__ == "__main__":
    add_og_tags()
