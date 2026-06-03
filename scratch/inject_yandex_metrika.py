import os

directory = r"c:\Users\imran\OneDrive\Desktop\ELB code"
html_files = [f for f in os.listdir(directory) if f.endswith(".html")]

print(f"Found {len(html_files)} HTML files. Beginning injection...")

yandex_code = """
<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){
        m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    })(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=103558768', 'ym');

    ym(103558768, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/103558768" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->
"""

count = 0
skipped = 0

for filename in html_files:
    path = os.path.join(directory, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='latin-1') as f:
            content = f.read()
            
    # Check if Yandex code is already present
    if "103558768" in content:
        skipped += 1
        continue
        
    if "</head>" in content:
        # Inject right before </head>
        content = content.replace("</head>", f"{yandex_code}\n</head>")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        except UnicodeEncodeError:
            with open(path, 'w', encoding='latin-1') as f:
                f.write(content)
        count += 1
    else:
        print(f"WARNING: No </head> tag found in {filename}")

print(f"\nCompleted!")
print(f"Successfully injected Yandex.Metrika in: {count} files.")
print(f"Skipped (already present): {skipped} files.")
