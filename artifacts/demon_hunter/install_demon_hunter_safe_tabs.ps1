param(
    [string]$Workspace = "C:\Users\monty\Documents\Codex\2026-04-29\i-am-creating-a-world-of",
    [string]$ClientRoot = "C:\Program Files (x86)\ChromieCraft_3.3.5a",
    [string]$ServerRoot = "C:\Build\bin\Debug"
)

$ErrorActionPreference = "Stop"

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$patchSource = Join-Path $Workspace "artifacts\demon_hunter\patch-4.demonhunter-throwglaive-fel-20260505.MPQ"
$clientPatch = Join-Path $ClientRoot "Data\patch-4.MPQ"
$dbcSource = Join-Path $Workspace "artifacts\playable_races\mpq_staging\DBFilesClient"
$serverDbc = Join-Path $ServerRoot "data\dbc"
$dbcNames = @(
    "Spell.dbc",
    "SpellIcon.dbc",
    "SkillLine.dbc",
    "SkillLineAbility.dbc",
    "SkillRaceClassInfo.dbc",
    "SpellVisual.dbc",
    "SpellVisualKit.dbc",
    "SpellVisualEffectName.dbc"
)
$sqlFiles = @(
    "2026_05_05_04_demon_hunter_felrush_safety_spellbook_sync.sql",
    "2026_05_05_05_demon_hunter_retail_talent_pass.sql",
    "2026_05_05_06_demon_hunter_retail_spellbook_tabs_safety_pass.sql",
    "2026_05_05_07_demon_hunter_throw_glaive_visual_polish.sql"
)

if (!(Test-Path -LiteralPath $patchSource)) {
    throw "Missing generated patch: $patchSource"
}
if (!(Test-Path -LiteralPath $clientPatch)) {
    throw "Missing client patch target: $clientPatch"
}
if (!(Test-Path -LiteralPath $dbcSource)) {
    throw "Missing generated DBC folder: $dbcSource"
}
if (!(Test-Path -LiteralPath $serverDbc)) {
    throw "Missing server DBC target: $serverDbc"
}

$world = Get-Process worldserver -ErrorAction SilentlyContinue
if ($world) {
    Stop-Process -Id $world.Id -Force
    Start-Sleep -Seconds 3
}

Copy-Item -LiteralPath $clientPatch -Destination "$clientPatch.before-dh-safe-tabs-$stamp" -Force
Copy-Item -LiteralPath $patchSource -Destination $clientPatch -Force

foreach ($name in $dbcNames) {
    $src = Join-Path $dbcSource $name
    $dst = Join-Path $serverDbc $name
    if (!(Test-Path -LiteralPath $src)) {
        throw "Missing generated DBC: $src"
    }
    Copy-Item -LiteralPath $dst -Destination "$dst.before-dh-safe-tabs-$stamp" -Force
    Copy-Item -LiteralPath $src -Destination $dst -Force
}

foreach ($sql in $sqlFiles) {
    $sqlPath = Join-Path $Workspace "artifacts\demon_hunter\$sql"
    if (!(Test-Path -LiteralPath $sqlPath)) {
        throw "Missing SQL sync file: $sqlPath"
    }
    Get-Content -Raw -LiteralPath $sqlPath | mysql -u root -pascent
}

Start-Process -FilePath (Join-Path $ServerRoot "worldserver.exe") -WorkingDirectory $ServerRoot -WindowStyle Hidden
Write-Output "Installed Demon Hunter safe tabs patch, synced SQL, and restarted worldserver."
