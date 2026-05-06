import os

def update_emails():
    old_email = "info@eliteluxurybookings.com"
    new_email = "contact@eliteluxurybookings.com"
    count = 0
    
    for root, dirs, files in os.walk("."):
        if ".git" in dirs:
            dirs.remove(".git")
        if "_archive" in dirs:
            dirs.remove("_archive")
            
        for file in files:
            if file.endswith((".html", ".php", ".js", ".css", ".txt")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if old_email in content:
                        new_content = content.replace(old_email, new_email)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {file_path}")
                        count += 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    print(f"\nTotal files updated: {count}")

if __name__ == "__main__":
    update_emails()
