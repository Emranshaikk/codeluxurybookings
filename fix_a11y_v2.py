import glob
import re

files_changed = 0

for filepath in glob.glob("*.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    old_content = content
    
    # Advanced regex to catch <label> and the following input/select/textarea
    # It looks for label without a "for" attribute, and the next input without an "id" attribute
    
    def replacer(match):
        label_attrs = match.group(1)
        label_content = match.group(2)
        tag = match.group(3)
        before_name = match.group(4)
        name = match.group(5)
        after_name = match.group(6)
        
        # Avoid double adding
        if 'for=' in label_attrs or 'id=' in before_name or 'id=' in after_name:
            return match.group(0)
            
        return f'<label for="{name}"{label_attrs}>{label_content}</label>\n                        <{tag} id="{name}"{before_name}name="{name}"{after_name}>'

    pattern = re.compile(r'<label([^>]*)>(.*?)</label>\s*<(input|select|textarea)([^>]*)name=["\']([^"\']+)["\']([^>]*)>', re.IGNORECASE | re.DOTALL)
    
    content = pattern.sub(replacer, content)

    if content != old_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        files_changed += 1

print(f"Updated {files_changed} files.")
