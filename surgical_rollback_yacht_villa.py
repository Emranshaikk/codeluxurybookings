import os
import re

def surgical_rollback():
    count = 0
    # Targeted Cleanup for Yacht and Villa pages that got the Aviation Engine by mistake
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'index.html':
                path = os.path.join(root, file)
                
                # Exclude obvious non-aviation directories
                is_yacht_dir = 'luxury-yacht-rentals' in root or 'yacht' in root.lower()
                is_villa_dir = 'luxury-villa-rentals' in root or 'villa' in root.lower()
                
                if not (is_yacht_dir or is_villa_dir):
                    continue
                    
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'ELB_VALENS_API_ENGINE_START' in content:
                    # Remove the aviation engine
                    original = content
                    content = re.sub(r'<!-- ELB_VALENS_API_ENGINE_START -->.*?<!-- ELB_VALENS_API_ENGINE_END -->', '', content, flags=re.DOTALL)
                    
                    # Cleanup duplicated </header> tags if any
                    content = re.sub(r'</header>\s*</header>', '</header>', content)
                    
                    if content != original:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                        print(f"Surgical Rollback: {path}")

    print(f"\nCleaned up {count} Yacht/Villa pages that accidentally received the Aviation Engine.")

if __name__ == "__main__":
    surgical_rollback()
