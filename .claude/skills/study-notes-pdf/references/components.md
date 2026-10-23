# Component catalogue

Every class below is already styled in `assets/_head.html`. Copy these snippets
into lesson fragments. Pick the component that matches the *shape* of the
information, not the one that looks nicest: a definition goes in `.def`, two
things being contrasted go in `.card.vs` with `.cols`, a list of N things goes
in a list whose count is highlighted green.

## Lesson wrapper (one per lesson, starts a new page)
```html
<section class="lesson" id="l1">
<h2><span class="num">1</span>Chapter 1: Sources of Human Rights</h2>
<p class="lead">Three topics: (1) ..., (2) ..., (3) ...</p>
...
</section>
```
The `id` must match the lesson id in `project.json` (TOC link). A lesson that is
long can be split over files `02a_*.html` / `02b_*.html`: open `<section>` in
the first, close it in the last.

## Section heading inside a lesson
```html
<h3>Section 1: Rights related to personal safety</h3>
```

## Cards
```html
<div class="card intro"><h4>Overview</h4><ul>...</ul></div>   <!-- tinted, chapter opener -->
<div class="card"><h4>Right to life</h4>...</div>              <!-- normal -->
<div class="card wide">...</div>                               <!-- full width, outside .grid -->
<div class="grid"><div class="card">...</div><div class="card">...</div></div>  <!-- two short cards side by side -->
```
Put two cards in a `.grid` only when both are short and roughly equal height;
otherwise a tall card leaves a hole beside the short one. Long cards stand alone.

## Definition box
```html
<div class="def"><b>Torture:</b> any act causing <mark>severe pain or suffering, physical or mental</mark>, inflicted <mark>intentionally</mark> ...</div>
```

## Comparison (X vs Y): the most exam-useful component
```html
<div class="card vs">
<h4><mark class="p">Human rights × International humanitarian law</mark></h4>
<div class="cols">
<div><b>Human rights:</b> apply <mark>in peace and war</mark> ...</div>
<div><b>Humanitarian law:</b> applies <mark>only in armed conflict</mark> ...</div>
</div>
</div>
```
Use `.cols3` for three-way comparisons. A one-line contrast inside a normal card:
`<div class="vsline"><b>Difference:</b> ...</div>`.

## Tables: when items share the same attributes (≥3 items × ≥3 attributes)
```html
<table class="t small">
<tr><th>Committee</th><th>Treaty</th><th>Members</th><th>Main powers</th></tr>
<tr><td><b>1. CERD</b> <span class="ab">CERD</span></td><td>...</td><td><mark class="g">18</mark> members</td><td>...</td></tr>
</table>
```
`.ab` is a small pill for an abbreviation; it is always LTR so it works inside RTL text.
If the source does not give a value, write "(not stated)" / "(لم يُذكر)" instead of guessing.

## Short Q&A (exam mode)
```html
<div class="card qa">
<h4>Exam questions: Process management</h4>
<p class="q">Why does the kernel need a scheduler?</p>
<p class="a">To share <mark>one CPU</mark> among many processes → <mark>multitasking</mark>.</p>
</div>
```

## Lists
```html
<p><b>Five characteristics (<mark class="g">5</mark>):</b></p>
<ol class="tight"><li>...</li></ol>
```
A paragraph that introduces a list is kept with it automatically (CSS
`p:has(+ ul)`), so the label never ends a page alone.

## Highlight colours (`<mark>`)
| class | colour | use for |
|---|---|---|
| (none) | yellow | the key concept / keyword of a sentence |
| `g` | green | numbers, counts, ages, amounts, article numbers worth memorising |
| `p` | pink | distinctions, exceptions, "not", traps, precise wording |
| `b` | blue | examples |

Highlight the 2-5 words a student would underline, not whole sentences. If
everything is highlighted nothing is.
