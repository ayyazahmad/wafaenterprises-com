#!/usr/bin/env python3
"""Apply Google Analytics and full SEO meta tags to all static HTML pages."""
import html
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SITE_URL = "https://wafaenterprises.com"
GA_ID = "G-47Q89BQC69"
OG_IMAGE = f"{SITE_URL}/wp-content/uploads/2022/01/Wafa-Enterprises-Logo-1-1.png"
LOGO_URL = OG_IMAGE
TODAY = date.today().isoformat()

PAGE_SEO = {
    "/": {
        "title": "Wafa Enterprises | Food Distribution & Import in Lahore, Pakistan",
        "description": "Wafa Enterprises is a leading distributor of imported foods, beverages and consumer goods in Lahore. Import, manufacturing and nationwide distribution across Pakistan.",
        "keywords": "Wafa Enterprises, food distributor Lahore, imported food Pakistan, beverage distributor, consumer goods distribution",
        "og_type": "website",
    },
    "/about/": {
        "title": "About Wafa Enterprises | Food Distribution Company in Lahore",
        "description": "Learn about Wafa Enterprises — our vision, mission, leadership team and 500+ retail partnerships serving Lahore and Pakistan with quality food brands.",
        "keywords": "about Wafa Enterprises, food distribution company, Lahore distributor, WAFA team",
        "og_type": "article",
    },
    "/partners/": {
        "title": "Our Partners | Wafa Enterprises Brand Portfolio",
        "description": "Explore Wafa Enterprises partners and brands including KittyKat, Suree, Euro Cake, Tiffany, Move and more imported and local food products.",
        "keywords": "Wafa Enterprises partners, food brands Pakistan, KittyKat, Suree, Euro Cake, Tiffany wafers",
        "og_type": "article",
    },
    "/contact/": {
        "title": "Contact Wafa Enterprises | Lahore Head Office & Branches",
        "description": "Contact Wafa Enterprises in Lahore. Head office on Defence Road, phone 042-36621301. Reach our Defence, Ichhra, S&H and Model Town branches.",
        "keywords": "contact Wafa Enterprises, Lahore food distributor phone, Defence Road Lahore",
        "og_type": "website",
    },
    "/services/": {
        "title": "Services | Import, Distribution & Manufacturing | Wafa Enterprises",
        "description": "Wafa Enterprises services include food import, nationwide distribution, warehousing and brand marketing for consumer goods across Pakistan.",
        "keywords": "food import services, distribution Lahore, FMCG distribution Pakistan",
        "og_type": "article",
    },
}

ORGANIZATION_JSONLD = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": f"{SITE_URL}/#organization",
    "name": "Wafa Enterprises",
    "url": SITE_URL,
    "logo": LOGO_URL,
    "image": OG_IMAGE,
    "description": "Major distributor of imported foods, beverages and consumer goods in Lahore, Pakistan.",
    "telephone": "+92-42-36621301",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "House # E-141-1, Street # 7, New Super Town, Defence Road",
        "addressLocality": "Lahore",
        "addressCountry": "PK",
    },
    "areaServed": "Pakistan",
    "sameAs": [],
}

WEBSITE_JSONLD = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": f"{SITE_URL}/#website",
    "url": SITE_URL,
    "name": "Wafa Enterprises",
    "publisher": {"@id": f"{SITE_URL}/#organization"},
    "inLanguage": "en-US",
}

GA_SNIPPET = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>
"""


def page_path_from_file(path: str) -> str:
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/"


def breadcrumb_jsonld(path: str, title: str) -> dict | None:
    if path == "/":
        return None
    crumbs = [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
    ]
    label = title.split("|")[0].strip()
    crumbs.append(
        {"@type": "ListItem", "position": 2, "name": label, "item": f"{SITE_URL}{path}"}
    )
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": crumbs,
    }


def build_seo_block(path: str, seo: dict) -> str:
    url = f"{SITE_URL}/" if path == "/" else f"{SITE_URL}{path.rstrip('/')}/"
    title = seo["title"]
    desc = seo["description"]
    keywords = seo["keywords"]
    og_type = seo["og_type"]

    schemas = [
        ORGANIZATION_JSONLD,
        WEBSITE_JSONLD,
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": title,
            "description": desc,
            "isPartOf": {"@id": f"{SITE_URL}/#website"},
            "about": {"@id": f"{SITE_URL}/#organization"},
            "inLanguage": "en-US",
            "dateModified": TODAY,
        },
    ]
    bc = breadcrumb_jsonld(path, title)
    if bc:
        schemas.append(bc)

    jsonld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
        for s in schemas
    )

    return f"""{GA_SNIPPET}<meta name="description" content="{html.escape(desc, quote=True)}" />
<meta name="keywords" content="{html.escape(keywords, quote=True)}" />
<meta name="author" content="Wafa Enterprises" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="theme-color" content="#366ec2" />
<link rel="canonical" href="{url}" />
<link rel="alternate" hreflang="en" href="{url}" />
<link rel="alternate" hreflang="x-default" href="{url}" />
<meta property="og:locale" content="en_US" />
<meta property="og:type" content="{og_type}" />
<meta property="og:title" content="{html.escape(title, quote=True)}" />
<meta property="og:description" content="{html.escape(desc, quote=True)}" />
<meta property="og:url" content="{url}" />
<meta property="og:site_name" content="Wafa Enterprises" />
<meta property="og:image" content="{OG_IMAGE}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{html.escape(title, quote=True)}" />
<meta name="twitter:description" content="{html.escape(desc, quote=True)}" />
<meta name="twitter:image" content="{OG_IMAGE}" />
{jsonld}
"""


def clean_head(content: str) -> str:
    content = re.sub(
        r"<!-- Global site tag \(gtag\.js\)[\s\S]*?<script async src=\"\"></script>\s*",
        "",
        content,
    )
    content = re.sub(
        r"<!-- Google tag \(gtag\.js\)[\s\S]*?gtag\('config', '[^']+'\);\s*</script>\s*",
        "",
        content,
    )
    content = re.sub(r'<meta name="description"[^>]*>\s*', "", content)
    content = re.sub(r'<meta name="keywords"[^>]*>\s*', "", content)
    content = re.sub(r'<meta name="author"[^>]*>\s*', "", content)
    content = re.sub(r'<meta name="theme-color"[^>]*>\s*', "", content)
    content = re.sub(r'<meta property="og:[^"]+"[^>]*>\s*', "", content)
    content = re.sub(r'<meta name="twitter:[^"]+"[^>]*>\s*', "", content)
    content = re.sub(
        r'<script type="application/ld\+json">[\s\S]*?</script>\s*',
        "",
        content,
    )
    content = re.sub(r'<link rel="canonical"[^>]*>\s*', "", content)
    content = re.sub(r'<link rel="alternate" hreflang="[^"]+"[^>]*>\s*', "", content)
    content = re.sub(r'<meta name="robots"[^>]*>\s*', "", content)
    content = re.sub(
        r"<meta name='robots' content='max-image-preview:large' />\s*",
        "",
        content,
    )
    content = re.sub(
        r'<meta name="generator" content="WordPress[^"]*" />\s*',
        "",
        content,
    )
    content = re.sub(
        r'<meta name="generator" content="Powered by[^"]*" />\s*',
        "",
        content,
    )
    return content


def apply_to_html(path: str) -> bool:
    page_path = page_path_from_file(path)
    seo = PAGE_SEO.get(page_path)
    if not seo:
        return False

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    content = clean_head(content)
    content = re.sub(r"<title>[^<]*</title>", f"<title>{seo['title']}</title>", content, count=1)

    block = build_seo_block(page_path, seo)
    insert_after = re.search(r"<meta charset=\"UTF-8\"\s*/>\s*", content, re.I)
    if insert_after:
        pos = insert_after.end()
        content = content[:pos] + "\n" + block + content[pos:]
    else:
        content = content.replace("<head>", "<head>\n" + block, 1)

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return True


def write_sitemap() -> None:
    urls = []
    for path in PAGE_SEO:
        loc = f"{SITE_URL}/" if path == "/" else f"{SITE_URL}{path.rstrip('/')}/"
        priority = "1.0" if path == "/" else "0.8"
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n    <priority>{priority}</priority>\n  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    with open("sitemap.xml", "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)


def write_robots() -> None:
    content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    with open("robots.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


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
            if apply_to_html(fpath):
                changed += 1
                print(f"SEO  {os.path.relpath(fpath, ROOT)}")
    write_sitemap()
    write_robots()
    print(f"\nUpdated {changed} pages, sitemap.xml and robots.txt")


if __name__ == "__main__":
    main()
