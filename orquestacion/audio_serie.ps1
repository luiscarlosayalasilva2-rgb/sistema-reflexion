# Voice (Fish, Valentino, one synthesis at a time) + polish + SRT (Groq whisper) + diff for one or more series folders.
param([string]$Series = 'mozo,terreno', [string]$VoiceId = '8d2c17a9b26d4d83888ea67a1ee565b2', [string]$Speed = '1')
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$py = 'C:\Users\Luis\AppData\Local\Programs\Python\Python313\python.exe'
foreach ($s in ($Series -split '[,\s]+' | Where-Object { $_ })) {
  $dir = "C:\Users\Luis\calude\$s"
  Set-Location $dir
  "===== $s : tts $(Get-Date -Format HH:mm) ====="
  & powershell -NoProfile -ExecutionPolicy Bypass -File "$dir\src\tts.ps1" -VoiceId $VoiceId -Speed $Speed
  "===== $s : pulir ====="
  & powershell -NoProfile -ExecutionPolicy Bypass -File "$dir\src\pulir.ps1"
  "===== $s : srt (Groq) ====="
  & $py "$dir\src\srt.py" 1 2 3 4 5
  foreach ($n in 1..5) { & $py "$dir\src\diff.py" $n }
  "===== $s : LISTO $(Get-Date -Format HH:mm) ====="
}
"TODO LISTO"
