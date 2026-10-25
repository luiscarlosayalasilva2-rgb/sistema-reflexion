param([int[]]$Caps = @(1,2,3,4,5))
# Pulido: max 0.3 s of air at each end + loudnorm. Output audio\pulido\capN.mp3 (the SRT is made from THIS file).
$root = Split-Path $PSScriptRoot
$out = Join-Path $root 'audio\pulido'; New-Item -ItemType Directory -Force $out | Out-Null
$trim = 'silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.3'
$af = "$trim,areverse,$trim,areverse,loudnorm=I=-16:TP=-1.5:LRA=11"
foreach ($n in $Caps) {
  $src = Join-Path $root "audio\cap$n.mp3"; $dst = Join-Path $out "cap$n.mp3"
  if (-not (Test-Path $src)) { "cap$n sin audio"; continue }
  ffmpeg -hide_banner -loglevel error -y -i $src -af $af -ar 44100 -b:a 192k $dst
  $d1 = [double](ffprobe -v error -show_entries format=duration -of csv=p=0 $src)
  $d2 = [double](ffprobe -v error -show_entries format=duration -of csv=p=0 $dst)
  "cap$n  original {0:N2}s  pulido {1:N2}s" -f $d1, $d2
}
