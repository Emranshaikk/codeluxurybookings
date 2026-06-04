import os

root_dir = r'c:\Users\imran\OneDrive\Desktop\ELB code'
old_cdn = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
new_cdn = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css'

def upgrade():
    count = 0
    for filename in os.listdir(root_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(root_dir, filename)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if old_cdn in content:
                content = content.replace(old_cdn, new_cdn)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Upgraded FontAwesome CDN in {filename}")
                count += 1
    print(f"Total upgraded files: {count}")

if __name__ == '__main__':
    upgrade()
