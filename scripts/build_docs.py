#!/usr/bin/env python3
"""Build the password-gated GitHub Pages site under docs/ from the latest LP.

Usage: python3 scripts/build_docs.py <password>

- Inlines css/style.css and js/main.js into index.html (and thanks.html).
- Rewrites CSS image paths (../Image -> Image) so they resolve under docs/.
- Encrypts the inlined index.html with AES-256-CBC (PBKDF2/SHA-256, 200000 iters)
  via openssl and embeds the base64 payload into the gate template
  (reused from HEAD:docs/index.html, preserving its UI + iframe rendering).
- Writes docs/index.html (gate), docs/thanks.html (plain inlined), docs/Image/.
"""
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def inline_css():
    css = read("css/style.css").replace("../Image/", "Image/")
    return "<style>\n" + css + "\n</style>"


def inline_js():
    js = read("js/main.js").replace("</script>", "<\\/script>")
    return "<script>\n" + js + "\n</script>"


def inline_page(html):
    html = re.sub(
        r'<link[^>]*href="\./css/style\.css"[^>]*/?>', inline_css(), html
    )
    html = re.sub(
        r'<script[^>]*src="\./js/main\.js"[^>]*></script>', inline_js(), html
    )
    return html


def encrypt(plaintext, password):
    out = subprocess.run(
        [
            "openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "200000",
            "-md", "sha256", "-salt", "-base64", "-A", "-pass", "pass:" + password,
        ],
        input=plaintext.encode("utf-8"),
        capture_output=True,
        check=True,
    )
    return out.stdout.decode("ascii").strip()


def gate_template():
    with open(os.path.join(ROOT, "scripts", "gate_template.html"), encoding="utf-8") as f:
        return f.read()


def main():
    if len(sys.argv) < 2 or not sys.argv[1]:
        sys.exit("usage: build_docs.py <password>")
    password = sys.argv[1]

    # 1. Encrypt the inlined LP and embed into the gate template.
    inlined = inline_page(read("index.html"))
    cipher = encrypt(inlined, password)
    tmpl = gate_template()
    gate = re.sub(r'var CIPHER_B64 = "[^"]*";',
                  'var CIPHER_B64 = "%s";' % cipher, tmpl, count=1)
    if 'var CIPHER_B64 = "%s"' % cipher not in gate:
        sys.exit("failed to inject CIPHER_B64 into gate template")

    # 2. Recreate docs/.
    if os.path.isdir(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(DOCS)
    with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as f:
        f.write(gate)

    # 3. Thanks page (plain inlined; low sensitivity, reached via form submit).
    with open(os.path.join(DOCS, "thanks.html"), "w", encoding="utf-8") as f:
        f.write(inline_page(read("thanks.html")))

    # 4. Images.
    shutil.copytree(os.path.join(ROOT, "Image"), os.path.join(DOCS, "Image"))

    # 5. Static downloadable assets (e.g. the PDF guide linked from the LP).
    for name in ("yakusoku-tegata-guide.pdf",):
        src = os.path.join(ROOT, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(DOCS, name))

    print("built docs/ (cipher %d bytes)" % len(cipher))


if __name__ == "__main__":
    main()
