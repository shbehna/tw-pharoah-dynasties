<#
.SYNOPSIS
    Builds dist\<pack> from the mod source in src\, and one pack per compatibility add-on.

.DESCRIPTION
    Creates a mod pack with RPFM and adds src\db, src\text and src\script; TSV tables
    are converted to the game's binary format on the way in. Each compatibility add-on
    (mod.json "compat_addons") is built from src_addons\<name> into dist\<its pack>.
#>
param()

. "$PSScriptRoot\common.ps1"
Assert-Tools
$config = Get-ModConfig

function Build-ModPack([string]$Source, [string]$PackName) {
    $pack = Join-Path $DistDir $PackName
    if (Test-Path $pack) { Remove-Item -Force -Path $pack -Confirm:$false }

    Write-Host "Building $PackName ..."
    Invoke-Rpfm pack create -p $pack | Out-Null
    $arguments = @('pack', 'add', '-p', $pack, '-t', $SchemaRon)
    foreach ($folder in @('db', 'text', 'script')) {
        $path = Join-Path $Source $folder
        if (Test-Path $path) { $arguments += @('-F', "$path;$folder") }
    }
    Invoke-Rpfm @arguments | Out-Null

    # Every source file must be in the pack (tables lose their .tsv extension, texts become .loc).
    $root = (Resolve-Path $Source).Path
    $expected = @(Get-ChildItem -Path $root -Recurse -File | ForEach-Object {
        ($_.FullName.Substring($root.Length + 1) -replace '\\', '/') -replace '\.tsv$', ''
    })
    $listed = @(Invoke-Rpfm pack list -p $pack | ForEach-Object { "$_".Trim() })
    $missing = @($expected | Where-Object { $listed -notcontains $_ })
    if ($missing.Count -gt 0) { throw "Files missing from ${PackName}: $($missing -join ', ')" }
    $size = [math]::Round((Get-Item $pack).Length / 1KB)
    Write-Host "Built ${PackName}: $($expected.Count) files, $size KB."
}

if (-not (Test-Path (Join-Path $SourceDir 'db'))) {
    throw 'src\ is empty. Run: python generator\generate.py'
}
New-Item -ItemType Directory -Force -Path $DistDir | Out-Null
Build-ModPack -Source $SourceDir -PackName $config.pack

foreach ($addon in @($config.compat_addons)) {
    if (-not $addon) { continue }
    $source = Join-Path $ProjectRoot "src_addons\$($addon.name)"
    $pack = Join-Path $DistDir $addon.pack
    if (-not (Test-Path (Join-Path $source 'db'))) {
        # A stale add-on pack must not be installed with a newer main pack.
        if (Test-Path $pack) { Remove-Item -Force -Path $pack -Confirm:$false }
        Write-Warning "$($addon.title) add-on not built: src_addons\$($addon.name) is empty (see scripts\extract.ps1)."
        continue
    }
    Build-ModPack -Source $source -PackName $addon.pack
}
