# All project plumbing lives here. Emulator code belongs in src/Gba.Core.
param(
    [ValidateSet('menu', 'help', 'build', 'run', 'test', 'watch', 'learn', 'lab', 'lab-watch', 'doctor')]
    [string] $Command = 'menu',
    [string] $Filter = '',
    [string] $Rom = ''
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$desktop = Join-Path $repo 'src/Gba.Desktop/Gba.Desktop.csproj'
$tests = Join-Path $repo 'tests/Gba.Core.Tests/Gba.Core.Tests.csproj'
$lab = Join-Path $repo '.work/SyntaxLab/SyntaxLab.csproj'
$script:dotnet = $null

function Show-Help {
    Write-Host @'
RevoAdvance - save your C# file, then run one command:

  .\dev.cmd                 Open the menu (also works by double-clicking)
  .\dev.cmd run             Compile and run the desktop app
  .\dev.cmd test            Compile and run your emulator tests
  .\dev.cmd watch           Rerun emulator tests whenever you save
  .\dev.cmd build           Check that the whole project compiles
  .\dev.cmd lab             Create/reuse and run the C# scratchpad
  .\dev.cmd lab-watch       Rerun the scratchpad whenever you save
  .\dev.cmd doctor          Check which SDK is being used

  .\dev.cmd test -Filter LowByteTests
  .\dev.cmd watch -Filter LowByteTests
  .\dev.cmd run -Rom "C:\Games\Your Game.gba"

Write emulator code in src/Gba.Core and tests in tests/Gba.Core.Tests.
New .cs files are included automatically. Save before running.
The desktop app is currently a placeholder; ROM support is yours to implement.
Stop a watcher with Ctrl+C. An empty test run proves no emulator behavior.
'@
}

function Initialize-Sdk {
    if ($script:dotnet) { return }
    $candidates = @((Join-Path $repo '.work/dotnet10/dotnet.exe'))
    $installed = Get-Command dotnet -CommandType Application -ErrorAction SilentlyContinue
    if ($installed) { $candidates += $installed.Source }
    foreach ($candidate in $candidates) {
        if (-not (Test-Path -LiteralPath $candidate)) { continue }
        $version = & $candidate --version 2>$null
        if ($LASTEXITCODE -eq 0 -and "$version" -match '^10\.\d+\.\d+$') {
            $script:dotnet = $candidate
            $env:DOTNET_ROOT = Split-Path $candidate -Parent
            $env:PATH = "$env:DOTNET_ROOT;$env:PATH"
            return
        }
    }
    throw 'A stable .NET 10 SDK is needed. Install the SDK from https://dotnet.microsoft.com/en-us/download/dotnet/10.0, reopen your terminal, and run dev.cmd again. No Bash or other build tools are needed.'
}

function Invoke-Dotnet([string[]] $Arguments) {
    & $script:dotnet @Arguments
    if ($LASTEXITCODE -ne 0) {
        $script:result = $LASTEXITCODE
        throw "Command failed (exit $LASTEXITCODE). Read the first error above, fix it, save, and rerun."
    }
}

function Get-TestSourceStamp {
    # Include newly created files, even when Core/tests initially contain no C#.
    $files = @(
        Get-ChildItem (Join-Path $repo 'src/Gba.Core'), (Join-Path $repo 'tests/Gba.Core.Tests') -Recurse -File |
            Where-Object { $_.FullName -notmatch '[\\/](bin|obj)[\\/]' -and $_.Extension -in @('.cs', '.csproj', '.props', '.targets', '.json', '.config', '.resx') }
        Get-ChildItem $repo -File | Where-Object { $_.Extension -in @('.json', '.props', '.targets', '.config') }
    )
    return (($files | Sort-Object FullName | ForEach-Object {
        '{0}|{1}|{2}' -f $_.FullName, $_.LastWriteTimeUtc.Ticks, $_.Length
    }) -join "`n")
}

function Invoke-Action([string] $Action) {
    if ($Action -eq 'help') { Show-Help; return }
    Initialize-Sdk
    $testArgs = @('--logger', 'console;verbosity=normal')
    if ($Filter) { $testArgs += @('--filter', "FullyQualifiedName~$Filter") }
    if ($Action -in @('lab', 'lab-watch') -and -not (Test-Path -LiteralPath $lab)) {
        # dotnet new refuses conflicting files; never force/overwrite the user's work.
        Invoke-Dotnet @('new', 'console', '--framework', 'net10.0', '--output', (Split-Path $lab))
    }
    switch ($Action) {
        'doctor' {
            Write-Host "SDK: $script:dotnet"
            Invoke-Dotnet @('--version')
            Write-Host "Project: $repo"
            Write-Host 'SDK ready. Run build to check compilation and package restore.'
        }
        'build' { Invoke-Dotnet @('build', (Join-Path $repo 'GbaEmulator.sln'), '--nologo') }
        'run' {
            $runArgs = @('run', '--project', $desktop)
            if ($Rom) { $runArgs += @('--', $Rom) }
            Invoke-Dotnet $runArgs
        }
        'test' {
            Write-Host 'Check the executed test count: no tests / no matching tests is not a passing check.'
            Invoke-Dotnet (@('test', $tests, '--nologo') + $testArgs)
        }
        'learn' {
            & (Join-Path $PSScriptRoot 'course.ps1')
            $script:result = $LASTEXITCODE
        }
        'watch' {
            Write-Host 'Save a Core or test .cs file to rerun tests. Ctrl+C stops watching.'
            Write-Host 'Check the executed test count: no tests / no matching tests is not a passing check.'
            $previous = $null
            while ($true) {
                $current = Get-TestSourceStamp
                if ($current -ne $previous) {
                    $previous = $current
                    try {
                        Invoke-Dotnet (@('test', $tests, '--nologo') + $testArgs)
                        $script:result = 0
                    } catch {
                        Write-Host $_.Exception.Message -ForegroundColor Red
                    }
                    Write-Host 'Watching Core and tests. Save a file to run again; Ctrl+C stops.'
                }
                Start-Sleep -Milliseconds 500
            }
        }
        'lab' {
            Write-Host "Edit: $(Join-Path (Split-Path $lab) 'Program.cs')"
            Invoke-Dotnet @('run', '--project', $lab)
        }
        'lab-watch' {
            Write-Host "Edit: $(Join-Path (Split-Path $lab) 'Program.cs')"
            Write-Host 'Save to rerun. Ctrl+C stops watching.'
            Invoke-Dotnet @('watch', '--project', $lab, '--no-hot-reload', 'run')
        }
    }
}

$script:result = 0
Push-Location $repo
try {
    if ($Command -eq 'menu') {
        while ($true) {
            Write-Host "`nRevoAdvance - what do you want to do?"
            Write-Host '1 Run app   2 Test   3 Watch tests   4 Build   5 C# scratchpad   6 Watch scratchpad   7 SDK check   Q Quit'
            $choice = Read-Host 'Choose'
            if ($null -eq $choice -or $choice -eq 'q') { break }
            $actions = @{ '1' = 'run'; '2' = 'test'; '3' = 'watch'; '4' = 'build'; '5' = 'lab'; '6' = 'lab-watch'; '7' = 'doctor' }
            if (-not $actions.ContainsKey($choice)) { Write-Host 'Choose 1-7 or Q.'; continue }
            try { Invoke-Action $actions[$choice] }
            catch { Write-Host $_.Exception.Message -ForegroundColor Red }
        }
    } else {
        Invoke-Action $Command
    }
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($script:result -eq 0) { $script:result = 1 }
} finally {
    Pop-Location
}
exit $script:result
