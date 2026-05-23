import os
import re

def fix_seo_and_analytics():
    root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
    files = [f for f in os.listdir(root_dir) if f.endswith('.html')]
    
    analytics_script = """
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-J56D1LJLFM"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() { dataLayer.push(arguments); }
        gtag('js', new Date());
        gtag('config', 'G-J56D1LJLFM');
    </script>
"""
    
    for filename in files:
        filepath = os.path.join(root_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # 1. FIX ANALYTICS
        if 'G-J56D1LJLFM' not in content:
            # Inject before </head>
            if '</head>' in content:
                content = content.replace('</head>', analytics_script + '</head>')
                modified = True
                print(f"Added Analytics to {filename}")

        # 2. FIX CANONICAL
        expected_slug = filename.replace('.html', '')
        if expected_slug == 'index':
             expected_canonical = "https://eliteluxurybookings.com/"
        else:
             expected_canonical = f"https://eliteluxurybookings.com/{expected_slug}/"
             
        canonical_pattern = re.compile(r'<link rel="canonical" href="([^"]+)"')
        if canonical_pattern.search(content):
            content = canonical_pattern.sub(f'<link rel="canonical" href="{expected_canonical}"', content)
            modified = True
            print(f"Updated Canonical for {filename}")
        else:
            # Inject canonical after title or meta charset
            if '</title>' in content:
                 content = content.replace('</title>', f'</title>\n    <link rel="canonical" href="{expected_canonical}">')
                 modified = True
                 print(f"Injected Missing Canonical for {filename}")
            elif '<meta charset' in content:
                 content = re.sub(r'(<meta charset=[^>]+>)', r'\1\n    <link rel="canonical" href="' + expected_canonical + '">', content)
                 modified = True
                 print(f"Injected Missing Canonical (alt) for {filename}")

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    fix_seo_and_analytics()
