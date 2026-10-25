param([string]$Serie = 'laredo', [string]$Caps = '5,4,3', [int]$Parallel = 5)
$env:GLABS_IMG_MODEL = 'nano_banana_2'
$py = 'C:\Users\Luis\AppData\Local\Programs\Python\Python313\python.exe'
Set-Location "C:\Users\Luis\calude\$Serie"
foreach ($n in ($Caps -split ',')) { & $py src\glabs_api.py $n --parallel $Parallel *> "visual\cap$n\_glabs_flow.log" }
"FLOW $Serie FIN"
