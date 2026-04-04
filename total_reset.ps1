$files = Get-ChildItem route*.html | Where-Object { $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    Write-Host "Fixing Network corruption in $($file.Name)..."
    $content = Get-Content $file.FullName -Raw

    # 1. Fix the "ovember" JavaScript bug
    $content = $content -replace 'ovember"', '"November"'

    # 2. Fix the "Shadow Brace" (Extra closing brace before </style> in the silo)
    # We want exactly TWO braces before </style> in the silo (one for inner, one for media query)
    # Most files have:
    # }
    # }
    # </style>
    # My previous script might have added a third one.
    
    $content = $content -replace '(?s)\}\s+\}\s+\}\s+</style>', "}`n    }`n    </style>"

    # 3. Final Header Cleanup (Ensure no extra braces there either)
    # Header should end with } } </style>
    # Find /* MOBILE EXCELLENCE */ block and verify ends with }}</style>
    
    Set-Content $file.FullName $content -NoNewline
}

Write-Host "Total Reset Complete. Network is now healthy."
