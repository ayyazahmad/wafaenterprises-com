#!/usr/bin/env python3
"""Verify local asset files referenced in HTML exist on disk."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

missing = []
checked_pages = 0
for dirpath, _, files in os.walk(ROOT):
    rel = os.path.relpath(dirpath, ROOT)
    if rel.startswith(("scripts", ".git", "wp-includes", "wp-content")):
        continue
    for fname in files:
        if not fname.endswith(".html"):
            continue
        checked_pages += 1
        page = os.path.relpath(os.path.join(dirpath, fname), ROOT)
        with open(os.path.join(dirpath, fname), "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        for m in re.finditer(r'(?:href|src)=["\'](/wp-[^"\']+)["\']', content):
            path = m.group(1).split("?")[0]
            local = path.lstrip("/").replace("/", os.sep)
            if not os.path.exists(local):
                missing.append((page, path))
        if "https://wafaenterprises.com/" in content:
            missing.append((page, "EXTERNAL: wafaenterprises.com URL remains"))

unique = sorted(set(missing))
print(f"Checked {checked_pages} HTML pages")
print(f"Missing asset refs: {len(unique)}")
for page, path in unique[:80]:
    print(f"  {path}  ({page})")
if len(unique) > 80:
    print(f"  ... and {len(unique) - 80} more")
