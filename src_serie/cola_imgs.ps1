param([string]$Caps = '1,2,3,4,5')
# Generates scenes chapter by chapter through G-Labs (8 in parallel), one chapter at a time. Usage: -Caps 1,2,3
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$root = Split-Path $PSScriptRoot
Set-Location $root
foreach ($n in ($Caps -split '[,\s]+' | Where-Object { $_ })) {
  python "$root\src\glabs_api.py" $n --parallel 8 *> "$root\visual\cap$n\_glabs.log"
  "cap$n listo"
}
