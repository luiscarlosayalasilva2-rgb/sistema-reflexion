# Guarda las 2 claves (Fish y G-Labs) como variables de USUARIO de Windows. Gemini ya no se usa.
# Las pide por pantalla (no se ven al pegarlas) y NO las escribe en ningun archivo.
# Ejecutar en TU ventana de PowerShell:
#   powershell -ExecutionPolicy Bypass -File C:\Users\Luis\calude\guardar_claves.ps1
$nombres = 'FISH_API_KEY', 'GLABS_API_KEY'
foreach ($n in $nombres) {
    $actual = [Environment]::GetEnvironmentVariable($n, 'User')
    if ($actual) {
        $r = Read-Host "$n ya existe. Reemplazar? (s/N)"
        if ($r -notmatch '^[sS]') { continue }
    }
    $sec = Read-Host "Pega la clave de $n y pulsa Enter (no se vera al pegar)" -AsSecureString
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
    try { $v = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
    $v = $v.Trim().Trim('"').Trim("'")
    if ($v.Length -lt 16) {
        Write-Host "$n : vacia o demasiado corta, NO se guardo." -ForegroundColor Yellow
        continue
    }
    [Environment]::SetEnvironmentVariable($n, $v, 'User')
    Write-Host "$n : guardada ($($v.Length) caracteres)." -ForegroundColor Green
}
Write-Host ""
Write-Host "Listo. Cierra y abre Claude, y escribe 'listo' para que las revise."
