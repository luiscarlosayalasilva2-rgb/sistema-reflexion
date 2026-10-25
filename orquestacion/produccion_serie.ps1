param([string]$Serie = 'mozo')
# Fichas -> imagenes (nano_pics) -> clips (omni_vids) for one series, hands-off.
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$py = 'C:\Users\Luis\AppData\Local\Programs\Python\Python313\python.exe'
$root = "C:\Users\Luis\calude\$Serie"
Set-Location $root
$env:GLABS_IMG_MODEL = $(if ($env:IMG_MODEL) { $env:IMG_MODEL } else { 'nano_pics' })
$env:CLIP_MODEL = 'omni_vids'
"$(Get-Date -Format 'dd HH:mm') fichas $Serie"
for ($i = 0; $i -lt 4; $i++) { & $py "$root\src\glabs_fichas.py" --parallel 3; if (-not (Select-String -Path "$root\fichas_log.txt" -Pattern 'zzz' -Quiet)) { } ; Start-Sleep 5 }
& "$PSScriptRoot\cola_imgs_serie.ps1" -Serie $Serie -Parallel 4
& "$PSScriptRoot\cola_clips_serie.ps1" -Serie $Serie -Parallel 2
"===== PRODUCCION $Serie FIN $(Get-Date -Format 'dd HH:mm') ====="