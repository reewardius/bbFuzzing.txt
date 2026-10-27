#!/usr/bin/env python3
"""
clean_fp.py - filter false positives from a list of discovered endpoints.

Input line format (typical httpx / dirb-like scanner output):
    http://host/path [200] [412] [text/html] [host] [nginx]
    i.e.:  URL  [status] [content-length] [content-type] [host] [server]

Filtering rules (toggleable via flags):
  1. content-type == text/html             -> FP   (disable with --keep-html)
  2. content-length that repeats often     -> boilerplate/FP
                                              (--threshold, disable with --keep-dupes)
  3. status in the "uninteresting" list    -> FP   (--bad-status)
  4. keep only application/json            -> optional (--only-json)

Examples:
    python3 clean_fp.py scan.txt
    python3 clean_fp.py scan.txt -o clean.txt --threshold 5
    python3 clean_fp.py scan.txt --keep-html --only-json
    cat scan.txt | python3 clean_fp.py -           # read from stdin
"""
import argparse
import collections
import re
import sys

BRACKET_RE = re.compile(r"\[([^\]]*)\]")


def parse_line(line):
    """Return a dict for one line, or None if it does not parse."""
    line = line.rstrip("\n")
    if not line.strip():
        return None
    url = line.split(None, 1)[0]
    fields = BRACKET_RE.findall(line)
    # normalize: strip trailing spaces and annotations like (PII)
    clean = lambda s: re.sub(r"\(.*?\)$", "", s).strip()
    return {
        "url": url.strip(),
        "status": clean(fields[0]) if len(fields) > 0 else "",
        "length": clean(fields[1]) if len(fields) > 1 else "",
        "ctype":  clean(fields[2]) if len(fields) > 2 else "",
        "host":   clean(fields[3]) if len(fields) > 3 else "",
        "server": clean(fields[4]) if len(fields) > 4 else "",
        "raw": line,
    }


def load(path):
    rows = []
    f = sys.stdin if path == "-" else open(path, encoding="utf-8", errors="replace")
    try:
        for ln in f:
            r = parse_line(ln)
            if r:
                rows.append(r)
    finally:
        if f is not sys.stdin:
            f.close()
    return rows


def main():
    ap = argparse.ArgumentParser(
        description="Filter false positives from an endpoint list.")
    ap.add_argument("input", help="scanner output file, or '-' for stdin")
    ap.add_argument("-o", "--output",
                    help="write clean hits here (default: stdout)")
    ap.add_argument("-t", "--threshold", type=int, default=5,
                    help="a content-length seen MORE than N times is treated "
                         "as boilerplate/FP (default: 5)")
    ap.add_argument("--keep-html", action="store_true",
                    help="do not drop text/html")
    ap.add_argument("--keep-dupes", action="store_true",
                    help="do not drop repeated content-length")
    ap.add_argument("--bad-status", default="",
                    help="comma-separated statuses to treat as FP, e.g. '404,400,403'")
    ap.add_argument("--only-json", action="store_true",
                    help="keep only application/json")
    ap.add_argument("--stats", action="store_true",
                    help="print statistics to stderr")
    args = ap.parse_args()

    rows = load(args.input)
    total = len(rows)
    if total == 0:
        print("Empty or unrecognized input.", file=sys.stderr)
        sys.exit(1)

    len_counts = collections.Counter(r["length"] for r in rows)
    bad_status = {s.strip() for s in args.bad_status.split(",") if s.strip()}

    kept, dropped = [], collections.Counter()
    for r in rows:
        if not args.keep_html and r["ctype"] == "text/html":
            dropped["text/html"] += 1
            continue
        if not args.keep_dupes and r["length"] and len_counts[r["length"]] > args.threshold:
            dropped["dup-length"] += 1
            continue
        if bad_status and r["status"] in bad_status:
            dropped["bad-status"] += 1
            continue
        if args.only_json and r["ctype"] != "application/json":
            dropped["not-json"] += 1
            continue
        kept.append(r)

    # json first, then by rarity of length, then by url
    kept.sort(key=lambda r: (r["ctype"] != "application/json",
                             len_counts[r["length"]], r["url"]))

    out = sys.stdout if not args.output else open(args.output, "w", encoding="utf-8")
    try:
        for r in kept:
            out.write(r["raw"] + "\n")
    finally:
        if out is not sys.stdout:
            out.close()

    if args.stats or args.output:
        e = sys.stderr
        print(f"[*] Total lines:        {total}", file=e)
        for reason, n in dropped.most_common():
            print(f"[-] Dropped ({reason}): {n}", file=e)
        print(f"[+] Hits kept:          {len(kept)}", file=e)
        print(f"[*] Top content-length (boilerplate):", file=e)
        for l, c in len_counts.most_common(5):
            mark = "  <-- FP" if c > args.threshold else ""
            print(f"      len={l:>8}  x{c}{mark}", file=e)
        if args.output:
            print(f"[+] Written to: {args.output}", file=e)


if __name__ == "__main__":
    main()
