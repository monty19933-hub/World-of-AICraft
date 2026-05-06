import shutil
import sys
from pathlib import Path


WOW_EXE = Path(r"C:\Program Files (x86)\ChromieCraft_3.3.5a\Wow.exe")
BACKUP = WOW_EXE.with_name("Wow.exe.before-playable-races-gluexml.bak")

# 3.3.5a build 12340, file offset inside Wow.exe:
#   0F 85 2D FF FF FF    jne failed_gluexml_signature
# The preceding code compares the computed GlueXML signature against the signed
# value. NOPing only this conditional branch lets custom GlueXML load while
# leaving the rest of the client untouched.
PATCHES = [
    {
        "name": "GlueXML signature result switch bypass",
        "offset": 0xD9BE5,
        "original": bytes.fromhex("83 F8 03 77 34"),
        "patched": bytes.fromhex("E9 4B 00 00 00"),
    },
    {
        "name": "GlueXML final signature mismatch branch",
        "offset": 0xD9CEB,
        "original": bytes.fromhex("0F 85 2D FF FF FF"),
        "patched": bytes.fromhex("90 90 90 90 90 90"),
    },
]


def apply_patch():
    if not WOW_EXE.exists():
        raise FileNotFoundError(WOW_EXE)

    if not BACKUP.exists():
        shutil.copy2(WOW_EXE, BACKUP)
        print(f"Backed up {WOW_EXE} to {BACKUP}")

    data = bytearray(WOW_EXE.read_bytes())
    for patch in PATCHES:
        offset = patch["offset"]
        current = bytes(data[offset:offset + len(patch["original"])])
        if current == patch["patched"]:
            print(f"Already patched: {patch['name']}")
            continue
        if current != patch["original"]:
            raise RuntimeError(
                f"Unexpected bytes for {patch['name']} at 0x{offset:X}: "
                f"{current.hex(' ').upper()} expected {patch['original'].hex(' ').upper()}"
            )
        data[offset:offset + len(patch["patched"])] = patch["patched"]
        print(f"Patched: {patch['name']} at 0x{offset:X}")
    WOW_EXE.write_bytes(data)


def restore():
    if not BACKUP.exists():
        raise FileNotFoundError(f"Backup not found: {BACKUP}")
    shutil.copy2(BACKUP, WOW_EXE)
    print(f"Restored {WOW_EXE} from {BACKUP}")


def status():
    data = WOW_EXE.read_bytes()
    for patch in PATCHES:
        offset = patch["offset"]
        current = bytes(data[offset:offset + len(patch["original"])])
        if current == patch["patched"]:
            state = "patched"
        elif current == patch["original"]:
            state = "original"
        else:
            state = f"unexpected {current.hex(' ').upper()}"
        print(f"{patch['name']} at 0x{offset:X}: {state}")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "apply"
    if command == "apply":
        apply_patch()
    elif command == "restore":
        restore()
    elif command == "status":
        status()
    else:
        raise SystemExit("Usage: patch_wow_gluexml_signature.py [apply|restore|status]")
