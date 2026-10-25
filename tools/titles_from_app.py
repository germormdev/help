#!/usr/bin/env python3
"""Заголовки разделов мануала — из строк приложения (один источник: дерево приложения).

Звать: python3 tools/titles_from_app.py <корень дерева приложения или распакованный res> > _data/titles.json
Берёт help_title и help_section_* из app/src/main/res/values*/strings*.xml,
body_* из core/src/main/res/values*/strings_vehicle.xml. Папку values-iw пишет как he.
"""
import glob, json, os, re, sys
import xml.etree.ElementTree as ET

ROOT = sys.argv[1]
GENERAL = ["getting-started", "shift", "trip", "driving", "refuel", "parking", "camera", "history", "report",
           "garage", "documents", "maintenance", "address-book", "backup", "online", "settings"]
VEHICLE = ["flatbed", "container", "sidelifter", "refrigerated", "curtainsider", "tipper", "fuel-tanker", "tanker",
           "car-transporter"]
LANG_DIR = re.compile(r"values(?:-([a-z]{2}))?$")

def strings(pattern):
    out = {}
    for f in glob.glob(os.path.join(ROOT, pattern)):
        m = LANG_DIR.search(os.path.basename(os.path.dirname(f)))
        if not m:
            continue
        lang = {None: "en", "iw": "he"}.get(m.group(1), m.group(1))
        for s in ET.parse(f).getroot().iter("string"):
            text = "".join(s.itertext()).replace("\\'", "'").replace('\\"', '"')
            out.setdefault(lang, {})[s.get("name")] = text
    return out

app = strings("app/src/main/res/values*/strings*.xml")
veh = strings("core/src/main/res/values*/strings_vehicle.xml")
titles = {}
for lang in sorted(app):
    a, v = app[lang], veh.get(lang, {})
    if "help_title" not in a:
        continue
    sec = {s: a.get("help_section_" + s.replace("-", "_"), app["en"]["help_section_" + s.replace("-", "_")]) for s in GENERAL}
    sec.update({s: v.get("body_" + s.replace("-", "_"), veh["en"]["body_" + s.replace("-", "_")]) for s in VEHICLE})
    titles[lang] = {"help": a["help_title"], "app": a.get("app_name", "VecturaBook"), "sections": sec}
json.dump({"general": GENERAL, "vehicle": VEHICLE, "langs": titles}, sys.stdout, ensure_ascii=False, indent=1)
print()
