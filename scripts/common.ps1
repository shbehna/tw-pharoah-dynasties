# Shared helpers for the build scripts. Dot-source it: . "$PSScriptRoot\common.ps1"
# Compatible with Windows PowerShell 5.1.

$ErrorActionPreference = 'Stop'

$Script:ProjectRoot = Split-Path -Parent $PSScriptRoot
$Script:ToolsDir = Join-Path $ProjectRoot 'tools'
$Script:RpfmCli = Join-Path $ToolsDir 'rpfm\rpfm_cli.exe'
$Script:SchemaRon = Join-Path $ToolsDir 'schemas\schema_ph_dyn.ron'
$Script:SchemaJson = Join-Path $ToolsDir 'schemas\schema_ph_dyn.json'
$Script:ReferenceDir = Join-Path $ProjectRoot 'reference'
$Script:SourceDir = Join-Path $ProjectRoot 'src'
$Script:DistDir = Join-Path $ProjectRoot 'dist'

function Get-ModConfig {
    Get-Content -Raw -Path (Join-Path $ProjectRoot 'mod.json') | ConvertFrom-Json
}

function Get-SteamPath {
    foreach ($key in @('HKCU:\Software\Valve\Steam', 'HKLM:\SOFTWARE\WOW6432Node\Valve\Steam', 'HKLM:\SOFTWARE\Valve\Steam')) {
        try {
            $item = Get-ItemProperty -Path $key -ErrorAction Stop
            foreach ($name in @('SteamPath', 'InstallPath')) {
                $value = $item.$name
                if ($value -and (Test-Path $value)) { return (Resolve-Path $value).Path }
            }
        } catch {}
    }
    $default = 'C:\Program Files (x86)\Steam'
    if (Test-Path $default) { return $default }
    throw 'Steam installation not found. Pass -GamePath to the script.'
}

function Get-SteamLibraries {
    $steam = Get-SteamPath
    $libraries = @($steam)
    $vdf = Join-Path $steam 'steamapps\libraryfolders.vdf'
    if (Test-Path $vdf) {
        foreach ($match in [regex]::Matches((Get-Content -Raw $vdf), '"path"\s+"([^"]+)"')) {
            $path = $match.Groups[1].Value -replace '\\\\', '\'
            if ((Test-Path $path) -and ($libraries -notcontains $path)) { $libraries += $path }
        }
    }
    return $libraries
}

# Steam library folder that contains the game.
function Get-GameLibrary {
    $config = Get-ModConfig
    foreach ($library in Get-SteamLibraries) {
        if (Test-Path (Join-Path $library "steamapps\common\$($config.game_folder)")) { return $library }
    }
    throw "$($config.game_folder) not found in any Steam library. Pass -GamePath '<path to the game folder>'."
}

function Get-GamePath {
    param([string]$GamePath)
    if ($GamePath) {
        if (-not (Test-Path (Join-Path $GamePath 'data'))) { throw "No 'data' folder in $GamePath" }
        return (Resolve-Path $GamePath).Path
    }
    $config = Get-ModConfig
    return Join-Path (Get-GameLibrary) "steamapps\common\$($config.game_folder)"
}

function Assert-Tools {
    if (-not (Test-Path $RpfmCli) -or -not (Test-Path $SchemaRon)) {
        throw 'RPFM is not set up. Run scripts\setup.ps1 first.'
    }
}

# Runs rpfm_cli and fails on a non-zero exit code. RPFM logs every call at INFO level; those lines are hidden.
# Deliberately a simple function (no param block): its arguments, like -p, go to rpfm_cli untouched.
function Invoke-Rpfm {
    $Arguments = @($args | ForEach-Object { $_ })
    Assert-Tools
    $config = Get-ModConfig
    # Windows PowerShell 5.1 turns native stderr lines into terminating errors under 'Stop'.
    $previous = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $output = & $RpfmCli -g $config.game @Arguments 2>&1
        $code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $previous
    }
    foreach ($line in $output) {
        $text = "$line"
        if ($text -match '\[(WARN|ERROR)\]' -and $text -notmatch 'rpfm_reserved') { Write-Host $text }
    }
    if ($code -ne 0) { throw "rpfm_cli failed (exit code $code): $($Arguments -join ' ')" }
    return $output
}
