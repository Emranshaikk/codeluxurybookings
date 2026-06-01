with open(r"c:\Users\imran\OneDrive\Desktop\ELB code\index.html", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

print("Contains rel='icon'?:", "rel=\"icon\"" in content)
print("Contains rel='shortcut icon'?:", "rel=\"shortcut icon\"" in content or "rel='shortcut icon'" in content)
print("Contains favicon.png?:", "favicon.png" in content)
print("Contains favicon.ico?:", "favicon.ico" in content)

import re
head_match = re.search(r"<head[^>]*>", content, re.IGNORECASE)
if head_match:
    print("\nHead section starts:")
    pos = head_match.end()
    print(content[pos:pos+300])
else:
    print("No <head> tag found!")
