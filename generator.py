from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path


# ── Configuration ─────────────────────────────────────────────────────────────

REPO_ROOT  = Path(".")
INDEX_HTML = Path("index.html")

# Matches the entire <div id="musics">…</div> block (non-greedy, DOTALL).
MUSICS_DIV_RE = re.compile(
    r'(<div\s+id=["\']musics["\']>)(.*?)(</div>)',
    re.DOTALL,
)

# Matches one bracketed tag at the start of a stem: [NEW], [SPECIAL], etc.
TAG_RE = re.compile(r'^\[([A-Z0-9_]+)\]')


# ── File discovery ────────────────────────────────────────────────────────────

def git_commit_time(path: Path) -> int:
    """
    Return the Unix timestamp of the most recent git commit that touched
    this file.  Falls back to the filesystem mtime if git is unavailable
    or the file is untracked (new, not yet committed).
    """
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", str(path)],
            capture_output=True,
            text=True,
            check=True,
        )
        ts = result.stdout.strip()
        if ts:
            return int(ts)
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        pass
    # Fallback: filesystem modification time
    return int(path.stat().st_mtime)


def discover_mp3s(root: Path) -> list[Path]:
    """
    Return all *.mp3 files in root (non-recursive, non-hidden),
    sorted newest-first by git commit timestamp.
    """
    files = [
        p for p in root.iterdir()
        if p.is_file()
        and p.suffix.lower() == ".mp3"
        and not p.name.startswith(".")
    ]
    # Sort descending (newest first); use filename as tiebreaker for
    # deterministic output when two files share the same timestamp.
    files.sort(key=lambda p: (-git_commit_time(p), p.name.lower()))
    return files


# ── Filename parsing ──────────────────────────────────────────────────────────

def parse_tags(stem: str) -> tuple[list[str], str]:
    """
    Extract zero or more leading [TAG] prefixes from a filename stem.

    Returns (tags, remainder) where remainder is the stem with all
    tag prefixes removed.

    Examples
    ────────
    "Billie-Jean"            → ([], "Billie-Jean")
    "[NEW]-Cool-Song"        → (["NEW"], "Cool-Song")
    "[NEW][SPECIAL]-Another" → (["NEW", "SPECIAL"], "Another")
    """
    tags: list[str] = []
    while True:
        m = TAG_RE.match(stem)
        if not m:
            break
        tags.append(m.group(1))
        stem = stem[m.end():]           # consume matched tag
        stem = stem.lstrip("-")         # strip leading separator
    return tags, stem


def stem_to_title(stem: str) -> str:
    """
    Convert a filename stem (tags already removed) to a human-readable title.

    Rules:
      1. Replace hyphens with spaces.
      2. Collapse any run of whitespace to a single space.
      3. Strip leading/trailing whitespace.
      4. Apply Title Case.
      5. Preserve digits as-is (title() handles this correctly).
    """
    title = stem.replace("-", " ")
    title = re.sub(r"\s+", " ", title).strip()
    return title.title()


def build_entry(path: Path) -> dict:
    """
    Build a structured metadata dict for one MP3 file.

    Schema
    ──────
    {
        "filename": "Billie-Jean.mp3",   # original filename, URL-safe
        "title":    "Billie Jean",       # human-readable display title
        "tags":     ["NEW"],             # list of bracketed tag strings (may be empty)
        "path":     Path(...),           # Path object for internal use
    }

    The "tags" field is intentionally kept separate from "title" so
    future rendering code can act on e.g. tags=["NEW"] without touching
    the title or filename logic.
    """
    stem = path.stem                    # filename minus extension
    tags, remainder = parse_tags(stem)
    title = stem_to_title(remainder)

    return {
        "filename": path.name,
        "title":    title,
        "tags":     tags,
        "path":     path,
    }


def load_entries(root: Path) -> list[dict]:
    """Discover MP3s and return a list of entry dicts, newest first."""
    mp3_paths = discover_mp3s(root)
    entries = [build_entry(p) for p in mp3_paths]
    print(f"[INFO] Found {len(entries)} MP3 file(s) in {root.resolve()}.")
    return entries


# ── HTML generation ───────────────────────────────────────────────────────────

def build_music_block(entry: dict) -> str:
    """
    Render one <div class="music-item"> block.

    Both the href attribute value and the visible title are HTML-escaped
    so filenames with ampersands, quotes, or angle brackets can't break
    the page structure.
    """
    safe_href  = html.escape(entry["filename"], quote=True)
    safe_title = html.escape(entry["title"])
    return (
        f'      <div class="music-item">\n'
        f'        <a href="{safe_href}" download>\n'
        f'          {safe_title}\n'
        f'        </a>\n'
        f'      </div>'
    )


def build_empty_block() -> str:
    """Fallback block shown when the repository contains no MP3 files."""
    return '      <p class="no-music">No music available.</p>'


def build_musics_html(entries: list[dict]) -> str:
    """
    Join all music blocks with a blank line separator.
    Returns a fallback message block if the list is empty.
    """
    if not entries:
        return build_empty_block()
    blocks = [build_music_block(e) for e in entries]
    return "\n\n".join(blocks)


# ── HTML injection ────────────────────────────────────────────────────────────

def inject_into_html(original: str, inner_html: str) -> str:
    """
    Replace only the content inside <div id="musics">…</div>.
    Everything outside that div is preserved byte-for-byte.

    Raises RuntimeError if the marker div is not present.
    """
    def replacer(m: re.Match) -> str:
        opening = m.group(1)    # <div id="musics">
        closing = m.group(3)    # </div>
        return f"{opening}\n\n{inner_html}\n\n    {closing}"

    updated, count = MUSICS_DIV_RE.subn(replacer, original, count=1)
    if count == 0:
        raise RuntimeError(
            '[ERROR] <div id="musics"> not found in index.html. '
            "Ensure the id attribute is present and uses straight quotes."
        )
    return updated


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    # 1. Discover and parse MP3 files
    entries = load_entries(REPO_ROOT)

    # 2. Read index.html
    if not INDEX_HTML.exists():
        sys.exit(f"[ERROR] {INDEX_HTML} not found.")
    original_html = INDEX_HTML.read_text(encoding="utf-8")

    # 3. Build inner HTML
    inner_html = build_musics_html(entries)

    # 4. Inject into index.html
    try:
        updated_html = inject_into_html(original_html, inner_html)
    except RuntimeError as exc:
        sys.exit(str(exc))

    # 5. Write only if something actually changed (keeps git diff clean)
    if updated_html == original_html:
        print("[INFO] index.html is already up to date. Nothing written.")
        return

    INDEX_HTML.write_text(updated_html, encoding="utf-8")
    print(f"[INFO] index.html updated with {len(entries)} music entry/entries.")


if __name__ == "__main__":
    main()
