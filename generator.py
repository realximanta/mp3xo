"""
generator.py — MP3X static HTML generator
Reads musics.txt, builds music-item HTML blocks, and injects them
into the <div id="musics">…</div> section of index.html.

musics.txt line format (pipe-separated, extensible):
    filename.mp3|Title
    filename.mp3|Title|TAG1|TAG2   ← future fields, safely ignored for now
"""

from pathlib import Path
import re
import sys


# ── Configuration ────────────────────────────────────────────────────────────

MUSICS_TXT  = Path("musics.txt")
INDEX_HTML  = Path("index.html")

# Regex that matches the entire <div id="musics">…</div> block (non-greedy,
# DOTALL so newlines are included).
MUSICS_DIV_RE = re.compile(
    r'(<div\s+id=["\']musics["\']>)(.*?)(</div>)',
    re.DOTALL,
)


# ── Parsing ───────────────────────────────────────────────────────────────────

def parse_music_line(line: str) -> dict | None:
    """
    Parse one line from musics.txt.

    Returns a dict with at minimum 'filename' and 'title'.
    Extra pipe-separated fields are stored in 'extras' list so
    future code can read them without touching this function.

    Returns None for blank or malformed lines.
    """
    line = line.strip()
    if not line:
        return None                     # blank line — skip silently

    parts = [p.strip() for p in line.split("|")]

    filename = parts[0] if len(parts) > 0 else ""
    title    = parts[1] if len(parts) > 1 else ""

    if not filename or not title:
        print(f"  [WARN] Skipping malformed line: {line!r}", file=sys.stderr)
        return None

    return {
        "filename": filename,
        "title":    title,
        "extras":   parts[2:],          # reserved for future fields
    }


def load_musics(path: Path) -> list[dict]:
    """Read and parse every valid line in musics.txt."""
    if not path.exists():
        sys.exit(f"[ERROR] {path} not found.")

    entries = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        entry = parse_music_line(raw_line)
        if entry:
            entries.append(entry)

    print(f"[INFO] Parsed {len(entries)} music entries from {path}.")
    return entries


# ── HTML generation ───────────────────────────────────────────────────────────

def build_music_block(entry: dict) -> str:
    """
    Render one <div class="music-item"> block for a single entry.

    The download attribute is kept so browsers that support it offer
    a Save dialog; browsers/phones that ignore it still follow the href.
    """
    filename = entry["filename"]
    title    = entry["title"]
    return (
        f'      <div class="music-item">\n'
        f'        <a href="{filename}" download>\n'
        f'          {title}\n'
        f'        </a>\n'
        f'      </div>'
    )


def build_musics_html(entries: list[dict]) -> str:
    """Join all music blocks with a blank line between them."""
    blocks = [build_music_block(e) for e in entries]
    return "\n\n".join(blocks)


# ── Injection ─────────────────────────────────────────────────────────────────

def inject_into_html(html: str, inner_html: str) -> str:
    """
    Replace the content inside <div id="musics">…</div>.
    Raises RuntimeError if the marker div is not found.
    """
    def replacer(m: re.Match) -> str:
        opening = m.group(1)   # <div id="musics">
        closing = m.group(3)   # </div>
        return f"{opening}\n\n{inner_html}\n\n    {closing}"

    new_html, count = MUSICS_DIV_RE.subn(replacer, html, count=1)
    if count == 0:
        raise RuntimeError(
            '[ERROR] Could not find <div id="musics"> in index.html. '
            "Make sure the id attribute uses double quotes or single quotes."
        )
    return new_html


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    # 1. Load music entries
    entries = load_musics(MUSICS_TXT)
    if not entries:
        sys.exit("[ERROR] No valid entries found in musics.txt. Aborting.")

    # 2. Read existing index.html
    if not INDEX_HTML.exists():
        sys.exit(f"[ERROR] {INDEX_HTML} not found.")
    original_html = INDEX_HTML.read_text(encoding="utf-8")

    # 3. Build inner HTML
    inner_html = build_musics_html(entries)

    # 4. Inject
    try:
        updated_html = inject_into_html(original_html, inner_html)
    except RuntimeError as exc:
        sys.exit(str(exc))

    # 5. Write only if content actually changed
    if updated_html == original_html:
        print("[INFO] index.html is already up to date. Nothing to write.")
        return

    INDEX_HTML.write_text(updated_html, encoding="utf-8")
    print(f"[INFO] index.html updated with {len(entries)} music entries.")


if __name__ == "__main__":
    main()
