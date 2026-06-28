#!/usr/bin/env python3
"""Fix HTML URLs and download missing assets only."""
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

spec = importlib.util.spec_from_file_location("build_site", os.path.join(ROOT, "scripts", "build_site.py"))
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

print("=== Fix HTML ===")
print(f"Updated {build.fix_all_html()} HTML files")

print("\n=== Download assets ===")
refs = build.collect_asset_refs()
print(f"Found {len(refs)} asset refs")
print(f"Downloaded {build.download_assets(refs)} missing assets")

print("\n=== Final HTML fix ===")
print(f"Updated {build.fix_all_html()} HTML files")
