param([int[]]$Caps = @(2,3,4,5))
# Full montage chain per chapter, ONE render at a time: montage -> music -> subtitles -> hook subtitles -> join + checks.
$s = $PSScriptRoot
foreach ($n in $Caps) {
  "===== CAP $n  $(Get-Date -Format HH:mm) ====="
  python "$s\montaje.py" $n 2>&1 | Where-Object { $_ -notmatch '^seg' }
  python "$s\mezclar.py" $n
  python "$s\subs.py" $n
  python "$s\quemar.py" $n "$(Split-Path $s)\out\cap${n}_base_m.mp4"
  python "$s\subs_hook.py" $n
  python "$s\unir.py" $n
}
"===== FIN $(Get-Date -Format HH:mm) ====="
