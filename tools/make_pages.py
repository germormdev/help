#!/usr/bin/env python3
"""Заглушки мануала по постоянным адресам help.vecturabook.com/<язык>/<раздел>.

Звать из корня репозитория: python3 tools/make_pages.py
Пишет <язык>/index.md (оглавление) и <язык>/<раздел>.md с пометкой `stub: true` — только там, где настоящего текста
ещё нет. Файл без пометки `stub: true` (текст Клода Мака) не трогает никогда.
Проверка без записи: python3 tools/make_pages.py --check — код 1, если какой-то адрес не покрыт страницей.
"""
import json, os, sys

T = json.load(open("_data/titles.json", encoding="utf-8"))
SLUGS = T["general"] + T["vehicle"]

def is_stub(path):
    if not os.path.exists(path):
        return True
    head = open(path, encoding="utf-8").read(400)
    return head.startswith("---") and "\nstub: true\n" in head

def write(path, text):
    if not is_stub(path):
        return 0
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old == text:
        return 0
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)
    return 1

def q(s):
    return json.dumps(s, ensure_ascii=False)

missing = [f"{l}/{s}" for l in T["langs"] for s in SLUGS + ["index"] if not os.path.exists(f"{l}/{s}.md")]
if "--check" in sys.argv:
    print("не покрыто адресов:", len(missing), *missing[:20])
    sys.exit(1 if missing else 0)

n = 0
for lang, t in T["langs"].items():
    for slug in SLUGS:
        n += write(f"{lang}/{slug}.md",
                   f"---\nlayout: page\nstub: true\nlang: {lang}\nsection: {slug}\ntitle: {q(t['sections'][slug])}\n---\n")
    n += write(f"{lang}/index.md", f"---\nlayout: toc\nstub: true\nlang: {lang}\ntitle: {q(t['help'])}\n---\n")
print("записано заглушек:", n)
