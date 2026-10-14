<#
.SYNOPSIS
    Extracts the game data into reference\ as TSV files.

.DESCRIPTION
    The generator (generator\generate.py) reads these files. Run it again after a game update.

    - reference\vanilla\db        game database tables (data_db.pack)
    - reference\vanilla\text\db   English texts (local_en.pack)
    - reference\addons\<name>     tables of the mods that have a compatibility add-on (mod.json
                                  "compat_addons"), from the Workshop folder, enabled or not
    - reference\active_mods\...   with -ActiveMods: every mod enabled in the launcher
                                  (used by generator\conflicts.py)

.PARAMETER GamePath
    Game folder, if it is not found automatically.

.PARAMETER ActiveMods
    Also extract the mods currently enabled in the launcher (from used_mods.txt).
#>
param(
    [string]$GamePath,
    [switch]$ActiveMods
)

. "$PSScriptRoot\common.ps1"
Assert-Tools
$config = Get-ModConfig
$game = Get-GamePath -GamePath $GamePath
Write-Host "Game: $game"

function Reset-Folder([string]$path) {
    if (Test-Path $path) { Remove-Item -Recurse -Force -Path $path -Confirm:$false }
    New-Item -ItemType Directory -Force -Path $path | Out-Null
}

# Extracts folders of a pack as TSV. $Folders: paths inside the pack ('/' = everything).
function Export-Pack([string]$Pack, [string]$Destination, [string[]]$Folders) {
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    $arguments = @('pack', 'extract', '-p', $Pack, '-t', $SchemaRon)
    foreach ($folder in $Folders) { $arguments += @('-F', "$folder;$Destination") }
    Invoke-Rpfm @arguments | Out-Null
    # RPFM writes its own notes/settings files next to the extracted data.
    Get-ChildItem -Path $Destination -Filter '*.rpfm_reserved*' -File | Remove-Item -Force -Confirm:$false
}

# --- Game data -------------------------------------------------------------------------------
$vanilla = Join-Path $ReferenceDir 'vanilla'
Reset-Folder $vanilla
Write-Host 'Extracting game tables ...'
Export-Pack -Pack (Join-Path $game 'data\data_db.pack') -Destination $vanilla -Folders @('db')
Write-Host 'Extracting English texts ...'
Export-Pack -Pack (Join-Path $game 'data\local_en.pack') -Destination $vanilla -Folders @('text/db')
Write-Host 'Listing game scripts ...'
# Used by the conflict report to spot mods that replace a game script.
Invoke-Rpfm pack list -p (Join-Path $game 'data\data.pack') | ForEach-Object { "$_".Trim() } |
    Where-Object { $_ -like 'script/*' } | Set-Content -Path (Join-Path $vanilla 'script_files.txt') -Encoding utf8
$binary = @(Get-ChildItem -Path (Join-Path $vanilla 'db') -Recurse -File | Where-Object { $_.Extension -ne '.tsv' })
if ($binary.Count -gt 0) {
    Write-Warning "$($binary.Count) game tables could not be decoded with the schema (game updated?). Try: scripts\setup.ps1 -Force -SchemaRef master"
}

# --- Mods with a compatibility add-on (mod.json "compat_addons") -------------------------------------
$addonsDir = Join-Path $ReferenceDir 'addons'
Reset-Folder $addonsDir
$workshop = Join-Path (Get-GameLibrary) "steamapps\workshop\content\$($config.steam_app_id)"
foreach ($addon in @($config.compat_addons)) {
    if (-not $addon) { continue }
    $source = @(Get-ChildItem -Path (Join-Path $workshop $addon.workshop_id) -Filter '*.pack' -File -ErrorAction SilentlyContinue)
    if ($source.Count -eq 0) {
        Write-Warning "$($addon.title) (Workshop $($addon.workshop_id)) is not downloaded: subscribe to it to build its add-on."
        continue
    }
    Write-Host "Extracting $($addon.title) for its compatibility add-on ..."
    Export-Pack -Pack $source[0].FullName -Destination (Join-Path $addonsDir $addon.name) -Folders @('db')
}

# --- Mods enabled in the launcher ----------------------------------------------------------------
if ($ActiveMods) {
    $usedMods = Join-Path $game 'used_mods.txt'
    if (-not (Test-Path $usedMods)) { throw "No used_mods.txt in $game. Start the game once from the launcher." }
    $lines = Get-Content -Path $usedMods
    $directories = @($lines | ForEach-Object { if ($_ -match '^add_working_directory "([^"]+)"') { $Matches[1] } })
    $enabled = @($lines | ForEach-Object { if ($_ -match '^mod "([^"]+)"') { $Matches[1] } })
    $active = Join-Path $ReferenceDir 'active_mods'
    Reset-Folder $active
    $order = @()
    foreach ($name in $enabled) {
        if ($name -eq $config.pack) { continue }
        $pack = $null
        foreach ($directory in ($directories + @(Join-Path $game 'data'))) {
            $candidate = Join-Path $directory $name
            if (Test-Path $candidate) { $pack = Get-Item $candidate; break }
        }
        if (-not $pack) { Write-Warning "Enabled mod not found: $name"; continue }
        $id = Split-Path -Leaf $pack.DirectoryName
        $label = if ($id -match '^\d+$') { "$($id)_$($pack.BaseName)" } else { "local_$($pack.BaseName)" }
        Write-Host "Extracting enabled mod $($pack.Name) ..."
        try {
            Export-Pack -Pack $pack.FullName -Destination (Join-Path $active $label) -Folders @('db', 'text', 'script')
        } catch {
            Write-Warning "Could not fully extract $($pack.Name): $($_.Exception.Message)"
        }
        $order += $label
    }
    # Launcher order, for the conflict report.
    $order | Set-Content -Path (Join-Path $active 'load_order.txt') -Encoding utf8
}

Write-Host 'Extraction complete. Next: python generator\generate.py'
