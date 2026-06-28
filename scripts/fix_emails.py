#!/usr/bin/env python3
"""Restore visible email addresses and strip Cloudflare obfuscation markup."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

EMAIL = "info@wafaenterprises.com"
EMAIL_ENC = "info&#64;wafaenterprises.com"
EMAIL_LINK = (
    f'<!--email_off--><a href="mailto:{EMAIL}">{EMAIL_ENC}</a><!--/email_off-->'
)


def fix_emails(content: str) -> str:
    content = re.sub(
        r'<a\s+href="/cdn-cgi/l/email-protection#[^"]*"[^>]*>\s*'
        r'(?:<span class="__cf_email__"[^>]*>\[email(?:&#160;|\s)protected\]</span>'
        r'|\[email(?:&#160;|\s)protected\])\s*</a>',
        EMAIL_LINK,
        content,
        flags=re.IGNORECASE,
    )
    content = re.sub(
        r'<span class="__cf_email__"[^>]*>\[email(?:&#160;|\s)protected\]</span>',
        EMAIL_ENC,
        content,
        flags=re.IGNORECASE,
    )
    content = re.sub(
        r'\[email(?:&#160;|\s)protected\]',
        EMAIL_ENC,
        content,
        flags=re.IGNORECASE,
    )
    content = re.sub(
        r'href="/cdn-cgi/l/email-protection#[^"]*"',
        f'href="mailto:{EMAIL}"',
        content,
        flags=re.IGNORECASE,
    )

    def wrap_mailto(match: re.Match[str]) -> str:
        tag = match.group(0)
        if "<!--email_off-->" in tag:
            return tag
        tag = tag.replace(">info@wafaenterprises.com<", f">{EMAIL_ENC}<")
        return f"<!--email_off-->{tag}<!--/email_off-->"

    content = re.sub(
        r'<a\s+href="mailto:info@wafaenterprises\.com"[^>]*>.*?</a>',
        wrap_mailto,
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )

    content = content.replace("<!--email_off--><!--email_off-->", "<!--email_off-->")
    content = content.replace("<!--/email_off--><!--/email_off-->", "<!--/email_off-->")

    # Encode stray plain-text emails (keeps mailto hrefs intact).
    content = re.sub(
        rf"(?<![\w@/]){re.escape(EMAIL)}(?![\w@])",
        EMAIL_ENC,
        content,
    )
    content = content.replace(f"mailto:{EMAIL_ENC}", f"mailto:{EMAIL}")
    return content


def patch_html_files() -> int:
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
            updated = fix_emails(original)
            if updated != original:
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(updated)
                changed += 1
                print(f"fixed  {os.path.relpath(path, ROOT)}")
    return changed


if __name__ == "__main__":
    print(f"Updated {patch_html_files()} pages")
