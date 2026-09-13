# Learning workflow only. Emulator behavior lives in learner-owned src files.
param(
    [string] $Lesson = '',
    [switch] $Once,
    [switch] $Next,
    [switch] $List
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$catalog = Get-Content (Join-Path $repo 'course/lessons.json') -Raw | ConvertFrom-Json
$catalog = @($catalog)
$statePath = Join-Path $repo '.work/course-progress.json'
$script:checked = $false
$script:exitCode = 1
$script:currentIndex = 0
$state = @{ current = '01'; reviewed = @() }

function Save-Progress {
    New-Item -ItemType Directory -Path (Split-Path $statePath) -Force | Out-Null
    $state.current = $catalog[$script:currentIndex].id
    $temporary = "$statePath.tmp"
    $state | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $temporary -Encoding UTF8
    Move-Item -LiteralPath $temporary -Destination $statePath -Force
}

function Prepare-Lesson {
    # Prepare prerequisites too, so selecting a later lesson cannot omit required types.
    for ($i = 0; $i -le $script:currentIndex; $i++) {
        foreach ($template in $catalog[$i].templates) {
            $target = Join-Path $repo $template.target
            if (-not (Test-Path -LiteralPath $target)) {
                New-Item -ItemType Directory -Path (Split-Path $target) -Force | Out-Null
                Copy-Item -LiteralPath (Join-Path $repo $template.source) -Destination $target
            }
        }
    }
    Save-Progress
    $item = $catalog[$script:currentIndex]
    Write-Host "`nLesson $($item.id): $($item.title)" -ForegroundColor Cyan
    Write-Host "Read: $(Join-Path $repo "$($item.folder)/README.md")"
    Write-Host "Write: $(Join-Path $repo $item.file)"
    Write-Host 'Save to check. O opens the lesson. N next. P previous. R recheck. Q quit.'
}

function Source-Stamp {
    $files = @(
        Get-ChildItem (Join-Path $repo 'src'), (Join-Path $repo 'tests') -Recurse -File |
            Where-Object { $_.FullName -notmatch '[\\/](bin|obj)[\\/]' -and $_.Extension -in @('.cs','.csproj','.props','.targets','.json','.config','.resx') }
        Get-ChildItem $repo -File | Where-Object { $_.Extension -in @('.json','.props','.targets','.config') }
    )
    return (($files | Sort-Object FullName | ForEach-Object { '{0}|{1}|{2}' -f $_.FullName,$_.LastWriteTimeUtc.Ticks,$_.Length }) -join "`n")
}

function Run-Captured([string[]] $Arguments, [string] $Log) {
    $savedPreference = $ErrorActionPreference
    try {
        # In Windows PowerShell, native stderr must not abort the report-producing process.
        $ErrorActionPreference = 'Continue'
        & $script:dotnet @Arguments *> $Log
        $script:exitCode = $LASTEXITCODE
    } finally { $ErrorActionPreference = $savedPreference }
}

function Show-BuildError([string] $Log) {
    Write-Host 'Code could not be checked. Fix the first error, then save:' -ForegroundColor Yellow
    $errors = @(Get-Content -LiteralPath $Log | Select-String 'error ' | Select-Object -First 4)
    if ($errors.Count) { $errors | ForEach-Object { Write-Host $_.Line } }
    else { Get-Content -LiteralPath $Log -Tail 8 | ForEach-Object { Write-Host $_ } }
    Write-Host "Details: $Log"
}

function Check-Lesson {
    $script:checked = $false
    $item = $catalog[$script:currentIndex]
    $outputFolder = Join-Path $repo '.work/course-check'
    New-Item -ItemType Directory -Path $outputFolder -Force | Out-Null
    $log = Join-Path $outputFolder 'output.log'
    $report = Join-Path $outputFolder 'result.trx'
    if (Test-Path -LiteralPath $report) { Remove-Item -LiteralPath $report }
    Write-Host "`nChecking lesson $($item.id)..."
    # Host lessons must compile the host too, even though Core tests do not reference it.
    if ($item.mode -eq 'observed') {
        Run-Captured @('build', (Join-Path $repo 'GbaEmulator.sln'), '--nologo') $log
        if ($script:exitCode -ne 0) { Show-BuildError $log; return }
    }
    $active = @($catalog[0..$script:currentIndex] | Where-Object { $_.mode -eq 'automatic' })
    $filter = ($active | ForEach-Object { "Lesson=$($_.id)" }) -join '|'
    $expected = ($active | Measure-Object -Property count -Sum).Sum
    $retired = @($active | ForEach-Object { $_.retireChecks } | Where-Object { $_ -and [int]$_.fromLesson -le [int]$item.id })
    if ($retired.Count) {
        $filter = "($filter)" + (($retired | ForEach-Object { "&FullyQualifiedName!=$($_.name)" }) -join '')
        $expected -= $retired.Count
    }
    Run-Captured @('test', (Join-Path $repo 'tests/Gba.Core.Tests/Gba.Core.Tests.csproj'), '--nologo', '--filter', $filter, '--logger', 'trx;LogFileName=result.trx', '--results-directory', $outputFolder) $log
    if (-not (Test-Path -LiteralPath $report)) { Show-BuildError $log; return }
    [xml] $xml = Get-Content -LiteralPath $report -Raw
    $results = @($xml.SelectNodes("//*[local-name()='UnitTestResult']"))
    $passed = @($results | Where-Object { $_.outcome -eq 'Passed' }).Count
    $currentClass = if ($item.id -eq '01') { 'EwramTests.' } else { "Course$($item.id)Tests." }
    foreach ($result in $results) {
        $isCurrent = $result.testName.StartsWith($currentClass)
        if ($isCurrent -or $result.outcome -ne 'Passed') {
            $name = ($result.testName -replace '^.*Tests\.', '') -replace '_', ' '
            $prefix = if ($isCurrent) { '' } else { 'Earlier check: ' }
            if ($result.outcome -eq 'Passed') { Write-Host "  OK    $name" -ForegroundColor Green }
            else {
                Write-Host "  TODO  $prefix$name" -ForegroundColor Yellow
                $message = $result.SelectSingleNode(".//*[local-name()='Message']")
                if ($message -and $message.InnerText -notmatch 'NotImplementedException') {
                    Write-Host (($message.InnerText -split "`n" | Select-Object -First 4) -join "`n")
                }
            }
        }
    }
    if ($results.Count -ne $expected) {
        Write-Host "Expected $expected supplied checks, discovered $($results.Count). Missing/skipped checks cannot complete a lesson." -ForegroundColor Yellow
    }
    if ($script:exitCode -ne 0 -or $results.Count -ne $expected -or $passed -ne $expected) {
        $script:exitCode = 1
        Write-Host "$passed/$expected automatic checks passed. Keep editing and save."
        Write-Host "Details: $log"
        return
    }
    $script:checked = $true
    if ($item.mode -eq 'automatic') {
        $script:exitCode = 0
        Write-Host "$passed/$expected checks passed, including earlier lessons. Press N when ready for the next small step." -ForegroundColor Green
    } else {
        $script:exitCode = 2
        Write-Host 'Build and earlier automatic checks passed. This lesson still needs your observations:' -ForegroundColor Cyan
        foreach ($check in $item.checks) { Write-Host "  - $check" }
        Write-Host 'After observing every case, press N. A build alone does not complete this lesson.'
    }
}

function Move-Next {
    # Recheck disk contents even if the last result was green.
    Check-Lesson
    if (-not $script:checked) { return $false }
    $item = $catalog[$script:currentIndex]
    if ($item.mode -eq 'observed') {
        if ($Once -or $Next -or [Console]::IsInputRedirected) {
            Write-Host 'Observed lessons need interactive self-check acknowledgement; progress was not advanced.'
            return $false
        }
        $answer = Read-Host 'Have you observed ALL listed cases? Type yes to record a self-check, or Enter to keep working'
        if ($answer -ne 'yes') { return $false }
    }
    $state.reviewed = @($state.reviewed | Where-Object { $_.id -ne $item.id }) + @(@{ id=$item.id; kind=$item.mode; at=[DateTime]::UtcNow.ToString('o') })
    if ($script:currentIndex + 1 -lt $catalog.Count) { $script:currentIndex++ }
    else { Write-Host 'Course integration milestone reached. Keep using this loop for compatibility work.' }
    Prepare-Lesson
    return $true
}

Push-Location $repo
try {
    if ($List) {
        $catalog | ForEach-Object { Write-Host "$($_.id)  $($_.title) [$($_.mode)]" }
        exit 0
    }
    if (Test-Path -LiteralPath $statePath) {
        try {
            $saved = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
            $state.current = $saved.current
            $state.reviewed = @($saved.reviewed)
        } catch { throw 'Could not read .work/course-progress.json. Your code is intact; repair or rename that progress file to start navigation again.' }
    }
    $selected = if ($Lesson) { $Lesson.PadLeft(2,'0') } else { $state.current }
    $ids = @($catalog | ForEach-Object { $_.id })
    $script:currentIndex = [Array]::IndexOf($ids, $selected)
    if ($script:currentIndex -lt 0) { throw "Unknown lesson '$selected'. Choose 01 through $($catalog[-1].id)." }
    $candidates = @((Join-Path $repo '.work/dotnet10/dotnet.exe'))
    $installed = Get-Command dotnet -CommandType Application -ErrorAction SilentlyContinue
    if ($installed) { $candidates += $installed.Source }
    foreach ($candidate in $candidates) {
        if (-not (Test-Path -LiteralPath $candidate)) { continue }
        $version = & $candidate --version 2>$null
        if ($LASTEXITCODE -eq 0 -and "$version" -match '^10\.\d+\.\d+$') { $script:dotnet = $candidate; break }
    }
    if (-not $script:dotnet) { throw 'Install a stable .NET 10 SDK from https://dotnet.microsoft.com/en-us/download/dotnet/10.0 and reopen learn.cmd. Your code is preserved.' }
    $env:DOTNET_ROOT = Split-Path $script:dotnet -Parent
    $env:PATH = "$env:DOTNET_ROOT;$env:PATH"
    Prepare-Lesson
    if ($Next) { $null = Move-Next; exit $script:exitCode }
    $previous = Source-Stamp
    Check-Lesson
    if ($Once) { exit $script:exitCode }
    while ($true) {
        Start-Sleep -Milliseconds 500
        $stamp = Source-Stamp
        if ($stamp -ne $previous) { $previous = $stamp; Check-Lesson }
        if (-not [Console]::IsInputRedirected -and [Console]::KeyAvailable) {
            $key = [Console]::ReadKey($true).Key
            switch ($key) {
                'Q' { exit 0 }
                'O' {
                    $readme = Join-Path $repo "$($catalog[$script:currentIndex].folder)/README.md"
                    try { Start-Process -FilePath $readme }
                    catch { Write-Host "Open this file in your editor: $readme" }
                }
                'R' { Check-Lesson }
                'N' { if (Move-Next) { $previous = Source-Stamp; Check-Lesson } }
                'P' {
                    if ($script:currentIndex -gt 0) { $script:currentIndex--; Prepare-Lesson; $previous=Source-Stamp; Check-Lesson }
                }
            }
        }
    }
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
} finally { Pop-Location }
