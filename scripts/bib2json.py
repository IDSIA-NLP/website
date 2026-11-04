#!/usr/bin/env python3
"""Convert publications.bib into data/publications.json for Hugo.

Standard library only, so it runs anywhere without installing anything.
Run from the repository root:  python3 scripts/bib2json.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "publications.bib"
DST = ROOT / "data" / "publications.json"


def parse_entries(text):
    """Yield (type, key, fields) for each @type{key, ...} entry."""
    i, n = 0, len(text)
    while True:
        at = text.find("@", i)
        if at < 0:
            return
        m = re.match(r"@(\w+)\s*([{(])", text[at:])
        if not m:
            i = at + 1
            continue
        etype = m.group(1).lower()
        j = at + m.end()
        # find matching closing brace of the entry
        depth, k = 1, j
        while k < n and depth:
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
            k += 1
        body = text[j:k - 1]
        i = k
        if etype in ("comment", "preamble", "string"):
            continue
        key, _, rest = body.partition(",")
        yield etype, key.strip(), parse_fields(rest)


def parse_fields(s):
    fields, i, n = {}, 0, len(s)
    while i < n:
        m = re.compile(r"\s*([\w-]+)\s*=\s*").match(s, i)
        if not m:
            break
        name, i = m.group(1).lower(), m.end()
        if i < n and s[i] == "{":
            depth, j = 1, i + 1
            while j < n and depth:
                depth += {"{": 1, "}": -1}.get(s[j], 0)
                j += 1
            value, i = s[i + 1:j - 1], j
        elif i < n and s[i] == '"':
            j = s.index('"', i + 1)
            value, i = s[i + 1:j], j + 1
        else:
            m2 = re.compile(r"[^,]*").match(s, i)
            value, i = m2.group(0), m2.end()
        fields[name] = clean(value)
        i = s.find(",", i)
        if i < 0:
            break
        i += 1
    return fields


def clean(v):
    v = re.sub(r"\s+", " ", v).strip()
    v = v.replace("---", "—").replace("--", "–").replace("\\&", "&")
    return v.replace("{", "").replace("}", "")


def split_authors(s):
    out = []
    for a in re.split(r"\s+and\s+", s):
        a = a.strip()
        if not a:
            continue
        if "," in a:
            last, first = [p.strip() for p in a.split(",", 1)]
        else:
            parts = a.split()
            last, first = parts[-1], " ".join(parts[:-1])
        out.append({"first": first, "last": last, "full": f"{first} {last}".strip()})
    return out


def main():
    if not SRC.exists():
        sys.exit(f"Missing {SRC}")
    pubs, errors = [], []
    for etype, key, f in parse_entries(SRC.read_text(encoding="utf-8")):
        if "title" not in f or "year" not in f:
            errors.append(f"{key}: needs at least title and year")
            continue
        venue = f.get("booktitle") or f.get("journal") or f.get("howpublished") or ""
        if etype == "proceedings":
            venue = "Edited proceedings" + (f" ({f['publisher']})" if f.get("publisher") else "")
        if etype == "misc" and not venue and f.get("eprint"):
            venue = "arXiv"
        doi = f.get("doi", "")
        pubs.append({
            "key": key,
            "type": etype,
            "title": f["title"],
            "authors": split_authors(f.get("author") or f.get("editor", "")),
            "editors": "author" not in f and "editor" in f,
            "year": int(re.sub(r"\D", "", f["year"]) or 0),
            "venue": venue,
            "doi": doi,
            "url": f.get("url") or (f"https://doi.org/{doi}" if doi else ""),
            "pdf": f.get("pdf", ""),
            "code": f.get("code", ""),
            "award": f.get("award", ""),
            "themes": [t.strip() for t in f.get("keywords", "").split(",") if t.strip()],
            "project": f.get("project", ""),
            "note": f.get("note", ""),
        })
    pubs.sort(key=lambda p: (-p["year"], p["authors"][0]["last"] if p["authors"] else ""))
    DST.parent.mkdir(exist_ok=True)
    DST.write_text(json.dumps(pubs, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(pubs)} publications -> {DST.relative_to(ROOT)}")
    for e in errors:
        print("WARNING:", e)


if __name__ == "__main__":
    main()
