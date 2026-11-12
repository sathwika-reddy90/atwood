"""Builds the static pages of the Atwood Dsigns site, and the photograph manifest (ASSETS.md).

Run from anywhere:  python3 tools/build.py

Every photograph is described once, in PHOTOS below: what it shows, where it came from, and its focal point.
Pages refer to photographs by key, so replacing a picture means changing one entry.

Journal posts are not in this file: they are written in the Sanity Studio (https://atwood-dsigns.sanity.studio,
code in studio/) and fetched at build time by tools/cms.py, so the build needs the internet.
"""
import json
import os

import cms

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = "assets/img/portfolio/"
I = "assets/img/"

PHONE = "+91 90001 81212"
TEL = "tel:+919000181212"
WA = "https://wa.me/919000181212"
EMAIL = "atwood.dsigns@gmail.com"
ADDR = "Unit-1, 1st Floor, E-Infra Tower, Plot No. 32, Sy. No. 135, Brindavan Colony, Opp. Johnson Grammar School, Kokapet, Hyderabad 500075"
ADDR_SHORT = "E-Infra Tower, Brindavan Colony, Kokapet, Hyderabad 500075"
SITE = "https://atwooddsigns.com/"

# ------------------------------------------------------------------------------------------------ photographs
# kind: "studio"  = photographs the studio uploaded of its own finished rooms (February 2026)
#       "library" = older images from the previous website, most likely stock supplied with its theme
# pos:  object-position, the focal point kept when a picture is cropped
PHOTOS = {
    # studio photographs
    "res-04": (P + "res-04.jpg", "Entrance foyer with backlit circular niches, dressed with marigolds", "studio", "50% 50%"),
    "res-05": (P + "res-05.jpg", "Dining table with upholstered chairs beneath sheer and navy curtains", "studio", "50% 62%"),
    "res-06": (P + "res-06.jpg", "Children's loft bed with a ladder and a jungle mural", "studio", "50% 60%"),
    "res-07": (P + "res-07.jpg", "Open hall leading to a blue L-shaped kitchen", "studio", "60% 60%"),
    "res-08": (P + "res-08.jpg", "Dining area with a bar counter, pendant lights and teal drapes", "studio", "62% 55%"),
    "res-09": (P + "res-09.jpg", "Feature wall washed by track lights at the end of a hallway", "studio", "50% 40%"),
    "res-11": (P + "res-11.jpg", "Dining area with a lit display unit, chandelier and teal drapes", "studio", "52% 58%"),
    "res-12": (P + "res-12.jpg", "Bedroom with an upholstered bed, geometric wardrobe and study desk", "studio", "64% 60%"),
    "res-14": (P + "res-14.jpg", "Space-themed kids' bedroom with a world-map study wall", "studio", "45% 50%"),
    "res-15": (P + "res-15.jpg", "Children's loft bed beneath a circular window niche", "studio", "50% 50%"),
    "res-18": (P + "res-18.jpg", "Wooden double door with glazed panels", "studio", "50% 45%"),
    "res-20": (P + "res-20.jpg", "Backlit mirror beside an astronaut wardrobe", "studio", "50% 45%"),
    "res-21": (P + "res-21.jpg", "Space-themed kids' bedroom with a scalloped headboard and illustrated wardrobe", "studio", "55% 48%"),
    "res-22": (P + "res-22.jpg", "Backlit pooja unit with a carved deity panel", "studio", "50% 42%"),
    "res-23": (P + "res-23.jpg", "Backlit TV unit with a floating console", "studio", "50% 50%"),
    "res-24": (P + "res-24.jpg", "Blue wardrobe and window seat in a bedroom", "studio", "72% 50%"),
    "res-25": (P + "res-25.jpg", "Illustrated sliding wardrobe in a kids' bedroom", "studio", "50% 45%"),
    "res-27": (P + "res-27.jpg", "Entrance with a marble wall, brass screen and marigold garlands", "studio", "45% 50%"),
    "res-29": (P + "res-29.jpg", "Kids' bed with a scalloped headboard", "studio", "50% 50%"),
    "res-30": (P + "res-30.jpg", "Open kitchen with a blue L-shaped counter and carved doors", "studio", "50% 55%"),
    "res-31": (P + "res-31.jpg", "Bedroom with full-height fitted wardrobes", "studio", "50% 45%"),
    "res-32": (P + "res-32.jpg", "Warmly lit entrance lobby with a wood-clad door", "studio", "50% 50%"),
    "res-33": (P + "res-33.jpg", "Grey modular kitchen with glass-fronted wall cabinets", "studio", "50% 62%"),
    "res-35": (P + "res-35.jpg", "Space-themed kids' bedroom seen from the doorway", "studio", "40% 50%"),
    "res-36": (P + "res-36.jpg", "Bedroom with a grey sliding wardrobe", "studio", "40% 45%"),
    "res-37": (P + "res-37.jpg", "Living room with a marble TV wall and cove ceiling", "studio", "32% 50%"),
    "res-39": (P + "res-39.jpg", "Navy and white modular kitchen", "studio", "62% 55%"),
    "res-40": (P + "res-40.jpg", "Mint modular kitchen with fluted-glass uppers and under-cabinet lighting", "studio", "50% 55%"),
    "res-41": (P + "res-41.jpg", "Living room with a cove ceiling, recliner sofa still wrapped after installation", "studio", "40% 55%"),
    "res-42": (P + "res-42.jpg", "Kids' room with a study niche, slatted screen and peach wardrobe", "studio", "55% 55%"),
    "res-43": (P + "res-43.jpg", "Bedroom with a pink and white arched wardrobe", "studio", "55% 50%"),
    "res-44": (P + "res-44.jpg", "Kids' bed with a scalloped headboard beside an illustrated wardrobe", "studio", "55% 60%"),
    # library images from the previous website
    "com-01": (P + "com-01.jpg", "Office cabin with a sculpted white desk", "library", "50% 55%"),
    "com-02": (P + "com-02.jpg", "Office breakout area with a meeting pod and slatted wall", "library", "45% 55%"),
    "com-03": (P + "com-03.jpg", "Poolside restaurant terrace", "library", "50% 60%"),
    "com-10": (P + "com-10.jpg", "Office lounge with hexagonal ceiling lights and a moss wall", "library", "50% 55%"),
    "com-17": (P + "com-17.jpg", "Office corridor with glass-walled meeting rooms", "library", "50% 55%"),
    "com-28": (P + "com-28.jpg", "Conference room with a long table and orange chairs", "library", "45% 55%"),
    "com-38": (P + "com-38.jpg", "Reception lounge with timber slats and a sculptural wall piece", "library", "45% 55%"),
    "com-45": (P + "com-45.jpg", "Open-plan office with a planted ceiling", "library", "50% 55%"),
    "com-47": (P + "com-47.jpg", "Open-plan workspace with suspended ceiling baffles", "library", "50% 55%"),
    "atwood1": (I + "atwood1.jpg", "Two people reviewing a drawing with material samples", "library", "50% 40%"),
    "atwood": (I + "atwood.jpg", "Two people going through plans together", "library", "50% 40%"),
    "plan": (I + "Interior-design-drawings-floor-plans.jpg", "Coloured floor plan of an apartment", "library", "50% 50%"),
    "company": (I + "company.jpg", "Hands marking up construction drawings", "library", "50% 50%"),
    "interior4": (I + "interior4.jpg", "Bathroom design illustration, half drawn and half rendered", "library", "50% 50%"),
    "sketch": (I + "bedroom-design.jpg", "Pencil sketch of a bedroom design", "library", "50% 50%"),
}
USED = {}  # key -> set of "page: place", collected while building and written to ASSETS.md


def jpeg_width(path):
    """Reads a JPEG's pixel width from its frame header, so srcset widths are exact."""
    with open(path, "rb") as f:
        data = f.read()
    i = 2
    while i < len(data):
        marker, size = data[i + 1], int.from_bytes(data[i + 2:i + 4], "big")
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            return int.from_bytes(data[i + 7:i + 9], "big")
        i += 2 + size
    return None


def img_tag(src, alt, sizes="(max-width: 860px) 100vw, 50vw", lazy=True, extra=""):
    lz = ' loading="lazy" decoding="async"' if lazy else ' decoding="async"'
    srcset = ""
    small = src[:-4] + "-800.jpg"
    if src.endswith(".jpg") and os.path.exists(os.path.join(OUT, small)):
        srcset = f' srcset="{small} 800w, {src} {jpeg_width(os.path.join(OUT, src))}w" sizes="{sizes}"'
    return f'<img src="{src}"{srcset} alt="{alt}"{lz}{extra}>'


PAGE = "index.html"


def ph(key, ratio="r-32", sizes="(max-width: 860px) 100vw, 50vw", lazy=True, where="", cls="", attrs="", alt=None, img_extra="", inner_link=None):
    """A photograph at a fixed proportion with its focal point; records where it is used."""
    src, desc, kind, pos = PHOTOS[key]
    USED.setdefault(key, set()).add(f"{PAGE}: {where}" if where else PAGE)
    tag = img_tag(src, desc if alt is None else alt, sizes, lazy, img_extra)
    if inner_link:
        tag = f'<a href="{inner_link}">{tag}</a>'
    drawing = ""
    return f'<div class="ph {ratio} {cls}{drawing}" style="--pos: {pos}"{attrs}>{tag}</div>'


# ------------------------------------------------------------------------------------------------ chrome
NAV = [("services.html", "Services"), ("portfolio.html", "Portfolio"), ("process.html", "Process"),
       ("ideas.html", "Ideas"), ("journal.html", "Journal"), ("about.html", "About")]
MENU = [("index.html", "Home")] + NAV + [("contact.html", "Contact")]
CUR = ' aria-current="page"'

ICON_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1112 21.8zm8.4-18.2A11.8 11.8 0 001.7 17.9L0 24l6.3-1.6A11.8 11.8 0 0024 12c0-3.2-1.2-6.1-3.6-8.4z"/></svg>'
ARROW_L = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'
ARROW_R = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'
CLOSE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>'
PAUSE_PLAY = '<svg class="i-pause" width="12" height="12" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z" fill="currentColor"/></svg><svg class="i-play" width="12" height="12" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l13 8-13 8z" fill="currentColor"/></svg>'
ARR = '<span class="arr" aria-hidden="true">&rarr;</span>'


def header(current, over=False):
    links = "".join(f'<a href="{h}"{CUR if h == current else ""}>{t}</a>' for h, t in NAV)
    menu = "".join(f'<li><a href="{h}" data-n="{i + 1:02d}"{CUR if h == current else ""}>{t}</a></li>' for i, (h, t) in enumerate(MENU))
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header{' site-header--over' if over else ''}">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Atwood Dsigns, home"><img src="{I}logo-web-new-2.png" alt="Atwood Dsigns" width="255" height="97"><span class="brand__line" aria-hidden="true">Interior design<br>and build studio</span></a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <a class="btn header-cta" href="contact.html">Book a consultation</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu-panel">Menu</button>
  </div>
</header>
<div class="menu-panel" id="menu-panel" aria-hidden="true">
  <nav aria-label="Menu"><ul>{menu}</ul></nav>
  <p><a href="{TEL}">{PHONE}</a><br>{ADDR_SHORT}</p>
</div>'''


FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot">
      <div class="foot__brand">
        <img src="{I}logo-web-new-2.png" alt="" width="255" height="97" loading="lazy">
        <p class="foot__word">Atwood Dsigns</p>
        <p>An interior design and build studio in Kokapet, Hyderabad, creating homes, offices and shops from the first sketch to handover.</p>
      </div>
      <div class="foot__col"><h2>Studio</h2><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in MENU[1:])}</ul></div>
      <div class="foot__col"><h2>Follow</h2><ul>
        <li><a href="https://www.instagram.com/atwooddsigns/" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="https://www.linkedin.com/company/atwooddsigns/" target="_blank" rel="noopener">LinkedIn</a></li>
        <li><a href="https://www.pinterest.com/atwooddsignss/" target="_blank" rel="noopener">Pinterest</a></li></ul></div>
      <div class="foot__col foot__col--wide"><h2>Visit or call</h2>
        <address>{ADDR}</address>
        <ul style="margin-top:16px"><li><a href="{TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></li></ul>
      </div>
    </div>
    <div class="legal"><span>&copy; <span id="year">2026</span> Atwood Dsigns LLP. All rights reserved.</span><span>Kokapet, Hyderabad</span></div>
  </div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Chat with Atwood Dsigns on WhatsApp">{ICON_WA}</a>
<nav class="mbar" aria-label="Quick contact"><a href="{TEL}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>Call the studio</a><a href="{WA}" target="_blank" rel="noopener">{ICON_WA}WhatsApp</a></nav>'''


def cta():
    return f'''<section class="cta" aria-labelledby="cta-h">
  <figure class="cta__pic">
    {ph("res-40", "", "(max-width: 960px) 100vw, 50vw", where="consultation band", attrs="")}
    <figcaption><span class="meta">Mint modular kitchen, a room we finished</span></figcaption>
  </figure>
  <div class="cta__text">
    <p class="label" data-rise>Free first consultation</p>
    <h2 id="cta-h" data-lines>Start with a conversation</h2>
    <p class="lead" data-rise>Tell us about your home, your office or the one room that isn't working. We'll meet you at our studio in Kokapet or at your site.</p>
    <div class="actions" data-rise><a class="btn btn--light" href="contact.html">Book a consultation {ARR}</a><a class="btn btn--line-light" href="{WA}" target="_blank" rel="noopener">Message on WhatsApp</a></div>
    <div class="cta__contacts" data-stagger>
      <div><span class="meta">Call</span><a href="{TEL}">{PHONE}</a></div>
      <div><span class="meta">Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div><span class="meta">Studio</span><span>Kokapet, Hyderabad</span></div>
    </div>
  </div>
</section>'''


def page(fname, title, desc, body, closing=True, over=False, og_image=None, og_type="website", head_extra="", section=None):
    canonical = SITE + ("" if fname == "index.html" else fname.replace(".html", "/"))
    og_image = og_image or P + "res-11.jpg"
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Atwood Dsigns">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og_image}">{head_extra}
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f3f0e9">
<link rel="icon" href="{I}cropped-favicon-192x192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
<script>(function (d) {{ d.classList.add('js'); if ('onpagereveal' in window) d.classList.add('vt'); setTimeout(function () {{ if (!d.classList.contains('ready')) d.classList.remove('js'); }}, 4000); }})(document.documentElement)</script>
<script type="speculationrules">{{"prefetch": [{{"where": {{"selector_matches": "a[href$='.html']"}}, "eagerness": "moderate"}}]}}</script>
</head>
<body>
{header(section or fname, over)}
<main id="main">
{body}
{cta() if closing else ""}
</main>
{FOOTER}
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(html)


LABELS = {"services.html": "01 / Services", "portfolio.html": "02 / Portfolio", "process.html": "03 / Process", "ideas.html": "04 / Ideas",
          "journal.html": "05 / Journal", "about.html": "06 / About", "contact.html": "07 / Contact"}


def page_head(h1, lead, aside=""):
    return f'''<section class="page-head">
  <div class="wrap grid">
    <p class="label" data-rise>{LABELS.get(PAGE, "")}</p>
    <h1 data-lines>{h1}</h1>
    <p class="lead" data-rise>{lead}</p>
    {f'<div class="page-head__aside" data-rise>{aside}</div>' if aside else ""}
  </div>
</section>'''


def head_photo(key, where="opening photograph"):
    pic = ph(key, "r-219 head-ph", "(max-width: 1320px) 100vw, 1320px", lazy=False, where=where, img_extra=' fetchpriority="high"')
    return f'<div class="wrap">{pic}</div>'


# ------------------------------------------------------------------------------------------------ content
STAGES = [
    ("Design", "Concept design", "A detailed conversation to learn your needs, agree the scope and understand how the space should look and work.", "atwood1"),
    ("Design", "Schematic design", "Spatial planning and 3D visual concepts that set the overall design direction.", "plan"),
    ("Design", "Detailed design", "The design evolves with you, detail by detail, and we choose the materials together.", "sketch"),
    ("Design", "Construction drawings", "Complete working drawings for every trade: electrical layouts, false ceilings, carpentry and more.", "company"),
    ("Design", "Site supervision", "Our designers visit the site regularly to make sure the design is built as drawn.", "res-24"),
    ("Build", "Quantity surveying", "A detailed cost estimate based on the chosen design and materials.", "atwood"),
    ("Build", "Procurement", "Our procurement team selects and buys furnishings, fixtures and accessories, tracks orders and checks every delivery.", "res-36"),
    ("Build", "Project planning", "A detailed timeline setting out the order of the work and how long each stage takes.", "res-07"),
    ("Build", "Site management", "A dedicated site supervisor runs the day-to-day work, checks materials, organises the crew and resolves problems.", "res-41"),
    ("Build", "Quality control", "An internal review confirms the work meets industry standards before handover.", "res-44"),
]

QUOTES = [
    ("They turned our plain living room into a stylish and welcoming space. The designers considered how we live and gave us a layout that feels elegant and comfortable.", "Avinash Kumar", "Living room"),
    ("They redesigned our corporate office and the results have been outstanding. The space looks modern, encourages collaboration and impresses our clients.", "Suresh", "Corporate office"),
    ("The lighting, furniture and soothing tones turned our bedroom into a relaxing retreat we look forward to every night.", "Padmavathi", "Bedroom"),
    ("The workspace is functional yet stylish, our team loves the new environment, and the project was delivered on time and within budget.", "Bharath", "Office interiors"),
    ("Our retail store needed a fresh look and they nailed it. The interiors attract more customers and the layout is much more efficient.", "Manjunath", "Retail store"),
    ("I wanted a kitchen that was both practical and beautiful, and that is exactly what they delivered. Cooking is so much easier now.", "Praveena", "Kitchen"),
]

FAQS = [
    ("How does the process work?", "We begin with a consultation to understand your requirements and preferences. We then develop design concepts for your approval, and once the design is final we manage the execution through to handover."),
    ("Can you work with my budget?", "Yes. We plan the space and choose materials carefully to create a beautiful, functional result within the budget you set."),
    ("How long does a project take?", "It depends on the size and complexity of the project. We strive to deliver within 30 days, though some projects need more time because of specific challenges."),
    ("Can I bring my own ideas?", "Yes. We work closely with you at every stage so the space reflects your personality and needs."),
    ("Which styles do you design in?", "Modern, traditional, minimalist, industrial, luxury, Scandinavian and contemporary, each customised to your preference."),
    ("How do I get started?", "We offer free consultations. Book one through the contact page or call us, and we'll guide you through the first steps."),
]

ROOMS = [  # room-by-room viewer: (name, portfolio filter, studio photographs)
    ("Kitchens", "kitchen", ["res-40", "res-39", "res-33", "res-30", "res-07"]),
    ("Bedrooms", "bedroom", ["res-12", "res-43", "res-36", "res-31", "res-24"]),
    ("Kids' rooms", "kids", ["res-21", "res-42", "res-25", "res-15", "res-14"]),
    ("Living and dining", "living", ["res-11", "res-08", "res-05", "res-37", "res-23"]),
    ("Entrances and pooja", "entrance", ["res-32", "res-22", "res-04", "res-18", "res-27", "res-09"]),
]


def stage_row(h2_id):
    cols = "".join(f'''<li class="moment">
        {ph(key, "r-45", "(max-width: 760px) 78vw, (max-width: 1100px) 31vw, 300px", where="ten stages")}
        <p class="moment__n moment__n--{"design" if phase == "Design" else "build"}"><b>{i + 1:02d}</b><span class="meta">{"Design" if phase == "Design" else "Execution"}</span></p>
        <h3>{t}</h3>
        <p>{d}</p>
      </li>''' for i, (phase, t, d, key) in enumerate(STAGES))
    return f'''<section class="moments sec dark" data-row aria-labelledby="{h2_id}">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="{h2_id}" data-lines>Ten stages, one team</h2>
      <p data-rise>Five stages of design and five of execution. The people who draw your space are the people who build it.</p>
    </div>
    <p class="moments__count" aria-hidden="true">Stages <b>1 to 4</b> of 10</p>
    <div class="rail"><div class="rail__group rail__group--design"><p class="rail__name">Design</p><div class="rail__ticks">{"".join(f'<button type="button" data-goto="{i}" aria-label="Go to stage {i + 1}, {t}">{i + 1:02d}</button>' for i, (_p, t, _d, _k) in enumerate(STAGES) if i < 5)}</div></div><div class="rail__group rail__group--build"><p class="rail__name">Execution</p><div class="rail__ticks">{"".join(f'<button type="button" data-goto="{i}" aria-label="Go to stage {i + 1}, {t}">{i + 1:02d}</button>' for i, (_p, t, _d, _k) in enumerate(STAGES) if i >= 5)}</div></div>
      <div class="moments__nav"><button class="icon-btn" type="button" data-dir="prev" aria-label="Earlier stages">{ARROW_L}</button><button class="icon-btn" type="button" data-dir="next" aria-label="Later stages">{ARROW_R}</button></div></div>
    <p class="sr-only" role="status" data-row-status></p>
    <ol class="row" aria-label="The ten stages, in order. Use the arrow keys to move between stages." tabindex="0">{cols}</ol>
  </div>
</section>'''


def room_viewer(h2_id="rooms-h"):
    """A viewer of the studio's own photographs, one room type at a time; nothing is cropped."""
    name0, cat0, keys0 = ROOMS[0]
    for _, _, keys in ROOMS:
        for k in keys:
            USED.setdefault(k, set()).add(f"{PAGE}: room-by-room viewer")
    def small(src):  # the 800px copy, only where one exists
        s800 = src[:-4] + "-800.jpg"
        return s800 if os.path.exists(os.path.join(OUT, s800)) else ""

    def data(keys):
        return "|".join(f"{PHOTOS[k][0]}::{PHOTOS[k][1]}::{small(PHOTOS[k][0])}::{jpeg_width(os.path.join(OUT, PHOTOS[k][0]))}" for k in keys)
    buttons = "".join(
        f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-cat="{cat}" data-photos="{data(keys)}"><span>{name}</span><span class="idx">{len(keys):02d}</span></button>'
        for i, (name, cat, keys) in enumerate(ROOMS))
    thumbs = "".join(
        f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" aria-label="Photograph {i + 1}: {PHOTOS[k][1]}">{img_tag(PHOTOS[k][0], "", "120px")}</button>'
        for i, k in enumerate(keys0))
    src0, alt0 = PHOTOS[keys0[0]][0], PHOTOS[keys0[0]][1]
    return f'''<section class="viewer sec dark" aria-labelledby="{h2_id}" data-viewer>
  <div class="wrap">
    <div class="sec-head">
      <h2 id="{h2_id}" data-lines>Room by room</h2>
      <p data-rise>Choose a room to look through the photographs of spaces we have designed and built in Hyderabad homes.</p>
    </div>
    <div class="grid">
      <figure class="viewer__stage">
        <div class="viewer__frame">{img_tag(src0, alt0, "(max-width: 960px) 100vw, 66vw", extra=' class="is-on"')}</div>
        <button class="icon-btn viewer__prev" type="button" aria-label="Previous photograph">{ARROW_L}</button>
        <button class="icon-btn viewer__next" type="button" aria-label="Next photograph">{ARROW_R}</button>
        <figcaption class="viewer__cap"><span class="meta viewer__alt">{alt0}</span><span class="idx viewer__count" aria-live="polite">01 / {len(keys0):02d}</span></figcaption>
      </figure>
      <div class="viewer__side">
        <p class="label">Choose a room</p>
        <div class="viewer__rooms" role="group" aria-label="Choose a room">{buttons}</div>
        <div class="viewer__thumbs" role="group" aria-label="Photographs of this room">{thumbs}</div>
        <a class="tlink viewer__more" href="portfolio.html#{cat0}">See this room type in the portfolio {ARR}</a>
      </div>
    </div>
  </div>
</section>'''


def voices():
    figs = "".join(f'<figure class="{"is-on" if i == 0 else ""}"><blockquote>{q}</blockquote><figcaption><b>{n}</b> <span>&nbsp;{p}</span></figcaption></figure>' for i, (q, n, p) in enumerate(QUOTES))
    return f'''<section class="voices sec quote-sec" aria-labelledby="voices-h">
  <div class="wrap grid">
    <div class="voices__head"><h2 id="voices-h" class="h3" data-lines>What clients say</h2></div>
    <div class="quotes" aria-live="off">{figs}</div>
    <div class="quote-ctl"><span class="count">1 of {len(QUOTES)}</span><button class="slide-toggle" type="button" aria-pressed="false" aria-label="Pause quotations">{PAUSE_PLAY}</button><button class="icon-btn" type="button" data-q="prev" aria-label="Previous quotation">{ARROW_L}</button><button class="icon-btn" type="button" data-q="next" aria-label="Next quotation">{ARROW_R}</button></div>
  </div>
</section>'''


def faq_block(h2_id="faq-h"):
    items = "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for q, a in FAQS)
    return f'''<section class="faq-block sec" aria-labelledby="{h2_id}">
  <div class="wrap grid">
    <div class="faq-block__head">
      <h2 class="h2" id="{h2_id}" data-lines>Questions clients ask</h2>
      <p data-rise>Something else on your mind? Call <a class="tlink tlink--bronze" href="{TEL}">{PHONE}</a></p>
    </div>
    <div class="faq" data-stagger>{items}</div>
  </div>
</section>'''


# ---------------------------------------------------------------- projects
# Only rooms photographed several times are projects. Everything written about them describes what is visible
# in the photographs: no client, location, year, brief or budget is stated, because none has been supplied.
PROJECTS = [
    dict(slug="project-space-kids-bedroom", title="Space-themed kids' bedroom", cat="Kids' room", filter="kids", contact="Bedroom+or+kids%27+room",
         lead="res-44", card="res-21", card_pos="30% 50%",
         overview="A child's bedroom organised around one idea: the night sky. Illustrated glass doors, a scalloped headboard and a lit mirror turn storage and furniture into the theme, while the study corner keeps it a room to grow up in.",
         seen=[("Sliding wardrobe", "Three full-height doors in sky-blue glass, printed with astronauts and set in slim black frames."),
               ("Headboard", "Deep-blue upholstered panels with rounded tops, fixed to the wall like a row of standing stones."),
               ("Storage bed", "A white bed base with storage, matched to the low drawers beneath the wardrobe."),
               ("Lit mirror", "A full-length mirror with a playful cut-out outline and a warm glow behind its edge."),
               ("Study corner", "A desk with a white drawer unit and a world map covering the wall above it."),
               ("Lighting", "Recessed downlights with a warm strip of light along the wardrobe wall.")],
         seq=[("res-21", "wide"), ("res-25", "half"), ("res-20", "half-tall"), ("res-14", "wide"), ("res-35", "half"), ("res-29", "half-tall")]),
    dict(slug="project-dining-bar", title="Dining, bar and display unit", cat="Living and dining", filter="living", contact="Living+room",
         lead="res-11", card="res-11", card_pos="52% 58%",
         overview="A dining space that opens onto a bar counter, framed by lit display cabinets and a wall of teal drapes. The ceiling, the joinery and the lighting are designed together, so the room reads as one composition from the table and from the bar.",
         seen=[("Display units", "Tall cabinets with glass shelves, black frames and warm vertical lighting."),
               ("Drapes", "Floor-to-ceiling teal curtains that soften the whole wall."),
               ("Dining set", "A white-topped table on a gold base, with upholstered chairs on gold-tipped black legs."),
               ("Bar counter", "A counter faced in black marble-effect stone, with high stools."),
               ("Pendants", "Open hexagonal pendant lights over the bar, with plants hung above them."),
               ("Ceiling", "A dropped ceiling with a reflective inset panel, a chandelier and linear lighting.")],
         seq=[("res-11", "wide"), ("res-08", "wide")]),
    dict(slug="project-open-kitchen", title="Open kitchen and hall", cat="Kitchen", filter="kitchen", contact="Kitchen",
         lead="res-30", card="res-30", card_pos="50% 55%",
         overview="An L-shaped kitchen open to the hall, with carved doors and an arched niche giving the space its character. A cove ceiling with warm light ties the kitchen and the hall together.",
         seen=[("Base cabinets", "An L-shaped run in deep blue, under a black countertop."),
               ("Wall cabinets", "Black-framed glass shutters above a marble-effect backsplash."),
               ("Doors", "Dark doors with carved floral motifs and slim horizontal inlays."),
               ("Arched niche", "A soft arch cut into the wall beside the doors."),
               ("Panelling", "A fluted white wall panel edged in brass at the entrance to the hall."),
               ("Ceiling", "A cove ceiling with a warm strip light, downlights and a ceiling fan.")],
         seq=[("res-30", "wide"), ("res-07", "wide")]),
]
PROJECT_BY_SLUG = {pr["slug"]: pr for pr in PROJECTS}
for pr in PROJECTS:  # every photograph of the space, lead first
    pr["photos"] = list(dict.fromkeys([pr["lead"]] + [k for k, _ in pr["seq"]]))


# ================================================================================================ HOME
PAGE = "index.html"
HERO = ("res-11", "Dining, bar and display unit", "project-dining-bar.html")  # (picture, room, where its caption leads)
USED.setdefault(HERO[0], set()).add("index.html: hero")
hero_img = img_tag(PHOTOS[HERO[0]][0], PHOTOS[HERO[0]][1], "(max-width: 860px) 100vw, 56vw",
                   extra=f' fetchpriority="high" style="--pos: {PHOTOS[HERO[0]][3]}"')

SERVICES = [  # (anchor, title, description, picture, caption)
    ("residential", "Residential interiors", "Apartments and villas: living rooms, bedrooms, modular kitchens, kids' rooms and complete home makeovers.", "res-12", "Bedroom with a study wall"),
    ("commercial", "Commercial interiors", "Offices, retail and hospitality spaces that work hard and reflect your brand.", "com-45", "Open-plan office"),
    ("specialized", "Specialized solutions", "Space planning, construction documentation, finish selection and 3D visualisation.", "plan", "Floor plan"),
    ("turnkey", "Turnkey execution", "Quantity surveying, procurement, site management and quality control through to handover.", "res-30", "Open kitchen"),
]
svc_items = "".join(f'''<a class="svc-item" href="services.html#{a}" data-preview="{i}">
      {ph(k, "r-32", "100vw", where="services list (phone)", alt="")}
      <span class="idx">{i + 1:02d}</span><h3>{t}</h3><span class="arr" aria-hidden="true">&rarr;</span><p>{d}</p></a>''' for i, (a, t, d, k, c) in enumerate(SERVICES))
svc_preview = "".join(img_tag(PHOTOS[k][0], PHOTOS[k][1], "(max-width: 860px) 0px, 40vw", extra=f' data-caption="{c}" data-index="{i + 1:02d} / 04" style="--pos: {PHOTOS[k][3]}"' + (' class="is-on"' if i == 0 else "")) for i, (a, t, d, k, c) in enumerate(SERVICES))

MORE_ROOMS = [("res-40", "Mint modular kitchen", "kitchen"), ("res-22", "Pooja unit", "entrance"), ("res-43", "Pink arched wardrobe", "bedroom"), ("res-32", "Warm-lit entrance lobby", "entrance")]


def project_feature(pr, n, ratio, sizes, cls):
    return f'''<a class="pj {cls}" href="{pr["slug"]}.html">
        <div class="ph {ratio}" style="--pos: {pr["card_pos"]}">{img_tag(PHOTOS[pr["card"]][0], PHOTOS[pr["card"]][1], sizes)}</div>
        <span class="pj__cap"><span class="idx">{n:02d}</span><span class="pj__title">{pr["title"]}</span><span class="meta">{pr["cat"]}, {len(pr["photos"])} photographs</span><em class="pj__go">View project &rarr;</em></span>
      </a>'''


pf = PROJECTS
more = "".join(f'''<a class="mr" href="portfolio.html#{c}">{ph(k, "r-45", "(max-width: 600px) 50vw, 25vw", where="more rooms", alt="")}<span class="meta">{t}</span></a>''' for k, t, c in MORE_ROOMS)
home = f'''<section class="hero" aria-labelledby="hero-h">
  <div class="hero__text">
    <p class="label">Kokapet, Hyderabad</p>
    <h1 id="hero-h" data-lines>Interiors designed, drawn and built</h1>
    <p class="hero__lead" data-rise>Homes, offices and shops, taken from the first conversation to handover by one studio.</p>
    <div class="actions" data-rise><a class="btn" href="contact.html">Book a free consultation {ARR}</a><a class="btn btn--ghost" href="portfolio.html">See our work</a></div>
  </div>
  <figure class="hero__pic">
    {hero_img}
    <figcaption><a href="{HERO[2]}"><span>{HERO[1]}</span><span class="meta">View the project {ARR}</span></a></figcaption>
  </figure>
</section>

<section class="work sec" aria-labelledby="work-h">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="work-h" data-lines>Selected projects</h2>
      <p data-rise>Rooms we have designed and built, with every photograph of each space and notes on what went into it.</p>
    </div>
    <div class="pjs">
      {project_feature(pf[0], 1, "r-45", "(max-width: 860px) 100vw, 50vw", "pj--feature")}
      <div class="pj__note">
        <p class="statement">{pf[0]["overview"]}</p>
        <ul class="pj__seen">{"".join(f"<li><span class='meta'>{a}</span>{b}</li>" for a, b in pf[0]["seen"][:3])}</ul>
        <a class="tlink" href="{pf[0]["slug"]}.html">Read the project {ARR}</a>
      </div>
      {project_feature(pf[1], 2, "r-32", "(max-width: 860px) 100vw, 58vw", "pj--wide")}
      {project_feature(pf[2], 3, "r-45", "(max-width: 860px) 100vw, 33vw", "pj--tall")}
    </div>
    <div class="more-rooms">
      <div class="more-rooms__head"><p class="label">More rooms</p><a class="tlink" href="portfolio.html">View all 27 rooms {ARR}</a></div>
      <div class="more-rooms__row">{more}</div>
    </div>
  </div>
</section>

<section class="intro sec sec--flush-top" aria-labelledby="intro-h">
  <div class="wrap grid">
    <div class="intro__text">
      <p class="label" data-rise>The studio</p>
      <h2 class="sr-only" id="intro-h">About the studio</h2>
      <p class="statement" data-rise>We design and build homes, offices and commercial interiors in Hyderabad, and the team that draws your space is the team that builds it.</p>
      <div class="intro__cols" data-rise>
        <p class="muted">We combine creativity, function and fine craftsmanship to bring your vision to life, with designs that blend timeless style and modern ideas so every detail feels personal and purposeful.</p>
        <p class="muted">Five stages of design are followed by five of execution: quantity surveying, procurement, project planning, a dedicated site supervisor and a final quality review before handover.</p>
      </div>
      <div class="actions" data-rise><a class="tlink" href="about.html">About the studio {ARR}</a><a class="tlink" href="process.html">How we work {ARR}</a></div>
    </div>
    <figure class="intro__pic" style="margin:0">
      {ph("res-08", "r-45", "(max-width: 860px) 100vw, 40vw", where="studio introduction", attrs="")}
      <figcaption class="cap"><span class="meta">Dining area with a bar counter</span></figcaption>
    </figure>
  </div>
</section>

{room_viewer()}

<section class="svc-index sec" aria-labelledby="svc-h">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="svc-h" data-lines>What we design and build</h2>
      <p data-rise>Four kinds of work, delivered by one team from the first drawing to the final check.</p>
    </div>
    <div class="grid">
      <div class="svc-list" data-stagger>{svc_items}</div>
      <div class="svc-preview" aria-hidden="true"><div class="ph r-45">{svc_preview}</div><p class="cap"><span class="meta" data-preview-caption>{SERVICES[0][4]}</span><span class="idx" data-preview-index>01 / 04</span></p></div>
    </div>
  </div>
</section>

{stage_row("moments-h")}

{voices()}'''
page("index.html", "Atwood Dsigns | Interior Design and Build Studio in Kokapet, Hyderabad",
     "Atwood Dsigns designs, draws and builds residential and commercial interiors in Hyderabad, from the first consultation to handover. Book a free consultation.", home)

# ================================================================================================ ABOUT
PAGE = "about.html"
about = page_head("Design shaped around how you live", "Atwood Dsigns is an interior design and build studio in Kokapet, Hyderabad. We believe great design goes beyond looks: it shapes the way you live, work and feel in your space.") + head_photo("res-11") + f'''
<section class="story sec" aria-labelledby="story-h">
  <div class="wrap">
    <div class="grid">
      <div class="story__label"><h2 class="h3" id="story-h" data-lines>Our philosophy</h2></div>
      <div class="story__text">
        <p class="statement" data-rise>We create interiors that are visually striking and deeply practical, tailored to the lifestyle and vision of each client.</p>
        <p class="muted" data-rise>Every project begins by listening: understanding your needs, your aspirations and the story you want your space to tell. We turn those ideas into well-planned designs that balance beauty, practicality and sustainability.</p>
        <p class="muted" data-rise>From warm, inviting homes to inspiring commercial environments, our team brings ideas to life with quality materials, considered layouts and a keen eye for detail. With Atwood, it isn't just design; it's the art of living beautifully.</p>
      </div>
    </div>
    <div class="pair-row">
      <figure style="margin:0">{ph("res-08", "r-32", "(max-width: 860px) 100vw, 58vw", where="story pair", attrs="")}<figcaption class="cap"><span class="meta">Dining area with a bar counter</span></figcaption></figure>
      <figure style="margin:0">{ph("res-22", "r-45", "(max-width: 860px) 100vw, 33vw", where="story pair", attrs="")}<figcaption class="cap"><span class="meta">Backlit pooja unit</span></figcaption></figure>
    </div>
  </div>
</section>
<section class="sec stone" aria-labelledby="val-h">
  <div class="wrap">
    <div class="sec-head"><h2 id="val-h" data-lines>What guides our work</h2><p data-rise>Drawn from our company values: creativity and function, guided by your vision, crafted with precision and enriched with sustainable choices.</p></div>
    <div class="values" data-stagger>
      <div><h3>Creativity</h3><p>Fresh ideas shaped around your vision and the way you want to live.</p></div>
      <div><h3>Functionality</h3><p>Layouts, storage and lighting planned for how the space is really used.</p></div>
      <div><h3>Sustainability</h3><p>Choices that respect both beauty and the environment.</p></div>
      <div><h3>Integrity</h3><p>Timeless quality as the goal, with integrity at the core of every project.</p></div>
    </div>
  </div>
</section>
<section class="sec" aria-labelledby="visit-h">
  <div class="wrap split split--rev">
    <figure class="split__pic" style="margin:0">{ph("res-32", "r-32", "(max-width: 860px) 100vw, 58vw", where="visit the studio", attrs="")}<figcaption class="cap"><span class="meta">Warm-lit entrance lobby, a room we finished</span></figcaption></figure>
    <div class="split__text">
      <p class="label" data-rise>Visit</p>
      <h2 id="visit-h" data-lines>The studio in Kokapet</h2>
      <p class="lead" data-rise>{ADDR}</p>
      <div class="actions" data-rise><a class="btn" href="contact.html">Book a visit {ARR}</a><a class="tlink" href="https://maps.google.com/?q=E-Infra+Tower+Brindavan+Colony+Kokapet+Hyderabad" target="_blank" rel="noopener">Open in Maps {ARR}</a></div>
    </div>
  </div>
</section>
{faq_block()}'''
page("about.html", "About the Studio | Atwood Dsigns", "Atwood Dsigns is an interior design and build studio in Kokapet, Hyderabad, creating interiors that balance beauty, practicality and sustainability.", about)

# ================================================================================================ SERVICES
PAGE = "services.html"
RES = [("Living rooms", "Inviting layouts, statement furniture and personal touches."),
       ("Bedrooms", "Calm, comfortable, customised rooms designed for rest."),
       ("Kitchens", "Smart, practical modular kitchens with beautiful finishes."),
       ("Dining spaces", "Elegant settings that bring the family together."),
       ("Kids' rooms", "Creative, playful and safe rooms that inspire imagination."),
       ("Complete makeovers", "From concept to execution, the whole home transformed.")]
COM = [("Office interiors", "Efficient, employee-friendly spaces that encourage collaboration."),
       ("Retail design", "Engaging layouts that attract customers and strengthen your brand."),
       ("Hospitality spaces", "Restaurants, cafés and hotels that leave a lasting impression."),
       ("Workspace planning", "Ergonomic furniture, lighting and storage planned for the team."),
       ("Customised solutions", "Designs that reflect your brand's personality and objectives.")]
SPEC = [("Commercial tenant improvements", "Interior design tailored to business spaces."),
        ("As-built surveying", "Accurate documentation of existing conditions."),
        ("Space planning and programming", "Efficient, purpose-driven layouts."),
        ("Schematic and design development", "From first concept to a refined design."),
        ("Construction documentation and bid coordination", "Clear specifications and coordinated proposals."),
        ("Construction administration", "Overseeing implementation and quality."),
        ("Interior finish selection", "Expert curation of materials and finishes."),
        ("Furniture and accessories", "Pieces that complement the design."),
        ("ADA analysis and code compliance", "Regulatory and accessibility standards."),
        ("Exterior colours and retail procurement", "Choices aligned to the site and the brand."),
        ("3D rendering", "Visualisation through digital modelling.")]


def deflist(items, cls="deflist"):
    return f'<ul class="{cls}" data-stagger>' + "".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a, b in items) + "</ul>"


services = page_head("Services", "Whether you are refreshing a commercial property or designing a welcoming home, we capture your vision and turn it into a space that is practical, elegant and yours.") + \
    head_photo("res-39") + '''
<nav class="jump" aria-label="Services on this page"><div class="wrap"><a href="#residential">Residential</a><a href="#commercial">Commercial</a><a href="#specialized">Specialized</a><a href="#turnkey">Turnkey delivery</a></div></nav>''' + f'''
<section class="sec" id="residential" aria-labelledby="res-h">
  <div class="wrap">
    <div class="sec-head"><h2 id="res-h" data-lines>Residential interiors</h2><p data-rise>Your home should reflect your personality, lifestyle and comfort. From modern apartments to luxury villas, we design timeless spaces with warmth, elegance and practicality in every corner.</p></div>
    <div class="trio">
      <figure style="margin:0">{ph("res-12", "r-45", "(max-width: 860px) 100vw, 33vw", where="residential", attrs="")}<figcaption class="cap"><span class="meta">Bedroom</span></figcaption></figure>
      <figure style="margin:0">{ph("res-40", "r-45", "(max-width: 860px) 50vw, 33vw", where="residential", attrs="")}<figcaption class="cap"><span class="meta">Modular kitchen</span></figcaption></figure>
      <figure style="margin:0">{ph("res-42", "r-45", "(max-width: 860px) 50vw, 33vw", where="residential", attrs="")}<figcaption class="cap"><span class="meta">Kids' room</span></figcaption></figure>
    </div>
    {deflist(RES)}
    <p style="margin-top:40px"><a class="tlink tlink--bronze" href="contact.html?type=Full+home+interiors">Plan your home with us {ARR}</a></p>
  </div>
</section>
<section class="sec stone" id="commercial" aria-labelledby="com-h">
  <div class="wrap split">
    <figure class="split__pic" style="margin:0">{ph("com-45", "r-32", "(max-width: 860px) 100vw, 58vw", where="commercial", attrs="")}<figcaption class="cap"><span class="meta">Open-plan office</span></figcaption></figure>
    <div class="split__text">
      <h2 data-lines>Commercial interiors</h2>
      <p class="lead" data-rise>Every workplace, retail space or hospitality venue should look impressive and also improve productivity, customer engagement and the overall experience.</p>
      {deflist(COM, "deflist deflist--1")}
      <p style="margin-top:32px"><a class="tlink tlink--bronze" href="contact.html?type=Office+interiors">Discuss a commercial project {ARR}</a></p>
    </div>
  </div>
</section>
<section class="sec" id="specialized" aria-labelledby="spec-h">
  <div class="wrap split split--wide-list">
    <div class="split__text">
      <h2 data-lines>Specialized interior solutions</h2>
      <p class="lead" data-rise>Good design comes from communication. Our specialized services focus on commercial tenant improvements, combining creative design with technical knowledge of construction standards.</p>
      {deflist(SPEC, "deflist deflist--2")}
    </div>
    <figure class="split__pic" style="margin:0">{ph("company", "r-45", "(max-width: 860px) 100vw, 33vw", where="specialized", attrs="")}<figcaption class="cap"><span class="meta">Marking up construction drawings</span></figcaption></figure>
  </div>
</section>
<section class="sec dark" id="turnkey" aria-labelledby="turn-h">
  <div class="wrap split split--rev">
    <figure class="split__pic" style="margin:0">{ph("res-33", "r-32", "(max-width: 860px) 100vw, 58vw", where="turnkey", attrs="")}<figcaption class="cap"><span class="meta">Grey modular kitchen</span></figcaption></figure>
    <div class="split__text">
      <h2 data-lines>Turnkey delivery</h2>
      <p class="lead" data-rise>We don't hand over drawings and walk away. Quantity surveying, procurement, project planning, site management and quality control are all ours, so one studio answers for the result.</p>
      <p data-rise><a class="tlink tlink--bronze" href="process.html">See all ten stages {ARR}</a></p>
    </div>
  </div>
</section>'''
page("services.html", "Interior Design Services | Atwood Dsigns", "Residential interiors, commercial interiors, specialized interior solutions and turnkey delivery from Atwood Dsigns, Hyderabad.", services)

# ================================================================================================ PROCESS
PAGE = "process.html"
design = "".join(f"<li><b>{i + 1:02d}</b><div><strong>{t}</strong><span>{d}</span></div></li>" for i, (ph_, t, d, k) in enumerate(STAGES) if ph_ == "Design")
build = "".join(f"<li><b>{i + 1:02d}</b><div><strong>{t}</strong><span>{d}</span></div></li>" for i, (ph_, t, d, k) in enumerate(STAGES) if ph_ == "Build")
process = page_head("From first conversation to handover", "Our design process captures exactly what you want; our execution process makes sure it is built that way. Here is what happens at each of the ten stages.") + head_photo("res-30") + f'''
<section class="sec" aria-labelledby="all-h">
  <div class="wrap">
    <div class="sec-head"><h2 id="all-h" data-lines>The ten stages</h2><p data-rise>A structured process ensures every project is handled with precision: consultation, planning and concept development, then sourcing, installation and a final quality review.</p></div>
    <div class="stages">
      <div><h3 data-rise>Design process</h3><ol data-stagger>{design}</ol></div>
      <div><h3 data-rise>Execution process</h3><ol data-stagger>{build}</ol></div>
    </div>
  </div>
</section>
{stage_row("proc-h")}
<section class="sec" aria-labelledby="why-h">
  <div class="wrap split">
    <figure class="split__pic" style="margin:0">{ph("res-24", "r-32", "(max-width: 860px) 100vw, 58vw", where="why one team", attrs="")}<figcaption class="cap"><span class="meta">Wardrobe and window seat on site</span></figcaption></figure>
    <div class="split__text">
      <h2 data-lines>Why one team matters</h2>
      <p class="lead" data-rise>When the people who design your space also manage its construction, nothing gets lost between the drawing and the site.</p>
      <p class="muted" data-rise>Our designers visit the site while work is in progress, and a committed site supervisor manages day-to-day activities, monitors materials and resolves problems as they arise.</p>
    </div>
  </div>
</section>'''
page("process.html", "Our Design and Build Process | Atwood Dsigns", "The ten stages of the Atwood Dsigns design and execution process, from concept design to quality control.", process)

# ================================================================================================ IDEAS
PAGE = "ideas.html"
IDEAS = [  # (anchor, title, built photo, drawing, portfolio filter, contact type, paragraphs)
    ("living-room", "Living room", "res-37", "res-08", "living", "Living+room",
     ["Your living room sets the tone for the entire home. It's the first space guests see and the corner where the family gathers to relax, talk, watch TV and celebrate, so its design should reflect your home's personality.",
      "We offer fully customised designs that bring out your individuality with comfort and elegance, and as a complete interior solutions provider we handle everything from civil work and electricals to painting and décor."]),
    ("tv-unit", "TV unit", "res-23", None, "living", "Living+room",
     ["A TV unit is more than a piece of furniture. It shapes viewing comfort and the whole feel of the living room, which is often where the family gathers to unwind.",
      "We design it as a focal point that complements your interiors and reflects your lifestyle, not just a place for a screen."]),
    ("kids-bedroom", "Kids' bedroom", "res-21", "res-42", "kids", "Bedroom+or+kids%27+room",
     ["A child's room should be lively and personal, supporting play, learning and growth as well as rest.",
      "Choosing colours, furniture and décor can feel overwhelming. We bring thoughtful, affordable ideas tailored to your space and your child's imagination, delivered on time."]),
    ("modular-kitchen", "Modular kitchen", "res-40", "res-39", "kitchen", "Kitchen",
     ["The kitchen is the heart of every home. Every choice, from layout to finishes, should reflect your taste and make daily routines easier, in a space that feels bright, organised and clutter-free.",
      "We design modern, elegant and customised modular kitchens around the way you cook. Ask us for designs and a personalised quote."]),
    ("bedroom", "Bedroom", "res-12", "res-43", "bedroom", "Bedroom+or+kids%27+room",
     ["Our bedrooms are modern, stylish and space-efficient, with elegance and function in every detail.",
      "A few ideas that make a real difference: make the ceiling feel taller, balance light and dark shades, keep one colour palette, add texture, and finish with a statement piece of wall art."]),
    ("bathroom", "Bathroom", "interior4", None, None, "Bathroom",
     ["A bathroom is one of the most used rooms in any home, so it should be planned with care. It must balance function with hygiene, which makes detailing especially important.",
      "Our end-to-end approach keeps you involved at every stage. By understanding the space and visualising how each element comes together, we create bathrooms that are practical, stylish and complete."]),
]
tiles = "".join(f'''<a href="#{a}">{ph(b, "r-45", "(max-width: 520px) 50vw, (max-width: 960px) 50vw, 33vw", where="room index", alt="")}<div class="cap"><h2>{t}</h2><span class="meta">{"Design illustration" if pf is None else "A room we built"}</span></div></a>''' for a, t, b, d, pf, ty, ps in IDEAS)
ideas = page_head("Ideas, room by room", "How we think about the rooms people ask us about most, shown with rooms we have designed and built.") + f'''
<section class="sec sec--flush-top" aria-label="Rooms"><div class="wrap"><div class="rooms-index" data-stagger>{tiles}</div></div></section>'''
for n, (a, t, b, d, pf, ty, ps) in enumerate(IDEAS):
    rev = " idea--rev" if n % 2 else ""
    if pf is None:  # no studio photograph of this room type: the illustration from the previous website
        pair = f'''<div class="idea__pair idea__pair--one">
        <figure style="margin:0">{ph(b, "r-32", "(max-width: 860px) 100vw, 58vw", where=f"{t} illustration", attrs="")}<figcaption><span class="meta">Design illustration</span></figcaption></figure>
      </div>'''
        more = ""
    elif d:
        pair = f'''<div class="idea__pair">
        <figure style="margin:0">{ph(b, "r-45", "(max-width: 860px) 50vw, 29vw", where=t, attrs="")}<figcaption><span class="meta">{PHOTOS[b][1]}</span></figcaption></figure>
        <figure style="margin:0" class="idea__second">{ph(d, "r-45", "(max-width: 860px) 50vw, 29vw", where=t, attrs="")}<figcaption><span class="meta">{PHOTOS[d][1]}</span></figcaption></figure>
      </div>'''
        more = f'<a class="tlink" href="portfolio.html#{pf}">See more in the portfolio {ARR}</a>'
    else:
        pair = f'''<div class="idea__pair idea__pair--one">
        <figure style="margin:0">{ph(b, "r-32", "(max-width: 860px) 100vw, 58vw", where=t, attrs="")}<figcaption><span class="meta">{PHOTOS[b][1]}</span></figcaption></figure>
      </div>'''
        more = f'<a class="tlink" href="portfolio.html#{pf}">See more in the portfolio {ARR}</a>'
    ideas += f'''
<section class="idea sec{rev}" id="{a}" aria-labelledby="{a}-h">
  <div class="wrap grid">
    {pair}
    <div class="idea__text">
      <h2 id="{a}-h" data-lines>{t}</h2>
      {"".join(f"<p data-rise>{p}</p>" for p in ps)}
      <div class="actions" data-rise><a class="btn" href="contact.html?type={ty}">Plan your {t if t.startswith("TV") else t.lower()} {ARR}</a>{more}</div>
    </div>
  </div>
</section>'''
page("ideas.html", "Interior Ideas, Room by Room | Atwood Dsigns", "Living room, TV unit, kids' bedroom, modular kitchen, bedroom and bathroom ideas from Atwood Dsigns, Hyderabad.", ideas)

# ================================================================================================ PORTFOLIO
PAGE = "portfolio.html"
CATS = [("all", "All"), ("kitchen", "Kitchens"), ("bedroom", "Bedrooms"), ("kids", "Kids' rooms"), ("living", "Living and dining"), ("entrance", "Entrances and pooja"), ("commercial", "Commercial")]
CAT_NAME = dict(CATS)
CAT_ONE = {"kitchen": "Kitchen", "bedroom": "Bedroom", "kids": "Kids' room", "living": "Living and dining", "entrance": "Entrance and pooja", "commercial": "Commercial"}
CARDS = [  # (title, category, photographs: the first leads)
    ("Space-themed kids' bedroom", "kids", ["res-21", "res-25", "res-14", "res-35", "res-44", "res-29", "res-20"]),
    ("Dining, bar and display unit", "living", ["res-11", "res-08"]),
    ("Warm-lit entrance lobby", "entrance", ["res-32"]),
    ("Mint modular kitchen", "kitchen", ["res-40"]),
    ("Bedroom with a study wall", "bedroom", ["res-12"]),
    ("Pooja unit", "entrance", ["res-22"]),
    ("Navy and white kitchen", "kitchen", ["res-39"]),
    ("Kids' study and wardrobe", "kids", ["res-42"]),
    ("Grey modular kitchen", "kitchen", ["res-33"]),
    ("Marble TV wall", "living", ["res-37"]),
    ("Pink arched wardrobe", "bedroom", ["res-43"]),
    ("Foyer with backlit niches", "entrance", ["res-04"]),
    ("Dining table by the window", "living", ["res-05"]),
    ("Loft bed for a child", "kids", ["res-15", "res-06"]),
    ("Open kitchen and hall", "kitchen", ["res-30", "res-07"]),
    ("Glazed timber door", "entrance", ["res-18"]),
    ("Grey sliding wardrobe", "bedroom", ["res-36"]),
    ("Lit feature wall", "entrance", ["res-09"]),
    ("Entrance with a brass screen", "entrance", ["res-27"]),
    ("Wardrobe and window seat", "bedroom", ["res-24"]),
    ("Fitted wardrobes", "bedroom", ["res-31"]),
    ("Backlit TV unit", "living", ["res-23"]),
    ("Office cabin", "commercial", ["com-01"]),
    ("Open-plan office", "commercial", ["com-45"]),
    ("Conference room", "commercial", ["com-28"]),
    ("Reception lounge", "commercial", ["com-38"]),
    ("Office lounge", "commercial", ["com-10"]),
]
HELD_BACK = {"res-41": "sofa still in its plastic wrapping (used only for the site management stage)", "res-46": "dark and cluttered",
             "res-13": "duplicate of com-38", "com-16": "duplicate of com-10",
             "com-19": "residential library image filed under commercial", "com-26": "library image of uncertain use",
             "com-34": "library image of a kitchen with a person in frame",
             "com-17": "library image; held back so the portfolio grid closes on full rows",
             "com-03": "library image; held back so the portfolio grid closes on full rows",
             "com-02": "library image; held back so the portfolio grid closes on full rows",
             "com-47": "library image; held back so the portfolio grid closes on full rows"}
counts = {c: sum(1 for _, cc, _ in CARDS if cc == c) for c, _ in CATS}
counts["all"] = len(CARDS)
cards = ""
for n, (title, cat, keys) in enumerate(CARDS, 1):
    lead = keys[0]
    photos = "|".join(f"{PHOTOS[k][0]}::{PHOTOS[k][1]}" for k in keys)
    for k in keys[1:]:
        USED.setdefault(k, set()).add("portfolio.html: viewer sequence")
    USED.setdefault(lead, set()).add("portfolio.html: card")
    more = f'<span class="more" aria-hidden="true">{len(keys)} photographs</span>' if len(keys) > 1 else ""
    label = f"{title}, {CAT_ONE[cat].lower()}" + (f", {len(keys)} photographs" if len(keys) > 1 else "")
    cards += f'''<a class="card" href="{PHOTOS[lead][0]}" data-cat="{cat}" data-photos="{photos}" aria-label="{label}">
      <div class="ph r-45" style="--pos: {PHOTOS[lead][3]}">{img_tag(PHOTOS[lead][0], PHOTOS[lead][1], "(max-width: 520px) 100vw, (max-width: 960px) 50vw, 33vw")}{more}</div>
      <div class="cap"><span class="idx">{n:02d}</span><h2>{title}</h2><span class="meta">{CAT_ONE[cat]}</span></div>
    </a>'''
chips = "".join(f'<button type="button" data-filter="{c}" aria-pressed="{"true" if c == "all" else "false"}">{n}<small>{counts[c]}</small></button>' for c, n in CATS)
pf_row = "".join(f'''<a class="pj" href="{pr["slug"]}.html">{ph(pr["card"], "r-45", "(max-width: 860px) 100vw, 33vw", where="portfolio projects", alt="", attrs="")}<span class="pj__cap"><span class="idx">{n:02d}</span><span class="pj__title">{pr["title"]}</span><span class="meta">{pr["cat"]}, {len(pr["photos"])} photographs</span><em class="pj__go">View project &rarr;</em></span></a>''' for n, pr in enumerate(PROJECTS, 1))
portfolio = page_head("Rooms we have designed and built", "Kitchens, bedrooms, kids' rooms, living spaces and entrances across Hyderabad. Choose a room to see it full size, with every photograph of that space.") + f'''
<section class="sec sec--flush-top pf-projects" aria-labelledby="pfp-h">
  <div class="wrap">
    <div class="sec-head"><h2 id="pfp-h" data-lines>Projects</h2><p data-rise>Spaces photographed in depth, with notes on what went into each.</p></div>
    <div class="pf-projects__row">{pf_row}</div>
  </div>
</section>
<div class="filterbar"><div class="wrap"><div class="chips" role="group" aria-label="Filter by room">{chips}</div><p class="count" aria-hidden="true"><b data-count>{len(CARDS)}</b> rooms</p></div></div>
<section class="sec sec--flush-top" aria-labelledby="pf-h">
  <div class="wrap">
    <h2 class="sr-only" id="pf-h">Rooms</h2>
    <p class="sr-only" role="status" id="filter-status"></p>
    <div class="gallery">{cards}</div>
  </div>
</section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photograph viewer" aria-hidden="true">
  <img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt="">
  <button class="icon-btn lb-close" type="button" aria-label="Close">{CLOSE}</button>
  <button class="icon-btn lb-prev" type="button" aria-label="Previous photograph">{ARROW_L}</button>
  <button class="icon-btn lb-next" type="button" aria-label="Next photograph">{ARROW_R}</button>
  <p class="lb-count"><span class="lb-caption"></span><span class="lb-index"></span></p>
</div>'''
page("portfolio.html", "Portfolio | Atwood Dsigns", "Kitchens, bedrooms, kids' rooms, living spaces and entrances designed and built by Atwood Dsigns in Hyderabad.", portfolio)

# ================================================================================================ PROJECT PAGES
for n, pr in enumerate(PROJECTS):
    PAGE = pr["slug"] + ".html"
    nxt = PROJECTS[(n + 1) % len(PROJECTS)]
    seq = ""
    for k, kind in pr["seq"]:
        cls = {"wide": "ps--wide", "half": "ps--half", "half-tall": "ps--half"}[kind]
        ratio = {"wide": "r-32", "half": "r-45", "half-tall": "r-45"}[kind]  # paired photographs share one proportion
        seq += f'''<figure class="ps {cls}">{ph(k, ratio, "(max-width: 860px) 100vw, " + ("100vw" if kind == "wide" else "50vw"), where="project sequence", attrs="")}<figcaption class="meta">{PHOTOS[k][1]}</figcaption></figure>'''
    body = f'''<section class="project-hero" aria-labelledby="pr-h">
  <div class="project-hero__media">{img_tag(PHOTOS[pr["lead"]][0], PHOTOS[pr["lead"]][1], "100vw", lazy=False, extra=f' fetchpriority="high" style="--pos: {PHOTOS[pr["lead"]][3]}"')}</div>
  <div class="hero__shade" aria-hidden="true"></div>
  <div class="wrap project-hero__text">
    <p class="label"><a href="portfolio.html">Portfolio</a> / Project {n + 1:02d}</p>
    <h1 data-lines>{pr["title"]}</h1>
    <dl class="project-facts">
      <div><dt class="meta">Room</dt><dd>{pr["cat"]}</dd></div>
      <div><dt class="meta">Photographs</dt><dd>{len(pr["photos"])}</dd></div>
      <div><dt class="meta">Studio</dt><dd>Atwood Dsigns, design and build</dd></div>
    </dl>
  </div>
</section>
<section class="sec" aria-labelledby="ov-h">
  <div class="wrap grid">
    <div class="project-side"><h2 class="label" id="ov-h">Overview</h2></div>
    <div class="project-main">
      <p class="statement" data-rise>{pr["overview"]}</p>
      <h3 class="label project-sub" data-rise>In the room</h3>
      <ul class="deflist deflist--2 project-seen" data-stagger>{"".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a, b in pr["seen"])}</ul>
      <p class="note" data-rise>Notes describe what is visible in the photographs.</p>
    </div>
  </div>
</section>
<section class="sec sec--flush-top" aria-label="Photographs">
  <div class="wrap pseq">{seq}</div>
</section>
<section class="sec stone project-next" aria-labelledby="nx-h">
  <div class="wrap grid">
    <div class="project-next__text">
      <h2 class="h2" id="nx-h" data-lines>Planning a room like this?</h2>
      <p class="lead muted" data-rise>Tell us about your space and we will walk you through how we would design and build it.</p>
      <div class="actions" data-rise><a class="btn" href="contact.html?type={pr["contact"]}">Plan a similar room {ARR}</a><a class="btn btn--ghost" href="portfolio.html#{pr["filter"]}">More {CAT_NAME[pr["filter"]].lower()}</a></div>
    </div>
    <a class="pj project-next__card" href="{nxt["slug"]}.html">{ph(nxt["card"], "r-32", "(max-width: 860px) 100vw, 40vw", where="next project", alt="")}<span class="pj__cap"><span class="idx">Next</span><span class="pj__title">{nxt["title"]}</span><span class="meta">{nxt["cat"]}</span><em class="pj__go">View project &rarr;</em></span></a>
  </div>
</section>'''
    page(PAGE, f"{pr['title']} | Atwood Dsigns", f"{pr['title']} by Atwood Dsigns, an interior design and build studio in Hyderabad: photographs and notes on the materials, joinery and lighting.", body, closing=False, over=True)

# ================================================================================================ JOURNAL
# Posts are written in the Sanity Studio and fetched by tools/cms.py. Each gets its own page, journal-<slug>.html,
# next to the project pages; journal.html lists them, featured first and then newest.
PAGE = "journal.html"
JOURNAL = cms.load_posts()
esc = cms.esc


def post_href(p):
    return f"journal-{p['slug']}.html"


def post_card(p, h="h2"):
    pic = cms.ph(p["cover"], "r-32", "(max-width: 520px) 100vw, 25vw", alt="") if p["cover"] else ""
    return f'''<a class="toc-item" href="{post_href(p)}">{pic}<div><p class="meta">{cms.fmt_date(p["date"])} &middot; {esc(p["category"])}</p><{h}>{esc(p["title"])}</{h}><p>{esc(p["excerpt"])}</p></div></a>'''


def ld(*objs):
    """JSON-LD blocks; "</" is escaped so text from the CMS can't close the script element."""
    data = [json.dumps(o, ensure_ascii=False).replace("</", "<\\/") for o in objs]
    return "".join(f'\n<script type="application/ld+json">{d}</script>' for d in data)


def og(img):
    """A 1200 x 630 crop around the Studio hotspot, for WhatsApp, Facebook and LinkedIn previews."""
    h = img.get("hotspot") or {}
    return f'{img["url"]}?w=1200&h=630&fit=crop&crop=focalpoint&fp-x={h.get("x", .5):.3f}&fp-y={h.get("y", .5):.3f}&auto=format'


journal = page_head("Journal", "Notes from the studio on designing homes and workplaces that work.") + f'''
<section class="sec sec--flush-top" aria-label="Articles"><div class="wrap"><div class="toc-list" data-stagger>{"".join(post_card(p) for p in JOURNAL)}</div></div></section>'''
page("journal.html", "Journal | Atwood Dsigns", "Articles from Atwood Dsigns on residential, sustainable and commercial interior design.", journal,
     head_extra=ld({"@context": "https://schema.org", "@type": "Blog", "name": "Journal | Atwood Dsigns", "url": SITE + "journal/",
                    "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": SITE + post_href(p).replace(".html", "/"),
                                  "datePublished": p["date"].isoformat()} for p in JOURNAL]}))

for p in JOURNAL:
    PAGE = post_href(p)
    url = SITE + PAGE.replace(".html", "/")
    body_html, faqs = cms.render_body(p["body"], SITE)
    by = esc(p["author"] or "Atwood Dsigns") + (f", {esc(p['author_role'])}" if p["author"] and p["author_role"] else "")
    hero = f'''<div class="wrap">{cms.ph(p["hero"], "r-219 head-ph", "(max-width: 1320px) 100vw, 1320px", lazy=False, extra=' fetchpriority="high"')}</div>''' if p["hero"] else ""
    same = [q for q in JOURNAL if q is not p and set(q["categories"]) & set(p["categories"])]
    more = (same + [q for q in JOURNAL if q is not p and q not in same])[:3]
    related = f'''<section class="sec post-more" aria-labelledby="more-h"><div class="wrap">
  <h2 class="h2" id="more-h" data-lines>Keep reading</h2>
  <div class="toc-list" data-stagger>{"".join(post_card(q, "h3") for q in more)}</div>
</div></section>''' if more else ""
    body = f'''<article aria-labelledby="post-h">
<section class="page-head">
  <div class="wrap grid">
    <p class="label" data-rise><a href="journal.html">05 / Journal</a> &middot; {esc(p["category"])}</p>
    <h1 id="post-h" data-lines>{esc(p["title"])}</h1>
    <p class="lead" data-rise>{esc(p["excerpt"])}</p>
    <div class="page-head__aside" data-rise><p class="meta">{cms.fmt_date(p["date"])}<br>{p["read"]}<br>{by}</p></div>
  </div>
</section>
{hero}
<section class="sec"><div class="wrap"><div class="article__body">
{body_html}
</div></div></section>
</article>
{related}'''
    img = p["cover"] or p["hero"]
    schema = [{"@context": "https://schema.org", "@type": "Article", "mainEntityOfPage": {"@type": "WebPage", "@id": url},
               "headline": p["title"], "description": p["seo_desc"] or p["excerpt"], "image": [og(img)] if img else [],
               "datePublished": p["date"].isoformat(), "dateModified": p["updated"].isoformat(),
               "keywords": ", ".join(p["keywords"]), "articleSection": p["category"],
               "author": {"@type": "Person", "name": p["author"]} if p["author"] else {"@type": "Organization", "name": "Atwood Dsigns", "url": SITE},
               "publisher": {"@type": "Organization", "name": "Atwood Dsigns", "logo": {"@type": "ImageObject", "url": SITE + I + "logo-web-new-2.png"}}},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                  {"@type": "ListItem", "position": 2, "name": "Journal", "item": SITE + "journal/"},
                  {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]}]
    if faqs:
        schema.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["question"], "acceptedAnswer": {"@type": "Answer", "text": f["answer"]}} for f in faqs]})
    extra = (f'\n<meta name="keywords" content="{esc(", ".join(p["keywords"]))}">' if p["keywords"] else "") + ld(*schema)
    page(PAGE, esc(p["seo_title"] or f"{p['title']} | Atwood Dsigns"), esc(p["seo_desc"] or p["excerpt"]), body,
         og_image=og(img) if img else None, og_type="article", head_extra=extra, section="journal.html")

# Remove the pages of posts that were unpublished or renamed in the Studio.
for f in os.listdir(OUT):
    if f.startswith("journal-") and f.endswith(".html") and f not in {post_href(p) for p in JOURNAL}:
        os.remove(os.path.join(OUT, f))
        print("removed", f)

# ================================================================================================ CONTACT
PAGE = "contact.html"
contact = page_head("Start with a conversation", "Whether you have a question, need expert advice or are ready to transform your space, we're here to help. The first consultation is free.") + f'''
<section class="quick sec--flush-top" aria-label="Quickest ways to reach us">
  <div class="wrap quick__row">
    <a class="quick__a" href="{TEL}"><span class="meta">Call</span><span class="quick__v">{PHONE}</span><span class="arr" aria-hidden="true">&rarr;</span></a>
    <a class="quick__a" href="{WA}" target="_blank" rel="noopener"><span class="meta">WhatsApp</span><span class="quick__v">Message the studio</span><span class="arr" aria-hidden="true">&rarr;</span></a>
    <a class="quick__a" href="mailto:{EMAIL}"><span class="meta">Email</span><span class="quick__v">{EMAIL}</span><span class="arr" aria-hidden="true">&rarr;</span></a>
  </div>
</section>
<section class="contact sec" aria-labelledby="studio-h">
  <div class="wrap grid">
    <div class="contact-info">
      <h2 class="sr-only" id="studio-h">Contact details</h2>
      <dl data-stagger>
        <div><dt class="meta">Studio</dt><dd>{ADDR}</dd></div>
        <div><dt class="meta">Directions</dt><dd><a href="https://maps.google.com/?q=E-Infra+Tower+Brindavan+Colony+Kokapet+Hyderabad" target="_blank" rel="noopener">Open in Maps</a></dd></div>
        <div><dt class="meta">Consultation</dt><dd>Free, at our studio or your site</dd></div>
      </dl>
    </div>
    <form class="form" id="enquiry" novalidate data-rise>
      <h2>Book a free consultation</h2>
      <p>Tell us a little about your project and we'll get back to you.</p>
      <div class="field-row">
        <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required aria-describedby="e-name"><span class="err" id="e-name">Enter your name.</span></div>
        <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required aria-describedby="e-phone"><span class="err" id="e-phone">Enter a 10-digit phone number, or include your country code.</span></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="e-email"><span class="err" id="e-email">Enter an email address like name@example.com.</span></div>
        <div class="field"><label for="f-type">Project type</label>
          <select id="f-type" name="type"><option>Full home interiors</option><option>Kitchen</option><option>Bedroom or kids' room</option><option>Living room</option><option>Bathroom</option><option>Office interiors</option><option>Retail or hospitality</option><option>Something else</option></select></div>
      </div>
      <div class="field"><label for="f-area">Locality <span class="opt">(optional)</span></label><input id="f-area" name="area" autocomplete="address-level2" placeholder="For example Kokapet, Gachibowli, Narsingi"></div>
      <div class="field"><label for="f-msg">About your project</label><textarea id="f-msg" name="message" required aria-describedby="e-msg" placeholder="Location, size of the space, timeline, anything you have in mind"></textarea><span class="err" id="e-msg">Tell us a little about your project.</span></div>
      <div class="actions"><button class="btn" type="submit">Send by email</button><button class="btn btn--ghost" type="button" data-whatsapp>Send on WhatsApp</button></div>
      <p class="form-note">Both open your email or WhatsApp app with your details filled in, ready to send. What you type is kept on this device until you send it.</p>
      <div class="form-status" role="status" aria-live="polite"></div>
    </form>
  </div>
  <div class="wrap map-wrap"><iframe class="map" title="Map showing Atwood Dsigns in Kokapet, Hyderabad" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=E-Infra%20Tower%2C%20Brindavan%20Colony%2C%20Kokapet%2C%20Hyderabad%20500075&z=15&output=embed"></iframe></div>
</section>'''
page("contact.html", "Contact and Free Consultation | Atwood Dsigns", "Book a free interior design consultation with Atwood Dsigns in Kokapet, Hyderabad. Call +91 90001 81212 or message us on WhatsApp.", contact, closing=False)

# ================================================================================================ manifest
KIND = {"studio": "Studio photograph", "library": "Library image (previous website)"}
lines = ["# Photograph manifest", "",
         "Generated by `tools/build.py` from its `PHOTOS` table. To replace a picture, change its entry there and rebuild.", "",
         "Studio photographs are the ones the studio uploaded of its own finished rooms (February 2026). Library images came with the",
         "previous website and are most likely stock; replace them with the studio's own photographs when available.", "",
         "| Key | File | Kind | Focal point | Shows | Used on |", "|---|---|---|---|---|---|"]
for k, (src, desc, kind, pos) in PHOTOS.items():
    lines.append(f"| {k} | `{src}` | {KIND[kind]} | {pos} | {desc} | {'; '.join(sorted(USED.get(k, []))) or 'not used'} |")
lines += ["", "## Held back from the site", "", "| File | Reason |", "|---|---|"]
lines += [f"| {k} | {r} |" for k, r in HELD_BACK.items()]
with open(os.path.join(OUT, "ASSETS.md"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
print("built")
