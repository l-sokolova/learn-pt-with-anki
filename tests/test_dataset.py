import os
import pathlib

HERE = pathlib.Path(__file__).parent.resolve()
DATASET_FOLDER = HERE.parent / "decks"  # adjust path if needed


def load_dataset(dataset_path):
    lines = []
    with dataset_path.open(encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):  # allow empty or commented lines
                continue
            lines.append((lineno, line))
    return lines


def test_dataset_is_parsable():
    for file in DATASET_FOLDER.iterdir():
        for lineno, line in load_dataset(file):
            assert ":" in line, f"Line {lineno} has no ':' → {line}"

            left, right = [part.strip() for part in line.split(":", maxsplit=1)]

            assert left, f"Line {lineno} missing Portuguese word → {line}"
            assert right, f"Line {lineno} missing Ukrainian translation → {line}"


def test_no_duplicate_portuguese_words():
    for file in DATASET_FOLDER.iterdir():
        seen = {}
        duplicates = {}
        for lineno, line in load_dataset(pathlib.Path(file)):
            word, _ = [part.strip() for part in line.split(":", maxsplit=1)]
            if word in seen:
                duplicates.setdefault(word, []).append(lineno)
            else:
                seen[word] = lineno

        if duplicates:
            messages = [
                f"'{word}' first at line {seen[word]}, also at lines {', '.join(map(str, lines))}"
                for word, lines in duplicates.items()
            ]
            raise AssertionError("Duplicate Portuguese words found:\n" + "\n".join(messages))


def test_only_one_colon_per_line():
    for file in DATASET_FOLDER.iterdir():
        for lineno, line in load_dataset(file):
            colon_count = line.count(":")
            assert colon_count == 1, (
                f"Line {lineno} has {colon_count} ':' characters, "
                f"but exactly one is required → {line}"
            )

