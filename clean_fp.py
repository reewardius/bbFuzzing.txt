#!/usr/bin/env python3
"""
clean_fp.py — відсів false positives зі списку знайдених ендпоінтів.

Формат вхідного рядка (як у виводі httpx/dirb-подібних сканерів):
    http://host/path [200] [412] [text/html] [host] [nginx]
    тобто:  URL  [status] [content-length] [content-type] [host] [server]

Правила відсіву (можна вмикати/вимикати прапорцями):
  1. content-type == text/html            -> FP            (--keep-html вимикає)
  2. content-length повторюється часто     -> шаблон/FP     (--threshold, --keep-dupes вимикає)
  3. status у списку «нецікавих»           -> FP            (--bad-status)

Приклади:
    python3 clean_fp.py scan.txt
    python3 clean_fp.py scan.txt -o clean.txt --threshold 5
    python3 clean_fp.py scan.txt --keep-html --json-only
    cat scan.txt | python3 clean_fp.py -           # зі stdin
"""
import argparse
import collections
import re
import sys

BRACKET_RE = re.compile(r"\[([^\]]*)\]")


def parse_line(line):
    """Повертає dict або None, якщо рядок не парситься."""
    line = line.rstrip("\n")
    if not line.strip():
        return None
    url = line.split(None, 1)[0]
    fields = BRACKET_RE.findall(line)
    # нормалізуємо: прибираємо хвостові пробіли та анотації типу (PII)
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
        description="Відсів false positives зі списку ендпоінтів.")
    ap.add_argument("input", help="файл виводу сканера, або '-' для stdin")
    ap.add_argument("-o", "--output",
                    help="куди записати чисті хіти (за замовч. — stdout)")
    ap.add_argument("-t", "--threshold", type=int, default=5,
                    help="content-length, що зустрічається БІЛЬШЕ за N разів, "
                         "вважається шаблоном/FP (за замовч. 5)")
    ap.add_argument("--keep-html", action="store_true",
                    help="не відкидати text/html")
    ap.add_argument("--keep-dupes", action="store_true",
                    help="не відкидати повторювані content-length")
    ap.add_argument("--bad-status", default="",
                    help="кома-перелік статусів, які теж вважати FP, напр. '404,400,403'")
    ap.add_argument("--only-json", action="store_true",
                    help="лишити тільки application/json")
    ap.add_argument("--stats", action="store_true",
                    help="показати статистику у stderr")
    args = ap.parse_args()

    rows = load(args.input)
    total = len(rows)
    if total == 0:
        print("Порожній або нерозпізнаний ввід.", file=sys.stderr)
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

    # json першим, далі за рідкістю довжини, далі за url
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
        print(f"[*] Всього рядків:        {total}", file=e)
        for reason, n in dropped.most_common():
            print(f"[-] Відкинуто ({reason}): {n}", file=e)
        print(f"[+] Залишилось хітів:     {len(kept)}", file=e)
        print(f"[*] Топ content-length (шаблони):", file=e)
        for l, c in len_counts.most_common(5):
            mark = "  <-- FP" if c > args.threshold else ""
            print(f"      len={l:>8}  x{c}{mark}", file=e)
        if args.output:
            print(f"[+] Записано у: {args.output}", file=e)


if __name__ == "__main__":
    main()
