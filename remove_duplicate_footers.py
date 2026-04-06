import os
import re

def remove_duplicate_footers():
    count_fixed = 0
    # Pattern to match the entire footer block including the markers with any whitespace
    footer_pattern = r'\s*<!-- ELB_FOOTER_START -->.*?<!-- ELB_FOOTER_END -->'
    
    for root, dirs, files in os.walk('.'):
        if 'index.html' in files:
            path = os.path.join(root, 'index.html')
            
            # Skip assets or temp folders
            if any(x in root for x in ['assets', '.', 'tmp']):
                continue
                
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                
                # Find all occurrences of the footer block
                blocks = list(re.finditer(footer_pattern, content, re.DOTALL))
                
                if len(blocks) > 1:
                    print(f"Found {len(blocks)} footer blocks in {path}. Fixing...")
                    
                    # Strategy: Keep only the LAST instance of the footer block
                    # We remove all but the last one by replacing them with empty space
                    
                    # Get the indices of the blocks to remove (all except the last)
                    # We work backwards to not mess up indices
                    blocks_to_remove = blocks[:-1]
                    new_content = content
                    for block in reversed(blocks_to_remove):
                        start, end = block.span()
                        new_content = new_content[:start] + new_content[end:]
                    
                    content = new_content
                    count_fixed += 1
                
                if content != original:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
            except Exception as e:
                print(f"Error processing {path}: {e}")

    print(f"Successfully deduplicated footers in {count_fixed} files.")

if __name__ == "__main__":
    remove_duplicate_footers()
