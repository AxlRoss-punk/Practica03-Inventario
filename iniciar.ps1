param(
    [ValidateSet('app', 'pruebas', 'evidencias', 'todo', 'bloqueo')]
    [string]$Modo = 'app',
    [string]$Python,
    [string]$Db
)

$ErrorActionPreference = 'Stop'
$practicePython = $Python
if (-not $practicePython) {
    $practiceRoots = @(
        (Join-Path $env:LOCALAPPDATA 'Python'),
        (Join-Path $env:LOCALAPPDATA 'Programs\Python')
    )
    foreach ($practiceRoot in $practiceRoots) {
        if (Test-Path -LiteralPath $practiceRoot) {
            $practiceCandidates = Get-ChildItem -LiteralPath $practiceRoot -Directory |
                Sort-Object Name -Descending |
                ForEach-Object { Join-Path $_.FullName 'python.exe' } |
                Where-Object { Test-Path -LiteralPath $_ }
            if ($practiceCandidates) {
                $practicePython = @($practiceCandidates)[0]
                break
            }
        }
    }
}
if (-not $practicePython) {
    $practiceExecutable = Get-Command python,python3 -ErrorAction SilentlyContinue |
        Where-Object { $_.Source -notlike '*\WindowsApps\*' } |
        Select-Object -First 1
    if ($practiceExecutable) { $practicePython = $practiceExecutable.Source }
}
if (-not $practicePython) {
    throw 'No se encontro Python. Instala Python con Tkinter o usa -Python con la ruta de python.exe.'
}

Push-Location -LiteralPath $PSScriptRoot
try {
    if ($Modo -eq 'app') {
        if ($Db) { & $practicePython app.py --db $Db }
        else { & $practicePython app.py }
        $practiceExit = $LASTEXITCODE
    }
    if ($Modo -eq 'pruebas' -or $Modo -eq 'todo') {
        & $practicePython ejecutar_pruebas.py
        $practiceExit = $LASTEXITCODE
        if ($practiceExit -ne 0) { exit $practiceExit }
    }
    if ($Modo -eq 'evidencias' -or $Modo -eq 'todo') {
        & $practicePython generar_evidencias.py
        $practiceExit = $LASTEXITCODE
    }
    if ($Modo -eq 'bloqueo') {
        if (-not $Db) { throw 'Indica -Db con la base de prueba que deseas bloquear.' }
        & $practicePython -m herramientas.bloquear_base --db $Db
        $practiceExit = $LASTEXITCODE
    }
    exit $practiceExit
}
finally {
    Pop-Location
}

