import os

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

def main():
    count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if not file.endswith('.html'): continue
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "instagram.com/eliteluxurybookings/" in content:
                    continue

                # Broad search for contact link and append
                if 'contact/' in content and '</a>' in content:
                    # Find all occurrences of contact/
                    pos = 0
                    while True:
                        pos = content.find('contact/', pos)
                        if pos == -1: break
                        
                        # Find the next </a>
                        end_tag = content.find('</a>', pos)
                        if end_tag != -1:
                            # Check if it's NOT in a list item (simple check)
                            snippet = content[end_tag:end_tag+20]
                            if '</li>' not in snippet:
                                content = content[:end_tag+4] + SOCIAL_A + content[end_tag+4:]
                                with open(path, 'w', encoding='utf-8') as f:
                                    f.write(content)
                                print(f"Updated standalone: {path}")
                                count += 1
                                break # Move to next file
                        pos += 1
            except Exception as e:
                print(f"Error {path}: {e}")
    print(f"Total: {count}")

if __name__ == "__main__":
    main()
