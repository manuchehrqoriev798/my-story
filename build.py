#!/usr/bin/env python3
"""Build the book. Run: python3 build.py

Two outputs, on purpose:

    index.html   the book. Committed, pushed, public.
    draft.html   the book PLUS everything in inspiration/. Never committed.

The split exists so a half-written story cannot reach the public book by
accident. There is no flag to remember and no build mode to get wrong: the
private material has nowhere to go except draft.html.

Stdlib only. No pandoc, no markdown package, no npm. Pagination happens in the
browser, see template.html. This script only turns markdown into semantic HTML.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BOOK = ROOT / "book"
INSPIRATION = ROOT / "inspiration"
OUT = ROOT / "index.html"
DRAFT = ROOT / "draft.html"

# Reading order. key-points.md sits inside Part One on purpose: it is the file
# you keep appending to, and every `## ` heading in it becomes a chapter.
ORDER = [
    BOOK / "00-title.md",
    BOOK / "01-part-one.md",
    ROOT / "key-points.md",
    BOOK / "02-part-two.md",
    BOOK / "03-unfair.md",
    BOOK / "04-choosing.md",
    BOOK / "05-knowing-yourself.md",
    BOOK / "06-patience.md",
    BOOK / "07-people.md",
    BOOK / "08-discipline.md",
    BOOK / "09-failure.md",
    BOOK / "10-name-and-time.md",
    BOOK / "11-tools.md",
    BOOK / "12-part-three.md",
    BOOK / "90-sayings.md",
]

# Everything in inspiration/ is picked up by glob, sorted by filename, so a new
# file needs no edit here. README.md is documentation, not book material.
WORKSHOP_DIVIDER = """%%part-page%%

# The Workshop

## Raw Material

*Not the book. Not published. Yours.*

Everything past this page is unfinished on purpose: stories before they are
chapters, lines before they have anywhere to sit, the things this book is
being built out of.

None of it exists in `index.html`, and none of it is on GitHub.
"""


def workshop_files():
    if not INSPIRATION.is_dir():
        return []
    return sorted(
        f for f in INSPIRATION.glob("*.md") if f.name.lower() != "readme.md"
    )

# ---------------------------------------------------------------- inline

SLOT = re.compile(r"⟨(.+?)⟩")
BOLD = re.compile(r"\*\*(.+?)\*\*")
ITAL = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
LINK = re.compile(r"\[(.+?)\]\((.+?)\)")
CODE = re.compile(r"`([^`]+)`")
STASH = re.compile(r"\x00(\d+)\x00")


def inline(text):
    out = html.escape(text.strip())

    # Pull `code` out first and leave a marker. Without this, a * or _ inside a
    # file name would be read as emphasis and the backticks would survive into
    # the page as literal characters.
    spans = []

    def stash(m):
        spans.append(m.group(1))
        return "\x00%d\x00" % (len(spans) - 1)

    out = CODE.sub(stash, out)
    out = LINK.sub(r'<a href="\2">\1</a>', out)
    out = BOLD.sub(r"<strong>\1</strong>", out)
    out = ITAL.sub(r"<em>\1</em>", out)
    # ⟨...⟩ marks a gap only Manu can fill. Visible on purpose.
    out = SLOT.sub(r'<span class="slot">\1</span>', out)
    return STASH.sub(lambda m: "<code>" + spans[int(m.group(1))] + "</code>", out)


# ---------------------------------------------------------------- blocks


def render(md):
    """Markdown subset -> HTML. Blocks are separated by blank lines."""
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)  # guidance comments never render
    lines = md.replace("\r\n", "\n").split("\n")

    # strip YAML front matter
    if lines and lines[0].strip() == "---":
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
        if end is not None:
            lines = lines[end + 1 :]

    # a `%%class%%` directive on the first non-blank line sets the section class
    section_class = "chapter"
    for i, l in enumerate(lines):
        if not l.strip():
            continue
        m = re.fullmatch(r"%%([a-z-]+)%%", l.strip())
        if m:
            section_class = m.group(1)
            lines = lines[i + 1 :]
        break

    out, buf, mode = [], [], None

    def flush():
        nonlocal buf, mode
        if not buf:
            mode = None
            return
        if mode == "p":
            out.append("<p>" + inline(" ".join(buf)) + "</p>")
        elif mode == "quote":
            # a bare ">" is a paragraph break inside the quote, not content
            paras, cur, cite = [], [], None
            for b in buf:
                if b.startswith("— "):
                    cite = b[2:]
                elif not b.strip():
                    if cur:
                        paras.append(" ".join(cur))
                        cur = []
                else:
                    cur.append(b)
            if cur:
                paras.append(" ".join(cur))
            q = "<blockquote>" + "".join(
                "<p>" + inline(x) + "</p>" for x in paras)
            if cite:
                q += "<cite>" + inline(cite) + "</cite>"
            out.append(q + "</blockquote>")
        elif mode in ("ul", "ol"):
            items = "".join("<li>" + inline(b) + "</li>" for b in buf)
            out.append(f"<{mode}>{items}</{mode}>")
        buf, mode = [], None

    for raw in lines:
        line = raw.rstrip()
        s = line.strip()

        if not s:
            flush()
            continue
        if s == "---":
            flush()
            out.append('<hr class="rule">')
            continue

        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            flush()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            continue

        if s.startswith(">"):
            if mode != "quote":
                flush()
                mode = "quote"
            buf.append(s[2:] if s.startswith("> ") else "")
            continue

        m = re.match(r"^[-*]\s+(.*)$", s)
        if m:
            if mode != "ul":
                flush()
                mode = "ul"
            buf.append(m.group(1))
            continue

        m = re.match(r"^\d+[.)]\s+(.*)$", s)
        if m:
            if mode != "ol":
                flush()
                mode = "ol"
            buf.append(m.group(1))
            continue

        if mode not in ("p",):
            flush()
            mode = "p"
        buf.append(s)

    flush()
    return section_class, "\n".join(out)


# ---------------------------------------------------------------- build


def section(cls, body, name):
    return f'<section class="{cls}" data-src="{name}">\n{body}\n</section>'


def collect(paths):
    """Render each file to a <section>. Returns (sections, chapter titles)."""
    sections, chapters, missing = [], [], []
    for path in paths:
        if not path.exists():
            missing.append(path.name)
            continue
        cls, body = render(path.read_text(encoding="utf-8"))
        sections.append(section(cls, body, path.name))
        chapters += [
            re.sub(r"<[^>]+>", "", c) for c in re.findall(r"<h2>(.*?)</h2>", body)
        ]
    if missing:
        print("missing source files: " + ", ".join(missing), file=sys.stderr)
    return sections, chapters


def write(target, sections, template):
    target.write_text(
        template.replace("<!--BOOK-->", "\n\n".join(sections)), encoding="utf-8"
    )
    words = len(re.sub(r"<[^>]+>", " ", "\n".join(sections)).split())
    slots = sum(sec.count('class="slot"') for sec in sections)
    return words, slots


def main():
    template = (ROOT / "template.html").read_text(encoding="utf-8")

    book, chapters = collect(ORDER)
    words, slots = write(OUT, book, template)
    print(f"{OUT.name:12} {len(book):3} sections  {len(chapters):3} chapters  "
          f"{words:5} words  {slots:2} unfilled slots   (public, committed)")
    for c in chapters:
        print("    - " + c)

    raw = workshop_files()
    if not raw:
        print(f"\n{'inspiration/':12} empty or absent, so no {DRAFT.name} written.")
        return
    cls, body = render(WORKSHOP_DIVIDER)
    shop, shop_chapters = collect(raw)
    shop = [section(cls, body, "workshop")] + shop
    dwords, dslots = write(DRAFT, book + shop, template)
    print(f"\n{DRAFT.name:12} {len(book)+len(shop):3} sections  "
          f"{len(chapters)+len(shop_chapters):3} chapters  {dwords:5} words  "
          f"{dslots:2} unfilled slots   (private, never committed)")
    for c in shop_chapters:
        print("    + " + c)
    print(f"    from: " + ", ".join(f.name for f in raw))


if __name__ == "__main__":
    main()
