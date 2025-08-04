from pathlib import Path


def write_contents_to_file(path: Path, contents: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(contents)