# Unfair to Everyone

A book by Manuchehr Qoriev, and the small amount of code that renders it as a
book: a two page spread you turn with the arrow keys.

Open `index.html` in any browser. Drag a page corner to turn it, or use the
arrow keys. No build step to read it, no install, and no network needed
beyond the two web fonts.

## The loop

```
key-points.md  +  book/*.md                    ->  python3 build.py  ->  index.html
                                 +  inspiration/*.md                 ->  draft.html
```

Two outputs, and the split is deliberate:

| File | Contains | Fate |
|---|---|---|
| `index.html` | the book | committed, pushed, public |
| `draft.html` | the book **plus** everything in `inspiration/` | gitignored, never leaves the machine |

`inspiration/` is the workshop: raw stories, notes, half-thoughts, the sources
the book borrows shape from. It is gitignored too, so none of it is on GitHub.

There is no flag to remember and no build mode to get wrong. Private material
has nowhere to go except `draft.html`, so a half-written story cannot reach
the public book by accident. Drop any `.md` into `inspiration/` and it is
picked up by glob, no list to edit. See `inspiration/README.md`.

That is the whole system. `build.py` is stdlib only Python: no pandoc, no
markdown package, no npm.

The page turning is [StPageFlip](https://github.com/Nodlik/StPageFlip) (MIT,
zero dependencies, 44KB), vendored into `vendor/` rather than loaded from a
CDN so a clone keeps working offline and cannot break when a CDN changes.

StPageFlip needs discrete, equally sized page elements, so the text is
measured and broken into pages in `template.html` before the library ever
sees it. Blocks are flattened into atoms, poured into pages one at a time,
and any atom that will not fit is trimmed word by word with the remainder
carried to the next page, which keeps italics, links and drafting marks
intact across a break.

## The file you keep adding to

**`key-points.md`.** Every `## ` heading in it becomes a chapter of Part One.
Add one heading per real turning point, then run `python3 build.py`.

A turning point is a fork, not a year. If nothing looked different
afterwards, it is not a chapter, it is a date. The file carries the entry
template in a comment at the top.

## What is in the book now

| Part | State |
|---|---|
| Part One, The Life | **empty.** Waiting on `key-points.md` |
| Part Two, The Lessons | **written.** 9 chapters, built from 42 sayings collected from 13 people |
| The Sayings (appendix) | all 42, unedited, in the order they were written down |
| Part Three, The Open Ending | designed, not built. Interactive, LLM behind it |
| The Workshop (`draft.html` only) | seeded with the sources, waiting on your stories |

Part Two exists because the sayings were already written down. Part One does
not exist yet because the turning points were not. That asymmetry is the
whole current state of this project.

## Drafting marks

Text like `⟨this⟩` renders in the book as a visible orange mark. It is a gap
that only Manu can fill, left deliberately visible so that unwritten things
stay unwritten instead of quietly becoming invented ones. `build.py` counts
them on every run.

## Layout

```
build.py         markdown subset -> html. ~200 lines, stdlib only
template.html    the book: typography, paginator, page turning
vendor/          StPageFlip, vendored so the book works offline
key-points.md    Part One. THE FILE YOU EDIT
book/            Part Two and the front matter, one file per chapter
inspiration/     the workshop. Private, gitignored, draft.html only
index.html       generated, committed so it works from a plain clone
draft.html       generated, gitignored, the book plus the workshop
sayings.txt      the raw source Part Two was built from
```

Screenshots taken while checking the rendering go to `.playwright-mcp/`,
which is ignored.

Reading order lives in the `ORDER` list at the top of `build.py`. To add or
move a chapter, add a file to `book/` and put it in that list.

## Still open

- Title. *Unfair to Everyone* is taken from saying 1 and is a working title.
- Part One, entirely.
- Part Three: how many paths, what each represents, what the exercise is, and
  what the one thing every path converges to actually is. That last one is
  the real thesis of the book.

Design notes for Part Three live in `Me/Book.md` in the private vault, not
here.
