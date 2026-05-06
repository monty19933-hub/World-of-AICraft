import struct
from pathlib import Path

from build_razorhill_flightpath import CRYPT_TABLE, CLIENT_PATCH, mpq_hash, mpq_encrypt_words


def decrypt_words(data: bytes, key: int):
    seed = 0xEEEEEEEE
    words = []
    for index in range(0, len(data), 4):
        encrypted = struct.unpack_from("<I", data, index)[0]
        seed = (seed + CRYPT_TABLE[0x400 + (key & 0xFF)]) & 0xFFFFFFFF
        word = (encrypted ^ ((key + seed) & 0xFFFFFFFF)) & 0xFFFFFFFF
        key = (((~key << 21) & 0xFFFFFFFF) + 0x11111111 | (key >> 11)) & 0xFFFFFFFF
        seed = (word + seed + ((seed << 5) & 0xFFFFFFFF) + 3) & 0xFFFFFFFF
        words.append(word)
    return words


def read_mpq(path: Path):
    data = path.read_bytes()
    magic, header_size, archive_size, version, block_shift, hash_pos, block_pos, hash_size, block_size = struct.unpack_from("<4sIIHHIIII", data, 0)
    if magic != b"MPQ\x1A":
        raise ValueError("Not an MPQ archive")
    block_words = decrypt_words(data[block_pos:block_pos + block_size * 16], mpq_hash("(block table)", 3))
    hash_words = decrypt_words(data[hash_pos:hash_pos + hash_size * 16], mpq_hash("(hash table)", 3))
    blocks = [tuple(block_words[i:i + 4]) for i in range(0, len(block_words), 4)]
    hashes = [tuple(hash_words[i:i + 4]) for i in range(0, len(hash_words), 4)]
    return data, blocks, hashes, hash_size


def extract(path: Path, name: str) -> bytes:
    data, blocks, hashes, hash_size = read_mpq(path)
    slot = mpq_hash(name, 0) % hash_size
    h1 = mpq_hash(name, 1)
    h2 = mpq_hash(name, 2)
    for _ in range(hash_size):
        entry = hashes[slot]
        if entry[3] == 0xFFFFFFFF:
            break
        if entry[0] == h1 and entry[1] == h2:
            file_pos, compressed_size, file_size, flags = blocks[entry[3]]
            payload = data[file_pos:file_pos + compressed_size]
            if len(payload) != file_size:
                raise ValueError(f"{name}: size mismatch")
            return payload
        slot = (slot + 1) % hash_size
    raise KeyError(name)


def dbc_header(blob: bytes):
    return struct.unpack_from("<4sIIII", blob, 0)


def main():
    for name in ["DBFilesClient\\TaxiNodes.dbc", "DBFilesClient\\TaxiPath.dbc", "DBFilesClient\\TaxiPathNode.dbc", "(listfile)"]:
        blob = extract(CLIENT_PATCH, name)
        if name.endswith(".dbc"):
            magic, records, fields, record_size, string_size = dbc_header(blob)
            print(f"{name}: {magic.decode()} records={records} fields={fields} record_size={record_size} strings={string_size}")
        else:
            print(f"{name}: {blob.decode('utf-8').strip()}")


if __name__ == "__main__":
    main()
