param([int]$From = 1, [int]$To = 99)
# Submits the Bloque 1 fichas of all chapters to Flow (characters 16:9 model sheets, locations 9:16), one job per ficha.
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$root = Split-Path $PSScriptRoot
$items = @()
foreach ($n in 1..5) {
  $b1 = Join-Path $root "REFLEXION_CAP${n}_BLOQUE1_PERSONAJES_LOCACIONES.txt"
  $b1b = Join-Path $root "REFLEXION_CAP${n}_BLOQUE1B_NOMBRES_REFERENCIA.txt"
  if (-not (Test-Path $b1b) -or -not (Get-Content $b1b -Raw -Encoding UTF8)) { continue }
  $prompts = @(([IO.File]::ReadAllText($b1, [Text.Encoding]::UTF8) -split "(\r?\n){2}") | Where-Object { $_.Trim() })
  $names = @(Get-Content $b1b -Encoding UTF8 | Where-Object { $_.Trim() })
  for ($k = 0; $k -lt $names.Count; $k++) { $items += [pscustomobject]@{ name = $names[$k].Trim(); prompt = $prompts[$k].Trim() } }
}
$i = 0
foreach ($it in $items) {
  $i++
  if ($i -lt $From -or $i -gt $To) { continue }
  $ar = if ($it.prompt -like '*model sheet*') { '16:9' } else { '9:16' }
  $cli = @('flow-text-to-image', '--prompt', $it.prompt, '--aspect-ratio', $ar, '--outputs', '1', '--index', $i, '--folder', 'testamento_fichas')
  if ($i -eq 1) { $cli += '--new-project' }
  "[$i] $($it.name) $ar"
  flow-auto generate create @cli
}
