param([Parameter(Mandatory)][int]$Cap, [int[]]$Only)
# Bloque 3 clips via Flow frame-to-video (omni-flash, 4 s, 9:16): the Bloque 2 image is the start frame.
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$root = Split-Path $PSScriptRoot
$blocks = @(([IO.File]::ReadAllText((Join-Path $root "REFLEXION_CAP${Cap}_BLOQUE3_CLIPS.txt"), [Text.Encoding]::UTF8) -split "(\r?\n){2}") | Where-Object { $_.Trim() })
foreach ($b in $blocks) {
  if ($b.Trim() -notmatch '^(\d+) \|\| (.*)$') { continue }
  $n = [int]$Matches[1]; $prompt = $Matches[2]
  if ($Only -and $Only -notcontains $n) { continue }
  $img = Join-Path $root ("visual\cap$Cap\imgs\{0:000}.jpg" -f $n)
  if (-not (Test-Path $img)) { "[$n] sin imagen todavía"; continue }
  if (Get-ChildItem -LiteralPath (Join-Path $env:USERPROFILE "Downloads\testamento_clips$Cap") -Filter "$n - *" -ErrorAction SilentlyContinue) { "[$n] ya existe"; continue }
  "[$n] clip"
  flow-auto generate create flow-frame-to-video --prompt $prompt --image $img --model omni-flash --duration 4 --aspect-ratio 9:16 --outputs 1 --index $n --folder "testamento_clips$Cap"
}
