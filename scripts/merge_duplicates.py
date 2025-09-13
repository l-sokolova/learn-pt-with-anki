import pathlib
HERE = pathlib.Path(__file__).parent.resolve()
DATASET_FILE = HERE.parent / "deck_pt_ua.txt"  # adjust path if needed
OUTPUT_FILE = DATASET_FILE  # overwrite in place; change if you want separate file


def merge_translations(translations):
    """Merge multiple translations into one string, removing duplicates."""
    unique = []
    for t in translations:
        for part in map(str.strip, t.split(",")):
            if part and part not in unique:
                unique.append(part)
    return ", ".join(unique)


def main():
    words = {}
    for lineno, raw in enumerate(DATASET_FILE.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            print(f"⚠️ Skipping unparsable line {lineno}: {line}")
            continue

        word, translation = [p.strip() for p in line.split(":", maxsplit=1)]

        if not word or not translation:
            print(f"⚠️ Skipping invalid line {lineno}: {line}")
            continue

        words.setdefault(word, []).append(translation)

    cleaned = []
    for word, translations in words.items():
        merged = merge_translations(translations)
        cleaned.append(f"{word} : {merged}")

    # sort by Portuguese word for consistency
    cleaned.sort(key=lambda l: l.split(":", 1)[0].strip())

    OUTPUT_FILE.write_text("\n".join(cleaned) + "\n", encoding="utf-8")
    print(f"✅ Cleaned dataset written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
