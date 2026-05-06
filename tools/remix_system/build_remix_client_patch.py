import shutil
import struct
import subprocess
import sys
from pathlib import Path


WORKSPACE = Path(r"C:\Users\monty\Documents\Codex\2026-04-29\i-am-creating-a-world-of")
SERVER_DBC = Path(r"C:\Build\bin\Debug\data\dbc")
OUT_DIR = WORKSPACE / "artifacts" / "remix_system"
TAXI_DIR = WORKSPACE / "artifacts" / "razorhill_flightpath"
ICON_SHEET = OUT_DIR / "remix_icon_sheet_gpt_image_2.png"
CLIENT_PATCH = Path(r"C:\Program Files (x86)\ChromieCraft_3.3.5a\Data\patch-4.MPQ")
MPQCLI = Path(r"C:\Users\monty\Documents\Codex\2026-04-30\files-mentioned-by-the-user-akheva\tools\mpqcli.exe")
WOW_PATCH_TOOLS = Path(r"C:\Users\monty\Documents\Codex\2026-04-30\files-mentioned-by-the-user-akheva\tools")

TOKEN_CREDITS = 900101
REBORN_TOKEN = 900113
REMIX_USE_SPELL = 900102
REMIX_SPELLS = [
    (900102, "Remix Interface", "Opens the Chrono-Thread upgrade interface.", "remix_interface"),
    (900103, "Remix Stamina", "Each stack grants +10 Stamina.", "remix_stamina"),
    (900104, "Remix Agility", "Each stack grants +5% Agility.", "remix_agility"),
    (900105, "Remix Strength", "Each stack grants +5% Strength.", "remix_strength"),
    (900106, "Remix Intellect", "Each stack grants +5% Intellect.", "remix_intellect"),
    (900107, "Remix Critical Strike", "Each stack grants +5% melee, ranged, and spell critical strike.", "remix_critical_strike"),
    (900108, "Remix Hit", "Each stack grants +5% melee, ranged, and spell hit.", "remix_hit"),
    (900109, "Remix Spell Damage", "Each stack grants +5% Spell Damage.", "remix_spell_damage"),
    (900110, "Remix Attack Power", "Each stack grants +5% melee and ranged Attack Power.", "remix_attack_power"),
    (900111, "Remix Experience", "Each stack grants +5% account-wide experience.", "remix_experience"),
    (900112, "Remix Gold Loot", "Each stack grants +1% account-wide gold from loot.", "remix_gold_loot"),
    (900114, "Reborn Experience", "Each stack grants +5% experience from kills and quests.", "remix_experience"),
    (900115, "Reborn Reputation", "Each stack grants +5% reputation gained.", "remix_gold_loot"),
    (900116, "Reborn Tokenfall", "Each stack grants +100% Remix Token drops.", "remix_interface"),
    (900117, "Reborn Momentum", "Each stack grants +2% movement speed.", "remix_agility"),
]
REMIX_STATUS_SPELLS = {spell_id: (name, description, icon) for spell_id, name, description, icon in REMIX_SPELLS if spell_id != REMIX_USE_SPELL}

SPELL_NAME_FIELDS = range(136, 152)
SPELL_NAME_FLAG = 152
SPELL_RANK_FIELDS = range(153, 169)
SPELL_RANK_FLAG = 169
SPELL_DESCRIPTION_FIELDS = range(170, 186)
SPELL_DESCRIPTION_FLAG = 186
SPELL_AURA_DESCRIPTION_FIELDS = range(187, 203)
SPELL_AURA_DESCRIPTION_FLAG = 203


def read_dbc(path: Path):
    data = path.read_bytes()
    magic, rows, fields, record_size, string_size = struct.unpack_from("<4sIIII", data, 0)
    if magic != b"WDBC":
        raise ValueError(f"{path} is not a WDBC file")
    records = [
        list(struct.unpack_from("<" + "I" * fields, data, 20 + i * record_size))
        for i in range(rows)
    ]
    strings = data[20 + rows * record_size:20 + rows * record_size + string_size]
    return fields, records, strings


def write_dbc(path: Path, fields: int, records: list[list[int]], strings: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        f.write(struct.pack("<4sIIII", b"WDBC", len(records), fields, fields * 4, len(strings)))
        for row in records:
            f.write(struct.pack("<" + "I" * fields, *row))
        f.write(strings)


def add_string(strings: bytearray, text: str) -> int:
    if not text:
        return 0
    needle = text.encode("utf-8") + b"\0"
    existing = bytes(strings).find(needle)
    if existing >= 0:
        return existing
    offset = len(strings)
    strings.extend(needle)
    return offset


def fill_localized(row: list[int], fields: range, flag_field: int, offset: int):
    for index in fields:
        row[index] = offset
    row[flag_field] = 0xFFFF


def empty_spell_row(fields: int, spell_id: int, name: str, description: str, aura_description: str, strings: bytearray) -> list[int]:
    row = [0] * fields
    row[0] = spell_id
    row[28] = 1
    row[46] = 1
    fill_localized(row, SPELL_NAME_FIELDS, SPELL_NAME_FLAG, add_string(strings, name))
    fill_localized(row, SPELL_RANK_FIELDS, SPELL_RANK_FLAG, 0)
    fill_localized(row, SPELL_DESCRIPTION_FIELDS, SPELL_DESCRIPTION_FLAG, add_string(strings, description))
    fill_localized(row, SPELL_AURA_DESCRIPTION_FIELDS, SPELL_AURA_DESCRIPTION_FLAG, add_string(strings, aura_description))
    return row


def patched_spell() -> Path:
    fields, rows, strings = read_dbc(SERVER_DBC / "Spell.dbc")
    if fields != 234:
        raise ValueError("Spell.dbc field count changed")

    custom_ids = {spell_id for spell_id, _, _, _ in REMIX_SPELLS}
    rows = [row for row in rows if row[0] not in custom_ids]
    strings = bytearray(strings)

    use = empty_spell_row(
        fields,
        REMIX_USE_SPELL,
        "Remix Interface",
        "Opens the Chrono-Thread upgrade interface.",
        "",
        strings,
    )
    use[133] = REMIX_USE_SPELL
    use[134] = REMIX_USE_SPELL
    rows.append(use)

    for spell_id, (name, description, _icon) in REMIX_STATUS_SPELLS.items():
        row = empty_spell_row(fields, spell_id, name, description, description, strings)
        row[4] = 0x80000000
        row[7] = 0x00100000
        row[40] = 21
        row[49] = 255
        row[71] = 6
        row[86] = 1
        row[95] = 4

        if spell_id == 900117:
            row[72] = 6
            row[73] = 6
            row[80] = 1
            row[81] = 1
            row[82] = 1
            row[87] = 1
            row[88] = 1
            row[95] = 31
            row[96] = 58
            row[97] = 206

        row[133] = spell_id
        row[134] = spell_id
        rows.append(row)

    rows.sort(key=lambda row: row[0])
    out = OUT_DIR / "Spell.dbc"
    write_dbc(out, fields, rows, bytes(strings))
    return out


def patched_spell_icon() -> Path:
    fields, rows, strings = read_dbc(SERVER_DBC / "SpellIcon.dbc")
    if fields != 2:
        raise ValueError("SpellIcon.dbc field count changed")

    custom_ids = {spell_id for spell_id, _, _, _ in REMIX_SPELLS}
    rows = [row for row in rows if row[0] not in custom_ids]
    strings = bytearray(strings)

    for spell_id, _name, _description, icon in REMIX_SPELLS:
        rows.append([spell_id, add_string(strings, f"Interface\\Icons\\{icon}")])

    rows.sort(key=lambda row: row[0])
    out = OUT_DIR / "SpellIcon.dbc"
    write_dbc(out, fields, rows, bytes(strings))
    return out


def patched_currency_types() -> Path:
    fields, rows, strings = read_dbc(SERVER_DBC / "CurrencyTypes.dbc")
    if fields != 4:
        raise ValueError("CurrencyTypes.dbc field count changed")
    custom_tokens = {TOKEN_CREDITS, REBORN_TOKEN}
    rows = [row for row in rows if row[0] not in custom_tokens and row[1] not in custom_tokens]
    rows.append([TOKEN_CREDITS, TOKEN_CREDITS, 1, 30])
    rows.append([REBORN_TOKEN, REBORN_TOKEN, 1, 31])
    rows.sort(key=lambda row: row[0])
    out = OUT_DIR / "CurrencyTypes.dbc"
    write_dbc(out, fields, rows, strings)
    return out


def build_icon_textures(staging: Path):
    if not ICON_SHEET.exists():
        raise FileNotFoundError(f"Missing generated icon sheet: {ICON_SHEET}")

    from PIL import Image

    sys.path.insert(0, str(WOW_PATCH_TOOLS))
    import wow335_patch_tools as wow

    sheet = Image.open(ICON_SHEET).convert("RGBA")
    crop_boxes = [
        (12, 115, 318, 421),
        (322, 115, 628, 421),
        (628, 115, 934, 421),
        (936, 115, 1242, 421),
        (12, 463, 318, 769),
        (322, 463, 628, 769),
        (628, 463, 934, 769),
        (936, 463, 1242, 769),
        (12, 812, 318, 1118),
        (322, 812, 628, 1118),
        (628, 812, 934, 1118),
    ]

    png_dir = OUT_DIR / "icons_png"
    blp_dir = staging / "Interface" / "Icons"
    png_dir.mkdir(parents=True, exist_ok=True)
    blp_dir.mkdir(parents=True, exist_ok=True)

    for (_spell_id, _name, _description, icon), box in zip(REMIX_SPELLS, crop_boxes):
        png = png_dir / f"{icon}.png"
        blp = blp_dir / f"{icon}.blp"
        sheet.crop(box).resize((64, 64), Image.Resampling.LANCZOS).save(png)
        wow.image_to_blp2_dxt1(png, blp)


def build_patch():
    staging = OUT_DIR / "mpq_staging"
    if staging.exists():
        shutil.rmtree(staging)
    (staging / "DBFilesClient").mkdir(parents=True)

    for name in ["TaxiNodes.dbc", "TaxiPath.dbc", "TaxiPathNode.dbc"]:
        src = TAXI_DIR / name
        if src.exists():
            shutil.copy2(src, staging / "DBFilesClient" / name)

    shutil.copy2(patched_currency_types(), staging / "DBFilesClient" / "CurrencyTypes.dbc")
    shutil.copy2(patched_spell(), staging / "DBFilesClient" / "Spell.dbc")
    shutil.copy2(patched_spell_icon(), staging / "DBFilesClient" / "SpellIcon.dbc")
    build_icon_textures(staging)

    if CLIENT_PATCH.exists():
        CLIENT_PATCH.unlink()

    subprocess.run(
        [str(MPQCLI), "create", str(staging), "--output", str(CLIENT_PATCH), "--game", "wow-wotlk"],
        check=True,
    )


if __name__ == "__main__":
    build_patch()
    print(f"Wrote {CLIENT_PATCH}")
