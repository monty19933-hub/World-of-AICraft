import math
import struct
from pathlib import Path


ROOT = Path(r"C:\Build\bin\Debug\data\dbc")


def read_dbc(path: Path):
    data = path.read_bytes()
    magic, records, fields, record_size, string_size = struct.unpack_from("<4sIIII", data, 0)
    if magic != b"WDBC":
        raise ValueError(f"{path} is not a WDBC file")
    pos = 20
    rows = []
    for _ in range(records):
        row = struct.unpack_from("<" + "I" * fields, data, pos)
        rows.append(row)
        pos += record_size
    strings = data[pos:pos + string_size]
    return records, fields, record_size, rows, strings


def get_str(block: bytes, offset: int) -> str:
    end = block.find(b"\0", offset)
    if end < 0:
        return ""
    return block[offset:end].decode("utf-8", errors="replace")


nodes_meta = read_dbc(ROOT / "TaxiNodes.dbc")
paths_meta = read_dbc(ROOT / "TaxiPath.dbc")
pathnodes_meta = read_dbc(ROOT / "TaxiPathNode.dbc")

nodes = {}
for row in nodes_meta[3]:
    node_id = row[0]
    map_id = row[1]
    x, y, z = struct.unpack("<fff", struct.pack("<III", row[2], row[3], row[4]))
    name = get_str(nodes_meta[4], row[5])
    horde_mount = row[22]
    alliance_mount = row[23]
    nodes[node_id] = {
        "id": node_id,
        "map": map_id,
        "x": x,
        "y": y,
        "z": z,
        "name": name,
        "horde_mount": horde_mount,
        "alliance_mount": alliance_mount,
    }

paths = []
for row in paths_meta[3]:
    paths.append({"id": row[0], "from": row[1], "to": row[2], "cost": row[3]})

used_node_ids = set(nodes)
used_path_ids = {p["id"] for p in paths}

print("TaxiNodes", nodes_meta[:3], "max", max(used_node_ids), "missing under 448", [i for i in range(1, 449) if i not in used_node_ids][:30])
print("TaxiPath", paths_meta[:3], "max", max(used_path_ids), "next", max(used_path_ids) + 1)
print("TaxiPathNode", pathnodes_meta[:3], "max row id", max(row[0] for row in pathnodes_meta[3]), "next", max(row[0] for row in pathnodes_meta[3]) + 1)

print("\nKalimdor Horde/neutral taxi nodes:")
for node in sorted(nodes.values(), key=lambda n: n["id"]):
    if node["map"] == 1 and node["horde_mount"] and node["horde_mount"] != 32981:
        print(f"{node['id']:3d} {node['name']:<45} ({node['x']:.1f}, {node['y']:.1f}, {node['z']:.1f}) mount={node['horde_mount']} ally={node['alliance_mount']}")

print("\nSample Kalimdor path costs:")
for p in sorted(paths, key=lambda p: p["id"]):
    a = nodes.get(p["from"])
    b = nodes.get(p["to"])
    if not a or not b or a["map"] != 1 or b["map"] != 1:
        continue
    d = math.dist((a["x"], a["y"], a["z"]), (b["x"], b["y"], b["z"]))
    if p["cost"]:
        print(f"{p['id']:4d} {p['from']:3d}->{p['to']:3d} {p['cost']:4d} {d:8.1f} {p['cost']/d:.4f} {a['name']} -> {b['name']}")
