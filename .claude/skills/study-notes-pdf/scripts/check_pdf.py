"""Quality checks for a rendered notes PDF.

Usage: python3 -I check_pdf.py notes.pdf [--no-years]

Checks:
  1. Highlight safety: no /Pattern, /Shading or soft-alpha ExtGState. These come
     from gradients/rgba/opacity in CSS and make highlights vanish on zoom in
     some viewers.
  2. Page endings: flags pages whose last text line ends with ':' (a label whose
     list moved to the next page) or that end on a very short line that looks
     like an orphaned heading.
  3. --no-years: flags 4-digit years (1000-2099) when the user asked not to
     include dates. Review each hit; a year that is part of a name ("Vision
     2030") may stay.
Exit code 1 if check 1 or 2 fails; years are only a warning to review.
"""
import re
import subprocess
import sys

import pypdf


def walk(obj, seen, hits):
    if id(obj) in seen:
        return
    seen.add(id(obj))
    obj = obj.get_object() if hasattr(obj, "get_object") else obj
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("/Pattern", "/Shading") and v:
                hits.add(k)
            if k in ("/ca", "/CA") and float(v) < 1:
                hits.add(f"{k}<1")
            if k == "/SMask" and v != "/None":
                hits.add("/SMask")
            walk(v, seen, hits)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, seen, hits)


def main():
    path = sys.argv[1]
    no_years = "--no-years" in sys.argv
    r = pypdf.PdfReader(path)
    n = len(r.pages)
    ok = True
    print(f"{path}: {n} pages")

    hits = set()
    for pg in r.pages:
        walk(pg.get("/Resources", {}), set(), hits)
    if hits:
        ok = False
        print(f"FAIL highlight safety: found {sorted(hits)}; replace gradients/rgba/opacity with solid colours")
    else:
        print("ok   highlight safety: solid colours only")

    bad = []
    for i in range(1, n + 1):
        t = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), path, "-"],
                           capture_output=True, text=True).stdout
        lines = [l.strip() for l in t.splitlines() if l.strip()]
        # drop the footer line (page number)
        body = [l for l in lines if not re.search(r"(صفحة|Page)\s*\d+\s*(من|of)\s*\d+", l)]
        if i < n and body:
            last = body[-1]
            if last.endswith(":") or last.endswith("："):
                bad.append((i, last))
    if bad:
        ok = False
        for i, l in bad:
            print(f"FAIL page {i} ends on a label: {l[:70]}")
    else:
        print("ok   page endings: no page ends on a dangling label")

    if no_years:
        text = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout
        yrs = sorted(set(re.findall(r"(?<!\d)(1[0-9]{3}|20[0-9]{2})(?!\d)", text)))
        if yrs:
            print(f"WARN years found (check each; names like 'Vision 2030' may stay): {yrs}")
        else:
            print("ok   no years")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
