#!/usr/bin/env python3
"""Download missing brand/partner images referenced on the live site."""
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

TARGETS = {
    "Sabiniya": "wp-content/uploads",
    "MAXIUMS": "wp-content/uploads",
    "Maximums": "wp-content/uploads",
    "Al-Kareem": "wp-content/uploads",
    "Al Kareem": "wp-content/uploads",
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def download(url: str, dest: str) -> bool:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest) and os.path.getsize(dest) > 500:
        print(f"  skip (exists) {dest}")
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = resp.read()
        if len(data) < 500:
            print(f"  fail (too small) {url}")
            return False
        with open(dest, "wb") as f:
            f.write(data)
        print(f"  saved {dest}")
        return True
    except Exception as exc:
        print(f"  fail {url}: {exc}")
        return False


def main() -> None:
    html = fetch("https://wafaenterprises.com/")
    found = {}
    for m in re.finditer(
        r'<div class="icon_box[^>]*>.*?<h4 class="title[^"]*">([^<]+)</h4>',
        html,
        re.S,
    ):
        title = m.group(1).strip()
        block = m.group(0)
        img = re.search(r'src="(/wp-content/uploads/[^"]+)"', block)
        if img:
            found[title] = img.group(1)

    with open("index.html", encoding="utf-8", errors="ignore") as f:
        page = f.read()

    for title, path in sorted(found.items()):
        local = path.lstrip("/").replace("/", os.sep)
        if not os.path.exists(local):
            download("https://wafaenterprises.com" + path, local)

    # Patch index.html icon boxes missing images
    updated = page
    for title, path in found.items():
        pattern = (
            rf'(<h4 class="title ">{re.escape(title)}</h4>)'
        )
        if re.search(
            rf'column_icon_box[^>]*>.*?{re.escape(title)}.*?</div></div></div>',
            updated,
            re.S,
        ):
            block_pat = (
                rf'(<div class="icon_box icon_position_top no_border">)'
                rf'(<div class="desc_wrapper"><h4 class="title ">{re.escape(title)}</h4></div></div>)'
            )
            replacement = (
                rf'\1<div class="image_wrapper"><img class="scale-with-grid" '
                rf'src="{path}" alt="{title}" width="219" height="102"/></div>'
                rf'<div class="desc_wrapper"><h4 class="title ">{title}</h4></div></div>'
            )
            if re.search(block_pat, updated):
                updated = re.sub(block_pat, replacement, updated, count=1)
                print(f"patched HTML for {title}")

    if updated != page:
        with open("index.html", "w", encoding="utf-8", newline="\n") as f:
            f.write(updated)
        print("Updated index.html with missing brand images")


if __name__ == "__main__":
    main()
