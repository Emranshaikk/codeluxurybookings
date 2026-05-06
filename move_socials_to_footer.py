import os
import re

SOCIAL_LI = """
                        <li><a href="https://www.instagram.com/eliteluxurybookings/" target="_blank"
                                style="color: rgba(255, 255, 255, 0.85); text-decoration:none; font-size:0.9rem; transition:color 0.3s;"
                                onmouseover="this.style.color='#D4AF37'"
                                onmouseout="this.style.color='rgba(255, 255, 255, 0.85)'">Instagram</a></li>
                        <li><a href="https://www.facebook.com/profile.php?id=61575800006704" target="_blank"
                                style="color: rgba(255, 255, 255, 0.85); text-decoration:none; font-size:0.9rem; transition:color 0.3s;"
                                onmouseover="this.style.color='#D4AF37'"
                                onmouseout="this.style.color='rgba(255, 255, 255, 0.85)'">Facebook</a></li>
"""

SOCIAL_A = """
                <a href="https://www.instagram.com/eliteluxurybookings/" target="_blank"
                    style="color: rgba(255, 255, 255, 0.7); text-decoration: none; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;"
                    onmouseover="this.style.color='#D4AF37'"
                    onmouseout="this.style.color='rgba(255,255,255,0.7)'">Instagram</a>
                <a href="https://www.facebook.com/profile.php?id=61575800006704" target="_blank"
                    style="color: rgba(255, 255, 255, 0.7); text-decoration: none; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;"
                    onmouseover="this.style.color='#D4AF37'"
                    onmouseout="this.style.color='rgba(255,255,255,0.7)'">Facebook</a>
"""

def process_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        
        # 1. REMOVE from Header (anything before 60% of the file)
        split_point = int(len(content) * 0.6)
        header_area = content[:split_point]
        footer_area = content[split_point:]
        
        new_header_area = header_area
        # Remove instagram <li>
        new_header_area = re.sub(r'<li>\s*<a href="https://www\.instagram\.com/eliteluxurybookings/".*?</a>\s*</li>', '', new_header_area, flags=re.DOTALL)
        # Remove facebook <li>
        new_header_area = re.sub(r'<li>\s*<a href="https://www\.facebook\.com/profile\.php\?id=61575800006704".*?</a>\s*</li>', '', new_header_area, flags=re.DOTALL)
        
        if new_header_area != header_area:
            header_area = new_header_area
            updated = True

        # 2. ADD to Footer (if not already there in the footer area)
        if "instagram.com/eliteluxurybookings/" not in footer_area:
            # Try list pattern first (footer services list)
            blog_li_pattern = r'(<li>\s*<a href="[^"]*?blog/".*?</a>\s*</li>)'
            matches = list(re.finditer(blog_li_pattern, footer_area, re.DOTALL))
            if matches:
                match = matches[-1]
                footer_area = footer_area[:match.end()] + SOCIAL_LI + footer_area[match.end():]
                updated = True
            else:
                # Try standalone pattern (centered footer)
                contact_a_pattern = r'(<a href="[^"]*?contact/".*?</a>)'
                matches = list(re.finditer(contact_a_pattern, footer_area, re.DOTALL))
                if matches:
                    match = matches[-1]
                    end = match.end()
                    footer_area = footer_area[:end] + SOCIAL_A + footer_area[end:]
                    updated = True

        if updated:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(header_area + footer_area)
            return True
    except Exception as e:
        print(f"Error processing {path}: {e}")
    return False

def main():
    count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                if process_file(os.path.join(root, file)):
                    count += 1
    print(f"Total files fixed: {count}")

if __name__ == "__main__":
    main()
