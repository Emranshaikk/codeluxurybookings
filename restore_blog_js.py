import re

try:
    with open("old_blog.html", "r", encoding="utf-16le") as f:
        old_content = f.read()
except Exception as e:
    print(f"Error reading old_blog.html: {e}")
    exit(1)

# Find the script block
# The exact signature is `let allPosts = [];` inside a script block.
script_match = re.search(r'<script>\s*let allPosts = \[\];.*?</script>', old_content, re.DOTALL)

if not script_match:
    print("Could not find the script block.")
    exit(1)

blog_script = script_match.group(0)

# Now read the current blog.html
with open("blog.html", "r", encoding="utf-8") as f:
    blog_content = f.read()

# Replace the toggleMobileMenu script block with the blog_script + toggleMobileMenu
# Wait! In the old_blog.html, toggleMobileMenu is IN THE SAME SCRIPT BLOCK!
# Look at the previous Get-Content output:
#         // Mobile Menu Toggle
#         function toggleMobileMenu() { ... }
#     </script>

# So `blog_script` ALREADY HAS toggleMobileMenu!
# Let's replace the entire script block at the bottom of `blog.html`
blog_content = re.sub(r'<script>\s*function toggleMobileMenu.*?<\/script>', blog_script, blog_content, flags=re.DOTALL)

with open("blog.html", "w", encoding="utf-8") as f:
    f.write(blog_content)

print("Successfully restored the blog script.")
