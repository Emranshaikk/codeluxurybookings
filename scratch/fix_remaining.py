import os

def fix_remaining():
    root_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
    
    # Fix old_blog.html navigation link
    path = os.path.join(root_dir, "old_blog.html")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        target = '<li><a href="https://eliteluxurybookings.com/blog/" style="color: rgba(255, 255, 255, 0.85); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=\'#D4AF37\'" onmouseout="this.style.color=\'rgba(255, 255, 255, 0.85)\'">Blog</a></li>'
        replacement = target + '\n                <li><a href="https://eliteluxurybookings.com/contact/" style="color: rgba(255, 255, 255, 0.85); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=\'#D4AF37\'" onmouseout="this.style.color=\'rgba(255, 255, 255, 0.85)\'">Contact</a></li>'
        
        if target in content:
            content = content.replace(target, replacement, 1)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Fixed: Restored contact navigation link in old_blog.html")
        else:
            print("Warning: Could not find exact blog link target in old_blog.html")

if __name__ == '__main__':
    fix_remaining()
