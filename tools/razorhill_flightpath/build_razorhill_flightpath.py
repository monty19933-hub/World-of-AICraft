import math
import shutil
import struct
import subprocess
from pathlib import Path


WORKSPACE = Path(r"C:\Users\monty\Documents\Codex\2026-04-29\i-am-creating-a-world-of")
SERVER_DBC = Path(r"C:\Build\bin\Debug\data\dbc")
OUT_DIR = WORKSPACE / "artifacts" / "razorhill_flightpath"
CLIENT_PATCH = Path(r"C:\Program Files (x86)\ChromieCraft_3.3.5a\Data\patch-4.MPQ")
SQL_OUT = OUT_DIR / "2026_04_30_00_razorhill_flightpath.sql"
SOURCE_SQL_OUT = Path(r"C:\Azerothcore\data\sql\custom\db_world\2026_04_30_00_razorhill_flightpath.sql")
MPQCLI = Path(r"C:\Users\monty\Documents\Codex\2026-04-30\files-mentioned-by-the-user-akheva\tools\mpqcli.exe")

RAZORHILL_NODE = 441
RAZORHILL_CREATURE = 900010
RAZORHILL_NAME = "Razor Hill, Durotar"

# Tower-top / high platform in Razor Hill so taxi takeoff and arrival do not begin inside street clutter.
RAZORHILL = (384.0, -4600.0, 76.17)
ORG = 23
RATCHET = 80

# Stock Orgrimmar routes use these low front-gate waypoints. Keep this segment
# unchanged so the taxi still enters and exits through the main gates.
ORG_GATE_CORRIDOR = [
    (1717.18, -4335.20, 67.25),
    (1713.89, -4374.61, 67.25),
    (1669.04, -4410.46, 60.89),
    (1562.84, -4414.54, 46.70),
    (1487.76, -4418.21, 29.62),
    (1439.58, -4419.20, 29.62),
    (1427.48, -4365.73, 29.62),
    (1348.87, -4378.23, 39.12),
    (1225.76, -4367.62, 44.12),
]

RAZORHILL_ORG_APPROACH = [
    (350.00, -4648.00, 96.00),
    (295.00, -4735.00, 122.00),
    (415.00, -4850.00, 146.00),
    (675.00, -4855.00, 156.00),
    (930.00, -4765.00, 148.00),
    (1060.00, -4595.00, 126.00),
    (1100.00, -4460.00, 92.00),
    (1105.00, -4358.00, 62.00),
]

RAZORHILL_TO_RATCHET = [
    (410.00, -4588.00, 78.50),
    (340.00, -4410.00, 88.00),
    (265.00, -4175.00, 84.00),
    (284.39, -3710.55, 55.39),
    (-86.96, -3707.59, 55.39),
    (-384.18, -3811.94, 52.67),
    (-613.95, -3862.66, 80.72),
    (-731.74, -3876.00, 69.59),
    (-828.30, -3830.81, 34.34),
    (-887.41, -3781.70, 16.06),
]

RATCHET_TO_RAZORHILL = [
    (-886.65, -3783.26, 16.56),
    (-876.86, -3799.56, 20.51),
    (-820.48, -3899.81, 55.26),
    (-701.75, -3943.16, 59.84),
    (-373.71, -3888.38, 60.26),
    (-56.51, -3836.85, 60.59),
    (312.92, -3859.24, 60.59),
    (265.00, -4175.00, 84.00),
    (340.00, -4410.00, 88.00),
    (410.00, -4588.00, 78.50),
]

PATHS = [
    # path_id, from, to, points
    (1979, RAZORHILL_NODE, ORG, [
        RAZORHILL,
        *RAZORHILL_ORG_APPROACH,
        *reversed(ORG_GATE_CORRIDOR),
        (1677.59, -4315.70, 61.17),
    ]),
    (1980, ORG, RAZORHILL_NODE, [
        (1678.60, -4317.23, 62.11),
        *ORG_GATE_CORRIDOR,
        *reversed(RAZORHILL_ORG_APPROACH),
        RAZORHILL,
    ]),
    (1981, RAZORHILL_NODE, RATCHET, [
        RAZORHILL,
        *RAZORHILL_TO_RATCHET,
        (-894.60, -3773.00, 11.50),
    ]),
    (1982, RATCHET, RAZORHILL_NODE, [
        (-894.60, -3773.00, 11.50),
        *RATCHET_TO_RAZORHILL,
        RAZORHILL,
    ]),
]


def fare(points):
    distance = sum(math.dist(points[i], points[i + 1]) for i in range(len(points) - 1))
    if distance <= 3000:
        return 110
    if distance <= 4000:
        return 210
    if distance <= 5000:
        return 430
    if distance <= 6500:
        return 630
    if distance <= 8000:
        return 730
    if distance <= 9500:
        return 830
    return 1020


def read_dbc(path: Path):
    data = path.read_bytes()
    magic, records, fields, record_size, string_size = struct.unpack_from("<4sIIII", data, 0)
    if magic != b"WDBC":
        raise ValueError(f"{path} is not a WDBC file")
    rows = [list(struct.unpack_from("<" + "I" * fields, data, 20 + i * record_size)) for i in range(records)]
    strings = bytearray(data[20 + records * record_size:20 + records * record_size + string_size])
    return fields, rows, strings


def write_dbc(path: Path, fields: int, rows: list[list[int]], strings: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    record_size = fields * 4
    with path.open("wb") as f:
        f.write(struct.pack("<4sIIII", b"WDBC", len(rows), fields, record_size, len(strings)))
        for row in rows:
            if len(row) != fields:
                raise ValueError(f"{path.name}: row has {len(row)} fields, expected {fields}")
            f.write(struct.pack("<" + "I" * fields, *row))
        f.write(strings)


def fbits(value: float) -> int:
    return struct.unpack("<I", struct.pack("<f", float(value)))[0]


def add_string(strings: bytearray, value: str) -> int:
    encoded = value.encode("utf-8") + b"\0"
    existing = bytes(strings).find(encoded)
    if existing >= 0:
        return existing
    offset = len(strings)
    strings.extend(encoded)
    return offset


def patched_dbc_files():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    node_fields, node_rows, node_strings = read_dbc(SERVER_DBC / "TaxiNodes.dbc")
    path_fields, path_rows, path_strings = read_dbc(SERVER_DBC / "TaxiPath.dbc")
    pathnode_fields, pathnode_rows, pathnode_strings = read_dbc(SERVER_DBC / "TaxiPathNode.dbc")

    node_rows = [row for row in node_rows if row[0] != RAZORHILL_NODE]
    path_ids = {path_id for path_id, *_ in PATHS}
    path_rows = [row for row in path_rows if row[0] not in path_ids]
    pathnode_rows = [row for row in pathnode_rows if row[1] not in path_ids]

    name_offset = add_string(node_strings, RAZORHILL_NAME)
    # TaxiNodes.dbc: ID, map, x/y/z, 16 locale string offsets, name mask, horde mount, alliance mount.
    node_rows.append([
        RAZORHILL_NODE,
        1,
        fbits(RAZORHILL[0]),
        fbits(RAZORHILL[1]),
        fbits(RAZORHILL[2]),
        name_offset,
        *([0] * 15),
        16712190,
        2224,
        0,
    ])
    node_rows.sort(key=lambda row: row[0])

    next_pathnode_id = max(row[0] for row in pathnode_rows) + 1
    for path_id, src, dst, points in PATHS:
        path_rows.append([path_id, src, dst, fare(points)])
        for index, (x, y, z) in enumerate(points):
            pathnode_rows.append([
                next_pathnode_id,
                path_id,
                index,
                1,
                fbits(x),
                fbits(y),
                fbits(z),
                0,
                0,
                0,
                0,
            ])
            next_pathnode_id += 1

    path_rows.sort(key=lambda row: row[0])
    pathnode_rows.sort(key=lambda row: row[0])

    files = {
        "DBFilesClient\\TaxiNodes.dbc": OUT_DIR / "TaxiNodes.dbc",
        "DBFilesClient\\TaxiPath.dbc": OUT_DIR / "TaxiPath.dbc",
        "DBFilesClient\\TaxiPathNode.dbc": OUT_DIR / "TaxiPathNode.dbc",
    }
    write_dbc(files["DBFilesClient\\TaxiNodes.dbc"], node_fields, node_rows, node_strings)
    write_dbc(files["DBFilesClient\\TaxiPath.dbc"], path_fields, path_rows, path_strings)
    write_dbc(files["DBFilesClient\\TaxiPathNode.dbc"], pathnode_fields, pathnode_rows, pathnode_strings)
    return files


CRYPT_TABLE = []


def prepare_crypt_table():
    seed = 0x00100001
    table = [0] * 0x500
    for index1 in range(0x100):
        index2 = index1
        for _ in range(5):
            seed = (seed * 125 + 3) % 0x2AAAAB
            temp1 = (seed & 0xFFFF) << 16
            seed = (seed * 125 + 3) % 0x2AAAAB
            temp2 = seed & 0xFFFF
            table[index2] = temp1 | temp2
            index2 += 0x100
    return table


CRYPT_TABLE = prepare_crypt_table()


def mpq_hash(value: str, hash_type: int) -> int:
    seed1 = 0x7FED7FED
    seed2 = 0xEEEEEEEE
    for ch in value.upper().replace("/", "\\"):
        val = CRYPT_TABLE[(hash_type << 8) + ord(ch)]
        seed1 = (val ^ (seed1 + seed2)) & 0xFFFFFFFF
        seed2 = (ord(ch) + seed1 + seed2 + ((seed2 << 5) & 0xFFFFFFFF) + 3) & 0xFFFFFFFF
    return seed1


def mpq_encrypt_words(words: list[int], key: int) -> bytes:
    seed = 0xEEEEEEEE
    output = bytearray()
    for word in words:
        seed = (seed + CRYPT_TABLE[0x400 + (key & 0xFF)]) & 0xFFFFFFFF
        encrypted = (word ^ ((key + seed) & 0xFFFFFFFF)) & 0xFFFFFFFF
        key = (((~key << 21) & 0xFFFFFFFF) + 0x11111111 | (key >> 11)) & 0xFFFFFFFF
        seed = (word + seed + ((seed << 5) & 0xFFFFFFFF) + 3) & 0xFFFFFFFF
        output.extend(struct.pack("<I", encrypted))
    return bytes(output)


def build_mpq(files: dict[str, Path], out_path: Path):
    if not MPQCLI.exists():
        raise FileNotFoundError(MPQCLI)

    staging = OUT_DIR / "mpq_staging"
    if staging.exists():
        shutil.rmtree(staging)
    for archive_name, src in files.items():
        dst = staging / archive_name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()
    subprocess.run(
        [
            str(MPQCLI),
            "create",
            str(staging),
            "--output",
            str(out_path),
            "--game",
            "wow-wotlk",
        ],
        check=True,
    )


def sql_literal(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def generate_sql():
    pathnode_id = 46875
    lines = [
        "-- Razor Hill flight path test for AzerothCore WotLK 3.3.5a.",
        "-- Adds a Horde flight master and a client/server taxi node connected to Orgrimmar and Ratchet.",
        "-- Client patch: Data\\patch-4.MPQ",
        "",
        f"SET @RAZORHILL_NODE := {RAZORHILL_NODE};",
        f"SET @RAZORHILL_CREATURE := {RAZORHILL_CREATURE};",
        "",
        "DELETE FROM `creature` WHERE `id1` = @RAZORHILL_CREATURE;",
        "DELETE FROM `creature_template_model` WHERE `CreatureID` = @RAZORHILL_CREATURE;",
        "DELETE FROM `creature_equip_template` WHERE `CreatureID` = @RAZORHILL_CREATURE;",
        "DELETE FROM `creature_template_movement` WHERE `CreatureId` = @RAZORHILL_CREATURE;",
        "DELETE FROM `creature_template` WHERE `entry` = @RAZORHILL_CREATURE;",
        "DELETE FROM `taxinodes_dbc` WHERE `ID` = @RAZORHILL_NODE;",
        "DELETE FROM `taxipath_dbc` WHERE `ID` BETWEEN 1979 AND 1982;",
        "DELETE FROM `taxipathnode_dbc` WHERE `PathID` BETWEEN 1979 AND 1982;",
        "",
        "INSERT INTO `taxinodes_dbc`",
        "(`ID`,`ContinentID`,`X`,`Y`,`Z`,`Name_Lang_enUS`,`Name_Lang_enGB`,`Name_Lang_koKR`,`Name_Lang_frFR`,`Name_Lang_deDE`,`Name_Lang_enCN`,`Name_Lang_zhCN`,`Name_Lang_enTW`,`Name_Lang_zhTW`,`Name_Lang_esES`,`Name_Lang_esMX`,`Name_Lang_ruRU`,`Name_Lang_ptPT`,`Name_Lang_ptBR`,`Name_Lang_itIT`,`Name_Lang_Unk`,`Name_Lang_Mask`,`MountCreatureID_1`,`MountCreatureID_2`)",
        "VALUES",
        f"(@RAZORHILL_NODE,1,{RAZORHILL[0]},{RAZORHILL[1]},{RAZORHILL[2]},{sql_literal(RAZORHILL_NAME)},'', '', '', '', '', '', '', '', '', '', '', '', '', '', '',16712190,2224,0);",
        "",
        "INSERT INTO `taxipath_dbc` (`ID`,`FromTaxiNode`,`ToTaxiNode`,`Cost`) VALUES",
    ]
    lines.extend(
        f"({path_id},{src},{dst},{fare(points)}){',' if i < len(PATHS) - 1 else ';'}"
        for i, (path_id, src, dst, points) in enumerate(PATHS)
    )
    lines += ["", "INSERT INTO `taxipathnode_dbc` (`ID`,`PathID`,`NodeIndex`,`ContinentID`,`LocX`,`LocY`,`LocZ`,`Flags`,`Delay`,`ArrivalEventID`,`DepartureEventID`) VALUES"]
    rows = []
    for path_id, _, _, points in PATHS:
        for index, (x, y, z) in enumerate(points):
            rows.append(f"({pathnode_id},{path_id},{index},1,{x},{y},{z},0,0,0,0)")
            pathnode_id += 1
    for index, row in enumerate(rows):
        lines.append(row + ("," if index < len(rows) - 1 else ";"))

    lines += [
        "",
        "INSERT INTO `creature_template`",
        "(`entry`,`difficulty_entry_1`,`difficulty_entry_2`,`difficulty_entry_3`,`KillCredit1`,`KillCredit2`,`name`,`subname`,`IconName`,`gossip_menu_id`,`minlevel`,`maxlevel`,`exp`,`faction`,`npcflag`,`speed_walk`,`speed_run`,`speed_swim`,`speed_flight`,`detection_range`,`rank`,`dmgschool`,`DamageModifier`,`BaseAttackTime`,`RangeAttackTime`,`BaseVariance`,`RangeVariance`,`unit_class`,`unit_flags`,`unit_flags2`,`dynamicflags`,`family`,`type`,`type_flags`,`lootid`,`pickpocketloot`,`skinloot`,`PetSpellDataId`,`VehicleId`,`mingold`,`maxgold`,`AIName`,`MovementType`,`HoverHeight`,`HealthModifier`,`ManaModifier`,`ArmorModifier`,`ExperienceModifier`,`RacialLeader`,`movementId`,`RegenHealth`,`CreatureImmunitiesId`,`flags_extra`,`ScriptName`,`VerifiedBuild`)",
        "VALUES",
        "(@RAZORHILL_CREATURE,0,0,0,0,0,'Gor''mul Windtamer','Wind Rider Master',NULL,0,55,55,0,29,8195,1,1.14286,1,1,20,0,0,1,2000,2000,1,1,1,0,0,0,0,7,0,0,0,0,0,0,0,0,'',0,1,1,1,1,1,0,0,1,0,0,'',12340);",
        "",
        "INSERT INTO `creature_template_model` (`CreatureID`,`Idx`,`CreatureDisplayID`,`DisplayScale`,`Probability`,`VerifiedBuild`)",
        "VALUES (@RAZORHILL_CREATURE,0,1311,1,1,12340);",
        "",
        "INSERT INTO `creature_equip_template` (`CreatureID`,`ID`,`ItemID1`,`ItemID2`,`ItemID3`,`VerifiedBuild`)",
        "VALUES (@RAZORHILL_CREATURE,1,3433,0,0,18019);",
        "",
        "INSERT INTO `creature`",
        "(`id1`,`id2`,`id3`,`map`,`zoneId`,`areaId`,`spawnMask`,`phaseMask`,`equipment_id`,`position_x`,`position_y`,`position_z`,`orientation`,`spawntimesecs`,`wander_distance`,`currentwaypoint`,`curhealth`,`curmana`,`MovementType`,`npcflag`,`unit_flags`,`dynamicflags`,`ScriptName`,`VerifiedBuild`,`CreateObject`,`Comment`)",
        "VALUES",
        "(@RAZORHILL_CREATURE,0,0,1,14,362,1,1,1,384.0,-4600.0,76.17,3.89208,600,0,0,10572,0,0,0,0,0,'',0,0,'Codex Razorhill Flightpath: Flight Master');",
        "",
    ]
    SQL_OUT.write_text("\n".join(lines), encoding="utf-8")
    SOURCE_SQL_OUT.write_text(SQL_OUT.read_text(encoding="utf-8"), encoding="utf-8")


def main():
    files = patched_dbc_files()
    build_mpq(files, CLIENT_PATCH)
    generate_sql()
    print(f"Wrote {CLIENT_PATCH}")
    print(f"Wrote {SQL_OUT}")
    print(f"Wrote {SOURCE_SQL_OUT}")


if __name__ == "__main__":
    main()
