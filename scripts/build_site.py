#!/usr/bin/env python3
"""Download wafaenterprises.com static export, localize assets, fix layout."""
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)
os.chdir(ROOT)

from fix_emails import EMAIL_LINK, fix_emails

BASE_URL = "https://wafaenterprises.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

PAGES = ["/", "/about/", "/partners/", "/contact/", "/services/"]

REPLACEMENTS = [
    ("https://wafaenterprises.com/wp-content/", "/wp-content/"),
    ("https://wafaenterprises.com/wp-includes/", "/wp-includes/"),
    ("http://wafaenterprises.com/wp-content/", "/wp-content/"),
    ("http://wafaenterprises.com/wp-includes/", "/wp-includes/"),
    ("//wafaenterprises.com/wp-content/", "/wp-content/"),
    ("//wafaenterprises.com/wp-includes/", "/wp-includes/"),
]

PAGE_LINKS = [
    ("https://wafaenterprises.com/", "/"),
    ("https://wafaenterprises.com/about/", "/about/"),
    ("https://wafaenterprises.com/partners/", "/partners/"),
    ("https://wafaenterprises.com/contact/", "/contact/"),
    ("https://wafaenterprises.com/services/", "/services/"),
]

LAYOUT_FIX = """
<style id="static-layout-fix">
@media only screen and (max-width: 767px) {
  #Wrapper { max-width: 100% !important; }
  .content_wrapper .section_wrapper,
  .container,
  .four.columns .widget-area {
    max-width: 100% !important;
    padding-left: 15px !important;
    padding-right: 15px !important;
  }
}
body.layout-boxed #Wrapper {
  margin-left: auto;
  margin-right: auto;
}
</style>
"""

FONTS_DIR = os.path.join(ROOT, "wp-content", "themes", "betheme", "fonts", "google")
LOCAL_FONTS_CSS = "/wp-content/themes/betheme/fonts/google/fonts.css"
GOOGLE_FONTS_API = (
    "https://fonts.googleapis.com/css2?"
    "family=Lato:ital,wght@0,300;0,400;0,700;0,900;1,400;1,700&display=swap"
)


def download(url: str, dest: str, retries: int = 3, min_size: int = 0) -> bool:
    if "${" in url:
        return False
    if "#" in dest:
        dest = dest.split("#", 1)[0]
    if os.path.exists(dest) and os.path.getsize(dest) > max(min_size, 50):
        return True
    dest_dir = os.path.dirname(dest)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    for attempt in range(retries):
        try:
            result = subprocess.run(
                [
                    "curl.exe",
                    "-sL",
                    "--max-time",
                    "90",
                    "-A",
                    UA,
                    "-o",
                    dest,
                    "-w",
                    "%{http_code}",
                    url,
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            code = (result.stdout or "").strip()
            size = os.path.getsize(dest) if os.path.exists(dest) else 0
            ok_code = code.startswith("2") or code == "500"
            if ok_code and size > max(min_size, 50):
                with open(dest, "rb") as f:
                    head = f.read(200).lower()
                if b"<!doctype html" in head or b"<html" in head:
                    print(f"OK  {dest} ({code})")
                    return True
            if os.path.exists(dest):
                os.remove(dest)
        except Exception as exc:
            if attempt == retries - 1:
                print(f"FAIL {url} -> {exc}")
                return False
        time.sleep(2)
    print(f"FAIL {url}")
    return False


def fetch_sitemap_pages() -> list[str]:
    pages = set(PAGES)
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/wp-sitemap-posts-page-1.xml", headers={"User-Agent": UA}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            root = ET.fromstring(resp.read())
        for loc in root.findall(".//sm:loc", NS):
            path = loc.text.replace(BASE_URL, "").rstrip("/") + "/"
            if path == "//":
                path = "/"
            pages.add(path)
    except Exception as exc:
        print(f"Sitemap fetch skipped: {exc}")
    return sorted(pages, key=lambda p: (p != "/", p))


def download_pages(pages: list[str]) -> int:
    ok = 0
    for path in pages:
        url = BASE_URL + (path if path != "/" else "/")
        dest = "index.html" if path == "/" else os.path.join(
            path.strip("/").replace("/", os.sep), "index.html"
        )
        if download(url, dest, min_size=5000):
            ok += 1
        time.sleep(3)
    return ok


def ensure_lato_fonts() -> None:
    os.makedirs(FONTS_DIR, exist_ok=True)
    req = urllib.request.Request(GOOGLE_FONTS_API, headers={"User-Agent": UA})
    css = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
    local_css = css
    for match in re.finditer(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css):
        font_url = match.group(1)
        filename = font_url.rsplit("/", 1)[-1].split("?")[0]
        dest = os.path.join(FONTS_DIR, filename)
        download(font_url, dest)
        local_css = local_css.replace(font_url, f"./{filename}")
    with open(os.path.join(FONTS_DIR, "fonts.css"), "w", encoding="utf-8", newline="\n") as f:
        f.write(local_css)


STATIC_FOOTER = f"""
	<footer id="Footer" class="clearfix wafa-footer">
		<div class="widgets_wrapper wafa-footer__main">
			<div class="container">
				<div class="wafa-footer__grid">
					<div class="wafa-footer__brand">
						<a href="/" class="wafa-footer__logo">
							<img src="/wp-content/uploads/2022/01/Wafa-Enterprises-Logo-1-1.png" alt="Wafa Enterprises" width="200" height="75" loading="lazy">
						</a>
						<p class="wafa-footer__tagline">Major distributors of imported foods, beverages and consumer goods — import, manufacturing and nationwide distribution across Pakistan.</p>
						<a class="wafa-footer__cta" href="/contact/">Get in touch</a>
					</div>
					<nav class="wafa-footer__col" aria-label="Footer navigation">
						<h4>Quick Links</h4>
						<ul class="wafa-footer__links">
							<li><a href="/">Home</a></li>
							<li><a href="/about/">About</a></li>
							<li><a href="/partners/">Partners</a></li>
							<li><a href="/contact/">Contact</a></li>
						</ul>
					</nav>
					<div class="wafa-footer__col">
						<h4>Our Business</h4>
						<ul class="wafa-footer__links">
							<li><a href="/about/">Import &amp; Distribution</a></li>
							<li><a href="/partners/">Brand Partners</a></li>
							<li><a href="/services/">Services</a></li>
						</ul>
					</div>
					<div class="wafa-footer__col">
						<h4>Head Office</h4>
						<address class="wafa-footer__contact">
							<p class="wafa-footer__address">House # E-141-1, Street # 7,<br>New Super Town, Defence Road,<br>Lahore, Pakistan</p>
							<p class="wafa-footer__contact-row">
								<span class="wafa-footer__contact-icon" aria-hidden="true">&#9742;</span>
								<a href="tel:+924236621301">042-36621301</a>
							</p>
							<p class="wafa-footer__contact-row">
								<span class="wafa-footer__contact-icon" aria-hidden="true">&#9993;</span>
								{EMAIL_LINK}
							</p>
						</address>
						<p class="wafa-footer__branches"><strong>Lahore branches</strong> Defence &middot; Ichhra &middot; S &amp; H &middot; Model Town</p>
					</div>
				</div>
			</div>
		</div>
		<div class="footer_copy wafa-footer__bottom">
			<div class="container">
				<div class="wafa-footer__bottom-inner">
				<span class="copyright">Copyright &copy; {datetime.now().year} Wafa Enterprises, All rights reserved. Crafted with &#10084;&#65039; by <a href="https://azad.co/developer/" target="_blank" rel="noopener noreferrer">AzAd Solutions</a></span>
				<ul class="wafa-footer__bottom-links">
					<li><a href="/contact/">Contact</a></li>
					<li><a href="/about/">About</a></li>
					<li><a href="/partners/">Partners</a></li>
				</ul>
				</div>
			</div>
		</div>
	</footer>
</div>
<a id="back_to_top" class="button button_js sticky scroll" href="#" aria-label="Back to top"><i class="icon-up-open-big"></i></a>
<script id="static-back-to-top">
jQuery(function($) {
  var $btn = $('#back_to_top.sticky.scroll');
  if (!$btn.length) return;
  function update() {
    $btn.toggleClass('visible', $(window).scrollTop() > 200);
  }
  $(window).on('scroll', update);
  update();
});
</script>
<script src="/assets/js/mfn-config.js"></script>
<script src="/wp-content/themes/betheme/js/plugins.min.js?ver=28.2.1"></script>
<script src="/wp-content/themes/betheme/js/menu.min.js?ver=28.2.1"></script>
<script src="/wp-content/themes/betheme/js/scripts.min.js?ver=28.2.1"></script>
<script src="/assets/js/wafa-mobile-menu.js?v=3" defer></script>
</body>
</html>
"""


def sanitize_html(content: str) -> str:
    """Remove WordPress error page appended by broken PHP footer."""
    marker = "<!DOCTYPE html>"
    first = content.find(marker)
    if first == -1:
        return content
    second = content.find(marker, first + len(marker))
    if second != -1:
        content = content[:second].rstrip()
    err = content.find('<body id="error-page">')
    if err != -1:
        content = content[:err].rstrip()
    if "</html>" not in content.lower():
        content = content.rstrip() + STATIC_FOOTER
    return content


def fix_html_content(content: str) -> str:
    content = sanitize_html(content)
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    for old, new in PAGE_LINKS:
        content = content.replace(f'href="{old}"', f'href="{new}"')
        content = content.replace(f"href='{old}'", f"href='{new}'")
    content = re.sub(
        r'href="//wafaenterprises\.com([^"]*)"',
        lambda m: f'href="{m.group(1) or "/"}"',
        content,
    )
    content = content.replace('href="https://wafaenterprises.com"', 'href="/"')
    content = content.replace("href='https://wafaenterprises.com'", "href='/'")
    content = re.sub(
        r"https://wafaenterprises\.com/wp-json/[^\"']+",
        "#",
        content,
    )
    content = re.sub(
        r"https://wafaenterprises\.com/xmlrpc\.php[^\"']*",
        "#",
        content,
    )
    content = re.sub(
        r"https://wafaenterprises\.com/\?p=\d+",
        "#",
        content,
    )
    content = re.sub(
        r'href="https://wafaenterprises\.com/feed/[^"]*"',
        'href="#"',
        content,
    )
    content = re.sub(
        r'href="https://wafaenterprises\.com/comments/feed/[^"]*"',
        'href="#"',
        content,
    )
    content = re.sub(
        r'href="https://wafaenterprises\.com/home/feed/[^"]*"',
        'href="#"',
        content,
    )
    content = re.sub(
        r'action="https://wafaenterprises\.com/"',
        'action="/"',
        content,
    )
    content = re.sub(
        r'href="https://wafaenterprises\.com/wp-json/"',
        'href="#"',
        content,
    )
    content = re.sub(
        r"https://wafaenterprises\.com/wp-json/oembed/[^\"']+",
        "#",
        content,
    )
    content = re.sub(
        r'<link[^>]+href=["\']//fonts\.googleapis\.com[^"\']*["\'][^>]*>\s*',
        "",
        content,
        flags=re.IGNORECASE,
    )
    content = re.sub(
        r'<link[^>]+href=["\']https://fonts\.googleapis\.com[^"\']*["\'][^>]*>\s*',
        "",
        content,
        flags=re.IGNORECASE,
    )
    content = content.replace('<link rel="dns-prefetch" href="//fonts.googleapis.com">', "")
    content = content.replace('<link rel="dns-prefetch" href="//fonts.googleapis.com" />', "")
    content = re.sub(
        r"url\(/cf-fonts/s/lato/[^)]+\)",
        f'url("{LOCAL_FONTS_CSS}")',
        content,
    )
    content = re.sub(
        r"@font-face\s*\{[^}]*url\(/cf-fonts/[^}]+\}",
        "",
        content,
    )
    content = re.sub(r'<style id="static-layout-fix">[\s\S]*?</style>\s*', "", content)
    font_link = f'<link rel="stylesheet" href="{LOCAL_FONTS_CSS}" media="all">\n'
    head_end = content.lower().find("</head>")
    if head_end != -1:
        inject = (font_link if LOCAL_FONTS_CSS not in content else "") + LAYOUT_FIX
        content = content[:head_end] + inject + content[head_end:]
    content = re.sub(
        r'<script src="/cdn-cgi/scripts/[^"]+"[^>]*></script>\s*',
        "",
        content,
    )
    content = fix_emails(content)
    content = re.sub(
        r"https://wafaenterprises\.com/wp-content/uploads/",
        "/wp-content/uploads/",
        content,
    )
    content = re.sub(
        r"https://www\.googletagmanager\.com/gtag/js[^\"']*",
        "",
        content,
    )
    content = re.sub(
        r"<script>\s*window\.dataLayer[^<]*gtag\([^<]*</script>\s*",
        "",
        content,
        flags=re.DOTALL,
    )
    return content


def fix_all_html() -> int:
    changed = 0
    for dirpath, _, files in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        if rel.startswith(("scripts", ".git", "wp-includes", "wp-content")):
            continue
        for fname in files:
            if not fname.endswith(".html"):
                continue
            path = os.path.join(dirpath, fname)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                original = f.read()
            content = fix_html_content(original)
            if content != original:
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(content)
                changed += 1
    return changed


def collect_asset_refs() -> set[str]:
    refs = set()
    for dirpath, _, files in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        if rel.startswith(("scripts", ".git")):
            continue
        for fname in files:
            if not fname.endswith((".html", ".css", ".js")):
                continue
            with open(os.path.join(dirpath, fname), "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            for m in re.finditer(
                r'(?:href|src|url)\(["\']?(/wp-(?:content|includes)/[^"\')\s?#]+)',
                content,
            ):
                path = m.group(1).split("?")[0]
                if "${" not in path:
                    refs.add(path)
            for m in re.finditer(r"/wp-content/uploads/[^\s\"'<>?)]+", content):
                refs.add(m.group(0).split("?")[0])
    return refs


def download_assets(refs: set[str]) -> int:
    ok = 0
    for path in sorted(refs):
        dest = path.lstrip("/").replace("/", os.sep)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            continue
        url = BASE_URL + path
        if download(url, dest):
            ok += 1
        time.sleep(0.1)
    return ok


def main():
    print("=== Download pages ===")
    pages = fetch_sitemap_pages()
    print(f"Pages: {pages}")
    n_pages = download_pages(pages)

    print("\n=== Fix HTML URLs ===")
    n_fixed = fix_all_html()
    print(f"Updated {n_fixed} HTML files")

    print("\n=== Download Lato fonts ===")
    ensure_lato_fonts()

    print("\n=== Download assets (pass 1) ===")
    refs = collect_asset_refs()
    n_assets = download_assets(refs)

    print("\n=== Re-fix HTML after asset scan ===")
    fix_all_html()

    print("\n=== Download assets (pass 2) ===")
    refs2 = collect_asset_refs()
    n_assets2 = download_assets(refs2)

    print(f"\nDone: {n_pages} pages, {n_assets + n_assets2} assets downloaded")


if __name__ == "__main__":
    main()
