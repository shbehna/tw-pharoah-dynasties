<#
.SYNOPSIS
    Builds dist\<pack> from the mod source in src\.

.DESCRIPTION
    Creates a mod pack with RPFM and adds src\db, src\text and src\script; TSV tables
    are converted to the game's binary format on the way in.
#>
param()

. "$PSScriptRoot\common.ps1"
Assert-Tools
$config = Get-ModConfig

if (-not (Test-Path (Join-Path $SourceDir 'db'))) {
    throw 'src\ is empty. Run: python generator\generate.py'
}
New-Item -ItemType Directory -Force -Path $DistDir | Out-Null
$pack = Join-Path $DistDir $config.pack
if (Test-Path $pack) { Remove-Item -Force -Path $pack -Confirm:$false }

Write-Host "Building $($config.pack) ..."
Invoke-Rpfm pack create -p $pack | Out-Null
$arguments = @('pack', 'add', '-p', $pack, '-t', $SchemaRon)
foreach ($folder in @('db', 'text', 'script')) {
    $path = Join-Path $SourceDir $folder
    if (Test-Path $path) { $arguments += @('-F', "$path;$folder") }
}
Invoke-Rpfm @arguments | Out-Null

# Every source file must be in the pack (tables lose their .tsv extension, texts become .loc).
$expected = @(Get-ChildItem -Path $SourceDir -Recurse -File | ForEach-Object {
    ($_.FullName.Substring($SourceDir.Length + 1) -replace '\\', '/') -replace '\.tsv$', ''
})
$listed = @(Invoke-Rpfm pack list -p $pack | ForEach-Object { "$_".Trim() })
$missing = @($expected | Where-Object { $listed -notcontains $_ })
if ($missing.Count -gt 0) { throw "Files missing from the pack: $($missing -join ', ')" }
$size = [math]::Round((Get-Item $pack).Length / 1KB)
Write-Host "Built $($config.pack): $($expected.Count) files, $size KB."
