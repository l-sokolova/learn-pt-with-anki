import pathlib
HERE = pathlib.Path(__file__).parent.resolve()
DATASET_FILE = HERE.parent / "deck_pt_ua.txt"  # adjust path if needed
OUTPUT_FILE = DATASET_FILE  # overwrite in place; change if you want separate file


def merge_translations(existing, new):
    """Merge translations into a comma-separated string without duplicates."""
    unique = []
    for t in (existing, new):
        for part in map(str.strip, t.split(",")):
            if part and part not in unique:
                unique.append(part)
    return ", ".join(unique)


def main():
    lines = DATASET_FILE.read_text(encoding="utf-8").splitlines()
    seen = {}
    to_remove = set()

    for idx, raw in enumerate(lines):
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue

        word, translation = [p.strip() for p in line.split(":", maxsplit=1)]

        if word in seen:
            first_idx, first_translation = seen[word]
            if translation == first_translation or translation in first_translation.split(","):
                # full duplicate → drop current line
                to_remove.add(idx)
            else:
                # merge different translations → update first line
                merged = merge_translations(first_translation, translation)
                lines[first_idx] = f"{word} : {merged}"
                seen[word] = (first_idx, merged)
                to_remove.add(idx)
        else:
            seen[word] = (idx, translation)

    # Rebuild file, skipping removed lines
    cleaned = [line for i, line in enumerate(lines) if i not in to_remove]

    OUTPUT_FILE.write_text("\n".join(cleaned) + "\n", encoding="utf-8")
    print(f"✅ Cleaned dataset written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()