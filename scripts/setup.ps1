<#
.SYNOPSIS
    Downloads the tools needed to build the mod into tools\ (run once).

.DESCRIPTION
    - RPFM (Rusted PackFile Manager) 4.7.4: the last release that ships rpfm_cli.exe,
      used to read the game's packs and to build the mod's pack.
    - The RPFM table schema for Pharaoh Dynasties, plus a JSON copy for the Python generator.

.PARAMETER Force
    Download again even if the files are already there.

.PARAMETER SchemaRef
    Git ref (commit or branch) of github.com/Frodo45127/rpfm-schemas to download the schema from.
    Use 'master' after a game update if the extraction reports tables it cannot decode.
#>
param(
    [switch]$Force,
    [string]$SchemaRef = '04ae66b53835b0b922e3eeed8ab5ffddd94a6b0e'
)

. "$PSScriptRoot\common.ps1"
$config = Get-ModConfig
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$ProgressPreference = 'SilentlyContinue'  # Invoke-WebRequest is very slow with the progress bar in 5.1

New-Item -ItemType Directory -Force -Path (Join-Path $ToolsDir 'schemas') | Out-Null

if ($Force -or -not (Test-Path $RpfmCli)) {
    $version = $config.rpfm_version
    $url = "https://github.com/Frodo45127/rpfm/releases/download/$version/rpfm-$version-x86_64-pc-windows-msvc.zip"
    $zip = Join-Path $ToolsDir 'rpfm.zip'
    Write-Host "Downloading RPFM $version ..."
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
    $target = Join-Path $ToolsDir 'rpfm'
    if (Test-Path $target) { Remove-Item -Recurse -Force -Path $target -Confirm:$false }
    Expand-Archive -Path $zip -DestinationPath $target
    Remove-Item -Force -Path $zip -Confirm:$false
    if (-not (Test-Path $RpfmCli)) { throw "rpfm_cli.exe not found in the RPFM $version download." }
} else {
    Write-Host 'RPFM already installed.'
}

if ($Force -or -not (Test-Path $SchemaRon) -or -not (Test-Path $SchemaJson)) {
    $url = "https://raw.githubusercontent.com/Frodo45127/rpfm-schemas/$SchemaRef/schema_ph_dyn.ron"
    Write-Host "Downloading the Pharaoh Dynasties schema ($SchemaRef) ..."
    Invoke-WebRequest -Uri $url -OutFile $SchemaRon -UseBasicParsing
    if (Test-Path $SchemaJson) { Remove-Item -Force -Path $SchemaJson -Confirm:$false }
    # Converts every schema in the folder; it complains about the other games' schemas, which are not needed.
    $previous = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    & $RpfmCli -g $config.game schemas to-json -s (Split-Path -Parent $SchemaRon) 2>&1 | Out-Null
    $ErrorActionPreference = $previous
    if (-not (Test-Path $SchemaJson)) { throw 'Converting the schema to JSON failed.' }
} else {
    Write-Host 'Schema already downloaded.'
}

Write-Host 'Setup complete. Next: scripts\extract.ps1'
