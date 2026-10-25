param([string]$Caps = '1,2,3,4,5')
# Hook pipeline for a series: board shots -> storyboards -> prompts -> 10 s videos -> transcription/frames review.
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$s = $PSScriptRoot
Set-Location (Split-Path $s)
$list = $Caps -split '[,\s]+' | Where-Object { $_ }
foreach ($n in $list) { python "$s\hook_tomas.py" $n }
python "$s\glabs_tomas.py" @list
python "$s\glabs_tomas.py" @list   # second pass retries any shot that failed
foreach ($n in $list) { python "$s\tablero.py" $n; python "$s\hook_prompt.py" $n | Select-Object -First 1 }
python "$s\glabs_hook.py" @list
python "$s\revisar_hook.py" @list
"===== HOOKS FIN ====="
