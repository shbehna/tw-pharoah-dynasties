<#
.SYNOPSIS
    Builds the mod and copies it into the game's data folder (no Workshop upload).

.DESCRIPTION
    After installing, enable the mod in the game launcher; it shows up as a local mod
    named after the pack file.

.PARAMETER GamePath
    Game folder, if it is not found automatically,
    e.g. 'D:\SteamLibrary\steamapps\common\Total War PHARAOH DYNASTIES'.

.PARAMETER SkipBuild
    Copy the pack already in dist\ instead of building it first.

.PARAMETER Uninstall
    Remove the mod from the game's data folder.
#>
param(
    [string]$GamePath,
    [switch]$SkipBuild,
    [switch]$Uninstall
)

. "$PSScriptRoot\common.ps1"
$config = Get-ModConfig
$target = Join-Path (Get-GamePath -GamePath $GamePath) "data\$($config.pack)"

if (Get-Process -Name 'Pharaoh' -ErrorAction SilentlyContinue) {
    Write-Warning 'The game is running: changes apply the next time it starts.'
}
$lockedHint = 'The file is in use: close the game (it locks the packs it loaded) and run the script again.'

if ($Uninstall) {
    if (Test-Path $target) {
        try { Remove-Item -Force -Path $target -Confirm:$false } catch { throw "$lockedHint ($($_.Exception.Message))" }
        Write-Host "Removed $target"
    } else {
        Write-Host "Not installed: $target"
    }
    return
}

if (-not $SkipBuild) {
    & (Join-Path $PSScriptRoot 'build.ps1')
}
$pack = Join-Path $DistDir $config.pack
if (-not (Test-Path $pack)) { throw 'No pack in dist\. Run scripts\build.ps1 first.' }

try { Copy-Item -Force -Path $pack -Destination $target } catch { throw "$lockedHint ($($_.Exception.Message))" }
Write-Host "Installed $target"
Write-Host "Enable '$($config.pack)' in the launcher (see README.md for mods that overlap with it)."
