<#
.SYNOPSIS
    Builds the mod and its compatibility add-ons and copies them into the game's data folder (no Workshop upload).

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
$dataDir = Join-Path (Get-GamePath -GamePath $GamePath) 'data'
$target = Join-Path $dataDir $config.pack
$addons = @($config.compat_addons | Where-Object { $_ })

if (Get-Process -Name 'Pharaoh' -ErrorAction SilentlyContinue) {
    Write-Warning 'The game is running: changes apply the next time it starts.'
}
$lockedHint = 'The file is in use: close the game (it locks the packs it loaded) and run the script again.'

if ($Uninstall) {
    foreach ($name in @($config.pack) + @($addons | ForEach-Object { $_.pack })) {
        $path = Join-Path $dataDir $name
        if (Test-Path $path) {
            try { Remove-Item -Force -Path $path -Confirm:$false } catch { throw "$lockedHint ($($_.Exception.Message))" }
            Write-Host "Removed $path"
        } else {
            Write-Host "Not installed: $path"
        }
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

# Compatibility add-ons: enable each one only together with the mod it is for.
foreach ($addon in $addons) {
    $addonPack = Join-Path $DistDir $addon.pack
    $addonTarget = Join-Path $dataDir $addon.pack
    if (-not (Test-Path $addonPack)) {
        # Never leave an add-on from an older build next to the new main pack.
        if (Test-Path $addonTarget) {
            try { Remove-Item -Force -Path $addonTarget -Confirm:$false } catch { throw "$lockedHint ($($_.Exception.Message))" }
            Write-Host "Removed outdated $addonTarget"
        }
        continue
    }
    try { Copy-Item -Force -Path $addonPack -Destination $addonTarget } catch { throw "$lockedHint ($($_.Exception.Message))" }
    Write-Host "Installed $addonTarget"
    Write-Host "Enable '$($addon.pack)' only together with $($addon.title) (Workshop $($addon.workshop_id))."
}
