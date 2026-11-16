param(
    [int]$Port = 3000,
    [int]$SizeMB = 5,
    [int]$Count = 10,
    [string]$LogPath = "speed-log.txt"
)

$ErrorActionPreference = "Stop"

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$env:PORT = "$Port"
$env:SIZE_MB = "$SizeMB"

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logLines = @()
$logLines += "Internet Speed Test Log"
$logLines += "======================="
$logLines += "Timestamp: $timestamp"
$logLines += "URL: http://localhost:$Port/"
$logLines += "Payload size (MB): $SizeMB"
$logLines += "Requests: $Count"
$logLines += ""

Write-Host "Starting test server (port=$Port, size=${SizeMB}MB)..."
$server = Start-Process -FilePath "node" -ArgumentList "server.js" -PassThru -NoNewWindow

try {
    Start-Sleep -Seconds 1

    $cmdLine = "python speed_test.py http://localhost:$Port/ -n $Count"
    Write-Host "Running test: $cmdLine"
    Write-Host ""
    $logLines += "Command: $cmdLine"
    $logLines += "Output:"
    $logLines += "-------"

    $prevEAP = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $output = & python speed_test.py "http://localhost:$Port/" -n $Count 2>&1 | ForEach-Object { "$_" }
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $prevEAP

    foreach ($line in $output) {
        Write-Host $line
        $logLines += $line
    }

    $logLines += ""
    $logLines += "Exit code: $exitCode"
}
catch {
    $err = $_.Exception.Message
    Write-Host "Error: $err"
    $logLines += ""
    $logLines += "ERROR: $err"
    $exitCode = 1
}
finally {
    if ($server -and -not $server.HasExited) {
        Write-Host ""
        Write-Host "Stopping test server..."
        Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
    }
}

$logLines += "Finished: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$logLines | Set-Content -Path $LogPath -Encoding UTF8
Write-Host ""
Write-Host "Speed log saved: $LogPath"

exit $exitCode
