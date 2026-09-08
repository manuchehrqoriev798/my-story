# Unfair to Everyone

A book by Manuchehr Qoriev, and the small amount of code that renders it as a
book: a two page spread you turn with the arrow keys.

Open `index.html` in any browser. No build step to read it, no dependencies,
no network required beyond the two web fonts.

## The loop

```
key-points.md  +  book/*.md   ->   python3 build.py   ->   index.html
```

That is the whole system. `build.py` is stdlib only Python: no pandoc, no
markdown package, no npm. Pagination is not computed here, it is done by the
browser with CSS multi-column, so long text splits across pages the way a
printed book does.

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
template.html    the book: typography, spread, page turning
key-points.md    Part One. THE FILE YOU EDIT
book/            Part Two and the front matter, one file per chapter
index.html       generated, committed so it works from a plain clone
sayings.txt      the raw source Part Two was built from
```

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
