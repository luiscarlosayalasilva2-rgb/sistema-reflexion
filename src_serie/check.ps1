# Validates src\capN.txt against the Reflexión script rules and writes Parte A / Parte B files.
$root = Split-Path $PSScriptRoot
$bad = @('con','de','para','y','que','a','en','por','el','la','los','las','un','una','mi','su','sus','del','al','o','e','ni','sin','como','lo','le','les','me','se','te','tu','nos','mis')
foreach ($n in 1..5) {
  $lines = Get-Content (Join-Path $PSScriptRoot "cap$n.txt") -Encoding UTF8 | Where-Object { $_.Trim() }
  $issues = @()
  $i = 0
  foreach ($l in $lines) {
    $i++
    $w = ($l.Trim() -split '\s+')
    if ($w.Count -lt 4 -or $w.Count -gt 9) { $issues += "L$i words=$($w.Count): $l" }
    $last = ($w[-1] -replace '[^\p{L}]', '').ToLower()
    if ($bad -contains $last) { $issues += "L$i ends '$last': $l" }
    if ($l -match '\d') { $issues += "L$i digit: $l" }
    if ($l -match '[:;"\(\)—–]|\.\.\.|…') { $issues += "L$i punct: $l" }
  }
  $b = ($lines | ForEach-Object { $_.Trim() }) -join ' '
  foreach ($s in ($b -split '(?<=[\.\?!])\s+')) { if (([regex]::Matches($s, ',')).Count -gt 3) { $issues += "commas>3: $s" } }
  $chars = $b.Length; $words = ($b -split '\s+').Count
  $secs = [math]::Round($words / 2.4); $dur = '{0}:{1:00}' -f [math]::Floor($secs/60), ($secs % 60)
  "CAP$n chars=$chars words=$words dur=$dur imgs=$([math]::Round($chars/36)) lines=$($lines.Count)"
  $issues | ForEach-Object { "   $_" }
  $a = for ($k = 0; $k -lt $lines.Count; $k++) { '{0:00} | {1}' -f ($k+1), $lines[$k].Trim() }
  [IO.File]::WriteAllText((Join-Path $root "REFLEXION_CAP${n}_GUION_PARTE_A.txt"), ($a -join "`r`n"), (New-Object Text.UTF8Encoding $false))
  [IO.File]::WriteAllText((Join-Path $root "REFLEXION_CAP${n}_GUION_PARTE_B.txt"), $b, (New-Object Text.UTF8Encoding $false))
}
