# Source extraction quirks

## Arabic PDFs with broken text order
Some Arabic PDFs (often typeset with fonts like AL-Hotham, Traditional Arabic
or exported from InDesign) extract with swapped letter pairs, especially the
lam-alef ligature and the definite article. Read through it and write the
correct word; never copy the broken form into the notes.

| extracted | correct |
|---|---|
| احلقوق | الحقوق |
| اإلنسان | الإنسان |
| يف | في |
| ىلع / علي | على |
| إىل | إلى |
| اال / األ | الا / الأ (hamza on alef) |
| ـهلل | ـلله |

Clean-up approach that worked: run `pdftotext` without `-layout` too and
compare; apply obvious global replacements with a small script into a
`clean.txt`, then read the clean text in chunks of ~250 lines and fix the rest
by eye while writing. Check a couple of rendered pages of the source
(`pdftoppm -f N -l N -r 80 -png src.pdf page`) when a passage is unreadable.

## Scanned PDFs
If extract.py warns that there is almost no text, the PDF is scanned. OCR it
(`ocrmypdf -l ara+eng` or `tesseract`, see the pdf skill) before summarising, and
tell the user OCR may introduce errors.

## pptx lectures
- Speaker notes often contain the lecturer's own clarifications; they are
  extracted under `[notes]` and are authoritative over the slide text when they
  conflict. Mention conflicts to the user.
- Diagram-only slides extract as nothing. Render the slide
  (`soffice --headless --convert-to pdf` then `pdftoppm`) and look at it.

## Long sources (50+ pages)
Read in chunks and write each lesson fragment to disk as soon as that lesson
is done. That way a context compaction never loses finished work, and you
never need the whole book in context at once.
