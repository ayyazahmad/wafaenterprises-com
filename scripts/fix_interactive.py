#!/usr/bin/env python3
"""Fix hero slider init and sticky back-to-top for static export."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BACK_TO_TOP_OLD = (
    '<a id="back_to_top" class="button button_js" href="#" '
    'aria-label="Back to top"><i class="icon-up-open-big"></i></a>'
)
BACK_TO_TOP_NEW = (
    '<a id="back_to_top" class="button button_js sticky scroll" href="#" '
    'aria-label="Back to top"><i class="icon-up-open-big"></i></a>'
)

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

WAFA_HOME_CSS = '<link rel="stylesheet" href="/assets/css/wafa-home.css" media="all" />\n'
WAFA_FOOTER_CSS = '<link rel="stylesheet" href="/assets/css/wafa-footer.css?v=6" media="all" />\n'
WAFA_HERO_JS = '<script src="/assets/js/wafa-hero-slider.js" defer></script>\n'

ICONS_CSS_LINK = (
    '<link rel="stylesheet" id="mfn-icons-css" '
    'href="/wp-content/themes/betheme/fonts/mfn/icons.css?ver=28.2.1" media="all" />\n'
)

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


def strip_old_fixes(content: str) -> str:
    content = re.sub(r'<style id="static-interactive-fix">[\s\S]*?</style>\s*', "", content)
    content = re.sub(r'<link rel="stylesheet" id="mfn-icons-css"[^>]*>\s*', "", content)
    content = re.sub(r'<script id="static-back-to-top">[\s\S]*?</script>\s*', "", content)
    content = re.sub(r'<script id="revslider11-init">[\s\S]*?</script>\s*', "", content)
    return content


def inject_before_first_head_close(content: str, block: str) -> str:
    if block.strip() in content:
        return content
    return content.replace("</head>", block + "\n</head>", 1)


def inject_icons_css(content: str) -> str:
    if ICONS_CSS_LINK.strip() in content:
        return content
    marker = '<link rel=\'stylesheet\' id=\'mfn-be-css\''
    if marker in content:
        return content.replace(marker, ICONS_CSS_LINK + marker, 1)
    return inject_before_first_head_close(content, ICONS_CSS_LINK)


def inject_before_betheme_scripts(content: str, block: str) -> str:
    if block.strip() in content:
        return content
    marker = '<script src="/wp-content/themes/betheme/js/scripts.min.js'
    if marker in content:
        return content.replace(marker, marker, 1) + ""  # no-op placeholder
    marker2 = '<script src="/wp-content/themes/betheme/js/plugins.min.js'
    if marker2 in content:
        return content.replace(marker2, block + marker2, 1)
    return content.replace("</body>", block + "</body>", 1)


def inject_after_scripts(content: str, block: str) -> str:
    if block.strip() in content:
        return content
    marker = '<script src="/wp-content/themes/betheme/js/scripts.min.js?ver=28.2.1"></script>'
    if marker in content:
        return content.replace(marker, marker + "\n" + block, 1)
    return inject_before_betheme_scripts(content, block)


def inject_home_assets(content: str) -> str:
    if WAFA_HOME_CSS.strip() not in content:
        content = inject_before_first_head_close(content, WAFA_HOME_CSS)
    if WAFA_HERO_JS.strip() not in content:
        content = inject_after_scripts(content, WAFA_HERO_JS)
    return content


def patch_file(path: str, is_home: bool) -> bool:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    original = content
    content = strip_old_fixes(content)
    content = content.replace(BACK_TO_TOP_OLD, BACK_TO_TOP_NEW)
    content = inject_icons_css(content)
    content = inject_before_first_head_close(content, INTERACTIVE_CSS)
    if WAFA_FOOTER_CSS.strip() not in content:
        content = inject_before_first_head_close(content, WAFA_FOOTER_CSS)
    if is_home:
        content = inject_home_assets(content)
    content = inject_after_scripts(content, BACK_TO_TOP_JS)

    if content == original:
        return False

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return True


def main() -> None:
    changed = 0
    for dirpath, _, files in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        if rel.startswith(("scripts", ".git", "wp-includes", "wp-content")):
            continue
        for fname in files:
            if fname != "index.html":
                continue
            fpath = os.path.join(dirpath, fname)
            is_home = os.path.normpath(dirpath) == os.path.normpath(ROOT)
            if patch_file(fpath, is_home):
                changed += 1
                print(f"fixed  {os.path.relpath(fpath, ROOT)}")
    print(f"\nUpdated {changed} pages")


if __name__ == "__main__":
    main()
