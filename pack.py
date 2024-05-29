from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path, PureWindowsPath, PurePath

self_path = Path(__file__).resolve()
dir_path = self_path.parent
zip_path = dir_path / "Constellations.zip"

ignore = [
    "screenshots/",
    ".git/",
    "*.psd",
    "*.disabled",
    self_path.name,
    zip_path.name,
    ".gitignore"
]

def walk(path): 
    for p in path.iterdir(): 
        rel = p.relative_to(dir_path)
        if any(PureWindowsPath(rel).match(ign) for ign in ignore):
            continue

        if p.is_dir(): 
            yield from walk(p)
            continue
        yield rel

if zip_path.exists():
    zip_path.unlink(True)

with ZipFile(zip_path, "x", compression=ZIP_DEFLATED) as zip:
    prefix = PurePath("GameData/ContractPacks") / dir_path.name
    for path in walk(dir_path):
        print(prefix / path)
        zip.write(dir_path / path, prefix / path)
