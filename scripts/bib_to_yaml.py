#!/usr/bin/env python3
"""
Convert publications.bib into data/publications.yml for the Hugo site.

Usage (run from anywhere):
    python3 scripts/bib_to_yaml.py                 # publications.bib -> data/publications.yml
    python3 scripts/bib_to_yaml.py other.bib       # use a different input file
    python3 scripts/bib_to_yaml.py --pi Rimoli     # surname shown in bold (default: Rimoli)
    python3 scripts/bib_to_yaml.py --dry-run       # report what would be written, change nothing

Needs only the Python standard library. Handles nested braces, LaTeX accents,
"Last, First" and "First Last" author forms, surname particles (van, de, di ...),
and "others" (rendered as "et al.").
"""

import argparse
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BIB = SITE_ROOT / "publications.bib"
DEFAULT_OUT = SITE_ROOT / "data" / "publications.yml"

TYPE_MAP = {
    "article": "journal",
    "inproceedings": "conference",
    "conference": "conference",
    "incollection": "chapter",
    "inbook": "chapter",
    "book": "book",
    "phdthesis": "thesis",
    "mastersthesis": "thesis",
    "techreport": "report",
}

# Lower-case surname particles that stay with the surname in "First Last" names.
PARTICLES = {"da", "de", "del", "della", "der", "den", "di", "do", "dos", "du",
             "la", "le", "van", "von", "ten", "ter"}

ACCENTS = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303",
           "=": "\u0304", ".": "\u0307", "u": "\u0306", "v": "\u030c", "H": "\u030b",
           "c": "\u0327", "d": "\u0323", "b": "\u0331", "k": "\u0328", "r": "\u030a"}
SPECIALS = {"ss": "ß", "o": "ø", "O": "Ø", "aa": "å", "AA": "Å", "ae": "æ", "AE": "Æ",
            "oe": "œ", "OE": "Œ", "i": "ı", "l": "ł", "L": "Ł"}
ACCENT_RE = re.compile(r"\\([`'^\"~=.uvHcdbkr])\s*\{?([A-Za-z])\}?")
SPECIAL_RE = re.compile(r"\\(ss|aa|AA|ae|AE|oe|OE|[oOiLl])(?![A-Za-z])")
ENTRY_HEAD = re.compile(r"@\s*([A-Za-z]+)\s*([{(])")
FIELD_NAME = re.compile(r"\s*([A-Za-z][\w\-:.]*)\s*=\s*")
INITIAL_RE = re.compile(r"(?:[A-Z]\.)+(?:-[A-Z]\.)*")
WARNINGS = []


def latex_to_text(s, strip_braces=True):
    """Turn LaTeX-isms into plain text: accents, ties, dashes, simple commands."""
    s = ACCENT_RE.sub(lambda m: unicodedata.normalize("NFC", m.group(2) + ACCENTS[m.group(1)]), s)
    s = SPECIAL_RE.sub(lambda m: SPECIALS[m.group(1)], s)
    for old, new in (("\\&", "&"), ("\\%", "%"), ("\\_", "_"), ("\\$", "$"), ("\\#", "#"),
                     ("---", "\u2014"), ("--", "\u2013"), ("``", "\u201c"), ("''", "\u201d"),
                     ("~", " ")):
        s = s.replace(old, new)
    s = re.sub(r"\\(?:emph|textit|textbf|mathrm|text)\{([^{}]*)\}", r"\1", s)
    if strip_braces:
        s = s.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def iter_entries(text):
    """Yield (entry_type, body, raw_text) for each entry, honouring nested braces."""
    pos = 0
    while True:
        m = ENTRY_HEAD.search(text, pos)
        if not m:
            return
        etype = m.group(1).lower()
        opener = m.group(2)
        i = m.end()
        depth = 1
        while i < len(text):
            c = text[i]
            if opener == "{":
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        break
            else:
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                elif c == ")" and depth == 1:
                    break
            i += 1
        raw = text[m.start():i + 1]
        body = text[m.end():i]
        pos = i + 1
        if etype in ("comment", "string", "preamble"):
            continue
        yield etype, body, raw


def parse_body(body):
    """Split an entry body into (citation_key, {field: value})."""
    comma = body.find(",")
    if comma < 0:
        return body.strip(), {}
    key = body[:comma].strip()
    rest = body[comma + 1:]
    fields = {}
    pos, n = 0, len(rest)
    while pos < n:
        while pos < n and rest[pos] in " \t\r\n,":
            pos += 1
        if pos >= n:
            break
        m = FIELD_NAME.match(rest, pos)
        if not m:
            break
        name = m.group(1).lower()
        pos = m.end()
        pieces = []
        while True:
            if pos < n and rest[pos] == "{":
                depth, start = 0, pos
                while pos < n:
                    if rest[pos] == "{":
                        depth += 1
                    elif rest[pos] == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    pos += 1
                pieces.append(rest[start + 1:pos])
                pos += 1
            elif pos < n and rest[pos] == '"':
                depth, start = 0, pos + 1
                pos += 1
                while pos < n:
                    if rest[pos] == "{":
                        depth += 1
                    elif rest[pos] == "}":
                        depth -= 1
                    elif rest[pos] == '"' and depth == 0:
                        break
                    pos += 1
                pieces.append(rest[start:pos])
                pos += 1
            else:
                m2 = re.match(r"[^,\s#]+", rest[pos:])
                if not m2:
                    break
                pieces.append(m2.group(0))
                pos += m2.end()
            m3 = re.match(r"\s*#\s*", rest[pos:])
            if m3:
                pos += m3.end()
                continue
            break
        fields[name] = re.sub(r"\s+", " ", "".join(pieces)).strip()
    return key, fields


def split_authors(s):
    """Split an author field on ' and ' outside braces."""
    out, depth, start, i = [], 0, 0, 0
    low = s.lower()
    while i < len(s):
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif depth == 0 and low.startswith(" and ", i):
            out.append(s[start:i])
            i += 5
            start = i
            continue
        i += 1
    out.append(s[start:])
    return [a.strip() for a in out if a.strip()]


def protected_split(s):
    """Split on whitespace, keeping {...} groups together (braces removed)."""
    tokens, cur, depth = [], [], 0
    for c in s:
        if c == "{":
            depth += 1
        elif c == "}":
            depth = max(0, depth - 1)
        elif c.isspace() and depth == 0:
            if cur:
                tokens.append("".join(cur))
                cur = []
        else:
            cur.append(c)
    if cur:
        tokens.append("".join(cur))
    return tokens


def initials(given):
    """'Jean-Baptiste' -> 'J.-B.', 'J.J.' -> 'J. J.', 'Bijun' -> 'B.'"""
    parts = []
    for tok in given.replace(".", ". ").split():
        subs = [s for s in tok.split("-") if s]
        parts.append("-".join(s[0].upper() + "." for s in subs))
    return " ".join(parts)


def format_name(raw):
    """'Last, First M.' or 'First M. Last' -> 'F. M. Last'. Returns None for 'others'."""
    raw = latex_to_text(raw, strip_braces=False)
    if raw.lower() == "others":
        return None
    suffix = ""
    if "," in raw:
        parts = [p.strip() for p in raw.split(",")]
        last = parts[0].replace("{", "").replace("}", "")
        if len(parts) >= 3:
            suffix, first = parts[1], " ".join(parts[2:])
        else:
            first = parts[1] if len(parts) > 1 else ""
    else:
        toks = protected_split(raw)
        if not toks:
            return ""
        if len(toks) == 1:
            return toks[0]
        if INITIAL_RE.fullmatch(toks[-1]) and not INITIAL_RE.fullmatch(toks[0]):
            # "Kraus J." is almost certainly "Kraus, J." with the comma missing.
            WARNINGS.append(f'author "{raw}" looks like "Surname Initial" with a missing comma; read as {toks[0]}, {" ".join(toks[1:])}')
            toks = toks[1:] + toks[:1]
        k = len(toks) - 1
        while k - 1 >= 1 and toks[k - 1].lower() in PARTICLES:
            k -= 1
        last = " ".join(toks[k:])
        first = " ".join(toks[:k])
    first = first.replace("{", "").replace("}", "")
    name = f"{initials(first)} {last}".strip()
    if suffix:
        name += f", {suffix}"
    return name


def format_author_list(names, pi=None):
    """Return (plain_text, html_with_pi_in_bold)."""
    plain, rich, et_al = [], [], False
    pi_re = re.compile(r"\b" + re.escape(pi) + r"$", re.IGNORECASE) if pi else None
    for raw in names:
        n = format_name(raw)
        if n is None:
            et_al = True
            continue
        if not n:
            continue
        plain.append(n)
        h = html.escape(n, quote=False)
        if pi_re and pi_re.search(n):
            h = f"<strong>{h}</strong>"
        rich.append(h)

    def join(items):
        if not items:
            return ""
        if et_al:
            return ", ".join(items) + ", et al."
        if len(items) == 1:
            return items[0]
        if len(items) == 2:
            return f"{items[0]} and {items[1]}"
        return ", ".join(items[:-1]) + f", and {items[-1]}"

    return join(plain), join(rich)


STATUS_LABELS = ("submitted", "under review", "in review", "in press", "accepted", "to appear", "in preparation")


def tidy_bibtex(raw):
    """Normalise whitespace and drop CV-only annotations such as year={2021 [{\\bf Cover article}]}."""
    raw = re.sub(r"(year\s*=\s*[{\"])\s*(\d{4})\s*\[.*?\]\s*([}\"])", r"\1\2\3", raw)
    return "\n".join(ln.replace("\t", "  ").rstrip() for ln in raw.strip().split("\n"))


def build_publication(etype, key, f, raw, pi):
    authors, authors_html = format_author_list(split_authors(f.get("author", "")), pi)
    year_raw = f.get("year", "")
    m = re.search(r"\d{4}", year_raw)
    year = int(m.group(0)) if m else 0
    status = "published"
    for label in STATUS_LABELS:
        if label in year_raw.lower():
            status = label
            break
    # A CV-style annotation in the year field, e.g. "2021 [{\\bf Cover article}]", becomes the award.
    award = latex_to_text(f.get("award", ""))
    m2 = re.search(r"\[(.*)\]", year_raw)
    if m2 and not award:
        award = latex_to_text(re.sub(r"\\bf\b\s*", "", m2.group(1)))
    if etype == "article":
        venue = f.get("journal", "")
    elif etype in ("inproceedings", "conference"):
        venue = f.get("booktitle", "")
    else:
        venue = (f.get("journal") or f.get("booktitle") or f.get("publisher")
                 or f.get("school") or f.get("institution") or "")
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", f.get("doi", "")).strip()
    url = f.get("url", "").strip()
    # Drop a url that only repeats the DOI or the publisher's page for the same DOI.
    if url and doi:
        if re.sub(r"^https?://(dx\.)?doi\.org/", "", url).lower() == doi.lower():
            url = ""
        elif "sciencedirect.com/science/article" in url and doi.lower().startswith("10.1016/"):
            url = ""
    url_label = "arXiv" if "arxiv.org" in url else "PMC" if "ncbi.nlm.nih.gov" in url else "Link" if url else ""
    return {
        "title": latex_to_text(f.get("title", "")),
        "authors": authors,
        "authors_html": authors_html if authors_html != authors else "",
        "year": year or None,
        "status": status,
        "type": TYPE_MAP.get(etype, "other"),
        "venue": latex_to_text(venue),
        "volume": f.get("volume", ""),
        "number": f.get("number", ""),
        "pages": latex_to_text(f.get("pages", "")),
        "doi": doi,
        "url": url,
        "url_label": url_label,
        "pdf": f.get("pdf", ""),
        "code": f.get("code", ""),
        "project_page": f.get("project_page", ""),
        "award": award,
        "abstract": latex_to_text(f.get("abstract", "")),
        "key": key,
        "bibtex": tidy_bibtex(raw),
    }


def yaml_scalar(v):
    if isinstance(v, int):
        return str(v)
    return json.dumps(v, ensure_ascii=False)   # a JSON string is a valid YAML double-quoted string


def emit_yaml(pubs):
    lines = ["# Generated from publications.bib by scripts/bib_to_yaml.py.",
             "# Do not edit by hand: edit publications.bib and re-run the script.", ""]
    for p in pubs:
        first = True
        for k, v in p.items():
            if v == "" or v is None:
                continue
            lead = "- " if first else "  "
            first = False
            if isinstance(v, str) and "\n" in v:
                lines.append(f"{lead}{k}: |")
                lines.extend(("    " + ln) if ln else "" for ln in v.split("\n"))
            else:
                lines.append(f"{lead}{k}: {yaml_scalar(v)}")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Convert a BibTeX file to data/publications.yml")
    ap.add_argument("bib", nargs="?", default=str(DEFAULT_BIB), help="input .bib file")
    ap.add_argument("-o", "--output", default=str(DEFAULT_OUT), help="output .yml file")
    ap.add_argument("--pi", default="Rimoli", help="surname to show in bold ('' to disable)")
    ap.add_argument("--dry-run", action="store_true", help="parse and report, write nothing")
    args = ap.parse_args()

    bib_path = Path(args.bib)
    if not bib_path.exists():
        sys.exit(f"Error: {bib_path} not found")
    text = bib_path.read_text(encoding="utf-8")

    pubs, problems, seen = [], [], set()
    for etype, body, raw in iter_entries(text):
        key, fields = parse_body(body)
        pub = build_publication(etype, key, fields, raw, args.pi or None)
        for field in ("title", "authors"):
            if not pub[field]:
                problems.append(f"{key}: missing or invalid {field}")
        if pub["status"] == "published" and not pub["year"]:
            problems.append(f"{key}: missing or invalid year")
        if key in seen:
            problems.append(f"{key}: duplicate citation key")
        seen.add(key)
        pubs.append(pub)
    # Published papers first, newest year first; submitted or in-press papers after them.
    # Within a year the order follows the .bib file.
    pubs.sort(key=lambda p: (0 if p["status"] == "published" else 1, -(p["year"] or 0)))

    print(f"Parsed {len(pubs)} entries from {bib_path}")
    for p in problems + WARNINGS:
        print(f"  warning: {p}")
    if args.dry_run:
        print("Dry run: nothing written.")
        return
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(emit_yaml(pubs), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
