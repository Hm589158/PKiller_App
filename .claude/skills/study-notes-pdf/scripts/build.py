"""Assemble lesson fragments into one HTML file and render it to an A4 PDF.

Usage: python3 -I build.py <project_dir>

<project_dir>/project.json:
{
  "name": "HR_Notes",                     # output file stem
  "lang": "ar", "dir": "rtl",
  "short_title": "مذكرة حقوق الإنسان",     # <title> and default footer
  "kicker": "كلية الحقوق",                 # small line above the title (optional)
  "title": "...", "subtitle": "...",
  "note": "حُذفت التواريخ ...",            # what was left out / how to read (optional)
  "footer": "...",                        # optional, defaults to short_title
  "no_years": true,                       # run the year check (user said dates not needed)
  "lessons": [ {"id": "l0", "title": "...", "summary": "..."} , ... ]
}
<project_dir>/notes/*.html  lesson fragments, concatenated in filename order
                            (00_intro.html, 01_ch1.html, 02a_ch2.html, 02b_ch2.html ...).
                            A lesson may span several files: open <section> in the
                            first, close it in the last.
Writes <project_dir>/out/<name>.html and .pdf, then runs check_pdf.py.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
LEGEND = {
    "ar": [("", "مفهوم أو كلمة مفتاحية"), ("g", "رقم أو عدد مهم"),
           ("p", "تمييز أو استثناء أو ملاحظة دقيقة"), ("b", "مثال")],
    "en": [("", "concept / keyword"), ("g", "number / count to memorise"),
           ("p", "distinction / exception / trap"), ("b", "example")],
}
VOID = {"br", "hr", "img", "meta", "link", "input", "wbr", "col", "source"}


def balance(src):
    stack = []
    for m in re.finditer(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*?(/?)>", re.sub(r"<!--.*?-->", "", src, flags=re.S)):
        close, tag, selfc = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID or selfc:
            continue
        if not close:
            stack.append(tag)
        elif tag in ("li", "p", "td", "th", "tr") and stack and stack[-1] != tag:
            continue
        elif stack and stack[-1] == tag:
            stack.pop()
        else:
            return f"unexpected </{tag}> near: {src[max(0, m.start()-80):m.start()]!r}"
    return f"unclosed: {stack}" if stack else None


def main():
    proj = Path(sys.argv[1]).resolve()
    cfg = json.loads((proj / "project.json").read_text())
    lang = cfg.get("lang", "en")
    esc = html.escape
    legend = "".join(f'<span><mark{" class=" + chr(34) + c + chr(34) if c else ""}>{esc(t)}</mark></span>'
                     for c, t in LEGEND.get(lang, LEGEND["en"]))
    toc = "\n".join(f'  <a href="#{l["id"]}"><b>{esc(l["title"])}</b><span>{esc(l.get("summary", ""))}</span></a>'
                    for l in cfg["lessons"])
    head = (SKILL / "assets/_head.html").read_text()
    for k, v in {"LANG": lang, "DIR": cfg.get("dir", "ltr"), "SHORT_TITLE": esc(cfg["short_title"]),
                 "KICKER": esc(cfg.get("kicker", "")), "TITLE": esc(cfg["title"]),
                 "SUBTITLE": esc(cfg.get("subtitle", "")), "NOTE": esc(cfg.get("note", "")),
                 "LEGEND": legend, "TOC": toc}.items():
        head = head.replace("{{" + k + "}}", v)
    frags = sorted((proj / "notes").glob("*.html"))
    body = "\n".join(f.read_text() for f in frags)
    doc = head + body + (SKILL / "assets/_tail.html").read_text()

    err = balance(body)
    if err:
        sys.exit(f"tag balance error: {err}")
    ids = set(re.findall(r'<section[^>]*\bid="([^"]+)"', body))
    missing = [l["id"] for l in cfg["lessons"] if l["id"] not in ids]
    if missing:
        sys.exit(f"TOC ids without a <section id=...>: {missing}")

    out = proj / "out"
    out.mkdir(exist_ok=True)
    h, p = out / f'{cfg["name"]}.html', out / f'{cfg["name"]}.pdf'
    h.write_text(doc)
    print(f"assembled {len(frags)} fragments -> {h}", flush=True)
    npm_root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", str(SKILL / "scripts/render.js"), str(h), str(p),
                    "--footer", cfg.get("footer", cfg["short_title"]), "--dir", cfg.get("dir", "ltr"), "--lang", lang],
                   check=True, env={**__import__("os").environ, "NODE_PATH": npm_root})
    check = [sys.executable, "-I", str(SKILL / "scripts/check_pdf.py"), str(p)]
    if cfg.get("no_years"):
        check.append("--no-years")
    sys.exit(subprocess.run(check).returncode)


if __name__ == "__main__":
    main()
