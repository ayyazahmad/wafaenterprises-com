#!/usr/bin/env python3
"""Replace Revolution Slider with custom hero; clean home page assets."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")

SLIDES = [
    ("slide-1.jpg", "KittyKat Thailand — imported pet food"),
    ("slide-2.jpg", "Suree — premium sauces and condiments"),
    ("slide-3.jpg", "Zingies — snacks and confectionery"),
    ("slide-4.jpg", "Move — fudge and toffee manufacturing"),
    ("slide-5.jpg", "Tiffany — wafers and cream products"),
]

HERO_HTML = """
<div class="mfn-main-slider wafa-hero-wrap">
\t<section class="wafa-hero" data-wafa-hero aria-label="Featured brands carousel" tabindex="0">
\t\t<div class="wafa-hero__track">
{slides}
\t\t</div>
\t\t<button type="button" class="wafa-hero__nav wafa-hero__nav--prev" aria-label="Previous slide">&#8249;</button>
\t\t<button type="button" class="wafa-hero__nav wafa-hero__nav--next" aria-label="Next slide">&#8250;</button>
\t\t<div class="wafa-hero__dots" role="tablist" aria-label="Slide navigation">
{dots}
\t\t</div>
\t</section>
</div>
"""

INTERACTIVE_CSS = """
<style id="static-interactive-fix">
body.template-slider .mfn-main-slider { min-height: 0; margin: 0; padding: 0; }
body.template-slider #Header_wrapper { min-height: 0; }
#back_to_top.sticky.scroll { opacity: 0; transition: opacity 0.3s ease-in-out; }
#back_to_top.sticky.scroll.visible,
#back_to_top.sticky.scroll:hover,
#back_to_top.sticky.scroll:focus { opacity: 1 !important; }
#back_to_top.sticky {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 9001;
  background: #325aa0 !important;
  color: #fff !important;
}
#back_to_top.sticky i:before { color: #fff; font-family: mfn-icons !important; }
</style>
"""

BACK_TO_TOP_JS = """
<script id="static-back-to-top">
(function() {
  function update() {
    var btn = document.getElementById('back_to_top');
    if (!btn) return;
    btn.classList.toggle('visible', window.scrollY > 200);
  }
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('load', update);
  update();
})();
</script>
"""

BRAND_PLACEHOLDERS = {
    "Sabiniya": "Sabiniya",
    "MAXIUMS": "Maxium's",
    "Al-Kareem Dates": "Al-Kareem",
}


def build_hero() -> str:
    slide_lines = []
    dot_lines = []
    for i, (fname, alt) in enumerate(SLIDES):
        active = " is-active" if i == 0 else ""
        hidden = "false" if i == 0 else "true"
        loading = ' loading="eager" fetchpriority="high"' if i == 0 else ' loading="lazy"'
        slide_lines.append(
            f'\t\t\t<div class="wafa-hero__slide{active}" aria-hidden="{hidden}">'
            f'<img src="/images/slides/{fname}" alt="{alt}" width="1240" height="520"{loading}></div>'
        )
        dot_active = " is-active" if i == 0 else ""
        selected = "true" if i == 0 else "false"
        dot_lines.append(
            f'\t\t\t<button type="button" class="wafa-hero__dot{dot_active}" '
            f'data-index="{i}" role="tab" aria-selected="{selected}" '
            f'aria-label="Slide {i + 1}"></button>'
        )
    return HERO_HTML.format(slides="\n".join(slide_lines), dots="\n".join(dot_lines))


def strip_revslider(content: str) -> str:
    content = re.sub(
        r'<div class="mfn-main-slider mfn-rev-slider">[\s\S]*?<!-- END REVOLUTION SLIDER -->\s*</div>',
        build_hero().strip(),
        content,
        count=1,
    )
    content = re.sub(
        r'<script id="tp-tools-js"[^>]*></script>\s*',
        "",
        content,
    )
    content = re.sub(
        r'<script id="revmin-js"[^>]*></script>\s*',
        "",
        content,
    )
    content = re.sub(r'<script>function setREVStartSize[\s\S]*?</script>\s*', "", content)
    content = re.sub(r'<script id="revslider11-init">[\s\S]*?</script>\s*', "", content)
    return content


def update_interactive_css(content: str) -> str:
    content = re.sub(
        r'<style id="static-interactive-fix">[\s\S]*?</style>\s*',
        INTERACTIVE_CSS.strip() + "\n",
        content,
        count=1,
    )
    return content


def ensure_assets(content: str) -> str:
    css = '<link rel="stylesheet" href="/assets/css/wafa-home.css?v=3" media="all" />'
    js = '<script src="/assets/js/wafa-hero-slider.js" defer></script>'
    if css not in content:
        content = content.replace("</head>", css + "\n</head>", 1)
    if js not in content:
        marker = '<script id="static-back-to-top">'
        if marker in content:
            content = content.replace(marker, js + "\n" + marker, 1)
        else:
            content = content.replace("</body>", js + "\n</body>", 1)
    return content


def fix_brand_placeholders(content: str) -> str:
    for title, label in BRAND_PLACEHOLDERS.items():
        pat = (
            rf'(<div class="icon_box icon_position_top no_border">)'
            rf'(<div class="desc_wrapper"><h4 class="title ">{re.escape(title)}</h4></div></div>)'
        )
        rep = (
            rf'\1<div class="brand-placeholder" aria-hidden="true">{label}</div>'
            rf'<div class="desc_wrapper"><h4 class="title ">{title}</h4></div></div>'
        )
        content = re.sub(pat, rep, content)
    return content


def main() -> None:
    with open(INDEX, encoding="utf-8", errors="ignore") as f:
        content = f.read()

    original = content
    content = strip_revslider(content)
    content = update_interactive_css(content)
    content = ensure_assets(content)
    content = fix_brand_placeholders(content)

    if BACK_TO_TOP_JS.strip() not in content:
        content = content.replace(
            '<script src="/wp-content/themes/betheme/js/scripts.min.js?ver=28.2.1"></script>',
            '<script src="/wp-content/themes/betheme/js/scripts.min.js?ver=28.2.1"></script>\n'
            + BACK_TO_TOP_JS.strip(),
        )

    if content == original:
        print("No changes needed")
        return

    with open(INDEX, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("Rebuilt home page hero slider")


if __name__ == "__main__":
    main()
