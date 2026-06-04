import os
import re

def clean_old_blog():
    filepath = r"c:\Users\imran\OneDrive\Desktop\ELB code\old_blog.html"
    if not os.path.exists(filepath):
        print("old_blog.html does not exist!")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Clean up the legacy Villa Silo block specifically
    old_len = len(content)
    content = re.sub(r'<!-- VILLA AUTHORITY SILO -->.*?Villa Authority Silo.*?</div>\s*</div>', '', content, flags=re.DOTALL)
    new_len = len(content)
    
    if old_len != new_len:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully cleaned up old_blog.html (removed {old_len - new_len} bytes)")
    else:
        print("Villa Silo block not found in old_blog.html or already clean.")

if __name__ == "__main__":
    clean_old_blog()
