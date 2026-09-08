#!/usr/bin/env python3
"""Build the book: markdown sources -> one self-contained index.html.

Stdlib only. No pandoc, no markdown package, no npm. Run: python3 build.py

Pagination is done by the browser with CSS multi-column, not here. This script
only turns markdown into semantic HTML and drops it into the template.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BOOK = ROOT / "book"
OUT = ROOT / "index.html"

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

# ---------------------------------------------------------------- inline

SLOT = re.compile(r"⟨(.+?)⟩")
BOLD = re.compile(r"\*\*(.+?)\*\*")
ITAL = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
LINK = re.compile(r"\[(.+?)\]\((.+?)\)")


def inline(text):
    out = html.escape(text.strip())
    out = LINK.sub(r'<a href="\2">\1</a>', out)
    out = BOLD.sub(r"<strong>\1</strong>", out)
    out = ITAL.sub(r"<em>\1</em>", out)
    # ⟨...⟩ marks a gap only Manu can fill. Visible on purpose.
    out = SLOT.sub(r'<span class="slot">\1</span>', out)
    return out


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


def main():
    parts, missing, chapters = [], [], []
    for path in ORDER:
        if not path.exists():
            missing.append(path.name)
            continue
        cls, body = render(path.read_text(encoding="utf-8"))
        parts.append(f'<section class="{cls}" data-src="{path.name}">\n{body}\n</section>')
        chapters += re.findall(r"<h2>(.*?)</h2>", body)

    if missing:
        print("missing source files: " + ", ".join(missing), file=sys.stderr)

    template = (ROOT / "template.html").read_text(encoding="utf-8")
    out = template.replace("<!--BOOK-->", "\n\n".join(parts))
    OUT.write_text(out, encoding="utf-8")

    words = len(re.sub(r"<[^>]+>", " ", "\n".join(parts)).split())
    slots = out.count('class="slot"')
    print(f"built {OUT.name}: {len(parts)} sections, {len(chapters)} chapters, "
          f"{words} words, {slots} unfilled slots")
    for c in chapters:
        print("  - " + re.sub(r"<[^>]+>", "", c))


if __name__ == "__main__":
    main()
