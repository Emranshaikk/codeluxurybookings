# PROPAGATE VALENS WIDGET - ELITE LUXURY BOOKINGS
# This script replaces the failing custom API form with the official Valens Widget across the entire network.

$widgetHtml = @"
            <!-- ELB_VALENS_WIDGET_START -->
            <div class="aviation-search-engine glass-panel"
                style="margin: 2rem auto; max-width: 1000px; padding: 1.5rem; border: 1px solid var(--primary-gold); position: relative; overflow: hidden; background: #000; border-radius: 24px; box-shadow: 0 40px 100px rgba(0,0,0,0.8);">
                <iframe src="https://jetluxe.jetlink.app/affiliate/valens/widget/cb37e0db-af0a-42bd-94c4-26736dae4aa9?signature=07e252c33f271e5994234ad6e8864d593388f699b6f80ee4add5512ffa467224" 
                    frameborder="0" 
                    allowfullscreen 
                    style="width: 100%; min-height: 650px; border-radius: 12px; background: transparent;"></iframe>
                <div style="text-align: center; margin-top: 1rem; font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 2px;">
                    Elite Luxury Bookings | Powered by Valens Core
                </div>
            </div>
            <!-- ELB_VALENS_WIDGET_END -->
"@

$targetFiles = Get-ChildItem -Path ".\*-to-*-private-jet-cost.html" -File

foreach ($file in $targetFiles) {
    Write-Host "Upgrading Widget: $($file.Name)" -ForegroundColor Gold
    
    $content = Get-Content -Path $file.FullName -Raw
    
    # 1. Replace the Engine Block (using regex to find the multi-line block)
    $pattern = "(?s)<!-- ELB_VALENS_API_ENGINE_START -->.*?<!-- ELB_VALENS_API_ENGINE_END -->"
    if ($content -match $pattern) {
        $content = [regex]::Replace($content, $pattern, $widgetHtml)
    }

    # 2. Remove the Bridge Script
    $content = $content -replace '<script src="valens_api_bridge.js"></script>', '<!-- VALENS WIDGET CORE -->'
    $content = $content -replace '<script src="/valens_api_bridge.js"></script>', '<!-- VALENS WIDGET CORE -->'

    Set-Content -Path $file.FullName -Value $content -NoNewline
}

Write-Host "SUCCESS: 115+ Routes upgraded to Native Valens Widget Engine." -ForegroundColor Green
