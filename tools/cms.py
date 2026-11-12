"""Journal posts from the Sanity CMS.

Project xbvaq1gt, dataset production, Studio https://atwood-dsigns.sanity.studio (code in studio/).
tools/build.py calls load_posts() and renders each post with render_body(). Standard library only, so the
build still needs nothing but python3.

Every style and block type in studio/schemaTypes/blockContent.ts has a case in render_body(), so an author
can't produce a layout the site has no answer for.
"""
import html
import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

# Public identifiers, not secrets: the dataset is public-read and drafts are never returned without a token.
SANITY = {
    "projectId": os.environ.get("SANITY_PROJECT_ID", "xbvaq1gt"),
    "dataset": os.environ.get("SANITY_DATASET", "production"),
    "apiVersion": "2025-10-01",
}

IMG = '{alt, caption, hotspot, "url": asset->url, "w": asset->metadata.dimensions.width, "h": asset->metadata.dimensions.height}'
QUERY = f'''*[_type == "post" && defined(slug.current) && publishedAt <= now()] | order(publishedAt desc) {{
  title, "slug": slug.current, excerpt, seoTitle, metaDescription, keywords,
  publishedAt, _updatedAt, featured, readTime,
  "author": author->{{name, role}},
  "categories": categories[]->title,
  "coverImage": coverImage{IMG},
  "heroImage": heroImage{IMG},
  body[]{{..., _type == "image" => {IMG}}}
}}'''

IST = timezone(timedelta(hours=5, minutes=30))
LADDER = [480, 800, 1200, 1600, 2400]

esc = lambda s: html.escape("" if s is None else str(s), quote=True)


def slugify(s):
    s = re.sub(r"[^a-z0-9\s-]", "", str(s).lower().strip())
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", s))


def youtube_id(url):
    """Same pattern as studio/youtube.ts, so a link the Studio accepts is one the site can embed."""
    m = re.search(r"(?:youtube(?:-nocookie)?\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/|live/)|youtu\.be/)([\w-]{11})", url or "")
    return m.group(1) if m else None


def ist_date(iso):
    """The calendar day in India: a post published at 00:30 IST is that day's."""
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(IST).date()


def fmt_date(d):
    return f"{d.day} {d.strftime('%B %Y')}"


# ------------------------------------------------------------------------------------------------ images
def focal(img):
    """The hotspot set in the Studio, as the object-position the site's .ph frames already use."""
    h = (img or {}).get("hotspot") or {}
    return f'{round(h.get("x", .5) * 100)}% {round(h.get("y", .5) * 100)}%'


def img_tag(img, sizes, lazy=True, alt=None, extra=""):
    """Sanity's image CDN resizes on request, so one URL per ladder width."""
    base, w = img["url"], img.get("w") or 0
    widths = [x for x in LADDER if x < w] + ([w] if w else [])
    srcset = f' srcset="{", ".join(f"{base}?w={x}&auto=format {x}w" for x in widths)}" sizes="{sizes}"' if widths else ""
    dims = f' width="{w}" height="{img["h"]}"' if w and img.get("h") else ""
    lz = ' loading="lazy" decoding="async"' if lazy else ' decoding="async"'
    return f'<img src="{base}?w={min(w or 1600, 1600)}&auto=format"{srcset}{dims} alt="{esc(img.get("alt") if alt is None else alt)}"{lz}{extra}>'


def ph(img, ratio, sizes, lazy=True, alt=None, extra=""):
    """A Sanity image in the same fixed-proportion frame as the studio photographs."""
    return f'<div class="ph {ratio}" style="--pos: {focal(img)}">{img_tag(img, sizes, lazy, alt, extra)}</div>'


# ------------------------------------------------------------------------------------------------ portable text
def plain(block):
    return "".join(c.get("text", "") for c in block.get("children", []))


def spans(block, site):
    defs = {d["_key"]: d for d in block.get("markDefs", [])}
    out = []
    for span in block.get("children", []):
        s = esc(span.get("text", "")).replace("\n", "<br>")
        for m in span.get("marks", []):
            if m == "strong":
                s = f"<strong>{s}</strong>"
            elif m == "em":
                s = f"<em>{s}</em>"
            elif defs.get(m, {}).get("_type") == "link" and defs[m].get("href"):
                href = defs[m]["href"]
                ext = ' target="_blank" rel="noopener"' if href.startswith("http") and not href.startswith(site) else ""
                s = f'<a class="tlink" href="{esc(href)}"{ext}>{s}</a>'
        out.append(s)
    return "".join(out)


def render_body(blocks, site):
    """Portable Text -> (html, faqs). FAQ items are returned for the FAQPage structured data."""
    out, faqs, lst = [], [], None

    def close():
        nonlocal lst
        if lst:
            out.append(f'<{lst[0]}>{"".join(f"<li>{i}</li>" for i in lst[1])}</{lst[0]}>')
        lst = None

    for b in blocks or []:
        t = b.get("_type")
        if t == "block" and b.get("listItem"):
            tag = "ol" if b["listItem"] == "number" else "ul"
            if not lst or lst[0] != tag:
                close()
                lst = (tag, [])
            lst[1].append(spans(b, site))
            continue
        close()
        if t == "block":
            text = plain(b)
            if not text.strip():
                continue
            style = b.get("style", "normal")
            if style == "h2":
                out.append(f'<h2 id="{slugify(text)}">{esc(text)}</h2>')
            elif style in ("h3", "h4"):
                out.append(f"<{style}>{esc(text)}</{style}>")
            elif style == "blockquote":
                out.append(f"<blockquote>{spans(b, site)}</blockquote>")
            else:
                out.append(f"<p>{spans(b, site)}</p>")
        elif t == "image" and b.get("url"):
            cap = f'<figcaption>{esc(b["caption"])}</figcaption>' if b.get("caption") else ""
            out.append(f'<figure>{img_tag(b, "(max-width: 760px) 100vw, 680px")}{cap}</figure>')
        elif t == "highlight":
            head = f'<p class="highlight-box__h">{esc(b["title"])}</p>' if b.get("title") else ""
            out.append(f'<aside class="highlight-box">{head}<p>{esc(b.get("body"))}</p></aside>')
        elif t == "table":
            rows = [r.get("cells", []) for r in b.get("rows", [])]
            if not rows:
                continue
            head = rows.pop(0) if b.get("headerRow", True) else None
            thead = f'<thead><tr>{"".join(f"<th>{esc(c)}</th>" for c in head)}</tr></thead>' if head else ""
            tbody = "".join(f'<tr>{"".join(f"<td>{esc(c)}</td>" for c in r)}</tr>' for r in rows)
            cap = f'<caption>{esc(b["caption"])}</caption>' if b.get("caption") else ""
            out.append(f'<div class="article-table"><table>{cap}{thead}<tbody>{tbody}</tbody></table></div>')
        elif t == "youtube":
            vid = youtube_id(b.get("url"))
            if not vid:
                continue
            title = esc(b.get("title") or "Video")
            out.append(f'<figure class="article-video"><div class="article-video__frame"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{title}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe></div><figcaption>{title}</figcaption></figure>')
        elif t == "faq":
            items = [i for i in b.get("items", []) if i.get("question") and i.get("answer")]
            if not items:
                continue
            title = b.get("title") or "Frequently asked questions"
            faqs += items
            qs = "".join(f'<details><summary><h3>{esc(i["question"])}</h3><i aria-hidden="true"></i></summary><p>{esc(i["answer"])}</p></details>' for i in items)
            out.append(f'<section class="article-faq"><h2 id="{slugify(title)}">{esc(title)}</h2><div class="faq">{qs}</div></section>')
        elif t == "cta":
            if b.get("text") and b.get("url"):
                nt = ' target="_blank" rel="noopener"' if b.get("newTab") else ""
                out.append(f'<p class="article-cta"><a class="btn" href="{esc(b["url"])}"{nt}>{esc(b["text"])} <span class="arr" aria-hidden="true">&rarr;</span></a></p>')
        else:
            print(f"  ! unrendered block type: {t}")
    close()
    return "\n".join(out), faqs


def word_count(blocks):
    n = 0
    for b in blocks or []:
        t = b.get("_type")
        if t == "block":
            s = plain(b)
        elif t == "highlight":
            s = f'{b.get("title", "")} {b.get("body", "")}'
        elif t == "table":
            s = " ".join(" ".join(r.get("cells", [])) for r in b.get("rows", []))
        elif t == "faq":
            s = " ".join(f'{i.get("question", "")} {i.get("answer", "")}' for i in b.get("items", []))
        else:
            s = ""
        n += len(s.split())
    return n


# ------------------------------------------------------------------------------------------------ load
def load_posts():
    """Published posts, featured first then newest. Raises rather than returning nothing, so a failed fetch
    never publishes an empty Journal."""
    # api., not apicdn.: a build triggered by a publish must see that publish, not a cached result.
    url = (f'https://{SANITY["projectId"]}.api.sanity.io/v{SANITY["apiVersion"]}/data/query/{SANITY["dataset"]}'
           f'?perspective=published&query={urllib.parse.quote(QUERY)}')
    with urllib.request.urlopen(url, timeout=30) as r:
        result = json.load(r)["result"]
    if not result:
        raise SystemExit("Sanity returned no published posts. Refusing to build an empty Journal.")
    posts = []
    for p in result:
        cover = p.get("coverImage") if (p.get("coverImage") or {}).get("url") else None
        hero = p.get("heroImage") if (p.get("heroImage") or {}).get("url") else cover
        cats = [c for c in (p.get("categories") or []) if c] or ["Journal"]
        author = p.get("author") or {}
        posts.append(dict(
            title=p["title"], slug=p["slug"], excerpt=p.get("excerpt") or "",
            seo_title=p.get("seoTitle") or "", seo_desc=p.get("metaDescription") or "",
            keywords=p.get("keywords") or [], featured=bool(p.get("featured")),
            date=ist_date(p["publishedAt"]), updated=ist_date(p.get("_updatedAt") or p["publishedAt"]),
            read=f'{p.get("readTime") or max(1, round(word_count(p.get("body")) / 200))} min read',
            author=author.get("name"), author_role=author.get("role"),
            category=cats[0], categories=cats, cover=cover, hero=hero, body=p.get("body") or [],
        ))
    posts.sort(key=lambda p: p["date"], reverse=True)
    posts.sort(key=lambda p: not p["featured"])
    return posts
