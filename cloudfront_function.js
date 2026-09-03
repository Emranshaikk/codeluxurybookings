function handler(event) {
    var request = event.request;
    var uri = request.uri;
    
    // Normalize URI: remove trailing slash and convert to lowercase for matching
    var cleanUri = uri.toLowerCase();
    if (cleanUri.endsWith('/') && cleanUri.length > 1) {
        cleanUri = cleanUri.slice(0, -1);
    }
    
    var redirectUrl = null;
    
    // --- Cluster A redirects (Formentera) ---
    var clusterAUrls = [
        "/boat-trip-from-mallorca-to-formentera",
        "/boat-trip-from-mallorca-to-formentera.html",
        "/yacht-charter-mallorca-to-formentera",
        "/yacht-charter-mallorca-to-formentera.html",
        "/yacht-charter-mallorca-formentera",
        "/yacht-charter-mallorca-formentera.html",
        "/mallorca-to-formentera-private-boat-cost",
        "/mallorca-to-formentera-private-boat-cost.html",
        "/luxury-yacht-rentals/boat-trip-from-mallorca-to-formentera",
        "/luxury-yacht-rentals/boat-trip-from-mallorca-to-formentera.html"
    ];
    
    for (var i = 0; i < clusterAUrls.length; i++) {
        if (cleanUri === clusterAUrls[i]) {
            redirectUrl = "https://eliteluxurybookings.com/private-boat-trip-mallorca-to-formentera/";
            break;
        }
    }
    
    // --- Cluster B redirects (Ibiza) ---
    if (!redirectUrl) {
        var clusterBUrls = [
            "/mallorca-to-ibiza-private-boat-charter",
            "/mallorca-to-ibiza-private-boat-charter.html",
            "/luxury-yacht-rentals/mallorca-to-ibiza-private-boat",
            "/luxury-yacht-rentals/mallorca-to-ibiza-private-boat.html",
            "/private-yacht-from-ibiza-to-mallorca",
            "/private-yacht-from-ibiza-to-mallorca.html"
        ];
        
        for (var j = 0; j < clusterBUrls.length; j++) {
            if (cleanUri === clusterBUrls[j]) {
                redirectUrl = "https://eliteluxurybookings.com/mallorca-to-ibiza-private-boat/";
                break;
            }
        }
    }
    
    // --- Redirect Loops / Critical Fixes ---
    if (!redirectUrl) {
        if (cleanUri === "/mykonos-yacht-charter-masterclass-2026" || cleanUri === "/mykonos-yacht-charter-masterclass-2026.html") {
            redirectUrl = "https://eliteluxurybookings.com/mykonos-yacht-charter/";
        } else if (cleanUri === "/luxury-private-jets") {
            redirectUrl = "https://eliteluxurybookings.com/elite-private-jet-charter/";
        } else if (cleanUri === "/luxury-private-yachts") {
            redirectUrl = "https://eliteluxurybookings.com/luxury-yacht-rentals/";
        } else if (cleanUri === "/blogs") {
            redirectUrl = "https://eliteluxurybookings.com/blog/";
        } else if (cleanUri === "/our-services") {
            redirectUrl = "https://eliteluxurybookings.com/elite-private-jet-charter/";
        } else if (cleanUri === "/how-private-jet-flight-bookings-work") {
            redirectUrl = "https://eliteluxurybookings.com/elite-private-jet-charter/";
        } else if (cleanUri === "/luxury-yacht-re") {
            redirectUrl = "https://eliteluxurybookings.com/luxury-yacht-rentals/";
        } else if (cleanUri === "/private-jet-charter-cost-guide-2026.html") {
            redirectUrl = "https://eliteluxurybookings.com/private-jet-charter-cost-estimator/";
        } else if (cleanUri === "/sitemap.html") {
            redirectUrl = "https://eliteluxurybookings.com/";
        }
    }
    
    // --- Global trailing slash and clean directory mapping (S3 helper) ---
    // If no explicit redirect but request ends in .html, map it to folder-based path
    if (!redirectUrl && uri.endsWith('.html')) {
        // Exclude special verify files
        if (!uri.includes('zohoverify') && !uri.includes('verifyforzoho') && !uri.includes('zoho-domain-verification')) {
            var newPath = uri.slice(0, -5); // remove .html
            redirectUrl = "https://eliteluxurybookings.com" + newPath + "/";
        }
    }
    
    if (redirectUrl) {
        return {
            statusCode: 301,
            statusDescription: 'Moved Permanently',
            headers: {
                'location': { value: redirectUrl }
            }
        };
    }
    
    // If no redirect matched, pass request through unmodified
    return request;
}
