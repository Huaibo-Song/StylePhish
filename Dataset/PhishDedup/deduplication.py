"""
dedupe_shots_by_sha256.py

Globally deduplicate based on the SHA-256 hash of shot.png:
- Scan all first-level subfolders under ./phish_sample_30k/
- Use multiple threads to calculate SHA-256 for each shot.png
- For files with exactly the same hash, keep the first one (sorted by folder name)
  and move the remaining entire subfolders to ./phishpedia_duplicate/<original_name>/
- Create ./phishpedia_duplicate/ if it does not exist; overwrite if the same name already exists
- Do not read info.txt and do not perform any URL-related processing
"""

import sys
import shutil
import hashlib
import concurrent.futures
from pathlib import Path

# ---- Dependency import and automatic installation protection ----
def ensure_package(pkg_name, import_name=None):
    try:
        __import__(import_name or pkg_name)
    except Exception:
        print(f"Missing dependency `{pkg_name}`, attempting installation...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])
        __import__(import_name or pkg_name)

ensure_package("tqdm")
from tqdm import tqdm

# ---- Configuration ----
SRC_ROOT = Path("./phish_sample_30k")
DUP_DIR  = Path("./phishpedia_duplicate")

# ---- SHA-256 ----
def sha256_of_file(path: Path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def process_folder(folder: Path):
    """Return (folder, hash_or_None); hash is None if shot.png is missing or cannot be read"""
    shot = folder / "shot.png"
    if not shot.is_file():
        return (folder, None)
    return (folder, sha256_of_file(shot))

# ---- Move duplicate subfolders ----
def move_to_dup(folder: Path) -> bool:
    dst = DUP_DIR / folder.name
    try:
        if dst.exists():
            shutil.rmtree(dst)   # overwrite
        shutil.move(str(folder), str(dst))
        return True
    except Exception as e:
        tqdm.write(f"[Failed] Move {folder.name}: {e}")
        return False

# ---- Main process ----
def main():
    if not SRC_ROOT.is_dir():
        print(f"Dataset directory does not exist: {SRC_ROOT.resolve()}")
        return

    DUP_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Dataset directory:   {SRC_ROOT.resolve()}")
    print(f"Duplicate directory: {DUP_DIR.resolve()}")

    subfolders = [p for p in SRC_ROOT.iterdir() if p.is_dir()]
    print(f"\nFound {len(subfolders)} subfolders, starting parallel SHA-256 calculation...\n")

    # Multi-threaded hash calculation
    results = []  # list[(folder, hash_or_None)]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_folder, f): f for f in subfolders}
        for fut in tqdm(concurrent.futures.as_completed(futures),
                        total=len(futures), desc="Calculating SHA-256", ncols=100):
            results.append(fut.result())

    # Sort by folder name to ensure the "first kept" folder is deterministic and reproducible
    results.sort(key=lambda x: x[0].name)

    no_shot = [f for f, h in results if h is None]
    valid   = [(f, h) for f, h in results if h is not None]
    print(f"\nValid shot.png: {len(valid)}, missing/read failed: {len(no_shot)}")

    if no_shot:
        for f in no_shot[:10]:
            print(f"  [Missing/broken shot.png] {f.name}")
        if len(no_shot) > 10:
            print(f"  ... {len(no_shot)} folders in total, remaining omitted")

    # ===== Global SHA-256 deduplication =====
    print("\n🔍 Global SHA-256 deduplication...\n")

    seen = {}              # hash -> first kept folder
    duplicates = []        # list[(folder, hash, kept_folder)]

    for folder, h in valid:
        if h in seen:
            duplicates.append((folder, h, seen[h]))
        else:
            seen[h] = folder

    print(f"Detected {len(duplicates)} duplicate folders, starting movement...\n")

    moved, failed = 0, 0

    for folder, h, kept in tqdm(duplicates, desc="Moving duplicates", ncols=100):
        if move_to_dup(folder):
            moved += 1
            tqdm.write(f"  [Moved] {folder.name}  ← duplicate of → {kept.name}")
        else:
            failed += 1

    # ===== Result statistics =====
    print("\n=== Processing Result ===")
    print(f"Total subfolders:          {len(subfolders)}")
    print(f"Missing/broken shot.png:   {len(no_shot)}")
    print(f"Unique kept:               {len(seen)}")
    print(f"Moved to phishpedia_duplicate: {moved}")
    print(f"Movement failed:           {failed}")

if __name__ == "__main__":
    main()
