param([string]$Serie = 'mozo')
# Waits for produccion_serie to finish, then runs the hook pipeline (Pics board shots + Vids 10 s hook + review).
$log = "C:\Users\Luis\calude\produccion_$Serie.log"
while (-not (Select-String -Path $log -Pattern 'PRODUCCION .* FIN' -Quiet -ErrorAction SilentlyContinue)) { Start-Sleep 20 }
$env:GLABS_IMG_MODEL = $(if ($env:IMG_MODEL) { $env:IMG_MODEL } else { 'nano_pics' })
$env:HOOK_MODEL = 'omni_vids'
"$(Get-Date -Format 'dd HH:mm') hooks $Serie"
& powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Luis\calude\$Serie\src\hooks_todo.ps1"
"===== POST $Serie FIN $(Get-Date -Format 'dd HH:mm') ====="