"""Builds the static pages of the Atwood Dsigns site.

Run from anywhere:  python3 tools/build.py
Edit the content below, run the script, and every page is rewritten with the shared header and footer.
"""
import os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PHONE = "+91 90001 81212"
TEL = "tel:+919000181212"
WA = "https://wa.me/919000181212"
EMAIL = "atwood.dsigns@gmail.com"
ADDR = "Unit-1, 1st Floor, E-Infra Tower, Plot No. 32, Sy. No. 135, Brindavan Colony, Opp. Johnson Grammar School, Kokapet, Hyderabad 500075"
ADDR_SHORT = "E-Infra Tower, Brindavan Colony, Kokapet, Hyderabad 500075"
P = "assets/img/portfolio/"
I = "assets/img/"

NAV = [("services.html", "Services"), ("portfolio.html", "Portfolio"), ("process.html", "How we work"),
       ("ideas.html", "Ideas"), ("journal.html", "Journal"), ("about.html", "About")]
MENU = [("index.html", "Home")] + NAV + [("contact.html", "Contact")]
CUR = ' aria-current="page"'

ICON_IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.4 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2zm0 4.9a4.9 4.9 0 100 9.8 4.9 4.9 0 000-9.8zm0 8.1a3.2 3.2 0 110-6.4 3.2 3.2 0 010 6.4zm5.1-9.4a1.1 1.1 0 100 2.3 1.1 1.1 0 000-2.3z"/></svg>'
ICON_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1112 21.8zm8.4-18.2A11.8 11.8 0 001.7 17.9L0 24l6.3-1.6A11.8 11.8 0 0024 12c0-3.2-1.2-6.1-3.6-8.4z"/></svg>'
ARROW_L = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'
ARROW_R = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'
CLOSE = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>'
PAUSE_PLAY = '<svg class="i-pause" width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4h4v16H7zM13 4h4v16h-4z" fill="currentColor"/></svg><svg class="i-play" width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l13 8-13 8z" fill="currentColor"/></svg>'
DRAG = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M9 6l-6 6 6 6M15 6l6 6-6 6"/></svg>'


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


def img(src, alt, w=1500, h=1000, lazy=True, extra="", sizes="(max-width: 860px) 100vw, 50vw"):
    """An <img> with intrinsic size, lazy loading, and an 800px alternative when one exists."""
    lz = ' loading="lazy" decoding="async"' if lazy else ' decoding="async"'
    srcset = ""
    small = src[:-4] + "-800.jpg"
    if src.endswith(".jpg") and os.path.exists(os.path.join(OUT, small)):
        full = jpeg_width(os.path.join(OUT, src))
        srcset = f' srcset="{small} 800w, {src} {full}w" sizes="{sizes}"'
    return f'<img src="{src}"{srcset} alt="{alt}" width="{w}" height="{h}"{lz}{extra}>'


def header(current, light):
    links = "".join(f'<a href="{h}"{CUR if h == current else ""}>{t}</a>' for h, t in NAV)
    menu = "".join(f'<li><a href="{h}"{CUR if h == current else ""}>{t}</a></li>' for h, t in MENU)
    cls = "site-header site-header--light" if light else "site-header"
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="{cls}">
  <a class="brand" href="index.html" aria-label="Atwood Dsigns, home">{img(I + "logo-web-new-2.png", "Atwood Dsigns", 255, 97, lazy=False)}</a>
  <nav class="nav" aria-label="Main">{links}</nav>
  <a class="btn header-cta" href="contact.html">Book a free consultation</a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu-panel">Menu</button>
</header>
<div class="menu-panel" id="menu-panel" aria-hidden="true">
  <nav aria-label="Menu"><ul>{menu}</ul></nav>
  <p><a href="{TEL}">{PHONE}</a><br>{ADDR_SHORT}</p>
</div>'''


FOOTER = f'''<footer class="site-footer">
  <div class="foot-cols">
    <div><h2>Studio</h2><address>{ADDR}</address></div>
    <div><h2>Pages</h2><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in MENU[1:])}</ul></div>
    <div><h2>Follow</h2><ul>
      <li><a href="https://www.instagram.com/atwooddsigns/" target="_blank" rel="noopener">Instagram</a></li>
      <li><a href="https://www.linkedin.com/company/atwooddsigns/" target="_blank" rel="noopener">LinkedIn</a></li>
      <li><a href="https://www.pinterest.com/atwooddsignss/" target="_blank" rel="noopener">Pinterest</a></li></ul></div>
    <div><h2>Talk to us</h2><ul>
      <li><a href="{TEL}">{PHONE}</a></li>
      <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></li>
      <li>First consultation free</li></ul></div>
  </div>
  <div class="wordmark" aria-hidden="true">
    <svg class="wm-one" viewBox="0 0 1000 132"><text x="0" y="112" font-size="140" textLength="1000" lengthAdjust="spacingAndGlyphs">Atwood Dsigns</text></svg>
  </div>
  <div class="legal"><span>&copy; <span id="year">2026</span> Atwood Dsigns LLP. All rights reserved.</span><span>Interior design and build, Kokapet, Hyderabad</span></div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Chat with Atwood Dsigns on WhatsApp">{ICON_WA}</a>'''


def close_row(pic=P + "res-04.jpg", alt="Entrance foyer finished by Atwood Dsigns"):
    return f'''<section class="close frame" aria-labelledby="close-h">
  <div class="grid">
    <p class="close__line" data-rise>Tell us about your home, your office or the one room that isn't working, and we'll plan it with you.</p>
    <div class="close__pic" data-open>{img(pic, alt, 400, 400, sizes="180px")}</div>
    <div class="close__links" data-rise>
      <h2 id="close-h">Book a free consultation</h2>
      <a class="link link--accent" href="contact.html">Send us your project</a>
      <a class="link" href="{TEL}">Call {PHONE}</a>
      <p>Studio in Kokapet, Hyderabad. The first meeting costs nothing.</p>
    </div>
  </div>
</section>'''


def page(fname, title, desc, body, light=True, closing=True):
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{P}res-32.jpg">
<meta name="theme-color" content="#1c1612">
<link rel="icon" href="{I}cropped-favicon-192x192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600&family=Marcellus&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
<script>(function (d) {{ d.classList.add('js'); if ('onpagereveal' in window) d.classList.add('vt'); setTimeout(function () {{ if (!d.classList.contains('ready')) d.classList.remove('js'); }}, 4000); }})(document.documentElement)</script>
<script type="speculationrules">{{"prefetch": [{{"where": {{"selector_matches": "a[href$='.html']"}}, "eagerness": "moderate"}}]}}</script>
</head>
<body>
{header(fname, light)}
<main id="main">
{body}
{close_row() if closing else ""}
</main>
{FOOTER}
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(html)


def page_head(crumb, h1, lead, pic, alt, aside=""):
    return f'''<section class="page-head frame">
  <div class="grid">
    <h1 class="display" data-lines>{h1}</h1>
    <p class="lead" data-rise>{lead}</p>
    {f'<div class="page-head__aside" data-rise>{aside}</div>' if aside else ""}
  </div>
</section>
<div class="head-pic">{img(pic, alt, 1500, 1000, lazy=False, extra=' data-scale fetchpriority="high"', sizes="100vw")}</div>'''


# ---------------------------------------------------------------- content
STAGES = [
    ("Design", "First, we listen", "A detailed conversation to learn your needs, agree the scope and understand how the space should look and work.", I + "atwood1.jpg", "Clients reviewing plans with a designer"),
    ("Design", "Then we plan the space", "Spatial planning and 3D visual concepts that set the overall design direction.", I + "Interior-design-drawings-floor-plans.jpg", "Coloured floor plan of an apartment"),
    ("Design", "We refine every detail", "The design evolves with you, detail by detail, and we choose the materials together.", I + "bedroom-design.jpg", "Pencil drawing of a bedroom design"),
    ("Design", "We draw it for every trade", "Complete working drawings: electrical layouts, false ceilings, carpentry and more.", I + "company.jpg", "Designers marking up construction drawings"),
    ("Design", "We visit the site", "Our designers check the work regularly so it is built exactly to plan.", P + "res-24.jpg", "Blue wardrobe being installed in a bedroom"),
    ("Build", "We price it exactly", "A detailed cost estimate based on the chosen design and materials, before work starts.", I + "atwood.jpg", "Clients going through an estimate"),
    ("Build", "We buy and check materials", "Our procurement team sources furnishings, fixtures and fittings and checks every delivery.", P + "res-31.jpg", "Bedroom with fitted wardrobes"),
    ("Build", "We schedule the work", "A project timeline that sets the order of every task and how long each one takes.", P + "res-36.jpg", "Bedroom with sliding wardrobe and side unit"),
    ("Build", "A supervisor runs the site", "Day-to-day management of materials, the crew and any problem that comes up.", P + "res-30.jpg", "Open kitchen and living area with false ceiling"),
    ("Build", "Last, we check everything", "An internal quality review against industry standards before we hand over the keys.", P + "res-41.jpg", "Finished living room with recliner sofa"),
]

QUOTES = [
    ("They turned our plain living room into a stylish, welcoming space that feels elegant and comfortable.", "Avinash Kumar", "living room"),
    ("They redesigned our corporate office. It looks modern, encourages collaboration and impresses our clients.", "Suresh", "corporate office"),
    ("The lighting, furniture and soothing tones turned our bedroom into a retreat we look forward to every night.", "Padmavathi", "bedroom"),
    ("Functional yet stylish, our team loves it, and the project was delivered on time and within budget.", "Bharath", "office interiors"),
    ("Our store needed a fresh look and they nailed it. It attracts more customers and the layout works far better.", "Manjunath", "retail store"),
    ("I wanted a kitchen that was practical and beautiful, and that's exactly what I got.", "Praveena", "kitchen"),
]

FAQS = [
    ("How does the process work?", "We start with a consultation to understand your requirements. We then develop design concepts for your approval, and once the design is final we manage the execution through to handover."),
    ("Can you work with my budget?", "Yes. We plan the space and choose materials to give you a beautiful, functional result within the budget you set."),
    ("How long does a project take?", "It depends on the size and complexity. We aim to deliver within 30 days, though some projects need longer."),
    ("Can I bring my own ideas?", "Of course. We work with you at every stage so the space reflects your personality and how you live."),
    ("Which styles do you design in?", "Modern, traditional, minimalist, industrial, luxury, Scandinavian and contemporary, each tailored to your taste."),
    ("How do I get started?", "Book a free consultation online or call us. We'll walk you through the first steps and answer your questions."),
]


def faq_list(light=False):
    return "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for q, a in FAQS)


ROOMS = [("Foyer", "res-04", "Entrance foyer with backlit circular niches"),
         ("Kitchen", "res-40", "Modular kitchen with mint shutters and under-cabinet lighting"),
         ("Kids' room", "res-21", "Space-themed kids' bedroom with a sliding wardrobe"),
         ("Dining", "res-08", "Dining area with teal drapes and a crockery unit"),
         ("Bedroom", "res-12", "Bedroom with a grey upholstered bed and study desk")]

POSTS = [
    ("sustainable", "trunkey-interior-3.jpg", "Sustainable interior design", "Responsible design for modern living",
     "Sustainability is no longer optional. Interior design can reduce environmental impact while improving the quality of life indoors.",
     [("Sustainable material choices", ["Eco-friendly materials reduce environmental harm while offering durability and health benefits. Low-VOC finishes, responsibly sourced wood and recycled materials improve indoor air quality and last longer."]),
      ("Energy-efficient design", ["Making the most of natural light, ventilation and spatial planning reduces energy use. Smart layouts cut the need for artificial lighting and climate control."]),
      ("Designing for longevity", ["Sustainable design favours durability over trends. Timeless aesthetics and quality craftsmanship help interiors age gracefully, so they need renovating less often."]),
      ("In short", ["Sustainable interior design combines responsibility with beauty. At Atwood Dsigns, sustainability is part of every stage of design."])]),
    ("commercial", "commercial-interior-5.jpg", "Commercial interior design", "Spaces that drive productivity and brand identity",
     "Commercial interiors shape perception, productivity and performance. We design commercial spaces that support business goals and inspire the people who use them.",
     [("Reflecting brand identity", ["An office or commercial space communicates a brand's values before a single word is spoken. Colours, materials and layouts all shape how clients and employees see the brand.", "We make sure the interior supports your brand story and professional credibility."]),
      ("Enhancing productivity through design", ["Design affects how people work. Ergonomic furniture, efficient layouts and good lighting reduce fatigue and improve focus. Zoning for collaboration and privacy makes teams more efficient."]),
      ("Creating positive customer experiences", ["Retail and commercial interiors should guide movement, create comfort and encourage engagement. Thoughtful layouts and inviting details improve customer satisfaction and retention."]),
      ("In short", ["Commercial interior design is a strategic investment. With careful planning and execution, interiors become tools for growth, productivity and brand success."])]),
    ("residential", "gallery7.jpg", "Residential interior design", "Creating homes that support real life",
     "A home is more than a structure; it's where life unfolds. Good residential design improves comfort, reflects personality and supports everyday routines.",
     [("Designing around lifestyle", ["Every household is different. Some families love to entertain, others value quiet. We shape each design around daily habits, family dynamics and future needs.", "That means kitchens that make cooking effortless, bedrooms that encourage rest and living spaces that bring people together."]),
      ("Comfort through thoughtful design", ["Comfort goes beyond furniture. It includes lighting levels, ventilation, acoustics and spatial balance. Soft lighting, natural materials and intuitive layouts create calm spaces that support well-being."]),
      ("Smart storage and functional layouts", ["Clutter-free homes feel bigger and calmer. Built-in units, modular furniture and hidden storage keep things organised without spoiling the look."]),
      ("Timeless design choices", ["Trends change, but good design lasts. We favour timeless styles that adapt over time, so your home stays relevant and elegant for years."]),
      ("In short", ["A thoughtfully designed home improves everyday life. We create residential interiors that feel personal, practical and beautifully livable."])]),
]


def moments_section(h2_id="moments-h"):
    cols = "".join(f'''<li class="moment">
        <p class="moment__stage">{stage}</p>
        <h3>{t}</h3>
        <p>{d}</p>
        <div class="gap"></div>
        <div class="pic">{img(src, alt, 800, 1000, sizes="(max-width: 700px) 72vw, 300px")}</div>
      </li>''' for stage, t, d, src, alt in STAGES)
    return f'''<section class="moments on-dark frame" data-row aria-labelledby="{h2_id}">
  <div class="moments__top">
    <h2 class="display" id="{h2_id}" data-lines>Ten stages, one team</h2>
    <p class="lead muted" data-rise>Five stages of design, five of building. The people who draw your space are the people who build it.</p>
    <div class="moments__nav"><button class="icon-btn" type="button" data-dir="prev" aria-label="Earlier stages">{ARROW_L}</button><button class="icon-btn" type="button" data-dir="next" aria-label="Later stages">{ARROW_R}</button></div>
  </div>
  <div class="progress-row" aria-hidden="true"><div class="progress"><span></span></div><p class="moments__count">Stages <b>1 to 4</b> of 10</p></div>
  <p class="sr-only" role="status" data-row-status></p>
  <ol class="row" aria-label="The ten stages, in order. Use the arrow keys to move between stages." tabindex="0">{cols}</ol>
</section>'''


def drawn_section():
    first = ROOMS[0]
    buttons = "".join(
        f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-built="{P}{f}.jpg" data-drawn="{I}drawn/{f}.jpg" data-alt="{alt}">{name}</button>'
        for i, (name, f, alt) in enumerate(ROOMS))
    return f'''<section class="drawn on-paper frame" aria-labelledby="drawn-h">
  <div class="grid">
    <div class="drawn__text">
      <h2 class="title" id="drawn-h" data-lines>Drawn first, then built</h2>
      <p data-rise>These are rooms we have finished. Drag across each one to see it as a drawing, the way it looked on our desk before a single cabinet was made.</p>
      <div class="rooms" role="group" aria-label="Choose a room" data-stagger>{buttons}</div>
    </div>
    <div class="compare" data-open>
      {img(P + first[1] + ".jpg", first[2], 1500, 1125, extra=' class="compare__built"', sizes="(max-width: 960px) 100vw, 60vw")}
      {img(I + "drawn/" + first[1] + ".jpg", "", 1500, 1125, extra=' class="compare__drawn"', sizes="(max-width: 960px) 100vw, 60vw")}
      <label class="sr-only" for="compare-range">Show more of the drawing or the finished <span class="compare__name">{first[0]}</span></label>
      <input id="compare-range" type="range" min="0" max="100" value="50" step="1">
      <div class="compare__handle" aria-hidden="true"><span class="compare__knob">{DRAG}</span></div>
      <span class="compare__tag compare__tag--l" aria-hidden="true">Drawn</span>
      <span class="compare__tag compare__tag--r" aria-hidden="true">Built</span>
    </div>
  </div>
</section>'''


def quote_section(bg=P + "res-37.jpg"):
    figs = "".join(f'<figure class="{"is-on" if i == 0 else ""}"><blockquote>&ldquo;{q}&rdquo;</blockquote><figcaption>{n} <span>&nbsp;on their {p}</span></figcaption></figure>' for i, (q, n, p) in enumerate(QUOTES))
    return f'''<section class="quote-sec" aria-labelledby="quote-h">
  <div class="slides">{img(bg, "", 1500, 1125, extra=' class="is-on"', sizes="100vw")}</div>
  <h2 id="quote-h">What clients say</h2>
  <div class="quote-sec__in">
    <div class="quotes" aria-live="off">{figs}</div>
    <div class="quote-ctl"><button class="icon-btn slide-toggle" type="button" aria-pressed="false" aria-label="Pause quotations">{PAUSE_PLAY}</button><span class="count">1 of {len(QUOTES)}</span><button class="icon-btn" type="button" data-q="prev" aria-label="Previous quotation">{ARROW_L}</button><button class="icon-btn" type="button" data-q="next" aria-label="Next quotation">{ARROW_R}</button></div>
  </div>
</section>'''


def faq_section():
    return f'''<section class="faq-sec on-stone frame" aria-labelledby="faq-h">
  <div class="grid">
    <div class="faq-sec__text">
      <h2 class="title" id="faq-h" data-lines>Before you call</h2>
      <ul class="facts" data-stagger>
        <li><span>Studio</span>{ADDR_SHORT}</li>
        <li><span>Phone</span><a href="{TEL}">{PHONE}</a></li>
        <li><span>Consultation</span>Free, at our studio or your site</li>
      </ul>
      <div class="faq" data-stagger>{faq_list()}</div>
      <div class="faq-sec__ctas"><a class="btn btn--light" href="contact.html">Book a free consultation</a><a class="link link--accent" href="about.html">About the studio</a></div>
    </div>
    <div class="faq-sec__pics">
      <div class="tall" data-open>{img(P + "res-05.jpg", "Dining table with upholstered chairs under sheer curtains", 1125, 1500)}</div>
      <div class="sq" data-open>{img(P + "res-22.jpg", "Backlit pooja unit with carved panel", 800, 800, sizes="(max-width: 960px) 38vw, 18vw")}</div>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- HOME
hero_imgs = [("res-32", "Entrance lobby", "Warmly lit entrance lobby with a wood-clad door"),
             ("res-22", "Pooja unit", "Backlit pooja unit with a carved panel"),
             ("res-09", "Feature wall", "Backlit feature wall with a warm wash of light"),
             ("res-18", "Main door", "Wooden main door with glazed panels")]
hero_stack = "".join(img(P + f + ".jpg", a, 1125, 1500, lazy=(i > 0), sizes="(max-width: 1100px) 74vw, 30vw",
                         extra=f' data-name="{n}"' + (' class="is-on" fetchpriority="high"' if i == 0 else "")) for i, (f, n, a) in enumerate(hero_imgs))

PROJECTS = [
    ("a", "res-08", "Dining and living", "Teal drapes, a gold-based dining table and a backlit glass crockery unit.", 1500, 1000),
    ("b", "res-32", "Entrance lobby", "Warm wall washes and a wood-clad door that frames the arrival.", 1125, 1500),
    ("c", "res-14", "Kids' bedroom", "A space-themed wardrobe, a scalloped headboard and a world-map study wall.", 1500, 675),
    ("a", "res-40", "Modular kitchen", "Mint shutters, fluted-glass uppers and light tucked under every cabinet.", 1500, 1500),
    ("d", "res-15", "Loft bed for a child", "A ladder bed with storage below, set under a circular window niche.", 1125, 1500),
    ("c", "com-45", "Open-plan office", "Planted ceilings, long shared benches and meeting rooms off the floor.", 1500, 1000),
]


def projects():
    out = []
    for i, (kind, f, name, desc, w, h) in enumerate(PROJECTS):
        remark = '<p class="remark" data-rise>Every room here was drawn in our studio before our own site team built it.</p>' if i == 1 else ""
        if kind in "ad":
            out.append(f'''<article class="proj proj--{kind}">
      <figure><a class="pic" href="portfolio.html" data-open data-cursor="View">{img(P + f + ".jpg", name + " by Atwood Dsigns", w, h)}</a></figure>
      <div class="side" data-rise><h3 class="name">{name}</h3><p class="desc">{desc}</p></div>
    </article>''')
            continue
        out.append(f'''<article class="proj proj--{kind}">
      {remark}
      <figure>
        <a class="pic" href="portfolio.html" data-open data-cursor="View">{img(P + f + ".jpg", name + " by Atwood Dsigns", w, h)}</a>
        <figcaption><h3 class="name">{name}</h3><p class="desc">{desc}</p></figcaption>
      </figure>
    </article>''')
    return "\n".join(out)


home = f'''<section class="hero" aria-labelledby="hero-h">
  <div class="hero__small" data-drift="0.06">{img(P + "res-20.jpg", "Backlit mirror with a glowing edge", 800, 800, lazy=False, sizes="(max-width: 1100px) 34vw, 12vw")}</div>
  <div class="hero__big" data-drift="-0.04">{hero_stack}</div>
  <div class="hero__copy">
    <h1 id="hero-h" data-lines>Interiors designed, drawn and built</h1>
  </div>
  <div class="hero__aside" data-rise>
      <p>Atwood Dsigns is one studio in Kokapet, Hyderabad, for homes, offices and shops, from the first sketch to the final coat of polish.</p>
      <a class="btn" href="contact.html">Book a free consultation <span class="arrow" aria-hidden="true">&rsaquo;</span></a>
  </div>
  <div class="hero__meta">
    <p class="hero__room"><span>{hero_imgs[0][1]}</span>, one of our finished rooms</p>
    <button class="slide-toggle slide-toggle--text" type="button" aria-pressed="false">{PAUSE_PLAY}<span class="label">Pause</span><span class="sr-only"> the slideshow</span></button>
  </div>
</section>

<section class="intro frame grid" aria-labelledby="intro-h">
  <h2 class="display" id="intro-h" data-lines>From sketch to handover</h2>
  <div class="intro__caps">
    <p data-rise>We turn spaces into experiences: a cosy home, a sharp office or a lively shop floor.</p>
    <p data-rise>Creativity, function and fine craftsmanship, with every detail made personal.</p>
  </div>
</section>
<div class="pano">{img(P + "res-27.jpg", "Entrance with a marble wall and a garlanded doorway, dressed for a housewarming", 1500, 699, extra=' data-scale')}</div>
<p class="pano-note frame">An entrance we designed and built, dressed in marigolds for the housewarming.</p>

{drawn_section()}

{moments_section()}

<section class="band-sec" aria-labelledby="band-h">
  <div class="band-sec__head frame">
    <h2 class="title" id="band-h" data-lines>What we design</h2>
    <p class="muted" data-rise>Four kinds of work, all delivered by the same team. Hover a panel to open it.</p>
  </div>
  <div class="band">
    <a class="panel" href="services.html#residential">{img(P + "res-42.jpg", "", 1125, 1500)}<div class="panel__label"><h3>Residential interiors</h3><p>Apartments and villas: living rooms, bedrooms, kitchens, kids' rooms and complete makeovers.</p></div></a>
    <a class="panel" href="services.html#commercial">{img(P + "com-45.jpg", "", 1500, 1000)}<div class="panel__label"><h3>Commercial</h3><p>Offices, retail and hospitality spaces that work hard and show your brand.</p></div></a>
    <a class="panel" href="services.html#specialized">{img(I + "specialized-interior-3.jpg", "", 1500, 1000)}<div class="panel__label"><h3>Specialized</h3><p>Tenant improvements, as-built surveys, code compliance and 3D rendering.</p></div></a>
    <a class="panel" href="process.html">{img(P + "res-33.jpg", "", 1125, 1500)}<div class="panel__label"><h3>Turnkey</h3><p>We manage procurement, the site and quality control through to handover.</p></div></a>
  </div>
  <p class="band-note frame">Residential, commercial, specialized and turnkey work, each with its own page.</p>
</section>

<section class="scatter frame" aria-labelledby="work-h">
  <h2 class="display" id="work-h" data-lines>Recent work</h2>
  {projects()}
  <div class="scatter__more" data-rise><a class="btn btn--ink" href="portfolio.html">See all 47 photographs</a><a class="link" href="ideas.html">Ideas for each room</a></div>
</section>

{quote_section()}

{faq_section()}'''

page("index.html", "Atwood Dsigns | Interior Designers in Kokapet, Hyderabad",
     "Atwood Dsigns designs, draws and builds residential and commercial interiors in Hyderabad. Book a free consultation.",
     home, light=False)

# ---------------------------------------------------------------- ABOUT
about = page_head("About", "Design for real life",
                  "Atwood Dsigns is an interior design and build studio in Kokapet, Hyderabad. We believe great design shapes how you live, work and feel.",
                  P + "res-11.jpg", "Open dining and living space with a blue curtain wall") + f'''
<section class="sec frame" aria-labelledby="ab-h">
  <div class="split">
    <div class="split__text">
      <h2 class="title" id="ab-h" data-lines>Beautiful, and made to be lived in</h2>
      <p data-rise>Our philosophy is to create interiors that are visually striking and deeply practical, tailored to each client's lifestyle and vision.</p>
      <p data-rise>Every project starts with listening: your needs, your hopes and the story you want your space to tell. We turn those ideas into well-planned designs that balance beauty, practicality and sustainability.</p>
      <p data-rise>From warm homes to inspiring workplaces, we bring ideas to life with quality materials, smart layouts and a sharp eye for detail. With Atwood, it isn't just design; it's the art of living beautifully.</p>
    </div>
    <div class="split__pics prints">
      <div class="p1" data-open>{img(I + "abouthome.jpg", "Sculptural vase on a marble plinth", 1125, 1500)}</div>
      <div class="p2" data-open>{img(P + "res-04.jpg", "Entrance foyer with backlit niches", 800, 800)}</div>
    </div>
  </div>
</section>
<section class="sec on-surface frame" aria-labelledby="val-h">
  <h2 class="title" id="val-h" data-lines>What we hold to</h2>
  <ul class="items" data-rise>
    <li><strong>Creativity</strong><span>Fresh ideas shaped around your vision, never a template.</span></li>
    <li><strong>Function</strong><span>Layouts, storage and lighting planned for how you actually use the space.</span></li>
    <li><strong>Sustainability</strong><span>Low-VOC finishes, responsibly sourced wood and designs made to last.</span></li>
    <li><strong>Integrity</strong><span>Clear costs, honest timelines and one team accountable from start to finish.</span></li>
  </ul>
</section>
{faq_section()}'''
page("about.html", "About | Atwood Dsigns", "Atwood Dsigns is an interior design and build studio in Kokapet, Hyderabad, creating interiors that balance beauty, practicality and sustainability.", about)

# ---------------------------------------------------------------- SERVICES
RES = [("Living rooms", "Inviting layouts, statement furniture and personal touches."),
       ("Bedrooms", "Calm, comfortable, customised rooms designed for rest."),
       ("Kitchens", "Smart, practical modular kitchens with beautiful finishes."),
       ("Dining spaces", "Elegant settings that bring the family together."),
       ("Kids' rooms", "Creative, playful and safe rooms that spark imagination."),
       ("Complete makeovers", "From concept to execution, the whole house transformed.")]
COM = [("Office interiors", "Efficient, employee-friendly spaces that encourage collaboration."),
       ("Retail design", "Engaging layouts that attract customers and strengthen your brand."),
       ("Hospitality", "Restaurants, cafés and hotels that leave a lasting impression."),
       ("Workspace planning", "Ergonomic furniture, lighting and storage, planned for the team."),
       ("Custom solutions", "Designs that reflect your brand's personality and business goals."),
       ("Brand-led details", "Colours, materials and signage that say who you are.")]
SPEC = [("Tenant improvements", "Interior design tailored to commercial spaces."),
        ("As-built surveying", "Accurate documentation of existing conditions."),
        ("Space planning", "Efficient, purpose-driven layouts and programming."),
        ("Schematic and design development", "From first concept to a refined design."),
        ("Construction documents and bids", "Clear specifications and coordinated contractor proposals."),
        ("Construction administration", "Overseeing implementation and quality on site."),
        ("Finish selection", "Expert curation of materials and finishes."),
        ("Furniture and accessories", "Pieces chosen to complete the design."),
        ("ADA analysis and code compliance", "Meeting accessibility and regulatory standards."),
        ("Exterior colours and retail procurement", "Choices aligned to the site and the brand."),
        ("3D rendering", "See the space in detail before anything is built.")]


def items(lst, cls="items"):
    return f'<ul class="{cls}" data-stagger>' + "".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a, b in lst) + "</ul>"


services = page_head("Services", "Design and build",
                     "Whether you're refreshing a commercial property or designing a welcoming home, we capture your vision and bring it to life with creativity and care.",
                     P + "res-39.jpg", "Modular kitchen with navy base units and glass uppers",
                     '<div class="chips"><a href="#residential">Residential</a><a href="#commercial">Commercial</a><a href="#specialized">Specialized</a><a href="#turnkey">Turnkey</a></div>') + f'''
<section class="sec frame" id="residential" aria-labelledby="res-h">
  <div class="split">
    <div class="split__text">
      <h2 class="title" id="res-h" data-lines>Residential interiors</h2>
      <p class="lead" data-rise>Your home should reflect your personality and the way you live. From modern apartments to luxury villas, we design timeless spaces with warmth, elegance and practicality in every corner.</p>
      {items(RES, "items items--one")}
    </div>
    <div class="split__pics prints">
      <div class="p1" data-open>{img(P + "res-42.jpg", "Pink kids' room with a study niche and wardrobe", 1125, 1500)}</div>
      <div class="p2" data-open>{img(P + "res-12.jpg", "Bedroom with a grey upholstered bed", 800, 800)}</div>
    </div>
  </div>
</section>
<section class="sec on-surface frame" id="commercial" aria-labelledby="com-h">
  <div class="split split--rev">
    <div class="split__text">
      <h2 class="title" id="com-h" data-lines>Commercial interiors</h2>
      <p class="lead" data-rise>Every workplace, shop or hospitality venue should look impressive and help the business run: better productivity, better customer engagement, a better experience.</p>
      {items(COM, "items items--one")}
    </div>
    <div class="split__pics prints prints--wide">
      <div class="p1" data-open>{img(P + "com-10.jpg", "Office lounge with hexagonal ceiling lights", 1500, 1000)}</div>
      <div class="p2" data-open>{img(P + "com-38.jpg", "Reception lounge with wood slat wall", 800, 800)}</div>
    </div>
  </div>
</section>
<section class="sec frame" id="specialized" aria-labelledby="spec-h">
  <div class="split">
    <div class="split__text">
      <h2 class="title" id="spec-h" data-lines>Specialized solutions</h2>
      <p class="lead" data-rise>Good design comes from communication. Our specialized services focus on commercial tenant improvements, pairing creative design with a working knowledge of construction standards.</p>
    </div>
    <div class="split__pics" data-open style="aspect-ratio:3/2;overflow:hidden">{img(I + "specialized-interior-1.jpg", "Living space with layered ceiling lighting", 1500, 1000)}</div>
  </div>
  {items(SPEC, "items items--three")}
</section>
<section class="sec on-dark frame" id="turnkey" aria-labelledby="turn-h">
  <div class="split">
    <div class="split__text">
      <h2 class="title" id="turn-h" data-lines>Turnkey delivery</h2>
      <p class="lead" data-rise>We don't hand over drawings and walk away. Quantity surveying, procurement, scheduling, site management and quality control are all ours, so one studio answers for the result.</p>
      <p data-rise><a class="link link--accent" href="process.html">See all ten stages</a></p>
    </div>
    <div class="split__pics" data-open style="aspect-ratio:4/3;overflow:hidden">{img(P + "res-33.jpg", "Grey modular kitchen with tall storage", 1125, 1500)}</div>
  </div>
</section>'''
page("services.html", "Interior Design Services | Atwood Dsigns", "Residential interiors, commercial interiors and specialized interior solutions in Hyderabad, with turnkey delivery.", services)

# ---------------------------------------------------------------- PROCESS
process = page_head("How we work", "Ten stages, one team",
                    "Our design process captures exactly what you want. Our build process makes sure it gets made that way.",
                    P + "res-30.jpg", "Open kitchen and living area with a layered false ceiling") + moments_section("proc-h") + drawn_section() + f'''
<section class="sec frame" aria-labelledby="why-h">
  <div class="split split--rev">
    <div class="split__text">
      <h2 class="title" id="why-h" data-lines>Why one team matters</h2>
      <p class="lead" data-rise>When the people who design your space also run its construction, nothing gets lost between the drawing and the site.</p>
      <p data-rise>Decisions are made once, costs are clear before work begins, and someone is always accountable. Our designers visit throughout the build, and a dedicated supervisor manages the site every day.</p>
    </div>
    <div class="split__pics prints">
      <div class="p1" data-open>{img(I + "company.jpg", "Designers marking up construction drawings", 1125, 1500)}</div>
      <div class="p2" data-open>{img(P + "res-24.jpg", "Wardrobe installed on site", 800, 800)}</div>
    </div>
  </div>
</section>'''
page("process.html", "How We Work | Atwood Dsigns", "Our ten-stage design and build process, from the first conversation to the final quality check.", process)

# ---------------------------------------------------------------- IDEAS
IDEAS = [
    ("living-room", "livingroom.jpg", "res-41", "Living room", ["Your living room sets the tone for the whole home. It's the first space guests see and where the family gathers to relax, talk, watch TV and celebrate, so it should carry your home's personality.", "We design it around you, and as a complete interior solutions provider we handle everything from civil work and electricals to painting and décor."]),
    ("tv-unit", "t.vunit_.jpg", "res-23", "TV unit", ["A TV unit is more than furniture. It shapes viewing comfort and the whole feel of the living room, and it's usually where the family unwinds.", "We design it as a focal point that complements your interiors and suits the way you live, not just a place to put a screen."]),
    ("kids-bedroom", "kidsbedroom.jpg", "res-21", "Kids' bedroom", ["A child's room should be lively and personal, supporting play, learning and growth as well as sleep.", "Choosing colours, furniture and décor can feel overwhelming. We bring thoughtful, affordable ideas tailored to your space and your child's imagination, delivered on time."]),
    ("modular-kitchen", "modularkitchen.jpg", "res-39", "Modular kitchen", ["The kitchen is the heart of the home. Every choice, from layout to finish, should suit your taste and make the daily routine easier, in a space that feels bright and clutter-free.", "We design modern, elegant modular kitchens around how you cook. Ask us for designs and a personalised quote."]),
    ("bedroom", "bedroom-design.jpg", "res-12", "Bedroom", ["We bring more than a decade of experience to modern, stylish and space-efficient bedrooms.", "A few ideas that make a big difference: make the ceiling feel taller, balance light and dark shades, keep one colour palette, add texture, and finish with a statement piece of wall art."]),
    ("bathroom", "interior4.jpg", "res-20", "Bathroom", ["The bathroom is one of the most used rooms in any home, so it needs careful planning. It has to balance function with hygiene, which makes detailing especially important.", "Our end-to-end approach keeps you involved at every stage, so the room is practical, stylish and has everything you need."]),
]
IDEA_TYPE = {"living-room": "Living+room", "tv-unit": "Living+room", "kids-bedroom": "Bedroom+or+kids%27+room",
             "modular-kitchen": "Kitchen", "bedroom": "Bedroom+or+kids%27+room", "bathroom": "Bathroom"}
ideas = page_head("Ideas", "Ideas, room by room",
                  "How we think about the rooms people ask us about most: each one as we draw it, beside one we have built.",
                  P + "res-13.jpg", "Reception lounge with wood slats and a marigold arrangement",
                  '<div class="chips">' + "".join(f'<a href="#{i}">{t}</a>' for i, _, _, t, _ in IDEAS) + "</div>")
for k, (iid, sketch, built, t, ps) in enumerate(IDEAS):
    rev = " split--rev" if k % 2 else ""
    ideas += f'''
<section class="idea frame" id="{iid}" aria-labelledby="{iid}-h">
  <div class="split{rev}">
    <div class="split__text">
      <h2 class="title" id="{iid}-h" data-lines>{t}</h2>
      {"".join(f"<p data-rise>{p}</p>" for p in ps)}
      <p data-rise><a class="link link--accent" href="contact.html?type={IDEA_TYPE[iid]}">Plan your {t if t.startswith("TV") else t.lower()} with us</a></p>
    </div>
    <figure class="split__pics pair">
      <div class="drawing" data-open>{img(I + sketch, t + " design drawing", 1500, 1200)}</div>
      <div class="built" data-open>{img(P + built + ".jpg", t + " built by Atwood Dsigns", 800, 1000)}</div>
      <figcaption>Left, the drawing. Right, one we built.</figcaption>
    </figure>
  </div>
</section>'''
page("ideas.html", "Interior Ideas | Atwood Dsigns", "Living room, TV unit, kids' bedroom, modular kitchen, bedroom and bathroom ideas from Atwood Dsigns, Hyderabad.", ideas)

# ---------------------------------------------------------------- PORTFOLIO
pdir = os.path.join(OUT, "assets/img/portfolio")
files = sorted((f for f in os.listdir(pdir) if f.endswith(".jpg") and not f.endswith("-800.jpg")),
               key=lambda f: int(f.split("-")[1].split(".")[0]))
res_n = sum(f.startswith("res") for f in files)
com_n = len(files) - res_n
gallery = "\n".join(
    f'<a href="{P}{f}" data-cat="{"residential" if f.startswith("res") else "commercial"}" data-cursor="Open" data-rise>{img(P + f, ("Residential" if f.startswith("res") else "Commercial") + " interior by Atwood Dsigns", 1500, 1000, sizes="(max-width: 560px) 50vw, (max-width: 900px) 50vw, 33vw")}</a>'
    for f in files)
portfolio = page_head("Portfolio", "Rooms we have built",
                      "Homes, offices and shops across Hyderabad. Select any photograph to see it full size.",
                      P + "res-06.jpg", "Bedroom with a ladder bed and illustrated wall") + f'''
<section class="sec--tight frame" aria-labelledby="pf-h">
  <h2 class="sr-only" id="pf-h">All projects</h2>
  <div class="chips" role="group" aria-label="Filter projects" style="margin:0 0 36px">
    <button type="button" data-filter="all" aria-pressed="true">All <small>{len(files)}</small></button>
    <button type="button" data-filter="residential" aria-pressed="false">Residential <small>{res_n}</small></button>
    <button type="button" data-filter="commercial" aria-pressed="false">Commercial <small>{com_n}</small></button>
  </div>
  <p class="sr-only" role="status" id="filter-status"></p>
  <div class="gallery">{gallery}</div>
</section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Project photograph" aria-hidden="true">
  <img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt="">
  <button class="icon-btn lb-close" type="button" aria-label="Close">{CLOSE}</button>
  <button class="icon-btn lb-prev" type="button" aria-label="Previous photograph">{ARROW_L}</button>
  <button class="icon-btn lb-next" type="button" aria-label="Next photograph">{ARROW_R}</button>
  <p class="lb-count"><span class="lb-caption"></span> <span class="lb-index"></span></p>
</div>'''
page("portfolio.html", "Portfolio | Atwood Dsigns", "Residential and commercial interiors designed and built by Atwood Dsigns in Hyderabad.", portfolio)

# ---------------------------------------------------------------- JOURNAL
arts = "\n".join(f'''<article class="article" id="{slug}" aria-labelledby="{slug}-h">
  <div class="article__pic" data-open>{img(I + pic, "", 1500, 1000)}</div>
  <h2 id="{slug}-h" data-lines>{t}</h2>
  <p class="sub">{sub}</p>
  <time datetime="2025-12-24">24 December 2025</time>
  <p class="lead">{intro}</p>
  {"".join(f"<h3>{h}</h3>" + "".join(f"<p>{p}</p>" for p in ps) for h, ps in secs)}
</article>''' for slug, pic, t, sub, intro, secs in POSTS)
journal = page_head("Journal", "Notes on good rooms",
                    "Short articles on designing homes and workplaces that work.",
                    I + "commercial-interior-3.jpg", "Office meeting area with planted ceiling",
                    '<div class="chips">' + "".join(f'<a href="#{s}">{t.split(" interior")[0]}</a>' for s, _, t, _, _, _ in POSTS) + "</div>") + f'''
<section class="sec frame"><div class="journal-wrap"><div>{arts}</div></div></section>'''
page("journal.html", "Journal | Atwood Dsigns", "Articles on sustainable, commercial and residential interior design from Atwood Dsigns.", journal)

# ---------------------------------------------------------------- CONTACT
contact = page_head("Contact", "Start with a conversation",
                    "Whether you have a question, need advice or are ready to begin, we're here to help. The first consultation is free.",
                    P + "res-04.jpg", "Entrance foyer with backlit niches") + f'''
<section class="sec frame" aria-labelledby="studio-h">
  <div class="contact-grid">
    <div class="contact-info">
      <h2 class="title" id="studio-h" data-lines>Our studio</h2>
      <dl data-stagger>
        <dt>Call</dt><dd><a href="{TEL}">{PHONE}</a></dd>
        <dt>WhatsApp</dt><dd><a href="{WA}" target="_blank" rel="noopener">Message us</a></dd>
        <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
        <dt>Visit</dt><dd>{ADDR}</dd>
      </dl>
    </div>
    <form class="form" id="enquiry" novalidate data-rise>
      <h2 class="title">Book a free consultation</h2>
      <p>Tell us a little about your project and we'll get back to you.</p>
      <div class="field-row">
        <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required aria-describedby="e-name"><span class="err" id="e-name">Enter your name.</span></div>
        <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required pattern="[0-9+ ()-]{{8,}}" aria-describedby="e-phone"><span class="err" id="e-phone">Enter a phone number we can call.</span></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="e-email"><span class="err" id="e-email">Enter an email address like name@example.com.</span></div>
        <div class="field"><label for="f-type">Project type</label>
          <select id="f-type" name="type"><option>Full home interiors</option><option>Kitchen</option><option>Bedroom or kids' room</option><option>Living room</option><option>Office interiors</option><option>Bathroom</option><option>Retail or hospitality</option><option>Something else</option></select></div>
      </div>
      <div class="field"><label for="f-msg">About your project</label><textarea id="f-msg" name="message" required aria-describedby="e-msg" placeholder="Location, size of the space, timeline, anything you have in mind"></textarea><span class="err" id="e-msg">Tell us a little about your project.</span></div>
      <div class="form-actions">
        <button class="btn" type="submit">Send by email</button>
        <button class="btn btn--ink" type="button" data-whatsapp>Send on WhatsApp</button>
      </div>
      <p class="form-note">Both open your email or WhatsApp app with your details filled in, ready to send. What you type is kept on this device until you send it.</p>
      <div class="form-status" role="status" aria-live="polite"></div>
    </form>
  </div>
</section>
<section class="sec--tight frame" aria-labelledby="handed-h">
  <h2 class="title" id="handed-h" data-lines>A few rooms we have handed over</h2>
  <div class="trio">
    <a class="t1" href="portfolio.html" data-open data-cursor="View">{img(P + "res-32.jpg", "Warmly lit entrance lobby", 1125, 1500)}</a>
    <a class="t2" href="portfolio.html" data-open data-cursor="View">{img(P + "res-08.jpg", "Dining area with teal drapes", 1500, 1000)}</a>
    <a class="t3" href="portfolio.html" data-open data-cursor="View">{img(P + "res-40.jpg", "Mint modular kitchen", 1500, 1500)}</a>
  </div>
</section>
<iframe class="map" title="Map showing Atwood Dsigns in Kokapet, Hyderabad" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=E-Infra%20Tower%2C%20Brindavan%20Colony%2C%20Kokapet%2C%20Hyderabad%20500075&z=15&output=embed"></iframe>'''
page("contact.html", "Contact | Atwood Dsigns", "Book a free interior design consultation with Atwood Dsigns in Kokapet, Hyderabad. Call +91 90001 81212.", contact, closing=False)
print("built")
