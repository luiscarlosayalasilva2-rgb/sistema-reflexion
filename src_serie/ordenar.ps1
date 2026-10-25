param([Parameter(Mandatory)][int]$Cap)
# Copies Downloads\testamento_capN\"N - ...jpg" to visual\capN\imgs\NNN.jpg (LiteralPath: names contain [brackets]).
$root = Split-Path $PSScriptRoot
$dst = Join-Path $root "visual\cap$Cap\imgs"; New-Item -ItemType Directory -Force $dst | Out-Null
$n = 0
foreach ($f in Get-ChildItem -LiteralPath (Join-Path $env:USERPROFILE "Downloads\testamento_cap$Cap") -File) {
  if ($f.Name -match '^(\d+) - ') {
    $out = Join-Path $dst ('{0:000}{1}' -f [int]$Matches[1], $f.Extension)
    if (-not (Test-Path -LiteralPath $out) -or (Get-Item -LiteralPath $out).LastWriteTime -lt $f.LastWriteTime) { Copy-Item -LiteralPath $f.FullName -Destination $out -Force }
    $n++
  }
}
$total = (Get-Content (Join-Path $root "REFLEXION_CAP${Cap}_BLOQUE4B_TIEMPOS_MS.txt")).Count
$have = (Get-ChildItem $dst -File).Name | ForEach-Object { [int]($_ -replace '\D', '') }
$missing = 1..$total | Where-Object { $have -notcontains $_ }
"cap${Cap}: $(@($have).Count) de $total" + ($(if ($missing) { " | faltan: $($missing -join ',')" } else { '' }))
