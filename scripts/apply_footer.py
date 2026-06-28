#!/usr/bin/env python3
"""Apply improved site footer to all HTML pages."""
import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

FOOTER_CSS = '<link rel="stylesheet" href="/assets/css/wafa-footer.css?v=6" media="all" />\n'

COPYRIGHT_HTML = (
    f"Copyright &copy; {datetime.now().year} Wafa Enterprises, All rights reserved. "
    f"Crafted with \u2764\ufe0f by "
    f'<a href="https://azad.co/developer/" target="_blank" rel="noopener noreferrer">AzAd Solutions</a>'
)

FOOTER_HTML = f"""\t<footer id="Footer" class="clearfix wafa-footer">
\t\t<div class="widgets_wrapper wafa-footer__main">
\t\t\t<div class="container">
\t\t\t\t<div class="wafa-footer__grid">
\t\t\t\t\t<div class="wafa-footer__brand">
\t\t\t\t\t\t<a href="/" class="wafa-footer__logo">
\t\t\t\t\t\t\t<img src="/wp-content/uploads/2022/01/Wafa-Enterprises-Logo-1-1.png" alt="Wafa Enterprises" width="200" height="75" loading="lazy">
\t\t\t\t\t\t</a>
\t\t\t\t\t\t<p class="wafa-footer__tagline">Major distributors of imported foods, beverages and consumer goods — import, manufacturing and nationwide distribution across Pakistan.</p>
\t\t\t\t\t\t<a class="wafa-footer__cta" href="/contact/">Get in touch</a>
\t\t\t\t\t</div>
\t\t\t\t\t<nav class="wafa-footer__col" aria-label="Footer navigation">
\t\t\t\t\t\t<h4>Quick Links</h4>
\t\t\t\t\t\t<ul class="wafa-footer__links">
\t\t\t\t\t\t\t<li><a href="/">Home</a></li>
\t\t\t\t\t\t\t<li><a href="/about/">About</a></li>
\t\t\t\t\t\t\t<li><a href="/partners/">Partners</a></li>
\t\t\t\t\t\t\t<li><a href="/contact/">Contact</a></li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</nav>
\t\t\t\t\t<div class="wafa-footer__col">
\t\t\t\t\t\t<h4>Our Business</h4>
\t\t\t\t\t\t<ul class="wafa-footer__links">
\t\t\t\t\t\t\t<li><a href="/about/">Import &amp; Distribution</a></li>
\t\t\t\t\t\t\t<li><a href="/partners/">Brand Partners</a></li>
\t\t\t\t\t\t\t<li><a href="/services/">Services</a></li>
\t\t\t\t\t\t</ul>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="wafa-footer__col">
\t\t\t\t\t\t<h4>Head Office</h4>
\t\t\t\t\t\t<address class="wafa-footer__contact">
\t\t\t\t\t\t\t<p class="wafa-footer__address">House # E-141-1, Street # 7,<br>New Super Town, Defence Road,<br>Lahore, Pakistan</p>
\t\t\t\t\t\t\t<p class="wafa-footer__contact-row">
\t\t\t\t\t\t\t\t<span class="wafa-footer__contact-icon" aria-hidden="true">&#9742;</span>
\t\t\t\t\t\t\t\t<a href="tel:+924236621301">042-36621301</a>
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t\t<p class="wafa-footer__contact-row">
\t\t\t\t\t\t\t\t<span class="wafa-footer__contact-icon" aria-hidden="true">&#9993;</span>
\t\t\t\t\t\t\t\t<a href="mailto:info@wafaenterprises.com">info@wafaenterprises.com</a>
\t\t\t\t\t\t\t</p>
\t\t\t\t\t\t</address>
\t\t\t\t\t\t<p class="wafa-footer__branches"><strong>Lahore branches</strong> Defence &middot; Ichhra &middot; S &amp; H &middot; Model Town</p>
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t\t<div class="footer_copy wafa-footer__bottom">
\t\t\t<div class="container">
\t\t\t\t<div class="wafa-footer__bottom-inner">
\t\t\t\t\t<span class="copyright">{COPYRIGHT_HTML}</span>
\t\t\t\t\t<ul class="wafa-footer__bottom-links">
\t\t\t\t\t\t<li><a href="/contact/">Contact</a></li>
\t\t\t\t\t\t<li><a href="/about/">About</a></li>
\t\t\t\t\t\t<li><a href="/partners/">Partners</a></li>
\t\t\t\t\t</ul>
\t\t\t\t</div>
\t\t\t</div>
\t\t</div>
\t</footer>"""


def inject_css(content: str) -> str:
    content = re.sub(
        r'<link rel="stylesheet" href="/assets/css/wafa-footer\.css[^"]*" media="all" />\s*',
        "",
        content,
    )
    if "</head>" in content:
        return content.replace("</head>", FOOTER_CSS + "</head>", 1)
    return content


def replace_footer(content: str) -> str:
    return re.sub(
        r'\t<footer id="Footer" class="clearfix[^"]*">[\s\S]*?\t</footer>',
        FOOTER_HTML,
        content,
        count=1,
    )


def patch_file(path: str) -> bool:
    with open(path, encoding="utf-8", errors="ignore") as f:
        content = f.read()
    original = content
    content = inject_css(content)
    content = replace_footer(content)
    if content == original:
        return False
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return True


def main() -> None:
    changed = 0
    for dirpath, _, files in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        if rel.startswith(("scripts", ".git", "wp-includes", "wp-content", "assets")):
            continue
        for fname in files:
            if fname != "index.html":
                continue
            fpath = os.path.join(dirpath, fname)
            if patch_file(fpath):
                changed += 1
                print(f"updated  {os.path.relpath(fpath, ROOT)}")
    print(f"\nFooter applied to {changed} pages")


if __name__ == "__main__":
    main()
