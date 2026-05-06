import math
import shutil
import struct
from dataclasses import dataclass
from pathlib import Path


WORKSPACE = Path(r"C:\Users\monty\Documents\Codex\2026-04-29\i-am-creating-a-world-of")
SERVER_DBC = Path(r"C:\Build\bin\Debug\data\dbc")
OUT_DIR = WORKSPACE / "artifacts" / "razorhill_flightpath"
SQL_OUT = OUT_DIR / "2026_05_03_00_starter_flightpaths.sql"
SOURCE_SQL_OUT = Path(r"C:\Azerothcore\data\sql\custom\db_world\2026_05_03_00_starter_flightpaths.sql")

PATHNODE_START = 46937


@dataclass(frozen=True)
class TaxiNode:
    node_id: int
    name: str
    map_id: int
    pos: tuple[float, float, float]
    horde_mount: int
    alliance_mount: int


@dataclass(frozen=True)
class FlightMaster:
    entry: int
    name: str
    subname: str
    faction: int
    display_id: int
    pos: tuple[float, float, float]
    orientation: float
    zone_id: int
    area_id: int
    equip_id: int = 0


@dataclass(frozen=True)
class TaxiPath:
    path_id: int
    src: int
    dst: int
    points: list[tuple[float, float, float]]


def reverse(points: list[tuple[float, float, float]]) -> list[tuple[float, float, float]]:
    return list(reversed(points))


# Existing stock taxi node IDs.
STORMWIND = 2
IRONFORGE = 6
UNDERCITY = 11
THUNDER_BLUFF = 22
ORGRIMMAR = 23
RUTTHERAN = 27
RATCHET = 80
SILVERMOON = 82
EXODAR = 94

# Custom starter-town access nodes.
RAZORHILL_NODE = 441
DOLANAAR_NODE = 443
BLOODHOOF_NODE = 444
KHARANOS_NODE = 445
GOLDSHIRE_NODE = 446
FALCONWING_NODE = 447
AZURE_WATCH_NODE = 448
# AzerothCore's 3.3.5 taxi-node lookup is fixed-size in debug builds, so keep
# custom IDs under 449. 437 is unused in the stock WotLK TaxiNodes.dbc.
BRILL_NODE = 437
STALE_NODE_IDS = {442, 449}
STALE_PATH_IDS = {1985, 1986}
STALE_CREATURE_IDS = {900041}

RAZORHILL = (384.0, -4600.0, 76.17)
DOLANAAR = (9848.37, 966.95, 1306.38)
BLOODHOOF = (-2240.91, -399.17, -9.42)
KHARANOS = (-5597.31, -483.40, 396.98)
GOLDSHIRE = (-9448.55, 68.24, 56.32)
FALCONWING = (9514.33, -6822.10, 16.49)
AZURE_WATCH = (-4190.85, -12516.50, 44.53)
BRILL = (2259.25, 290.43, 34.11)

CUSTOM_NODES = [
    TaxiNode(RAZORHILL_NODE, "Razor Hill, Durotar", 1, RAZORHILL, 2224, 0),
    TaxiNode(DOLANAAR_NODE, "Dolanaar, Teldrassil", 1, DOLANAAR, 0, 3837),
    TaxiNode(BLOODHOOF_NODE, "Bloodhoof Village, Mulgore", 1, BLOODHOOF, 2224, 0),
    TaxiNode(KHARANOS_NODE, "Kharanos, Dun Morogh", 0, KHARANOS, 0, 541),
    TaxiNode(GOLDSHIRE_NODE, "Goldshire, Elwynn", 0, GOLDSHIRE, 0, 541),
    TaxiNode(FALCONWING_NODE, "Falconwing Square, Eversong Woods", 530, FALCONWING, 19917, 0),
    TaxiNode(AZURE_WATCH_NODE, "Azure Watch, Azuremyst Isle", 530, AZURE_WATCH, 0, 3837),
    TaxiNode(BRILL_NODE, "Brill, Tirisfal Glades", 0, BRILL, 3574, 0),
]

FLIGHT_MASTERS = [
    FlightMaster(900010, "Gor'mul Windtamer", "Wind Rider Master", 29, 1311, RAZORHILL, 3.89208, 14, 362, 3433),
    FlightMaster(900040, "Lariia Moonfeather", "Hippogryph Master", 80, 1932, DOLANAAR, 3.77457, 141, 186),
    FlightMaster(900042, "Aponi Windmane", "Wind Rider Master", 104, 2412, BLOODHOOF, 2.53353, 215, 222),
    FlightMaster(900043, "Bromm Stonefeather", "Gryphon Master", 55, 5037, KHARANOS, 3.17566, 1, 131),
    FlightMaster(900044, "Maddie Stormwing", "Gryphon Master", 12, 5128, GOLDSHIRE, 2.11150, 12, 87),
    FlightMaster(900045, "Aelara Sunwing", "Dragonhawk Master", 1604, 16059, FALCONWING, 1.60979, 3430, 3462),
    FlightMaster(900046, "Naraani Skygazer", "Hippogryph Master", 1638, 17084, AZURE_WATCH, 1.34225, 3524, 3576),
    FlightMaster(900047, "Morga Gravewing", "Bat Handler", 68, 12569, BRILL, 0.98741, 85, 159),
]

# Keep this stock Orgrimmar gate segment unchanged from the Razorhill test.
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

# These hub points mirror stock Blizzard taxi splines around each hub. Custom
# routes use them so multi-hop flights transition naturally instead of snapping
# from a custom endpoint to a nearby stock departure point.
RUTTHERAN_DEPARTURE = (8643.30, 841.30, 25.00)
RUTTHERAN_ARRIVAL = (8643.80, 840.70, 27.10)
THUNDER_BLUFF_DEPARTURE = (-1197.00, 29.80, 179.20)
THUNDER_BLUFF_ARRIVAL = (-1196.80, 29.60, 180.40)
IRONFORGE_DEPARTURE = (-4822.80, -1158.00, 503.20)
IRONFORGE_ARRIVAL = (-4822.40, -1158.10, 503.40)
STORMWIND_DEPARTURE = (-8850.40, 497.30, 111.40)
STORMWIND_ARRIVAL = (-8834.50, 479.60, 112.70)
SILVERMOON_DEPARTURE = (9371.60, -7165.80, 13.10)
SILVERMOON_ARRIVAL = (9373.10, -7166.10, 11.50)
EXODAR_DEPARTURE = (-4053.60, -11789.10, 9.90)
EXODAR_ARRIVAL = (-4054.80, -11793.40, 11.10)
UNDERCITY_DEPARTURE = (1568.50, 268.50, -41.70)
UNDERCITY_ARRIVAL = (1568.50, 268.50, -42.10)

# Stock Undercity routes all use this tunnel/courtyard segment. Reusing it is
# much safer than inventing a new descent through the underground city.
UNDERCITY_OUT = [
    UNDERCITY_DEPARTURE,
    (1563.90, 250.30, -38.30),
    (1576.70, 220.70, -31.80),
    (1606.30, 217.30, -26.10),
    (1630.80, 239.20, -28.90),
    (1663.30, 239.20, -35.00),
    (1738.50, 242.50, -38.90),
    (1748.70, 278.60, -44.00),
]
UNDERCITY_IN = [
    (1741.90, 292.40, -42.10),
    (1751.10, 264.20, -42.10),
    (1733.60, 243.10, -38.10),
    (1663.30, 239.20, -30.10),
    (1638.80, 237.90, -26.10),
    (1606.30, 217.30, -26.10),
    (1573.90, 225.60, -34.10),
    UNDERCITY_ARRIVAL,
]

DOLANAAR_TO_RUTTHERAN = [
    DOLANAAR,
    (9846.20, 960.40, 1310.20),
    (9825.00, 900.00, 1345.00),
    (9778.00, 772.00, 1428.00),
    (9684.00, 540.00, 1512.00),
    (9505.453, 118.53508, 1558.6642),
    (9360.00, 18.00, 1450.00),
    (9185.00, 90.00, 1180.00),
    (9005.00, 260.00, 850.00),
    (8855.00, 485.00, 460.00),
    (8748.00, 690.00, 160.00),
    RUTTHERAN_ARRIVAL,
]

BLOODHOOF_TO_TB = [
    BLOODHOOF,
    (-2225.0, -364.0, 2.0),
    (-2138.0, -252.0, 52.0),
    (-1980.0, -120.0, 118.0),
    (-1748.0, -26.0, 185.0),
    (-1485.0, 48.0, 225.0),
    THUNDER_BLUFF_ARRIVAL,
]

KHARANOS_TO_IF = [
    KHARANOS,
    (-5580.0, -525.0, 410.0),
    (-5485.0, -640.0, 455.0),
    (-5320.0, -805.0, 535.0),
    (-5090.0, -1010.0, 575.0),
    IRONFORGE_ARRIVAL,
]

GOLDSHIRE_TO_SW = [
    GOLDSHIRE,
    (-9428.0, 96.0, 67.0),
    (-9340.0, 155.0, 92.0),
    (-9200.0, 265.0, 126.0),
    (-9025.0, 410.0, 148.0),
    STORMWIND_ARRIVAL,
]

FALCONWING_TO_SILVERMOON = [
    FALCONWING,
    (9521.0, -6865.0, 31.0),
    (9508.0, -6938.0, 78.0),
    (9470.0, -7024.0, 112.0),
    (9412.0, -7110.0, 74.0),
    SILVERMOON_ARRIVAL,
]

AZURE_TO_EXODAR = [
    AZURE_WATCH,
    (-4184.0, -12470.0, 58.0),
    (-4168.0, -12310.0, 104.0),
    (-4136.0, -12105.0, 130.0),
    (-4100.0, -11925.0, 78.0),
    EXODAR_ARRIVAL,
]

BRILL_TO_UNDERCITY = [
    BRILL,
    (2234.0, 304.0, 39.0),
    (2148.0, 330.0, 58.0),
    (2000.0, 345.0, 74.0),
    (1842.0, 324.0, 55.0),
    *UNDERCITY_IN,
]

UNDERCITY_TO_BRILL = [
    *UNDERCITY_OUT,
    (1842.0, 324.0, 55.0),
    (2000.0, 345.0, 74.0),
    (2148.0, 330.0, 58.0),
    (2234.0, 304.0, 39.0),
    BRILL,
]

PATHS = [
    TaxiPath(1979, RAZORHILL_NODE, ORGRIMMAR, [RAZORHILL, *RAZORHILL_ORG_APPROACH, *reversed(ORG_GATE_CORRIDOR), (1677.59, -4315.70, 61.17)]),
    TaxiPath(1980, ORGRIMMAR, RAZORHILL_NODE, [(1678.60, -4317.23, 62.11), *ORG_GATE_CORRIDOR, *reversed(RAZORHILL_ORG_APPROACH), RAZORHILL]),
    TaxiPath(1981, RAZORHILL_NODE, RATCHET, [RAZORHILL, *RAZORHILL_TO_RATCHET, (-894.60, -3773.00, 11.50)]),
    TaxiPath(1982, RATCHET, RAZORHILL_NODE, [(-894.60, -3773.00, 11.50), *RATCHET_TO_RAZORHILL, RAZORHILL]),
    TaxiPath(1983, DOLANAAR_NODE, RUTTHERAN, DOLANAAR_TO_RUTTHERAN),
    TaxiPath(1984, RUTTHERAN, DOLANAAR_NODE, [RUTTHERAN_DEPARTURE, *reverse(DOLANAAR_TO_RUTTHERAN[:-1])]),
    TaxiPath(1987, BLOODHOOF_NODE, THUNDER_BLUFF, BLOODHOOF_TO_TB),
    TaxiPath(1988, THUNDER_BLUFF, BLOODHOOF_NODE, [THUNDER_BLUFF_DEPARTURE, *reverse(BLOODHOOF_TO_TB[:-1])]),
    TaxiPath(1989, KHARANOS_NODE, IRONFORGE, KHARANOS_TO_IF),
    TaxiPath(1990, IRONFORGE, KHARANOS_NODE, [IRONFORGE_DEPARTURE, *reverse(KHARANOS_TO_IF[:-1])]),
    TaxiPath(1991, GOLDSHIRE_NODE, STORMWIND, GOLDSHIRE_TO_SW),
    TaxiPath(1992, STORMWIND, GOLDSHIRE_NODE, [STORMWIND_DEPARTURE, *reverse(GOLDSHIRE_TO_SW[:-1])]),
    TaxiPath(1993, FALCONWING_NODE, SILVERMOON, FALCONWING_TO_SILVERMOON),
    TaxiPath(1994, SILVERMOON, FALCONWING_NODE, [SILVERMOON_DEPARTURE, *reverse(FALCONWING_TO_SILVERMOON[:-1])]),
    TaxiPath(1995, AZURE_WATCH_NODE, EXODAR, AZURE_TO_EXODAR),
    TaxiPath(1996, EXODAR, AZURE_WATCH_NODE, [EXODAR_DEPARTURE, *reverse(AZURE_TO_EXODAR[:-1])]),
    TaxiPath(1997, BRILL_NODE, UNDERCITY, BRILL_TO_UNDERCITY),
    TaxiPath(1998, UNDERCITY, BRILL_NODE, UNDERCITY_TO_BRILL),
]


def fare(points: list[tuple[float, float, float]]) -> int:
    distance = sum(math.dist(points[i], points[i + 1]) for i in range(len(points) - 1))
    if distance <= 1600:
        return 60
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

    custom_node_ids = {node.node_id for node in CUSTOM_NODES}
    delete_node_ids = custom_node_ids | STALE_NODE_IDS
    path_ids = {path.path_id for path in PATHS} | STALE_PATH_IDS

    node_rows = [row for row in node_rows if row[0] not in delete_node_ids]
    path_rows = [row for row in path_rows if row[0] not in path_ids]
    pathnode_rows = [row for row in pathnode_rows if row[1] not in path_ids]

    for node in CUSTOM_NODES:
        name_offset = add_string(node_strings, node.name)
        node_rows.append([
            node.node_id,
            node.map_id,
            fbits(node.pos[0]),
            fbits(node.pos[1]),
            fbits(node.pos[2]),
            name_offset,
            *([0] * 15),
            16712190,
            node.horde_mount,
            node.alliance_mount,
        ])
    node_rows.sort(key=lambda row: row[0])

    next_pathnode_id = max(row[0] for row in pathnode_rows) + 1
    for path in PATHS:
        path_rows.append([path.path_id, path.src, path.dst, fare(path.points)])
        map_id = next(node.map_id for node in CUSTOM_NODES if node.node_id == path.src) if path.src in custom_node_ids else None
        for index, (x, y, z) in enumerate(path.points):
            point_map = map_id
            if point_map is None:
                point_map = next(node.map_id for node in CUSTOM_NODES if node.node_id == path.dst)
            pathnode_rows.append([next_pathnode_id, path.path_id, index, point_map, fbits(x), fbits(y), fbits(z), 0, 0, 0, 0])
            next_pathnode_id += 1

    path_rows.sort(key=lambda row: row[0])
    pathnode_rows.sort(key=lambda row: row[0])

    files = {
        "TaxiNodes.dbc": OUT_DIR / "TaxiNodes.dbc",
        "TaxiPath.dbc": OUT_DIR / "TaxiPath.dbc",
        "TaxiPathNode.dbc": OUT_DIR / "TaxiPathNode.dbc",
    }
    write_dbc(files["TaxiNodes.dbc"], node_fields, node_rows, node_strings)
    write_dbc(files["TaxiPath.dbc"], path_fields, path_rows, path_strings)
    write_dbc(files["TaxiPathNode.dbc"], pathnode_fields, pathnode_rows, pathnode_strings)
    return files


def sql_literal(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def generate_sql():
    pathnode_id = PATHNODE_START
    delete_node_ids = ", ".join(str(node_id) for node_id in sorted({node.node_id for node in CUSTOM_NODES} | STALE_NODE_IDS))
    path_ids = ", ".join(str(path_id) for path_id in sorted({path.path_id for path in PATHS} | STALE_PATH_IDS))
    creature_ids = ", ".join(str(entry) for entry in sorted({fm.entry for fm in FLIGHT_MASTERS} | STALE_CREATURE_IDS))

    lines = [
        "-- Starter-town flight paths for AzerothCore WotLK 3.3.5a.",
        "-- Adds blizz-like starter village flight masters and routes into the stock taxi networks.",
        "-- Client patch: Data\\patch-4.MPQ",
        "",
        f"DELETE FROM `creature` WHERE `id1` IN ({creature_ids});",
        f"DELETE FROM `creature_template_model` WHERE `CreatureID` IN ({creature_ids});",
        f"DELETE FROM `creature_equip_template` WHERE `CreatureID` IN ({creature_ids});",
        f"DELETE FROM `creature_template_movement` WHERE `CreatureId` IN ({creature_ids});",
        f"DELETE FROM `creature_template` WHERE `entry` IN ({creature_ids});",
        f"DELETE FROM `taxinodes_dbc` WHERE `ID` IN ({delete_node_ids});",
        f"DELETE FROM `taxipath_dbc` WHERE `ID` IN ({path_ids});",
        f"DELETE FROM `taxipathnode_dbc` WHERE `PathID` IN ({path_ids});",
        "",
        "INSERT INTO `taxinodes_dbc`",
        "(`ID`,`ContinentID`,`X`,`Y`,`Z`,`Name_Lang_enUS`,`Name_Lang_enGB`,`Name_Lang_koKR`,`Name_Lang_frFR`,`Name_Lang_deDE`,`Name_Lang_enCN`,`Name_Lang_zhCN`,`Name_Lang_enTW`,`Name_Lang_zhTW`,`Name_Lang_esES`,`Name_Lang_esMX`,`Name_Lang_ruRU`,`Name_Lang_ptPT`,`Name_Lang_ptBR`,`Name_Lang_itIT`,`Name_Lang_Unk`,`Name_Lang_Mask`,`MountCreatureID_1`,`MountCreatureID_2`)",
        "VALUES",
    ]
    for index, node in enumerate(CUSTOM_NODES):
        x, y, z = node.pos
        lines.append(
            f"({node.node_id},{node.map_id},{x},{y},{z},{sql_literal(node.name)},'', '', '', '', '', '', '', '', '', '', '', '', '', '', '',16712190,{node.horde_mount},{node.alliance_mount})"
            + ("," if index < len(CUSTOM_NODES) - 1 else ";")
        )

    lines += ["", "INSERT INTO `taxipath_dbc` (`ID`,`FromTaxiNode`,`ToTaxiNode`,`Cost`) VALUES"]
    for index, path in enumerate(PATHS):
        lines.append(f"({path.path_id},{path.src},{path.dst},{fare(path.points)})" + ("," if index < len(PATHS) - 1 else ";"))

    lines += ["", "INSERT INTO `taxipathnode_dbc` (`ID`,`PathID`,`NodeIndex`,`ContinentID`,`LocX`,`LocY`,`LocZ`,`Flags`,`Delay`,`ArrivalEventID`,`DepartureEventID`) VALUES"]
    pathnode_rows = []
    custom_maps = {node.node_id: node.map_id for node in CUSTOM_NODES}
    for path in PATHS:
        map_id = custom_maps.get(path.src, custom_maps.get(path.dst))
        for index, (x, y, z) in enumerate(path.points):
            pathnode_rows.append(f"({pathnode_id},{path.path_id},{index},{map_id},{x},{y},{z},0,0,0,0)")
            pathnode_id += 1
    for index, row in enumerate(pathnode_rows):
        lines.append(row + ("," if index < len(pathnode_rows) - 1 else ";"))

    lines += [
        "",
        "INSERT INTO `creature_template`",
        "(`entry`,`difficulty_entry_1`,`difficulty_entry_2`,`difficulty_entry_3`,`KillCredit1`,`KillCredit2`,`name`,`subname`,`IconName`,`gossip_menu_id`,`minlevel`,`maxlevel`,`exp`,`faction`,`npcflag`,`speed_walk`,`speed_run`,`speed_swim`,`speed_flight`,`detection_range`,`rank`,`dmgschool`,`DamageModifier`,`BaseAttackTime`,`RangeAttackTime`,`BaseVariance`,`RangeVariance`,`unit_class`,`unit_flags`,`unit_flags2`,`dynamicflags`,`family`,`type`,`type_flags`,`lootid`,`pickpocketloot`,`skinloot`,`PetSpellDataId`,`VehicleId`,`mingold`,`maxgold`,`AIName`,`MovementType`,`HoverHeight`,`HealthModifier`,`ManaModifier`,`ArmorModifier`,`ExperienceModifier`,`RacialLeader`,`movementId`,`RegenHealth`,`CreatureImmunitiesId`,`flags_extra`,`ScriptName`,`VerifiedBuild`)",
        "VALUES",
    ]
    for index, fm in enumerate(FLIGHT_MASTERS):
        lines.append(
            f"({fm.entry},0,0,0,0,0,{sql_literal(fm.name)},{sql_literal(fm.subname)},NULL,0,55,55,0,{fm.faction},8195,1,1.14286,1,1,20,0,0,1,2000,2000,1,1,1,0,0,0,0,7,0,0,0,0,0,0,0,0,'',0,1,1,1,1,1,0,0,1,0,0,'',12340)"
            + ("," if index < len(FLIGHT_MASTERS) - 1 else ";")
        )

    lines += ["", "INSERT INTO `creature_template_model` (`CreatureID`,`Idx`,`CreatureDisplayID`,`DisplayScale`,`Probability`,`VerifiedBuild`) VALUES"]
    for index, fm in enumerate(FLIGHT_MASTERS):
        lines.append(f"({fm.entry},0,{fm.display_id},1,1,12340)" + ("," if index < len(FLIGHT_MASTERS) - 1 else ";"))

    equipped = [fm for fm in FLIGHT_MASTERS if fm.equip_id]
    if equipped:
        lines += ["", "INSERT INTO `creature_equip_template` (`CreatureID`,`ID`,`ItemID1`,`ItemID2`,`ItemID3`,`VerifiedBuild`) VALUES"]
        for index, fm in enumerate(equipped):
            lines.append(f"({fm.entry},1,{fm.equip_id},0,0,18019)" + ("," if index < len(equipped) - 1 else ";"))

    lines += [
        "",
        "INSERT INTO `creature`",
        "(`id1`,`id2`,`id3`,`map`,`zoneId`,`areaId`,`spawnMask`,`phaseMask`,`equipment_id`,`position_x`,`position_y`,`position_z`,`orientation`,`spawntimesecs`,`wander_distance`,`currentwaypoint`,`curhealth`,`curmana`,`MovementType`,`npcflag`,`unit_flags`,`dynamicflags`,`ScriptName`,`VerifiedBuild`,`CreateObject`,`Comment`)",
        "VALUES",
    ]
    node_by_pos = {fm.pos: node for fm in FLIGHT_MASTERS for node in CUSTOM_NODES if node.pos == fm.pos}
    for index, fm in enumerate(FLIGHT_MASTERS):
        x, y, z = fm.pos
        node = node_by_pos[fm.pos]
        equipment_id = 1 if fm.equip_id else 0
        lines.append(
            f"({fm.entry},0,0,{node.map_id},{fm.zone_id},{fm.area_id},1,1,{equipment_id},{x},{y},{z},{fm.orientation},600,0,0,10572,0,0,0,0,0,'',0,0,{sql_literal('Codex Starter Flightpaths: ' + fm.name)})"
            + ("," if index < len(FLIGHT_MASTERS) - 1 else ";")
        )

    SQL_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    SOURCE_SQL_OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SQL_OUT, SOURCE_SQL_OUT)


def main():
    patched_dbc_files()
    generate_sql()
    print(f"Wrote {OUT_DIR / 'TaxiNodes.dbc'}")
    print(f"Wrote {OUT_DIR / 'TaxiPath.dbc'}")
    print(f"Wrote {OUT_DIR / 'TaxiPathNode.dbc'}")
    print(f"Wrote {SQL_OUT}")
    print(f"Wrote {SOURCE_SQL_OUT}")


if __name__ == "__main__":
    main()
