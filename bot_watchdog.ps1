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

# Only one watchdog per user session: a second copy would start a second bot
$WatchdogMutex = New-Object System.Threading.Mutex($false, "Local\JapaneseLearningBotWatchdog")
$HasMutex = $false
try {
    $HasMutex = $WatchdogMutex.WaitOne(0)
} catch [System.Threading.AbandonedMutexException] {
    # Previous watchdog died without releasing it; we own it now
    $HasMutex = $true
}
if (-not $HasMutex) {
    Write-Log "Another watchdog instance is already running. This copy exits."
    exit 0
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

# Terminate orphan copies of THIS project's bot only.
# Match python.exe / pythonw.exe whose command line ends with "bot.py" (not discord_bot.py etc.) AND
#   (a) whose executable lives inside this folder (the venv launcher), or
#   (b) whose parent is such a launcher (the venv launcher spawns the real interpreter as a child), or
#   (c) whose command line names this folder's bot.py by full path.
function Get-ProjectBotProcesses {
    $botCmdPattern = '(^|[\s"\\/])bot\.py"?\s*$'
    $workPrefix = $WorkDir.TrimEnd('\') + '\'
    $fullScript = $workPrefix + $BotScript
    $procs = @(Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe'" -ErrorAction SilentlyContinue)
    $launchers = @($procs | Where-Object {
        $_.CommandLine -and ($_.CommandLine -match $botCmdPattern) -and (
            ($_.ExecutablePath -and $_.ExecutablePath.StartsWith($workPrefix, [System.StringComparison]::OrdinalIgnoreCase)) -or
            ($_.CommandLine.IndexOf($fullScript, [System.StringComparison]::OrdinalIgnoreCase) -ge 0)
        )
    })
    $launcherIds = @($launchers | ForEach-Object { $_.ProcessId })
    $children = @($procs | Where-Object {
        $_.CommandLine -and ($_.CommandLine -match $botCmdPattern) -and ($launcherIds -contains $_.ParentProcessId)
    })
    return @($launchers + $children | Where-Object { $_.ProcessId -ne $PID })
}

try {
    foreach ($p in (Get-ProjectBotProcesses)) {
        Write-Log "Stopping duplicate bot process PID: $($p.ProcessId) ($($p.CommandLine))"
        # /T also stops the real interpreter that the venv launcher spawned
        & taskkill.exe /PID $p.ProcessId /T /F 2>&1 | Out-Null
    }
} catch {
    Write-Log "WARNING: duplicate-process check failed: $($_.Exception.Message)"
}

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

    # Windows PowerShell 5.1: ExitCode stays empty unless the process handle is opened right away
    $null = $proc.Handle
    Write-Log "Bot started successfully with PID: $($proc.Id)"

    $proc.WaitForExit()
    $exitCode = $proc.ExitCode
    $duration = (Get-Date) - $startTime

    Write-Log "WARNING: Bot stopped with ExitCode: $exitCode (Ran for $([math]::Round($duration.TotalSeconds))s)"

    # Exit code 0 means normal intended shutdown
    if ($exitCode -eq 0) {
        Write-Log "INFO: Bot stopped normally. Watchdog will exit."
        break
    }

    # Exit code 3: bot.py found another running instance (bot.lock held). Wait and retry without counting.
    if ($exitCode -eq 3) {
        Write-Log "INFO: Another bot instance is already running. Checking again in 60 seconds."
        Start-Sleep -Seconds 60
        continue
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

    # Back off when the bot keeps crashing right after start (10s, 20s, 30s ... capped at 5 minutes)
    $delay = [math]::Min($RestartDelaySec * ($restartCount + 1), 300)
    Write-Log "Restarting bot in $delay seconds... (Consecutive restart count: $restartCount)"
    Start-Sleep -Seconds $delay
}

Write-Log "=== Watchdog Finished ==="
try { $WatchdogMutex.ReleaseMutex() } catch {}
