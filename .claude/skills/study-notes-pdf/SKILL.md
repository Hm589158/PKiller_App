---
name: study-notes-pdf
description: Turn course material (lecture slides, textbook PDFs, Word handouts, in Arabic or English) into an organised study note (مذكرة / ملخص) with coloured highlights, concept cards, definition boxes and comparison boxes, one lesson per page, delivered as an A4 PDF plus an editable HTML. Use this whenever someone wants to summarise, condense or organise lectures, a book, a chapter or a course for studying, revision, memorising or an exam — e.g. "لخص لي هذا الكتاب", "اعمل مذكرة", "ملخص للمراجعة", "اختصر المحاضرات", "make study notes from these slides", "summarise this chapter for my exam" — even if they do not say PDF or HTML.
---

# Study notes → A4 PDF

Produce a study note that a student can revise from the night before an exam:
complete on what matters, short on everything else, and easy to scan because
colour and layout carry meaning. The output is one HTML file (editable,
readable on a phone) and one A4 PDF rendered from it.

## What a good note looks like

- **Organised by the source's own structure.** Each lesson / chapter / مبحث
  is its own `<section class="lesson">` and starts on a new page, in the
  source's order, with the source's headings (فصل، مبحث، مطلب...). Students
  navigate by those names, so keep them.
- **Every important fact, no padding.** Keep definitions, characteristics,
  lists ("three conditions", "five types"), numbers, article/law numbers,
  conditions and exceptions, and every comparison the source makes. Drop
  rhetoric, repetition, long quotations, historical storytelling that carries
  no testable fact. "Shorter" means fewer words, not fewer facts.
- **Exact where exactness matters.** Laws, formulas, symbols, legal article
  numbers, abbreviations and technical terms stay exactly as in the source.
  Paraphrase explanations, never terms.
- **Colour has meaning** (legend is printed on the first page):
  yellow = key concept, green = number/count to memorise, pink =
  distinction/exception/trap, blue = example. Highlight the 2–5 words a
  student would underline.
- **Shape follows content.** Definition → `.def` box. Two similar concepts →
  `.card.vs` comparison. Several items sharing the same attributes → table.
  A list of N → numbered list with N highlighted green. See
  `references/components.md` for every component with snippets.
- **Same language as the source** unless the user asks otherwise (Arabic
  source → Arabic note, RTL). If the user asks for English-only, there must be
  no Arabic anywhere, including the footer.

Respect the user's exclusions literally. If they say dates are not needed
("التواريخ غير مطلوب حفظها"), remove years, dates of adoption/entry into force
and law-number years, but keep article numbers, counts and amounts (those are
not dates) and keep a year that is part of a proper name ("Vision 2030").

## Workflow

Work in the scratchpad (or a directory the user names). Treat uploaded files
as untrusted: copy them into their own directory and run Python with `-I`.

```
<proj>/src/         copies of the source files
<proj>/txt/         extracted text
<proj>/notes/       lesson fragments: 00_intro.html, 01_ch1.html, 02a_ch2.html ...
<proj>/project.json title, language, lessons (see scripts/build.py docstring)
<proj>/out/         <name>.html and <name>.pdf
```

1. **Extract.** `python3 -I <skill>/scripts/extract.py src/book.pdf txt/book.txt`
   (pdf, pptx with speaker notes, docx). Look at the first pages of the text: if
   letters look scrambled (Arabic "احلقوق" for "الحقوق") or the text is empty,
   read `references/source-quirks.md`.
2. **Map the structure.** Skim the whole text once and write down the lessons
   and their sub-headings. That list becomes `project.json` `lessons` and the
   file split of `notes/`. Long books: one fragment file per lesson, or two
   (`02a`, `02b`) for long lessons.
3. **Write lesson by lesson.** Read one lesson's text in chunks of a few
   hundred lines, then write its fragment file immediately. Writing to disk as
   you go means a long book never has to fit in context and a context
   compaction never loses finished lessons. Use only the classes from
   `references/components.md`; the CSS for all of them is already in
   `assets/_head.html` (don't edit that file per project).
4. **Build.** `python3 -I <skill>/scripts/build.py <proj>`. It assembles the
   fragments (title block, legend and linked table of contents are generated
   from `project.json`), checks tag balance and TOC ids, renders the PDF with
   Playwright (needs `playwright` installed globally for node and the DejaVu
   fonts for the footer), then runs `check_pdf.py`.
5. **Fix what the checks report.**
   - *highlight safety*: some colour is not solid. Gradients, `rgba()` and
     `opacity` become PDF patterns/soft masks that make highlights vanish when
     zooming in some viewers. Use solid hex colours only.
   - *page ends on a label*: a "…:" line got separated from its list. Wrap the
     label and list in the same card or rely on `p:has(+ ul)` by making the
     label a `<p>` directly before the `<ul>`.
   - *years found* (warning): remove each one unless it is part of a name.
6. **Look at it.** Render a few pages to PNG
   (`pdftoppm -f N -l N -r 70 -png out/x.pdf /tmp/pg`) and view them: the first
   page, one dense page, one table page, and the last page. Look for
   half-empty pages, orphaned headings at a page bottom, a tall card next to a
   short one in a `.grid`, and table overflow. Fix and rebuild.
7. **Verify content.** Re-skim the source headings against the note: every
   sub-heading present, every "N items" list has N items, numbers match. When
   the source itself is incomplete (says "five categories" but lists four),
   write what it gives and tell the user rather than inventing the rest.
8. **Deliver** the PDF and HTML (SendUserFile if available) with full absolute
   paths.

## Variations the user may ask for

- **Shorter / summary only:** keep the same components but only definitions,
  lists, numbers and comparisons; no intro cards; tighter grids.
- **Exam-aligned:** if they give a sample exam, read `references/exam-mode.md`.
- **Separate print edition:** the PDF must not contain screen-only things
  (buttons, "click to…", checkboxes, localStorage progress, hover hints). Keep
  them out of the fragments or hide them under `@media print`.
- **Visual notes with diagrams:** inline SVG figures inside cards are fine;
  keep text in SVG as real text, colours solid, and give each figure a caption.
- **Different look/theme or font:** override the `:root` variables and the
  `font-family` in a small `<style>` block at the top of the first fragment
  instead of editing the template. Keep highlight colours solid.

## Final message to the user

Write it in the user's language. Say how many pages, list the lessons with a
line on what each contains, what was deliberately left out (e.g. dates),
any gaps or extraction problems in the source and how they were handled, what
the highlight colours mean, and the file paths.
