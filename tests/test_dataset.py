import pathlib

HERE = pathlib.Path(__file__).parent.resolve()
DATASET_FILE = HERE.parent / "deck_pt_ua.txt"  # adjust path if needed

def load_dataset():
    lines = []
    with DATASET_FILE.open(encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):  # allow empty or commented lines
                continue
            lines.append((lineno, line))
    return lines


def test_dataset_is_parsable():
    for lineno, line in load_dataset():
        assert ":" in line, f"Line {lineno} has no ':' → {line}"

        left, right = [part.strip() for part in line.split(":", maxsplit=1)]

        assert left, f"Line {lineno} missing Portuguese word → {line}"
        assert right, f"Line {lineno} missing Ukrainian translation → {line}"

def test_no_duplicate_portuguese_words():
    seen = {}
    duplicates = {}
    for lineno, line in load_dataset():
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
