import os
import re

def execute_upgrades():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    print(f"Processing {len(html_files)} HTML files...")
    
    org_schema = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Elite Luxury Bookings",
      "url": "https://eliteluxurybookings.com",
      "logo": "https://eliteluxurybookings.com/favicon.png",
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+918801079030",
        "contactType": "Concierge Customer Service",
        "availableLanguage": "English"
      }
    }
    </script>
"""

    preconnect_tags = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
"""

    files_changed = 0

    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        old_content = content
        
        # 1. Inject preconnect tags before preload of google fonts if missing
        if 'rel="preconnect" href="https://fonts.googleapis.com"' not in content:
            if '<link rel="preload"\n\n        href="https://fonts.googleapis.com' in content:
                 content = content.replace('<link rel="preload"\n\n        href="https://fonts.googleapis.com', preconnect_tags.strip() + '\n    <link rel="preload"\n\n        href="https://fonts.googleapis.com')
            elif '<link rel="preload" as="style" href="https://fonts.googleapis.com' in content:
                 content = content.replace('<link rel="preload" as="style" href="https://fonts.googleapis.com', preconnect_tags.strip() + '\n    <link rel="preload" as="style" href="https://fonts.googleapis.com')
        
        # 2. Inject Organization schema before </head> if missing
        if '"@type": "Organization"' not in content or '"name": "Elite Luxury Bookings"' not in content:
            # wait, the template has a Service schema that embeds Organization as the provider.
            # let's just make sure we don't duplicate. Wait, the template has "provider": {"@type": "Organization"}
            # We want a top level Organization schema.
            if 'contactPoint' not in content:
                content = content.replace('</head>', org_schema + '</head>')
                
        # 3. Absolute URLs for internal links (excluding CSS/JS/images)
        # Match href="/something" or href="/" but NOT href="/style.css" or href="/favicon.png"
        content = re.sub(r'href="/(?!style\.css|favicon\.png|assets/|images/)([^"]*)"', r'href="https://eliteluxurybookings.com/\1"', content)

        if content != old_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            files_changed += 1

    print(f"Upgrades applied to {files_changed} files.")

if __name__ == "__main__":
    execute_upgrades()
