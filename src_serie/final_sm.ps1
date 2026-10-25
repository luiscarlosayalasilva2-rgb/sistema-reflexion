param([string]$Caps = '1,2,3,4,5')
# Montage chain WITHOUT music, one render at a time: montage -> subtitles -> burn -> hook subtitles -> join + checks.
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$s = $PSScriptRoot
Set-Location (Split-Path $s)
foreach ($n in ($Caps -split '[,\s]+' | Where-Object { $_ })) {
  "===== CAP $n  $(Get-Date -Format HH:mm) ====="
  python "$s\montaje.py" $n 2>&1 | Where-Object { $_ -notmatch '^seg' }
  python "$s\subs.py" $n
  python "$s\quemar.py" $n "$(Split-Path $s)\out\cap${n}_base.mp4"
  python "$s\subs_hook.py" $n
  python "$s\unir.py" $n
}
"===== FIN $(Get-Date -Format HH:mm) ====="
