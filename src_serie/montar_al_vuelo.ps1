param([string]$Caps = '1,2,3,4,5', [string]$Vol = '0.10')
# Overlapped pipeline for a series: each chapter is mounted as soon as its 5 clips + _ok exist, while glabs_clips.py keeps generating the others.
# Run it in the series folder alongside the clips job:  powershell -ExecutionPolicy Bypass -File src\montar_al_vuelo.ps1
# Per chapter: montaje -> subs -> quemar -> subs_hook -> (needs hook) unir -> mezclar_subs (music) -> unir -> poner_banner.
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$s = $PSScriptRoot
Set-Location (Split-Path $s)
$pend = [System.Collections.ArrayList]@($Caps -split '[,\s]+' | Where-Object { $_ })
while ($pend.Count -gt 0) {
  $hecho = $false
  foreach ($n in @($pend)) {
    $clips = (Get-ChildItem "visual\cap$n\clips" -Filter *.mp4 -ErrorAction SilentlyContinue | Measure-Object).Count
    $hook = Test-Path "hooks\cap$n\HOOK_CAP$n.mp4"
    if ($clips -ge 5 -and $hook) {
      "===== CAP $n  $(Get-Date -Format HH:mm) ====="
      powershell -ExecutionPolicy Bypass -File "$s\final_sm.ps1" -Caps $n
      python "$s\mezclar_subs.py" $n $Vol
      python "$s\unir.py" $n
      python "$s\poner_banner.py" $n
      $pend.Remove($n); $hecho = $true
    }
  }
  if (-not $hecho) { Start-Sleep 60 }
}
"===== MONTAJE FIN $(Get-Date -Format HH:mm) ====="
