# Clips (4 s, 5 per chapter) with TWO Google accounts at once: Google Vids (omni_vids) for the first chapters, Flow (omni_flash) for the last ones.
# Odd passes use the chapter group's own model, even passes the other one, so leftovers (NO_OUTPUT) get a second chance on the other engine.
param([string]$Serie = 'mozo', [string]$VidsCaps = '1,2,3', [string]$FlowCaps = '4,5', [int]$Passes = 8, [int]$Parallel = 2)
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$py = 'C:\Users\Luis\AppData\Local\Programs\Python\Python313\python.exe'
$root = "C:\Users\Luis\calude\$Serie"
Set-Location $root
function Run-Group($caps, $primary, $other, $tag) {
  $list = $caps -split '[,\s]+' | Where-Object { $_ }
  for ($p = 1; $p -le $Passes; $p++) {
    $falta = 0
    foreach ($n in $list) { $falta += 5 - @(Get-ChildItem "$root\visual\cap$n\clips\*.mp4" -ErrorAction SilentlyContinue).Count }
    "$(Get-Date -Format 'dd HH:mm') [$tag] pasada $p, faltan $falta clips"
    if ($falta -le 0) { break }
    $env:CLIP_MODEL = $(if ($p % 2 -eq 1) { $primary } else { $other })
    & $py "$root\src\glabs_clips.py" @list --parallel 2 *> "$root\visual\_clips_${tag}_pasada$p.log"
    Start-Sleep 30
  }
  "[$tag] fin"
}
if ($MyInvocation.InvocationName -ne '.') {
  $flow = Start-Job -ScriptBlock {
    param($py, $root, $caps, $passes)
    Set-Location $root
    $list = $caps -split '[,\s]+' | Where-Object { $_ }
    for ($p = 1; $p -le $passes; $p++) {
      $falta = 0
      foreach ($n in $list) { $falta += 5 - @(Get-ChildItem "$root\visual\cap$n\clips\*.mp4" -ErrorAction SilentlyContinue).Count }
      "$(Get-Date -Format 'dd HH:mm') [flow] pasada $p, faltan $falta clips"
      if ($falta -le 0) { break }
      $env:CLIP_MODEL = $(if ($p % 2 -eq 1) { 'omni_flash' } else { 'omni_vids' })
      & $py "$root\src\glabs_clips.py" @list --parallel 2 *> "$root\visual\_clips_flow_pasada$p.log"
      Start-Sleep 30
    }
  } -ArgumentList $py, $root, $FlowCaps, $Passes
  Run-Group $VidsCaps 'omni_vids' 'omni_flash' 'vids'
  Wait-Job $flow | Out-Null
  Receive-Job $flow
}
"===== COLA CLIPS FIN $(Get-Date -Format 'dd HH:mm') ====="