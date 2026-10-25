# Generates the scene images of the series llamadas chapter by chapter through G-Labs, with automatic retries.
# - UNUSUAL_ACTIVITY / TOO_MUCH_TRAFFIC from Google: glabs_api.py stops sending work; this queue waits 10 minutes and retries with fewer in parallel.
# - Daily quota exhausted: switches the model to nano_pics (separate quota).
# Ends when every chapter has all its images. Resumable: images that already exist are skipped.
param([string]$Serie = 'mozo', [string]$Caps = '1,2,3,4,5', [int]$Parallel = 4, [int]$InitialWaitMin = 0)
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$py = 'C:\Users\Luis\AppData\Local\Programs\Python\Python313\python.exe'
$root = "C:\Users\Luis\calude\$Serie"
Set-Location $root
if ($InitialWaitMin -gt 0) { "$(Get-Date -Format 'dd HH:mm') espero $InitialWaitMin min antes de empezar"; Start-Sleep ($InitialWaitMin * 60) }
$list = $Caps -split '[,\s]+' | Where-Object { $_ }
$par = $Parallel
while ($true) {
  $pend = $false
  foreach ($n in $list) {
    $vd = "$root\visual\cap$n"
    $total = [regex]::Matches((Get-Content "$vd\imagenes.json" -Raw -Encoding UTF8), '"n":').Count
    $have = @(Get-ChildItem "$vd\imgs\*.jpg" -ErrorAction SilentlyContinue).Count
    if ($have -ge $total) { continue }
    $pend = $true
    "$(Get-Date -Format 'dd HH:mm') cap$n tiene $have de $total (modelo $(if ($env:GLABS_IMG_MODEL) { $env:GLABS_IMG_MODEL } else { 'nano_banana_2' }), $par en paralelo)"
    & $py "$root\src\glabs_api.py" $n --parallel $par *> "$vd\_glabs.log"
    $have2 = @(Get-ChildItem "$vd\imgs\*.jpg" -ErrorAction SilentlyContinue).Count
    "$(Get-Date -Format 'dd HH:mm') cap$n ahora tiene $have2 de $total"
    if ($have2 -lt $total) {
      if (Select-String -Path "$vd\_glabs.log" -Pattern 'Cuota diaria|QUOTA|RESOURCE_EXHAUSTED' -Quiet) { $env:GLABS_IMG_MODEL = 'nano_pics'; "cuota agotada: cambio a nano_pics" }
      if (Select-String -Path "$vd\_glabs.log" -Pattern 'UNUSUAL_ACTIVITY|TOO_MUCH_TRAFFIC' -Quiet) { $par = [math]::Max(2, $par - 1); "Google pidio esperar: pauso 10 min y bajo a $par en paralelo"; Start-Sleep 600 } else { Start-Sleep 90 }
      break
    }
  }
  if (-not $pend) { break }
}
"===== COLA IMAGENES FIN $(Get-Date -Format 'dd HH:mm') ====="
