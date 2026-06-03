import re

def fix_links():
    filepath = "yacht-charter-available-now.html"
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for markdown links: [text](url)
    # We need to handle potential newlines inside the text, so we use re.DOTALL and [\s\S]*?
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    def replacer(match):
        text = match.group(1).strip()
        url = match.group(2).strip()
        # Clean up inner whitespaces/newlines from text
        text = re.sub(r'\s+', ' ', text)
        return f'<a href="{url}">{text}</a>'

    fixed_content, count = pattern.subn(replacer, content)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"Successfully converted {count} markdown links to HTML in {filepath}")
    else:
        print("No markdown links found in the file.")

if __name__ == "__main__":
    fix_links()
