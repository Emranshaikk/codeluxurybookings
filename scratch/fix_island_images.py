import os

workspace_dir = r"c:\Users\imran\OneDrive\Desktop\ELB code"
filepath = os.path.join(workspace_dir, "all-inclusive-private-island-rental.html")

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any occurrence of 'assets/' that is not preceded by a slash or a letter/number
# Or we can do targeted replacements of typical patterns:
# src="assets/ -> src="/assets/
# src='assets/ -> src='/assets/
# url('assets/ -> url('/assets/
# url("assets/ -> url("/assets/
# url(assets/ -> url(/assets/

replacements = [
    ('src="assets/', 'src="/assets/'),
    ("src='assets/", "src='/assets/"),
    ('url(\'assets/', 'url(\'/assets/'),
    ('url("assets/', 'url("/assets/'),
    ('url(assets/', 'url(/assets/'),
    # Also check for link href="assets/ for favicon or styles
    ('href="assets/', 'href="/assets/'),
    ("href='assets/", "href='/assets/"),
    # Also check background-image: url('assets/
    ("url('assets/", "url('/assets/")
]

fixed_content = content
for target, replacement in replacements:
    count = fixed_content.count(target)
    if count > 0:
        fixed_content = fixed_content.replace(target, replacement)
        print(f"Replaced {count} occurrences of '{target}' with '{replacement}'")

# Double check if any raw 'assets/' references remain in quote marks
# For example, in og:image metadata: content="assets/...
metadata_reps = [
    ('content="assets/', 'content="/assets/'),
    ("content='assets/", "content='/assets/")
]

for target, replacement in metadata_reps:
    count = fixed_content.count(target)
    if count > 0:
        fixed_content = fixed_content.replace(target, replacement)
        print(f"Replaced {count} occurrences of '{target}' with '{replacement}'")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Finished fixing images in all-inclusive-private-island-rental.html")
