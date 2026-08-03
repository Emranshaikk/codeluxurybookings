import urllib.request
import urllib.parse
import sys

# Reconfigure stdout to use UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

urls = [
    # Cluster A (Mallorca to Formentera)
    "https://eliteluxurybookings.com/boat-trip-from-mallorca-to-formentera/",
    "https://eliteluxurybookings.com/yacht-charter-mallorca-to-formentera/",
    "https://eliteluxurybookings.com/mallorca-to-formentera-private-boat-cost/",
    "https://eliteluxurybookings.com/yacht-charter-mallorca-formentera/",
    "https://eliteluxurybookings.com/luxury-yacht-rentals/boat-trip-from-mallorca-to-formentera/",
    
    # Cluster B (Mallorca to Ibiza)
    "https://eliteluxurybookings.com/mallorca-to-ibiza-private-boat-charter/",
    "https://eliteluxurybookings.com/luxury-yacht-rentals/mallorca-to-ibiza-private-boat/",
    "https://eliteluxurybookings.com/private-yacht-from-ibiza-to-mallorca/",
    
    # Loop issues
    "https://eliteluxurybookings.com/luxury-private-jets/",
    "https://eliteluxurybookings.com/blogs/",
    "https://eliteluxurybookings.com/our-services/",
    "https://eliteluxurybookings.com/how-private-jet-flight-bookings-work/",
    "https://eliteluxurybookings.com/luxury-yacht-re/"
]

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        return None

opener = urllib.request.build_opener(NoRedirectHandler)

print("Balearic Boat Clusters & SEO Redirect Tracer")
print("================================================================================")
print("NOTE: This tests the LIVE domain. Live redirects will update once you deploy")
print("the new .htaccess, CloudFront Function, or S3 Routing Rules.")
print("================================================================================")

for url in urls:
    print(f"Testing: {url}")
    try:
        current_url = url
        chain_count = 0
        visited = set()
        
        while chain_count < 10:
            if current_url in visited:
                print(f"  --> [LOOP DETECTED] {current_url} visited twice!")
                break
            visited.add(current_url)
            
            req = urllib.request.Request(current_url, method="HEAD")
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) EliteRedirectTracer/1.0")
            
            try:
                response = opener.open(req, timeout=5)
                status = response.status
                headers = response.info()
            except urllib.error.HTTPError as e:
                status = e.code
                headers = e.headers
            except Exception as e:
                print(f"  --> [CONNECTION ERROR] {e}")
                break
                
            location = headers.get("Location")
            print(f"  Hop {chain_count + 1}: Status {status}")
            
            if location:
                # resolve relative location headers
                next_url = urllib.parse.urljoin(current_url, location)
                print(f"    --> Redirects to: {next_url}")
                current_url = next_url
                chain_count += 1
            else:
                print(f"    --> [FINAL DESTINATION] Status: {status}")
                break
        else:
            print("  --> [MAX REDIRECTS EXCEEDED] potential loop")
    except Exception as e:
        print(f"  --> [ERROR] {e}")
    print("-" * 80)
