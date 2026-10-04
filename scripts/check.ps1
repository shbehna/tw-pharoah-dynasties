<#
.SYNOPSIS
    Runs RPFM's diagnostics on dist\<pack> against the game data (invalid references, bad values...).

.DESCRIPTION
    Builds RPFM's dependencies cache of the game into tools\deps the first time.
    Reports about missing image files are skipped: RPFM's cache does not contain the game's
    UI art, so every unit portrait and effect icon is reported missing, vanilla ones included.
    Exits with code 1 when other problems are found.

.PARAMETER GamePath
    Game folder, if it is not found automatically.
#>
param([string]$GamePath)

. "$PSScriptRoot\common.ps1"
Assert-Tools
$config = Get-ModConfig
$game = Get-GamePath -GamePath $GamePath
$pack = Join-Path $DistDir $config.pack
if (-not (Test-Path $pack)) { throw 'No pack in dist\. Run scripts\build.ps1 first.' }

$cache = Join-Path $ToolsDir "deps\$($config.game).pak2"

function New-DependenciesCache {
    Write-Host 'Building the dependencies cache of the game ...'
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $cache) | Out-Null
    Invoke-Rpfm dependencies generate --pak-path $cache --game-path $game --schema-path $SchemaRon | Out-Null
}

# Problems reported for the pack, as "<path>: <type> <columns> <cells>" lines.
function Get-Problems {
    $output = Invoke-Rpfm pack diagnose --game-path $game --pak-path $cache --schema-path $SchemaRon --pack-path $pack
    $json = ($output | ForEach-Object { "$_" } | Where-Object { $_ -notmatch '^\d\d:\d\d:\d\d ' }) -join "`n"
    $report = $json | ConvertFrom-Json
    $ignored = @('FieldWithPathNotFound', 'NoReferenceTableNorColumnFoundNoPak')
    foreach ($result in $report.results) {
        foreach ($kind in $result.PSObject.Properties) {
            foreach ($item in $kind.Value.results) {
                $type = if ($item.report_type -is [string]) { $item.report_type } else { @($item.report_type.PSObject.Properties)[0].Name }
                if ($ignored -contains $type) { continue }
                "$($kind.Value.path): $type $($item.column_names -join ', ') $($item.cells_affected.Count) cell(s)"
            }
        }
    }
}

if (-not (Test-Path $cache)) { New-DependenciesCache }
Write-Host "Diagnosing $($config.pack) ..."
$problems = @(Get-Problems)
# RPFM considers the cache stale when the game's data folder changed (installing the mod does that).
if ($problems | Where-Object { $_ -match 'DependenciesCache' }) {
    New-DependenciesCache
    $problems = @(Get-Problems)
}
if ($problems.Count -eq 0) {
    Write-Host 'No problems found.'
} else {
    $problems | ForEach-Object { Write-Host $_ }
    Write-Host "$($problems.Count) problem(s) found."
    exit 1
}
