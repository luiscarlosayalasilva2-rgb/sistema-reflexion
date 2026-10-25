param([Parameter(Mandatory)][string]$VoiceId, [int[]]$Caps = @(1,2,3,4,5), [double]$Speed = 1)
# Fish Audio TTS, one chapter at a time (free tier: sequential only). Key comes from the user-level FISH_API_KEY env var and is never printed.
$ErrorActionPreference = 'Stop'
$key = [Environment]::GetEnvironmentVariable('FISH_API_KEY', 'User')
if (-not $key) { throw 'FISH_API_KEY no está configurada.' }
$root = Split-Path $PSScriptRoot
$out = Join-Path $root 'audio'; New-Item -ItemType Directory -Force $out | Out-Null
foreach ($n in $Caps) {
  $dest = Join-Path $out "cap$n.mp3"
  if ((Test-Path $dest) -and (Get-Item $dest).Length -gt 0) { "cap$n ya existe, se omite"; continue }
  $text = [IO.File]::ReadAllText((Join-Path $root "REFLEXION_CAP${n}_GUION_PARTE_B.txt")).Trim()
  $body = @{ text = $text; reference_id = $VoiceId; format = 'mp3'; mp3_bitrate = 192; prosody = @{ speed = $Speed } } | ConvertTo-Json -Compress
  $headers = @{ Authorization = "Bearer $key"; model = 's2.1-pro-free' }   # exact id: an unknown value silently falls back to the paid s2.1-pro
  try {
    Invoke-WebRequest -Uri 'https://api.fish.audio/v1/tts' -Method Post -Headers $headers -ContentType 'application/json; charset=utf-8' `
      -Body ([Text.Encoding]::UTF8.GetBytes($body)) -OutFile "$dest.part" -UseBasicParsing -TimeoutSec 600
  } catch {
    $code = $_.Exception.Response.StatusCode.value__
    Remove-Item "$dest.part" -ErrorAction SilentlyContinue
    throw "cap${n}: HTTP $code - $($_.Exception.Message)"
  }
  Move-Item "$dest.part" $dest -Force
  $hash = (Get-FileHash $dest -Algorithm SHA256).Hash.Substring(0,12)
  "cap$n OK  $([math]::Round((Get-Item $dest).Length/1KB)) KB  sha256:$hash"
}
