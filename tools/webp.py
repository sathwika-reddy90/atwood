"""Writes a WebP copy beside every JPEG in assets/img (including the -800 copies), for the build to serve first.

Run after adding photographs:  python3 tools/webp.py      (needs Pillow: pip install Pillow)

The build itself does not need Pillow: tools/build.py only checks whether a .webp sits beside each .jpg and, if so,
serves it through <picture> with the JPEG as the fallback. Existing WebP files newer than their JPEG are skipped.
"""
import os
import sys

from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")
QUALITY = 80

made = skipped = 0
before = after = 0
for folder, _, files in os.walk(ROOT):
    for name in sorted(files):
        if not name.lower().endswith(".jpg"):
            continue
        src = os.path.join(folder, name)
        dst = src[:-4] + ".webp"
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            skipped += 1
            continue
        with Image.open(src) as im:
            im.save(dst, "WEBP", quality=QUALITY, method=6)
        before += os.path.getsize(src)
        after += os.path.getsize(dst)
        made += 1

print(f"{made} written, {skipped} up to date", file=sys.stderr)
if made:
    print(f"JPEG {before // 1024} KB -> WebP {after // 1024} KB ({100 - after * 100 // before}% smaller)", file=sys.stderr)
