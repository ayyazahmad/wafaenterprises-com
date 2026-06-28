#!/usr/bin/env python3
"""Improve About, Partners, Contact, and Services inner pages."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)
os.chdir(ROOT)

from fix_emails import EMAIL_LINK, fix_emails

PAGES_CSS = '<link rel="stylesheet" href="/assets/css/wafa-pages.css?v=2" media="all" />\n'
CONTACT_JS = '<script src="/assets/js/wafa-contact-form.js" defer></script>\n'

ABOUT_STATS = """
<ul class="wafa-stats" aria-label="Company highlights">
<li><strong>500+</strong><span>Retail partners nationwide</span></li>
<li><strong>80+</strong><span>Team members</span></li>
<li><strong>5,000</strong><span>Sq ft warehouse</span></li>
<li><strong>4</strong><span>Lahore branch locations</span></li>
</ul>
<div class="wafa-cards">
<div class="wafa-card"><h3>Our Vision</h3><p>To be Pakistan's most trusted name in imported foods and consumer goods — connecting global brands with retailers and families across the country.</p></div>
<div class="wafa-card"><h3>Our Mission</h3><p>Import, distribute and market quality products with reliable service, strong partnerships and nationwide reach from our Lahore headquarters.</p></div>
<div class="wafa-card"><h3>Our Values</h3><p>Integrity in every deal, consistency in delivery, and long-term relationships with brand owners, retailers and consumers we serve.</p></div>
</div>
"""

PARTNERS_INTRO = """
<div class="wafa-page-intro">
<h2 class="wafa-section-title">Brand partners we represent</h2>
<p>Wafa Enterprises partners with leading international and local food brands. We import, distribute and market these products across Pakistan through our nationwide retail network.</p>
</div>
"""

SERVICES_SECTION = """
<section class="section mcb-section wafa-services-section" style="padding-top:56px;padding-bottom:56px">
<div class="section_wrapper"><div class="container">
<div class="wafa-page-intro">
<h2 class="wafa-section-title">What we offer</h2>
<p>From sourcing imported goods to delivering them nationwide, Wafa Enterprises provides end-to-end distribution and brand support for food and consumer products across Pakistan.</p>
</div>
<div class="wafa-services-grid">
<article class="wafa-service-card">
<div class="wafa-service-card__icon"><img src="/wp-content/uploads/2016/10/home_surveyor_services1.png" alt="" width="44" height="42" loading="lazy"></div>
<h3>Import &amp; Sourcing</h3>
<p>We source quality imported foods, beverages and consumer goods from trusted international suppliers and handle customs clearance and inbound logistics.</p>
</article>
<article class="wafa-service-card">
<div class="wafa-service-card__icon"><img src="/wp-content/uploads/2016/10/home_surveyor_services2.png" alt="" width="44" height="42" loading="lazy"></div>
<h3>Nationwide Distribution</h3>
<p>Our fleet and sales network supply 500+ retail partners across Pakistan, from modern trade to traditional wholesale and mom-and-pop stores.</p>
</article>
<article class="wafa-service-card">
<div class="wafa-service-card__icon"><img src="/wp-content/uploads/2016/10/home_surveyor_services3.png" alt="" width="44" height="42" loading="lazy"></div>
<h3>Warehousing &amp; Logistics</h3>
<p>5,000 sq ft central warehouse near Lahore airport with daily dispatch, inventory management and cold-chain capable storage where required.</p>
</article>
<article class="wafa-service-card">
<div class="wafa-service-card__icon"><img src="/wp-content/uploads/2016/10/home_surveyor_services4.png" alt="" width="44" height="42" loading="lazy"></div>
<h3>Brand Marketing</h3>
<p>In-store activations, trade marketing and brand positioning to grow awareness and shelf presence for our partner brands in the Pakistani market.</p>
</article>
<article class="wafa-service-card">
<div class="wafa-service-card__icon"><img src="/wp-content/uploads/2016/10/home_surveyor_services5.png" alt="" width="44" height="42" loading="lazy"></div>
<h3>Retail Partnerships</h3>
<p>Long-term relationships with supermarkets, wholesalers and independent retailers — backed by dedicated sales teams and responsive account support.</p>
</article>
<article class="wafa-service-card">
<div class="wafa-service-card__icon"><img src="/wp-content/uploads/2016/10/home_surveyor_services2.png" alt="" width="44" height="42" loading="lazy"></div>
<h3>Manufacturing Support</h3>
<p>Local manufacturing and co-packing partnerships to complement imported lines and meet market demand for selected product categories.</p>
</article>
</div>
<div class="wafa-services-cta">
<h3>Ready to partner with us?</h3>
<p>Whether you are a brand owner or retailer, our team is here to help.</p>
<a class="button button_size_2" href="/contact/"><span class="button_label">Contact our team</span></a>
</div>
</div></div>
</section>
"""

CONTACT_FORM = """
<form id="wafa-contact-form" class="wafa-contact-form" action="#" method="post">
<div class="wafa-form-grid">
<div class="wafa-form-row">
<label for="wafa-name">Your name</label>
<input type="text" id="wafa-name" name="name" required placeholder="Full name" autocomplete="name">
</div>
<div class="wafa-form-row">
<label for="wafa-email">Your email</label>
<input type="email" id="wafa-email" name="email" required placeholder="you@company.com" autocomplete="email">
</div>
</div>
<div class="wafa-form-row">
<label for="wafa-subject">Subject</label>
<input type="text" id="wafa-subject" name="subject" placeholder="How can we help?">
</div>
<div class="wafa-form-row">
<label for="wafa-message">Message</label>
<textarea id="wafa-message" name="message" required placeholder="Tell us about your enquiry…"></textarea>
</div>
<button type="submit" class="button button_size_2"><span class="button_label">Send message</span></button>
<p class="wafa-contact-form__note">This opens your email app addressed to info@wafaenterprises.com</p>
</form>
"""

MAP_EMBED = """
<iframe class="wafa-map-embed" title="Wafa Enterprises head office location"
src="https://maps.google.com/maps?q=31.4697,74.2728&amp;z=15&amp;output=embed"
loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
"""

BRANCHES_HTML = """
<div class="wafa-branches">
<div class="wafa-branch"><strong>Defence branch</strong>Lahore</div>
<div class="wafa-branch"><strong>Ichhra branch</strong>Lahore</div>
<div class="wafa-branch"><strong>S &amp; H branch</strong>Lahore</div>
<div class="wafa-branch"><strong>Model Town branch</strong>Lahore</div>
</div>
"""

SOCIAL_HTML = """
<h2>Follow us</h2>
<a href="https://www.facebook.com/WAFAEnterprizes/" class="wafa-social-link" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><i class="icon-facebook"></i></a>
"""


def inject_css(content: str) -> str:
    content = re.sub(
        r'<link rel="stylesheet" href="/assets/css/wafa-pages\.css\?v=\d+" media="all" />\s*',
        "",
        content,
    )
    if PAGES_CSS.strip() not in content:
        marker = '<link rel="stylesheet" href="/assets/css/wafa-footer.css'
        if marker in content:
            content = content.replace(marker, PAGES_CSS + marker, 1)
        else:
            content = content.replace("</head>", PAGES_CSS + "</head>", 1)
    return content


def add_body_class(content: str) -> str:
    if "wafa-inner-page" in content:
        return content
    return re.sub(r'<body class="', '<body class="wafa-inner-page ', content, count=1)


def fix_about(content: str) -> str:
    if "wafa-stats" not in content:
        content = content.replace(
            "<h2>About Wafa Enterprises</h2>",
            "<h2>About Wafa Enterprises</h2>" + ABOUT_STATS,
            1,
        )
    content = re.sub(
        r'href="/cdn-cgi/l/email-protection[^"]*"',
        'href="mailto:info@wafaenterprises.com"',
        content,
    )
    content = content.replace(
        '<span class="button_label">Contact with us</span>',
        '<span class="button_label">Get in touch</span>',
        1,
    )
    content = content.replace(
        "<h2>Our Executives</h2>",
        '<h2 class="wafa-section-title">Our leadership</h2>',
        1,
    )
    return content


def fix_partners(content: str) -> str:
    if "wafa-page-intro" not in content:
        content = content.replace(
            '<div class="lshowcase-clear-both">&nbsp;</div><div class="lshowcase-logos ">',
            PARTNERS_INTRO + '<div class="lshowcase-logos">',
            1,
        )
    return content


def fix_services(content: str) -> str:
    if "wafa-services-grid" in content:
        return content
    pattern = (
        r'<div data-id="10" class="mfn-builder-content mfn-default-content-buider">'
        r'[\s\S]*?</section></div>'
    )
    replacement = (
        '<div data-id="10" class="mfn-builder-content mfn-default-content-buider">'
        + SERVICES_SECTION
        + "</div>"
    )
    content, n = re.subn(pattern, replacement, content, count=1)
    if n == 0:
        print("  WARN: services section not replaced")
    return content


def fix_contact(content: str) -> str:
    content = re.sub(
        r'<div class="google-map" id="google-map-area-6a415008dc526"[^>]*>&nbsp;</div>',
        MAP_EMBED.strip(),
        content,
        count=1,
    )
    content = re.sub(
        r'<div class="wpcf7 no-js"[\s\S]*?</div>\s*</div></div></div>',
        CONTACT_FORM + "</div></div></div>",
        content,
        count=1,
    )
    content = re.sub(
        r"You can use this webform or alternatively email us at[^<]*<a[^>]*>\[email&#160;protected\]</a>\.",
        'Send us a message below or email ' + EMAIL_LINK + ' directly. Include your name and contact details so we can respond quickly.',
        content,
        count=1,
    )
    content = re.sub(
        r'Write us: <a href="/cdn-cgi/l/email-protection[^"]*"><span class="__cf_email__"[^>]*>\[email&#160;protected\]</span></a>',
        'Write us: ' + EMAIL_LINK,
        content,
        count=1,
    )
    content = re.sub(
        r'Contact us: <span style="color: #141b26;">\+92 \(42\) 3662 1301</span>',
        'Contact us: <a href="tel:+924236621301">+92 (42) 3662 1301</a>',
        content,
        count=1,
    )
    if "wafa-branches" not in content:
        content = content.replace(
            '<hr class="no_line" style="margin: 0 auto 10px auto"/>',
            BRANCHES_HTML + '<hr class="no_line" style="margin: 0 auto 10px auto"/>',
            1,
        )
    content = re.sub(
        r'<h2>Social Links</h2>[\s\S]*?<a href="#" aria-label="button with icon" class="icon_bar  icon_bar_small" ><span class="t"><i class="icon-twitter"></i></span><span class="b"><i class="icon-twitter"></i></span></a>',
        SOCIAL_HTML.strip(),
        content,
        count=1,
    )
    if CONTACT_JS.strip() not in content:
        content = content.replace(
            '<script src="/wp-content/themes/betheme/js/plugins.min.js',
            CONTACT_JS + '<script src="/wp-content/themes/betheme/js/plugins.min.js',
            1,
        )
    return content


def patch_file(path: str, fixer) -> None:
    with open(path, encoding="utf-8") as f:
        content = f.read()
    original = content
    content = inject_css(content)
    content = add_body_class(content)
    content = fixer(content)
    content = fix_emails(content)
    if content != original:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"Updated {path}")
    else:
        print(f"No changes {path}")


def main() -> None:
    patch_file(os.path.join(ROOT, "about", "index.html"), fix_about)
    patch_file(os.path.join(ROOT, "partners", "index.html"), fix_partners)
    patch_file(os.path.join(ROOT, "services", "index.html"), fix_services)
    patch_file(os.path.join(ROOT, "contact", "index.html"), fix_contact)
    print("Done.")


if __name__ == "__main__":
    main()
