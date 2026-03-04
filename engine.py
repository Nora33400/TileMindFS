import hashlib
import json
import os
import zlib
from typing import Any

DATA_DIR = "data"
TILE_DIR = os.path.join(DATA_DIR, "tiles")
MANIFEST = os.path.join(DATA_DIR, "manifest.json")


class TileStore:
    """Simple tile-based storage with deduplication and reconstruction."""

    def __init__(self) -> None:
        os.makedirs(TILE_DIR, exist_ok=True)
        if not os.path.exists(MANIFEST):
            self._save_manifest({})

    def _hash(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _load_manifest(self) -> dict[str, Any]:
        with open(MANIFEST, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def _save_manifest(self, manifest: dict[str, Any]) -> None:
        with open(MANIFEST, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2)

    def store_file(self, filepath: str) -> str:
        with open(filepath, "rb") as fh:
            data = fh.read()

        tile_hash = self._hash(data)
        tile_path = os.path.join(TILE_DIR, tile_hash)

        if not os.path.exists(tile_path):
            compressed = zlib.compress(data)
            with open(tile_path, "wb") as tile_fh:
                tile_fh.write(compressed)

        manifest = self._load_manifest()
        manifest[filepath] = [tile_hash]
        self._save_manifest(manifest)

        return f"Stored {filepath} in 1 tile."

    def reconstruct_file(self, original: str, output: str) -> str:
        manifest = self._load_manifest()

        if original not in manifest:
            raise KeyError("File not found in manifest")

        tile_hash = manifest[original][0]
        tile_path = os.path.join(TILE_DIR, tile_hash)

        with open(tile_path, "rb") as tile_fh:
            compressed = tile_fh.read()

        data = zlib.decompress(compressed)

        with open(output, "wb") as out_fh:
            out_fh.write(data)

        return f"Reconstructed {original} -> {output}"

    def report(self) -> str:
        manifest = self._load_manifest()
        files = len(manifest)
        unique_tiles = len(os.listdir(TILE_DIR))
        return f"Files tracked: {files}\nUnique tiles: {unique_tiles}"
