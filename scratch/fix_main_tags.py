import os
import re

def fix_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check if <main is present, but </main> is NOT present
    if '<main' in content.lower() and '</main>' not in content.lower():
        print(f"Fixing unclosed <main> in: {file_path}")
        
        # Determine the insertion point
        footer_comment_match = re.search(r'<!--\s*Master\s*Footer\s*-->', content, re.IGNORECASE)
        if footer_comment_match:
            insert_idx = footer_comment_match.start()
            new_content = content[:insert_idx] + "</main>\n\n    " + content[insert_idx:]
        else:
            footer_tag_match = re.search(r'<footer', content, re.IGNORECASE)
            if footer_tag_match:
                insert_idx = footer_tag_match.start()
                new_content = content[:insert_idx] + "</main>\n\n" + content[insert_idx:]
            else:
                body_close_match = re.search(r'</body>', content, re.IGNORECASE)
                if body_close_match:
                    insert_idx = body_close_match.start()
                    new_content = content[:insert_idx] + "</main>\n" + content[insert_idx:]
                else:
                    print(f"Could not find insert point for {file_path}")
                    return False
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '_archive' in root or 'scratch' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    fixed_count = 0
    for file_path in html_files:
        if fix_html_file(file_path):
            fixed_count += 1
            
    print(f"\nCompleted! Fixed unclosed <main> tags in {fixed_count} files.")

if __name__ == '__main__':
    main()
