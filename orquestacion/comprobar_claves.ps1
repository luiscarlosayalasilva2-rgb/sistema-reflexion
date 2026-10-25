# Comprueba FISH_API_KEY y GLABS_API_KEY SIN mostrarlas: existencia, formato y una prueba contra cada servicio.
# La prueba compara la respuesta con la clave real contra la respuesta con una clave falsa:
# si cambian (p. ej. 200 vs 401) la clave real es reconocida. No gasta creditos ni genera nada.
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

function Codigo($url, $headers) {
    try { return [int](Invoke-WebRequest -Uri $url -Headers $headers -UseBasicParsing -TimeoutSec 20).StatusCode }
    catch {
        if ($_.Exception.Response) { return [int]$_.Exception.Response.StatusCode }
        return "sin respuesta"
    }
}

foreach ($v in 'FISH_API_KEY', 'GLABS_API_KEY') {
    $k = [Environment]::GetEnvironmentVariable($v, 'User')
    if (-not $k) { Write-Host "$v : NO definida" -ForegroundColor Red; continue }
    $mal = @()
    if ($k -ne $k.Trim()) { $mal += 'espacios al inicio/fin' }
    if ($k -match '["'']') { $mal += 'comillas' }
    if ($k -match '\s') { $mal += 'espacios internos' }
    if ($k.Length -lt 16) { $mal += 'muy corta' }
    if ($mal.Count) { Write-Host "$v : definida ($($k.Length) car.) pero REVISAR: $($mal -join ', ')" -ForegroundColor Yellow }
    else { Write-Host "$v : definida, $($k.Length) caracteres, formato OK" -ForegroundColor Green }
}

$fish = [Environment]::GetEnvironmentVariable('FISH_API_KEY', 'User')
if ($fish) {
    $u = 'https://api.fish.audio/wallet/self/api-credit'
    $real = Codigo $u @{ Authorization = "Bearer $fish" }
    $falsa = Codigo $u @{ Authorization = 'Bearer clave-falsa-0000000000000000' }
    Write-Host "Fish  : con tu clave = $real | con clave falsa = $falsa"
    if ($real -eq 200 -and $falsa -ne 200) { Write-Host "Fish  : clave VALIDA" -ForegroundColor Green }
    elseif ($real -eq $falsa) { Write-Host "Fish  : no se pudo distinguir (respuesta igual)" -ForegroundColor Yellow }
    else { Write-Host "Fish  : clave RECHAZADA o error" -ForegroundColor Red }
}

$gl = [Environment]::GetEnvironmentVariable('GLABS_API_KEY', 'User')
if ($gl) {
    $u = 'http://127.0.0.1:8765/api/status/prueba-no-existe'
    $real = Codigo $u @{ 'X-API-Key' = $gl }
    $falsa = Codigo $u @{ 'X-API-Key' = 'clave-falsa-0000000000000000' }
    Write-Host "G-Labs: con tu clave = $real | con clave falsa = $falsa"
    if ($real -ne $falsa -and $falsa -in 401, 403) { Write-Host "G-Labs: clave VALIDA" -ForegroundColor Green }
    elseif ($real -eq $falsa) { Write-Host "G-Labs: no se pudo distinguir (respuesta igual)" -ForegroundColor Yellow }
    else { Write-Host "G-Labs: clave RECHAZADA o error" -ForegroundColor Red }
}
