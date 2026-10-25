param([Parameter(Mandatory)][int]$Cap, [int]$From = 1, [int]$To = 999)
# Submits Bloque 2 scene prompts to Flow as image-to-image, attaching every [TAG] of the prompt head as a Flow asset.
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$root = Split-Path $PSScriptRoot
$blocks = @(([IO.File]::ReadAllText((Join-Path $root "REFLEXION_CAP${Cap}_BLOQUE2_IMAGENES.txt"), [Text.Encoding]::UTF8) -split "(\r?\n){2}") | Where-Object { $_.Trim() })
foreach ($b in $blocks) {
  if ($b.Trim() -notmatch '^(\d+) \|\| (.*)$') { continue }
  $n = [int]$Matches[1]; $prompt = $Matches[2]
  if ($n -lt $From -or $n -gt $To) { continue }
  if (Get-ChildItem (Join-Path $env:USERPROFILE "Downloads\testamento_cap$Cap") -Filter "$n - *" -ErrorAction SilentlyContinue) { continue }  # already downloaded
  $head = ($prompt -split 'vertical 9:16')[0]
  $tags = [regex]::Matches($head, '\[([A-Z]+)\]') | ForEach-Object { $_.Groups[1].Value }
  $cli = @('flow-image-to-image', '--prompt', $prompt, '--aspect-ratio', '9:16', '--outputs', '1', '--index', $n, '--folder', "testamento_cap$Cap", '--batch', '8', '--speed', '6', '--model', 'nano-banana-2')
  foreach ($t in $tags) { $cli += '--asset'; $cli += "$t.jpg" }
  "[$n] $($tags -join ' ')"
  flow-auto generate create @cli
}
