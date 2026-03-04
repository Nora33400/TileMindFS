import json
from pathlib import Path

import pytest

import engine


@pytest.fixture
def isolated_store(monkeypatch, tmp_path: Path):
    data_dir = tmp_path / "data"
    tile_dir = data_dir / "tiles"
    manifest = data_dir / "manifest.json"

    monkeypatch.setattr(engine, "DATA_DIR", str(data_dir))
    monkeypatch.setattr(engine, "TILE_DIR", str(tile_dir))
    monkeypatch.setattr(engine, "MANIFEST", str(manifest))

    store = engine.TileStore()
    return store, manifest, tile_dir


def test_store_file_initializes_manifest_and_tile(isolated_store, tmp_path: Path):
    store, manifest_path, tile_dir = isolated_store
    src = tmp_path / "a.txt"
    src.write_bytes(b"hello-tiles")

    msg = store.store_file(str(src))

    assert msg == f"Stored {src} in 1 tile."
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert str(src) in manifest
    assert len(manifest[str(src)]) == 1
    assert len(list(tile_dir.iterdir())) == 1


def test_store_file_deduplicates_identical_content(isolated_store, tmp_path: Path):
    store, _manifest_path, tile_dir = isolated_store
    a = tmp_path / "a.bin"
    b = tmp_path / "b.bin"
    payload = b"same-content"
    a.write_bytes(payload)
    b.write_bytes(payload)

    store.store_file(str(a))
    store.store_file(str(b))

    assert len(list(tile_dir.iterdir())) == 1


def test_reconstruct_file_restores_original_content(isolated_store, tmp_path: Path):
    store, _manifest_path, _tile_dir = isolated_store
    src = tmp_path / "orig.txt"
    out = tmp_path / "restored.txt"
    content = b"tilemindfs-reconstruct-check"
    src.write_bytes(content)

    store.store_file(str(src))
    msg = store.reconstruct_file(str(src), str(out))

    assert msg == f"Reconstructed {src} -> {out}"
    assert out.read_bytes() == content


def test_reconstruct_missing_entry_raises_keyerror(isolated_store, tmp_path: Path):
    store, _manifest_path, _tile_dir = isolated_store

    with pytest.raises(KeyError):
        store.reconstruct_file("missing-file.txt", str(tmp_path / "out.txt"))


def test_report_counts_files_and_unique_tiles(isolated_store, tmp_path: Path):
    store, _manifest_path, _tile_dir = isolated_store
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_bytes(b"same")
    b.write_bytes(b"same")

    store.store_file(str(a))
    store.store_file(str(b))

    report = store.report()
    assert "Files tracked: 2" in report
    assert "Unique tiles: 1" in report
