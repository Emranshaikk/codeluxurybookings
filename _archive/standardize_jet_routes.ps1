# ELITE LUXURY BOOKINGS - JET ROUTE STANDARDIZATION SCRIPT
# This script propagates the optimized "Beijing to Seoul" template across the entire aviation route network.

$templateFile = "beijing-to-seoul-private-jet-cost.html"
$templateContent = Get-Content $templateFile -Raw

if (!$templateContent) {
    Write-Error "Template file not found or empty."
    exit
}

# Identify all route files (excluding the template and the silo master)
$routeFiles = Get-ChildItem "*-to-*-private-jet-cost.html" | Where-Object { 
    $_.Name -ne $templateFile -and $_.Name -ne "global-route-silo.html" 
}

foreach ($file in $routeFiles) {
    Write-Host "Standardizing: $($file.Name)..."
    
    # 1. Extract Origin and Destination from Filename
    # Example: london-to-paris-private-jet-cost.html -> London, Paris
    $baseName = $file.BaseName
    $parts = $baseName -split "-to-"
    if ($parts.Count -lt 2) { continue }
    
    $originRaw = $parts[0]
    $destRaw = ($parts[1] -split "-private-jet-cost")[0]
    
    $origin = (Get-Culture).TextInfo.ToTitleCase($originRaw.Replace("-", " "))
    $dest = (Get-Culture).TextInfo.ToTitleCase($destRaw.Replace("-", " "))

    # 2. Localize Content
    $newContent = $templateContent
    
    # Update Meta Tags
    $newContent = $newContent -replace "Beijing to Seoul Private Jet Charter", "$origin to $dest Private Jet Charter"
    $newContent = $newContent -replace "Beijing to Seoul Private Jet Cost", "$origin to $dest Private Jet Cost"
    $newContent = $newContent -replace "Beijing to Seoul", "$origin to $dest"
    
    # Update Canonical
    $newContent = $newContent -replace "https://eliteluxurybookings.com/beijing-to-seoul-private-jet-cost/", "https://eliteluxurybookings.com/$baseName/"
    
    # Update Descriptions (using the new premium pattern)
    $newContent = $newContent -replace "experience the ultimate Beijing to Seoul private jet charter", "experience the ultimate $origin to $dest private jet charter"
    $newContent = $newContent -replace "cultural heart of Beijing to the high-tech skyline of Seoul", "vibrant landscape of $origin to the premium destinations of $dest"
    $newContent = $newContent -replace "Beijing - Seoul corridor", "$origin - $dest corridor"
    
    # Update Schema (Breadcrumbs & Service)
    # The regex approach is safer for JSON
    $newContent = $newContent -replace '"name": "Beijing to Seoul"', "`"name`": `"$origin to $dest`""
    $newContent = $newContent -replace '"areaServed": "Beijing to Seoul"', "`"areaServed`": `"$origin to $dest`""
    
    # Update Form Select Options (Localization)
    $newContent = $newContent -replace '<option value="BEIJING">BEIJING - Beijing Terminal</option>', "<option value=`"$($origin.ToUpper())`">$($origin.ToUpper()) - $($origin) Terminal</option>"
    $newContent = $newContent -replace '<option value="SEOUL">SEOUL - Seoul Terminal</option>', "<option value=`"$($dest.ToUpper())`">$($dest.ToUpper()) - $($dest) Terminal</option>"
    $newContent = $newContent -replace "Beijing Airport", "$origin Airport"
    $newContent = $newContent -replace "Seoul Airport", "$dest Airport"

    # Update Hero H1 & Sub
    $newContent = $newContent -replace ">Beijing to Seoul Private Jet Charter</h1>", ">$origin to $dest Private Jet Charter</h1>"
    
    # Update Airports Section
    $newContent = $newContent -replace "<li>Beijing Capital \(PEK\) / Beijing Daxing \(PKX\)</li>", "<li>$origin Private Terminals (FBO)</li>"
    $newContent = $newContent -replace "<li>Seoul Gimpo \(GMP\) / Seoul Incheon \(ICN\)</li>", "<li>$dest Private Terminals (FBO)</li>"

    # 3. Save the standardized file
    Set-Content $file.FullName $newContent -NoNewline
}

Write-Host "Network-wide standardization complete. $($routeFiles.Count) pages updated."
