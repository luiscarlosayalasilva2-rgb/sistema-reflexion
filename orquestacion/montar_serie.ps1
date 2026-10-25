# Resumable montage of the series llamadas: for each chapter runs only the steps whose output is missing or truncated
# (checked with ffprobe durations), so a reboot or a stopped session never makes it start a chapter from zero.
# Steps: montaje -> subs -> quemar -> subs_hook -> mezclar_subs (music 0.10) -> unir (hook + chapter) -> poner_banner.
param([string]$Serie = 'mozo', [string]$Caps = '1,2,3,4,5', [string]$Vol = '0.10', [switch]$ConMusica, [switch]$SoloBase)
# Series llamadas goes WITHOUT music (Luis, 2026-10-19). Use -ConMusica to mix musica_serie.mp3 under the narration again.
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$py = 'C:\Users\Luis\AppData\Local\Programs\Python\Python313\python.exe'
$root = "C:\Users\Luis\calude\$Serie"
$s = "$root\src"
Set-Location $root

function Dur($f) {
  if (-not (Test-Path $f)) { return 0.0 }
  $o = ffprobe -v error -show_entries format=duration -of csv=p=0 $f 2>$null
  $d = 0.0; if ([double]::TryParse(($o | Select-Object -First 1), [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$d)) { return $d } else { return 0.0 }
}
function Ok($f, $esperado) { return ([math]::Abs((Dur $f) - $esperado) -lt 0.6) }

foreach ($n in ($Caps -split '[,\s]+' | Where-Object { $_ })) {
  $clips = @(Get-ChildItem "$root\visual\cap$n\clips\*.mp4" -ErrorAction SilentlyContinue).Count
  if ($clips -lt 5 -or (-not $SoloBase -and -not (Test-Path "$root\hooks\cap$n\HOOK_CAP$n.mp4"))) { "cap$n no tiene sus 5 clips y el hook, se salta"; continue }
  $final = "$root\out\REFLEXION_CAP${n}_FINAL.mp4"; $sinb = "$root\out\REFLEXION_CAP${n}_sin_banner.mp4"
  $a = Dur "$root\audio\pulido\cap$n.mp3"
  if ((Ok $sinb ($a + 10)) -and (Ok $final ($a + 10))) { "cap$n ya terminado (video final con banner), se omite"; continue }
  "===== CAP $n  $(Get-Date -Format HH:mm) ====="
  $base = "$root\out\cap${n}_base.mp4"; $bs = "$root\out\cap${n}_base_subs.mp4"; $bm = "$root\out\cap${n}_base_m_subs.mp4"
  Remove-Item Env:ENC_PRESET -ErrorAction SilentlyContinue; if (-not (Ok $base $a)) { "-- montaje"; $env:ENC_PRESET = 'ultrafast'; & $py "$s\montaje.py" $n 2>&1 | Where-Object { $_ -notmatch '^seg' } }
  if (-not (Test-Path "$root\srt\cap$n.ass")) { "-- subs"; & $py "$s\subs.py" $n }
  if (-not (Ok $bs $a)) { "-- quemar"; Remove-Item $bs -ErrorAction SilentlyContinue; $env:ENC_PRESET = 'ultrafast'; & $py "$s\quemar.py" $n $base; Remove-Item Env:ENC_PRESET -ErrorAction SilentlyContinue }
  if ($SoloBase) { "cap$n base con subtitulos lista (sin hook todavia)"; continue }
  if (-not (Test-Path "$root\srt\hook$n.ass")) { "-- subs_hook"; & $py "$s\subs_hook.py" $n }
  if ($ConMusica) { if (-not (Ok $bm $a)) { "-- musica"; Remove-Item $bm -ErrorAction SilentlyContinue; & $py "$s\mezclar_subs.py" $n $Vol } }
  else { Remove-Item $bm -ErrorAction SilentlyContinue }   # unir.py takes capN_base_m_subs.mp4 when it exists: make sure it does not
  if (-not (Ok $sinb ($a + 10))) {
    "-- unir"
    Remove-Item $final, $sinb -ErrorAction SilentlyContinue
    & $py "$s\unir.py" $n
    "-- banner"
    & $py "$s\poner_banner.py" $n
  }
  elseif (-not (Ok $final ($a + 10))) { "-- banner"; Copy-Item $sinb $final -Force; & $py "$s\poner_banner.py" $n }
  if (-not (Test-Path "$root\out\REFLEXION_CAP${n}_sin_marca.mp4")) { "-- marca de agua"; & $py "$s\poner_marca.py" $n }
  "cap$n listo: $(Dur $final) s"
}
"===== MONTAJE FIN $(Get-Date -Format HH:mm) ====="
