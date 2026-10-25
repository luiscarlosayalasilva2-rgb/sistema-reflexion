param([string]$Esperar, [string]$Patron, [string]$Caps, [string]$Log)
# Waits until $Esperar contains $Patron, then runs the no-music montage chain for $Caps into $Log.
while (-not ((Test-Path $Esperar) -and (Select-String -Path $Esperar -Pattern $Patron -Quiet))) { Start-Sleep 30 }
& powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\final_sm.ps1" -Caps $Caps *> $Log
