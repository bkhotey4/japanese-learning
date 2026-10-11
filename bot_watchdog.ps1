# ============================================================
#  Japanese Learning Discord Bot - Watchdog Script
#  Features: Start on logon + Auto restart on crash + Background hidden
#  Invoked by Windows Startup batch file.
# ============================================================

# Resolve the directory dynamically to avoid Chinese encoding path issues
$WorkDir = $PSScriptRoot
if ([string]::IsNullOrEmpty($WorkDir)) {
    $WorkDir = Split-Path -Parent $MyInvocation.MyCommand.Path
}
if ([string]::IsNullOrEmpty($WorkDir)) {
    $WorkDir = (Get-Item -Path ".").FullName
}

$LogFile = "$WorkDir\_watchdog.log"
$BotScript = "bot.py"
$PythonExe = "$WorkDir\venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    $PythonExe = "python"
}

$MaxRestarts = 99
$RestartDelaySec = 10
$StartupDelaySec = 10

# Set encoding to UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"

function Write-Log {
    param([string]$Msg)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] $Msg"
    Write-Host $line
    try {
        Add-Content -Path $LogFile -Value $line -Encoding UTF8
    } catch {}
}

Write-Log "=== Japanese Learning Bot Watchdog Started ==="
Write-Log "Waiting $StartupDelaySec seconds for network and system..."
Start-Sleep -Seconds $StartupDelaySec

# Check network connectivity before starting
$retries = 0
while ($retries -lt 12) {
    try {
        Test-Connection -ComputerName "discord.com" -Count 1 -ErrorAction Stop | Out-Null
        Write-Log "Network connection verified. Ready to start bot."
        break
    } catch {
        $retries++
        Write-Log "Waiting for network... ($retries/12)"
        Start-Sleep -Seconds 5
    }
}

if ($retries -ge 12) {
    Write-Log "WARNING: Network check timed out. Proceeding to launch anyway."
}

# Terminate any existing orphan bot.py processes in this folder
try {
    $existing = Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%$BotScript%'" -ErrorAction SilentlyContinue
    foreach ($p in $existing) {
        if ($p.CommandLine -match "Japanese_Learning") {
            Write-Log "Stopping duplicate bot process PID: $($p.ProcessId)"
            Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
        }
    }
} catch {}

$restartCount = 0

while ($restartCount -le $MaxRestarts) {
    Write-Log "Starting bot with $PythonExe (Attempt $($restartCount + 1))..."

    $startTime = Get-Date
    $proc = Start-Process `
        -FilePath $PythonExe `
        -ArgumentList $BotScript `
        -WorkingDirectory $WorkDir `
        -PassThru `
        -NoNewWindow

    Write-Log "Bot started successfully with PID: $($proc.Id)"

    # Wait 5 seconds to ensure it is alive
    Start-Sleep -Seconds 5

    $proc.WaitForExit()
    $exitCode = $proc.ExitCode
    $duration = (Get-Date) - $startTime

    Write-Log "WARNING: Bot stopped with ExitCode: $exitCode (Ran for $([math]::Round($duration.TotalSeconds))s)"

    # Exit code 0 means normal intended shutdown
    if ($exitCode -eq 0) {
        Write-Log "INFO: Bot stopped normally. Watchdog will exit."
        break
    }

    if ($duration.TotalSeconds -gt 60) {
        $restartCount = 0
    } else {
        $restartCount++
    }

    if ($restartCount -gt $MaxRestarts) {
        Write-Log "ERROR: Reached max consecutive restart limit ($MaxRestarts). Watchdog stopping."
        break
    }

    Write-Log "Restarting bot in $RestartDelaySec seconds... (Consecutive restart count: $restartCount)"
    Start-Sleep -Seconds $RestartDelaySec
}

Write-Log "=== Watchdog Finished ==="
