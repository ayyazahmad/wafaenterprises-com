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

@media (max-width: 1239px) {
  #Top_bar .top_bar_left {
    display: flex;
    flex-wrap: nowrap;
    align-items: center;
    justify-content: flex-start;
    position: relative !important;
    width: 100% !important;
    float: none !important;
    min-height: 60px;
    padding: 0 !important;
    box-sizing: border-box;
    z-index: 100010;
  }
  #Top_bar .top_bar_left .logo {
    flex: 0 1 auto;
    max-width: calc(100% - 52px);
    width: auto !important;
    float: none !important;
    margin: 0 !important;
    padding: 0 0 0 8px !important;
    text-align: left !important;
    position: static !important;
  }
  #Top_bar .top_bar_left .logo #logo,
  #Top_bar .top_bar_left .logo .custom-logo-link {
    margin: 6px 0 !important;
    padding: 0 !important;
    height: auto !important;
    line-height: normal !important;
  }
  #Top_bar .menu_wrapper {
    display: flex;
    flex: 0 0 auto;
    align-items: center;
    justify-content: flex-end;
    margin-left: auto !important;
    margin-right: 0 !important;
    padding: 0 8px 0 0 !important;
    position: static !important;
    float: none !important;
    width: auto !important;
  }
  body.mobile-header-mini #Top_bar a.responsive-menu-toggle,
  #Top_bar a.responsive-menu-toggle {
    display: flex !important;
    align-items: center;
    justify-content: center;
    position: relative !important;
    top: auto !important;
    right: auto !important;
    left: auto !important;
    margin: 0 !important;
    margin-top: 0 !important;
    width: 44px;
    height: 44px;
    flex: 0 0 44px;
    z-index: 100013;
    float: none !important;
  }
  #Top_bar a.responsive-menu-toggle i {
    font-family: mfn-icons !important;
    font-size: 22px;
    line-height: 1;
  }
  #Top_bar a.responsive-menu-toggle.active i.icon-cancel-fine:before {
    content: '\\e963';
  }
  #Top_bar #menu {
    display: none !important;
    position: absolute !important;
    top: 100%;
    left: 0;
    right: 0;
    width: 100% !important;
    margin: 0;
    padding: 8px 0;
    background: #366ec2;
    border-radius: 0 0 8px 8px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.22);
    z-index: 100012;
    max-height: calc(100vh - 120px);
    overflow-y: auto;
    float: none !important;
  }
  body.wafa-mobile-menu-open #Top_bar #menu {
    display: block !important;
  }
  body.wafa-mobile-menu-open #Top_bar {
    position: relative;
    z-index: 100015;
  }
  #Top_bar #menu ul { width: 100%; float: none; }
  #Top_bar #menu ul li { width: 100%; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
  #Top_bar #menu ul li:last-child { border-bottom: 0; }
  #Top_bar #menu ul li a {
    display: block;
    padding: 0 18px;
    color: #fff !important;
    line-height: 44px;
  }
  #Top_bar #menu ul li a span { color: inherit; border: 0; line-height: 44px; }
  #Top_bar #menu ul li.current-menu-item > a,
  #Top_bar #menu ul li.current_page_item > a { background: rgba(0, 0, 0, 0.12); }
}

#wafa-mobile-menu-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 100009;
}
#wafa-mobile-menu-overlay[hidden] { display: none !important; }
body.wafa-mobile-menu-open { overflow: hidden; }
</style>
"""

MFN_CONFIG_JS = '<script src="/assets/js/mfn-config.js"></script>\n'
WAFA_MOBILE_MENU_JS = '<script src="/assets/js/wafa-mobile-menu.js?v=3" defer></script>\n'

WAFA_HOME_CSS = '<link rel="stylesheet" href="/assets/css/wafa-home.css?v=3" media="all" />\n'
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
    content = re.sub(r'<script src="/assets/js/mfn-config\.js"></script>\s*', "", content)
    content = re.sub(r'<script src="/assets/js/wafa-mobile-menu\.js"[^>]*></script>\s*', "", content)
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


def inject_before_plugins(content: str, block: str) -> str:
    if block.strip() in content:
        return content
    marker = '<script src="/wp-content/themes/betheme/js/plugins.min.js'
    if marker in content:
        return content.replace(marker, block + marker, 1)
    return inject_before_betheme_scripts(content, block)


def inject_mfn_config(content: str) -> str:
    return inject_before_plugins(content, MFN_CONFIG_JS)


def inject_before_betheme_scripts(content: str, block: str) -> str:
    if block.strip() in content:
        return content
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
    content = inject_mfn_config(content)
    content = inject_after_scripts(content, BACK_TO_TOP_JS)
    content = inject_after_scripts(content, WAFA_MOBILE_MENU_JS)

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
