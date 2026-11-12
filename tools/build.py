"""Builds the static pages of the Atwood Dsigns site ("Atelier" design, assets/css/styles.css), and the photograph manifest (ASSETS.md).

Run from anywhere:  python3 tools/build.py

Every photograph is described once, in PHOTOS below: what it shows, where it came from, and its focal point.
Pages refer to photographs by key, so replacing a picture means changing one entry. Where a WebP copy sits beside a
JPEG (made by tools/webp.py), pages serve it first through <picture>, with the JPEG as the fallback.

Content rules (decided with the studio, November 2026):
- "library" photographs came with the previous website and are most likely stock. They are never placed where they
  would imply the studio designed or built the space.
- The client quotations are kept in QUOTES but not published until the studio confirms them (SHOW_QUOTES).

Journal posts are not in this file: they are written in the Sanity Studio (https://atwood-dsigns.sanity.studio,
code in studio/) and fetched at build time by tools/cms.py, so the build needs the internet.
"""
import hashlib
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
MAPS = "https://maps.google.com/?q=E-Infra+Tower+Brindavan+Colony+Kokapet+Hyderabad"
SITE = "https://atwooddsigns.com/"
SHOW_QUOTES = False  # switch on once the studio confirms the quotations are from real clients

# ------------------------------------------------------------------------------------------------ photographs
# kind: "studio"  = photographs the studio uploaded of its own finished rooms (February 2026)
#       "library" = older images from the previous website, most likely stock: never shown as the studio's work
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
    # supplied by the studio for the home hero (November 2026), used exactly as received
    "pooja-room": (P + "pooja-room.jpg", "Pooja room with a backlit carved arch around the deity, brass bells and lamps", "supplied", "50% 50%"),
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


def jpeg_size(path):
    """A JPEG's (width, height) from its frame header, so srcset widths and image sizes are exact."""
    with open(path, "rb") as f:
        data = f.read()
    i = 2
    while i < len(data):
        marker, size = data[i + 1], int.from_bytes(data[i + 2:i + 4], "big")
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            return int.from_bytes(data[i + 7:i + 9], "big"), int.from_bytes(data[i + 5:i + 7], "big")
        i += 2 + size
    return None, None


def exists(rel):
    return os.path.exists(os.path.join(OUT, rel))


def srcsets(src):
    """(JPEG srcset, WebP srcset or "") for a photograph, from its 800px copy and the full-size file."""
    if not src.endswith(".jpg"):
        return "", ""
    w = jpeg_size(os.path.join(OUT, src))[0]
    small = src[:-4] + "-800.jpg"
    jpg = f"{small} 800w, {src} {w}w" if exists(small) else ""
    webp = ""
    if exists(src[:-4] + ".webp"):
        webp = f"{small[:-4]}.webp 800w, {src[:-4]}.webp {w}w" if exists(small[:-4] + ".webp") else f"{src[:-4]}.webp {w}w"
    return jpg, webp


def img_tag(src, alt, sizes="(max-width: 860px) 100vw, 50vw", lazy=True, extra=""):
    jpg, webp = srcsets(src)
    lz = ' loading="lazy" decoding="async"' if lazy else ' decoding="async"'
    ss = f' srcset="{jpg}" sizes="{sizes}"' if jpg else ""
    tag = f'<img src="{src}"{ss} alt="{alt}"{lz}{extra}>'
    return f'<picture><source type="image/webp" srcset="{webp}" sizes="{sizes}">{tag}</picture>' if webp else tag


PAGE = "index.html"
ASSET_V = {k: hashlib.sha1(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)).read().encode()).hexdigest()[:8]
           for k, f in (("css", "assets/css/styles.css"), ("js", "assets/js/main.js"))}


def ph(key, ratio="r-32", sizes="(max-width: 860px) 100vw, 50vw", lazy=True, where="", cls="", alt=None, pos=None, img_extra=""):
    """A photograph at a fixed proportion with its focal point; records where it is used."""
    src, desc, kind, fpos = PHOTOS[key]
    USED.setdefault(key, set()).add(f"{PAGE}: {where}" if where else PAGE)
    return f'<div class="ph {ratio} {cls}" style="--pos: {pos or fpos}">{img_tag(src, desc if alt is None else alt, sizes, lazy, img_extra)}</div>'


def fig(key, ratio, sizes, caption=None, cls="", **kw):
    cap = f'<figcaption class="caption">{caption}</figcaption>' if caption else ""
    return f'<figure class="{cls}" style="margin:0">{ph(key, ratio, sizes, **kw)}{cap}</figure>'


def apos(s):
    """A true apostrophe in display type."""
    return s.replace("'", "&rsquo;")


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

# the portfolio: rooms the studio photographed. Library images are not cards (see HELD_BACK).
CATS = [("all", "All"), ("kitchen", "Kitchens"), ("bedroom", "Bedrooms"), ("kids", "Kids' rooms"), ("living", "Living and dining"), ("entrance", "Entrances and pooja")]
CAT_NAME = dict(CATS)
CAT_ONE = {"kitchen": "Kitchen", "bedroom": "Bedroom", "kids": "Kids' room", "living": "Living and dining", "entrance": "Entrance and pooja"}
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
CARDS = [c for c in CARDS if c[1] != "commercial" and all(PHOTOS[k][2] == "studio" for k in c[2])]
ROOM_COUNT = len(CARDS)
HELD_BACK = {"res-41": "sofa still in its plastic wrapping (shown only as a room during installation, on the process page)",
             "res-46": "dark and cluttered", "res-13": "duplicate of com-38", "com-16": "duplicate of com-10",
             "com-19": "library image", "com-26": "library image", "com-34": "library image with a person in frame"}
for _k, (_s, _d, _kind, _p) in PHOTOS.items():
    if _kind == "library":
        HELD_BACK.setdefault(_k, "library image from the previous website, most likely stock: not shown as the studio's work")

SERVICES = [  # (anchor, title, description)
    ("residential", "Residential interiors", "Apartments and villas: living rooms, bedrooms, modular kitchens, kids' rooms and complete home makeovers."),
    ("commercial", "Commercial interiors", "Offices, retail and hospitality spaces that work hard and reflect your brand."),
    ("specialized", "Specialised solutions", "Space planning, construction drawings, finish selection and 3D visualisation."),
    ("turnkey", "Turnkey delivery", "Quantity surveying, procurement, site management and quality control through to handover."),
]
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
SPEC = [  # the studio's specialised services, in Indian terms (no service added or removed)
    ("Commercial fit-outs", "Interior design tailored to business spaces."),
    ("As-built surveys", "Accurate documentation of existing conditions."),
    ("Space planning", "Efficient, purpose-driven layouts."),
    ("Schematic and design development", "From first concept to a refined design."),
    ("Construction drawings and tender coordination", "Clear specifications and coordinated quotations."),
    ("Construction supervision", "Overseeing implementation and quality."),
    ("Interior finish selection", "Expert curation of materials and finishes."),
    ("Furniture and accessories", "Pieces that complement the design."),
    ("Accessibility and code compliance", "Regulatory and accessibility standards."),
    ("Exterior colours and procurement", "Choices aligned to the site and the brand."),
    ("3D visualisation", "Seeing the design in digital models before it is built."),
]
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
IDEA_PHOTO = {"living-room": "res-37", "tv-unit": "res-23", "kids-bedroom": "res-42", "modular-kitchen": "res-39", "bedroom": "res-43", "bathroom": None}

# ------------------------------------------------------------------------------------------------ chrome
NAV = [("services.html", "Services"), ("portfolio.html", "Portfolio"), ("process.html", "Process"),
       ("ideas.html", "Ideas"), ("journal.html", "Journal"), ("about.html", "About")]
MENU = [("index.html", "Home")] + NAV + [("contact.html", "Contact")]
CUR = ' aria-current="page"'
ARR = '<span class="arr" aria-hidden="true">&rarr;</span>'
SERVICE_PICS = {  # anchor: (studio photograph, focal point); studio photographs only, never library images
    "residential": ("res-05", "50% 60%"),
    "commercial": ("res-32", "50% 90%"),   # no commercial project photographed yet: a warm-lit lobby from a home stands in
    "specialized": ("res-09", "50% 45%"),
    "turnkey": ("res-33", "50% 62%"),
}
ICON_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1112 21.8zm8.4-18.2A11.8 11.8 0 001.7 17.9L0 24l6.3-1.6A11.8 11.8 0 0024 12c0-3.2-1.2-6.1-3.6-8.4z"/></svg>'
ICON_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 013 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>'
ARROW_L = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'
ARROW_R = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'
CLOSE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>'


def go(href, text, extra=""):
    return f'<a class="go" href="{href}"{extra}>{text} {ARR}</a>'


def kicker(n, name, cls=""):
    """The running head that opens each chapter of a page: a copper number and the section's name."""
    num = f"<b>{n}</b>" if n else ""
    return f'<p class="kicker {cls}">{num}{name}</p>'


def em_last(title, n=2):
    """A title with its last words in italic, the display face's way of giving it emphasis."""
    words = apos(title).split(" ")
    if len(words) <= n:
        return f"<em>{' '.join(words)}</em>"
    return " ".join(words[:-n]) + f" <em>{' '.join(words[-n:])}</em>"


def header(current, over=False, wide=False):
    """over: the bar starts transparent in light type over a dark opening. wide: it aligns to the home hero."""
    links = "".join(f'<a href="{h}"{CUR if h == current else ""}>{t}</a>' for h, t in NAV)
    menu = "".join(f'<li><a href="{h}" data-n="{i + 1:02d}" style="--i: {i}"{CUR if h == current else ""}>{t}</a></li>' for i, (h, t) in enumerate(MENU))
    cls = "site-header" + (" site-header--over" if over else "") + (" site-header--wide" if wide else "")
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="{cls}">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Atwood Dsigns, home"><img src="{I}logo-web-new-2.png" alt="" width="255" height="97"><span class="brand__name">Atwood Dsigns</span></a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <a class="btn header-cta" href="contact.html">Book a consultation</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu-panel"><span class="menu-toggle__label">Menu</span><span class="menu-toggle__icon" aria-hidden="true"><i></i><i></i></span></button>
  </div>
</header>
<div class="menu-panel" id="menu-panel" aria-hidden="true">
  <nav aria-label="Menu"><ul>{menu}</ul></nav>
  <div class="menu-panel__contact">
    <a class="btn btn--light" href="contact.html">Book a free consultation {ARR}</a>
    <p><a href="{TEL}">{PHONE}</a> &middot; <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></p>
    <p>{ADDR_SHORT}</p>
  </div>
</div>'''


FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <p class="foot__word" aria-hidden="true">Atwood <em>Dsigns</em></p>
    <div class="foot">
      <div class="foot__brand">
        <img src="{I}logo-web-new-2.png" alt="Atwood Dsigns" width="255" height="97" loading="lazy">
        <p>An interior design and build studio in Kokapet, Hyderabad, creating homes, offices and shops from the first sketch to handover.</p>
      </div>
      <div class="foot__col"><h2>Studio</h2><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in MENU[1:])}</ul></div>
      <div class="foot__col"><h2>Follow</h2><ul>
        <li><a href="https://www.instagram.com/atwooddsigns/" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="https://www.linkedin.com/company/atwooddsigns/" target="_blank" rel="noopener">LinkedIn</a></li>
        <li><a href="https://www.pinterest.com/atwooddsignss/" target="_blank" rel="noopener">Pinterest</a></li></ul></div>
      <div class="foot__col foot__col--wide"><h2>Visit or call</h2>
        <address>{ADDR}</address>
        <ul><li><a href="{TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a></li></ul>
      </div>
    </div>
    <div class="legal"><span>&copy; <span id="year">2026</span> Atwood Dsigns LLP. All rights reserved.</span><span>Kokapet, Hyderabad</span></div>
  </div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Chat with Atwood Dsigns on WhatsApp">{ICON_WA}</a>
<nav class="mbar" aria-label="Quick contact"><a href="{TEL}">{ICON_TEL}Call the studio</a><a href="{WA}" target="_blank" rel="noopener">{ICON_WA}WhatsApp</a></nav>'''

CONSULT_KEY = "res-04"  # the foyer with backlit niches: a welcome, at the close of every page


def consult():
    """The close of every page: the studio's foyer beside the invitation and the three ways to reach the studio."""
    return f'''<section class="consult dark" aria-labelledby="consult-h">
  <figure class="consult__pic">{ph(CONSULT_KEY, "", "(max-width: 860px) 100vw, 42vw", where="consultation", alt="")}</figure>
  <div class="consult__text">
    {kicker("", "Free first consultation")}
    <h2 id="consult-h">Start with a <em>conversation</em></h2>
    <p class="lead">Tell us about your home, your office or the one room that isn't working. We'll meet you at our studio in Kokapet or at your site.</p>
    <div class="actions"><a class="btn btn--light" href="contact.html">Book a consultation {ARR}</a><a class="btn btn--dline" href="{WA}" target="_blank" rel="noopener">Message on WhatsApp</a></div>
    <div class="consult__contacts">
      <div><span>Call</span><a href="{TEL}">{PHONE}</a></div>
      <div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
      <div><span>Studio</span><p>Kokapet, Hyderabad</p></div>
    </div>
  </div>
</section>'''


FONTS = "https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Instrument+Sans:wght@400;500;600&display=swap"


def absolute(url):
    return url if url.startswith("http") else SITE + url


def page(fname, title, desc, body, closing=True, over=False, og_image=None, og_type="website", head_extra="", section=None, wide=False):
    canonical = SITE + ("" if fname == "index.html" else fname.replace(".html", "/"))
    og_image = absolute(og_image or P + "res-21.jpg")
    html = f'''<!doctype html>
<html lang="en-IN">
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
<meta name="theme-color" content="#f4f1ec">
<link rel="icon" href="{I}cropped-favicon-192x192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css?v={ASSET_V['css']}">
<script>(function (d) {{ d.classList.add('js'); try {{ if (sessionStorage.getItem('aw-intro')) d.classList.add('seen'); else sessionStorage.setItem('aw-intro', '1'); }} catch (e) {{ d.classList.add('seen'); }} setTimeout(function () {{ if (!d.classList.contains('ready')) d.classList.remove('js'); }}, 3000); }})(document.documentElement)</script>
<script type="speculationrules">{{"prefetch": [{{"where": {{"selector_matches": "a[href$='.html']"}}, "eagerness": "moderate"}}]}}</script>
</head>
<body>
{header(section or fname, over, wide)}
<main id="main">
{body}
{consult() if closing else ""}
</main>
{FOOTER}
<script src="assets/js/main.js?v={ASSET_V['js']}" defer></script>
</body>
</html>
'''
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(html)


def crumbs(*trail):
    """Home / ... / here; the last item is the current page."""
    items = [f'<li><a href="{h}">{t}</a></li>' for h, t in trail[:-1]] + [f'<li aria-current="page">{trail[-1]}</li>']
    return f'<nav aria-label="Breadcrumb"><ol class="crumbs"><li><a href="index.html">Home</a></li>{"".join(items)}</ol></nav>'


def opener(crumb, h1, lead, key, pos=None, caption=""):
    """An inner page's opening: the title and introduction on the left, a photograph bleeding off the right edge."""
    return f'''<section class="opener">
  <div class="opener__text">
    {crumbs(crumb)}
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
  <figure class="opener__pic">{ph(key, "", "(max-width: 899px) 100vw, 50vw", lazy=False, where="opening photograph", pos=pos, img_extra=' fetchpriority="high"')}</figure>
</section>'''


def plain(crumb, h1, lead):
    """An opening without a photograph, for pages whose first content is already pictures."""
    return f'''<section class="plain">
  <div class="wrap grid">
    <div class="plain__title">{crumbs(crumb)}<h1>{h1}</h1></div>
    <p class="plain__lead lead">{lead}</p>
  </div>
</section>'''


def journey(n, detailed=False, more=True, title="Ten stages, <em>one team</em>"):
    """The ten stages on terracotta, joined by a dotted path that draws as the section is read. The stages sit in a grid
    (a serpentine of two rows from 1000px, one column below); the script measures their markers and draws the path
    through them, so it always meets them, at any width. Without the script the stages are simply listed."""
    stages = "".join(f'''<li class="jstage" style="--i: {i}"><span class="jstage__mark" aria-hidden="true"></span><span class="jstage__n">{i + 1:02d}</span><h3>{name}</h3>{f"<p>{desc}</p>" if detailed else ""}</li>''' for i, (phase, name, desc, _k) in enumerate(STAGES))
    foot = f'<div class="journey__foot">{go("process.html", "What happens at each stage")}</div>' if more else ""
    return f'''<section class="journey{" journey--detailed" if detailed else ""}" aria-labelledby="journey-h" data-journey>
  <div class="wrap">
    <div class="journey__head">{kicker(n, "How we work")}<h2 id="journey-h" data-lines>{title}</h2><p>Stages one to five are design; six to ten are execution. The people who draw your space are the people who build it.</p></div>
    <div class="journey__map">
      <svg class="journey__svg" aria-hidden="true" focusable="false"><defs><mask id="journey-mask-{n}" maskUnits="userSpaceOnUse"><path class="journey__reveal" /></mask></defs><path class="journey__track" /><path class="journey__path" mask="url(#journey-mask-{n})" /><circle class="journey__dot" r="7" /></svg>
      <ol class="journey__stages">{stages}</ol>
    </div>
    {foot}
  </div>
</section>'''


def faq_block(h2_id="faq-h"):
    items = "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for q, a in FAQS)
    return f'''<section class="faq-block sec" aria-labelledby="{h2_id}">
  <div class="wrap grid">
    <div class="faq-block__head">
      <h2 id="{h2_id}">Questions <em>clients ask</em></h2>
      <p>Something else on your mind? Call <a href="{TEL}">{PHONE}</a>.</p>
    </div>
    <div class="faq">{items}</div>
  </div>
</section>'''


def voices():
    """Client quotations, published only once the studio confirms them (SHOW_QUOTES)."""
    if not SHOW_QUOTES:
        return ""
    figs = "".join(f'<div><b>&ldquo;</b><h3>{q}</h3><p>{n}, {p}</p></div>' for q, n, p in QUOTES[:4])
    return f'<section class="sec parch" aria-labelledby="voices-h"><div class="wrap"><div class="shead"><h2 id="voices-h">What <em>clients say</em></h2></div><div class="pillars">{figs}</div></div></section>'


# Journal posts are written in the Sanity Studio and fetched by tools/cms.py; the home page lists the latest.
JOURNAL = cms.load_posts()
esc = cms.esc


def post_href(p):
    return f"journal-{p['slug']}.html"


def post_meta(p):
    return f'<b>{esc(p["category"])}</b> &middot; {cms.fmt_date(p["date"])}'


# ================================================================================================ HOME
PAGE = "index.html"
# Hero, "Aperture": the dining room's lit display unit, teal drapes and chandelier, opened through a mask; the pooja
# room photograph supplied by the studio hangs in front of it, lower right, as a framed inset.
HERO_KEY, HERO_DETAIL = "res-11", "pooja-room"
HERO_SIZES = "(max-width: 899px) 100vw, 64vw"
_jpg, _webp = srcsets(PHOTOS[HERO_KEY][0])
HERO_PRELOAD = f'\n<link rel="preload" as="image" type="image/webp" imagesrcset="{_webp}" imagesizes="{HERO_SIZES}" fetchpriority="high">'
LOADER = f'<div class="loader" aria-hidden="true"><div class="loader__mark"><img src="{I}logo-web-new-2.png" alt="" width="255" height="97"><span>Atwood <em>Dsigns</em></span></div></div>'

# Selected work, a reel: three rooms, each framed at its photograph's own proportion (landscape, portrait, landscape).
# A project links to its page; the pooja unit, which has no project page, links to its room type in the portfolio.
# None of these photographs appears elsewhere on the home page. (shape: "land" 3:2, "tall" 3:4, "four" 4:3)
REEL = [
    dict(project="project-space-kids-bedroom", key="res-44", pos="50% 60%", shape="land"),
    dict(card="Pooja unit", key="res-22", pos="50% 40%", shape="tall", href="portfolio.html#entrance",
         line="A carved deity panel lit from behind, framed in dark wood, with a marble ledge for the lamps and drawers beneath."),
    dict(project="project-open-kitchen", key="res-07", pos="50% 55%", shape="four"),
]


def reel_item(i, it):
    if "project" in it:
        pr = PROJECT_BY_SLUG[it["project"]]
        href, title, cat, count = it["project"] + ".html", pr["title"], pr["cat"], len(pr["photos"])
        line = pr["overview"].split(". ")[0].rstrip(".") + "."
    else:
        title, cat_key, photos = next(c for c in CARDS if c[0] == it["card"])
        href, cat, count, line = it["href"], CAT_ONE[cat_key], len(photos), it["line"]
    sizes = "(max-width: 999px) 100vw, 46vw" if it["shape"] == "tall" else "(max-width: 999px) 100vw, 64vw"
    return f'''<article class="reel__item reel__item--{it["shape"]}" data-cursor="View">
        {ph(it["key"], "", sizes, where="selected work", pos=it["pos"])}
        <div class="reel__cap"><span class="reel__n">{i:02d}</span><h3><a href="{href}">{em_last(title)}</a></h3><p class="reel__meta">{apos(cat)} &middot; {count} photograph{"" if count == 1 else "s"}</p><p class="reel__line">{line}</p></div>
      </article>'''


ROOM_GALLERY = [  # (portfolio filter, label, photograph, focal point): the five room types of the portfolio
    ("kitchen", "Kitchen", "res-39", "60% 62%"), ("living", "Living &amp; dining", "res-08", "72% 55%"),
    ("bedroom", "Bedroom", "res-43", "55% 50%"), ("kids", "Kids&rsquo; room", "res-42", "55% 55%"),
    ("entrance", "Entrance &amp; pooja", "res-27", "50% 45%")]


def service_cards():
    """The four kinds of work as cards: photograph, number, title, description and a link to its part of Services."""
    out = ""
    for i, (a, t, d) in enumerate(SERVICES):
        key, pos = SERVICE_PICS[a]
        media = ph(key, "", "(max-width: 599px) 100vw, (max-width: 1099px) 50vw, 25vw", where="services cards", alt="", pos=pos)
        out += f'''<a class="svc-card" href="services.html#{a}" style="--i: {i}"><div class="svc-card__media">{media}</div><div class="svc-card__body"><span class="svc-card__n">{i + 1:02d}</span><h3>{t}</h3><p>{apos(d)}</p><span class="svc-card__more">Explore {ARR}</span></div></a>'''
    return out


def room_gallery(n):
    """Room types as an editorial gallery: varied proportions, the room type set large over each photograph."""
    tiles = ""
    for i, (cat, label, key, pos) in enumerate(ROOM_GALLERY):
        count = sum(1 for c in CARDS if c[1] == cat)
        tiles += f'''<a class="g-tile g-tile--{i + 1}" href="portfolio.html#{cat}" data-cursor="Explore" style="--i: {i}">{ph(key, "", "(max-width: 899px) 100vw, 66vw", where="room gallery", alt="", pos=pos)}<span class="g-label"><span class="g-name"><span>{label}</span></span><span class="g-count">{count} rooms {ARR}</span></span></a>'''
    return f'''<section class="rooms-gallery" aria-labelledby="rg-h">
  <div class="wrap"><div class="shead">{kicker(n, "Browse by room")}<h2 id="rg-h">Find the room <em>you are planning</em></h2><p>{ROOM_COUNT} rooms across five room types, each with every photograph we have of it.</p></div></div>
  <div class="wrap"><div class="rooms-gallery__grid" data-gallery>{tiles}</div></div>
  <div class="wrap rooms-gallery__foot">{go("portfolio.html", "View the full portfolio")}</div>
</section>'''


reel_items = "".join(reel_item(i + 1, t) for i, t in enumerate(REEL))
notes = "".join(f'''<article class="note"><p class="meta">{post_meta(p)}</p><h3><a href="{post_href(p)}">{esc(p["title"])}</a></h3><p>{esc(p["excerpt"])}</p></article>''' for p in JOURNAL[:3])
journal_note = f'''<section class="sec parch" aria-labelledby="notes-h">
  <div class="wrap">
    <div class="shead">{kicker("06", "Journal")}<h2 id="notes-h">Notes from <em>the studio</em></h2>{go("journal.html", "Read the journal")}</div>
    <div class="notes">{notes}</div>
  </div>
</section>''' if JOURNAL else ""

home = f'''{LOADER}
<section class="hero" aria-labelledby="hero-h">
  <figure class="hero__main" data-depth="0.1">{ph(HERO_KEY, "", HERO_SIZES, lazy=False, where="hero", pos="44% 58%", img_extra=' fetchpriority="high"')}</figure>
  <figure class="hero__inset" data-depth="0.22">
    <div class="hero__inset-frame">{ph(HERO_DETAIL, "", "(max-width: 899px) 40vw, 18vw", lazy=False, where="hero inset")}</div>
    <figcaption>Pooja room</figcaption>
  </figure>
  <div class="hero__content">
    <p class="hero__place">Kokapet, Hyderabad &middot; Interior design and build</p>
    <h1 class="hero__title" id="hero-h"><span class="hl"><span>Interiors designed,</span></span> <span class="hl"><span>drawn and <span class="hero__accent">built.</span></span></span></h1>
    <div class="hero__foot">
      <p class="hero__lead">Homes, offices and shops, taken from the first conversation to handover by one studio.</p>
      <div class="hero__ctas"><a class="btn btn--light hero__btn" href="contact.html"><span>Book a free consultation</span> {ARR}</a>{go("portfolio.html", "See our work")}</div>
      <span class="hero__cue" aria-hidden="true"><i></i>Scroll</span>
    </div>
  </div>
</section>

<section class="intro" aria-labelledby="studio-h">
  <div class="intro__text">
    <p class="intro__label"><b>01</b><i aria-hidden="true"></i>The studio</p>
    <h2 class="intro__title" id="studio-h" data-lines>The team that <em>draws</em> your space is the team that <em>builds</em> it.</h2>
    <p class="intro__lead">We design and build homes, offices and commercial interiors in Hyderabad, from the first conversation to handover.</p>
    <div class="intro__body">
      <p>We combine creativity, function and fine craftsmanship to bring your vision to life, with designs that blend timeless style and modern ideas so every detail feels personal and purposeful.</p>
      <p>Five stages of design are followed by five of execution: quantity surveying, procurement, project planning, a dedicated site supervisor and a final quality review before handover.</p>
    </div>
    <div class="intro__links"><a class="btn btn--line" href="about.html">About the studio {ARR}</a>{go("process.html", "How we work")}</div>
  </div>
  <figure class="intro__pic">{ph("res-12", "", "(max-width: 899px) 100vw, 54vw", where="studio introduction", pos="66% 55%")}<figcaption>Bedroom with an upholstered bed, geometric wardrobe and study desk</figcaption></figure>
</section>

<section class="reel dark" aria-labelledby="work-h" data-reel>
  <div class="reel__sticky">
    <div class="reel__track">
      <div class="reel__intro">{kicker("02", "Selected work")}<h2 id="work-h">Three rooms, <em>up close</em></h2><p>A kids&rsquo; room, a pooja unit and an open kitchen. Open one to see every photograph we have of it.</p><p class="reel__hint" aria-hidden="true">Keep scrolling <i></i></p></div>
      {reel_items}
      <div class="reel__end"><h3>{ROOM_COUNT} rooms <em>in the portfolio</em></h3><p>Or browse <a href="portfolio.html#kitchen">kitchens</a>, <a href="portfolio.html#bedroom">bedrooms</a> and <a href="portfolio.html#entrance">entrances and pooja units</a>.</p>{go("portfolio.html", f"View all {ROOM_COUNT} rooms")}</div>
    </div>
    <div class="reel__progress" aria-hidden="true"><i></i></div>
  </div>
</section>

<section class="sec" aria-labelledby="offer-h">
  <div class="wrap">
    <div class="shead">{kicker("03", "What we do")}<h2 id="offer-h">What we <em>design and build</em></h2><p>Four kinds of work, delivered by one team from the first drawing to the final check.</p></div>
    <div class="svc-cards" data-cards>{service_cards()}</div>
  </div>
</section>

{journey("04")}

{room_gallery("05")}
{voices()}
{journal_note}'''
page("index.html", "Atwood Dsigns | Interior Design and Build Studio in Kokapet, Hyderabad",
     "Atwood Dsigns designs, draws and builds residential and commercial interiors in Hyderabad, from the first consultation to handover. Book a free consultation.", home,
     head_extra=HERO_PRELOAD, over=True, wide=True)

# ================================================================================================ ABOUT
PAGE = "about.html"
ROLES = [  # what each part of the studio does, in the studio's own words from the ten stages; no names are invented
    ("Design", "Takes the brief, plans the space and develops the design with you, then visits the site regularly to make sure it is built as drawn."),
    ("Procurement", "Selects and buys furnishings, fixtures and accessories, tracks every order and checks each delivery."),
    ("Site supervision", "A dedicated site supervisor runs the day-to-day work, checks materials, organises the crew and resolves problems."),
    ("Quality review", "An internal review confirms the work meets industry standards before the space is handed over."),
]
VALUES = [("Creativity", "Fresh ideas shaped around your vision and the way you want to live."),
          ("Functionality", "Layouts, storage and lighting planned for how the space is really used."),
          ("Sustainability", "Choices that respect both beauty and the environment."),
          ("Integrity", "Timeless quality as the goal, with integrity at the core of every project.")]


def pillars(rows):
    return '<div class="pillars">' + "".join(f"<div><b>{i + 1:02d}</b><h3>{t}</h3><p>{d}</p></div>" for i, (t, d) in enumerate(rows)) + "</div>"


about = opener("About", "Design shaped around <em>how you live</em>", "Atwood Dsigns is an interior design and build studio in Kokapet, Hyderabad. We believe great design goes beyond looks: it shapes the way you live, work and feel in your space.", "res-22") + f'''
<section class="story sec" aria-labelledby="story-h">
  <div class="wrap grid">
    <div class="story__statement">{kicker("01", "Philosophy")}<h2 class="statement" id="story-h">We create interiors that are <em>visually striking</em> and deeply practical, tailored to the lifestyle and vision of each client.</h2></div>
    <div class="story__cols">
      <p>Every project begins by listening: understanding your needs, your aspirations and the story you want your space to tell. We turn those ideas into well-planned designs that balance beauty, practicality and sustainability.</p>
      <p>From warm, inviting homes to inspiring commercial environments, our team brings ideas to life with quality materials, considered layouts and a keen eye for detail. With Atwood, it isn't just design; it's the art of living beautifully.</p>
    </div>
    {fig("res-18", "r-23", "(max-width: 899px) 100vw, 25vw", "Wooden double door with glazed panels", cls="story__aside", where="philosophy")}
  </div>
</section>
<section class="sec dark" aria-labelledby="val-h">
  <div class="wrap">
    <div class="shead">{kicker("02", "Values")}<h2 id="val-h">What guides <em>our work</em></h2><p>Creativity and function, guided by your vision, crafted with precision and enriched with sustainable choices.</p></div>
    {pillars(VALUES)}
  </div>
</section>
<section class="sec" aria-labelledby="team-h">
  <div class="wrap">
    <div class="shead">{kicker("03", "The team")}<h2 id="team-h">One team, from drawing <em>to handover</em></h2><p>Your project stays with the same studio throughout. These are the responsibilities it carries at each step.</p></div>
    {pillars(ROLES)}
  </div>
</section>
<section class="visit sec dark" aria-labelledby="visit-h">
  <div class="wrap grid">
    <div class="visit__text">
      {kicker("04", "Visit")}
      <h2 id="visit-h">The studio <em>in Kokapet</em></h2>
      <p class="lead">Meet us at the studio, or we'll come to your site. The first consultation is free.</p>
      <div class="actions"><a class="btn btn--light" href="contact.html">Book a visit {ARR}</a>{go(MAPS, "Open in Maps", ' target="_blank" rel="noopener"')}</div>
    </div>
    <div class="visit__card">
      <div><span>Studio</span><p>{ADDR}</p></div>
      <div><span>Call</span><a href="{TEL}">{PHONE}</a></div>
      <div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
    </div>
  </div>
</section>
{faq_block()}'''
page("about.html", "About the Studio | Atwood Dsigns", "Atwood Dsigns is an interior design and build studio in Kokapet, Hyderabad, creating interiors that balance beauty, practicality and sustainability.", about, og_image=P + "res-22.jpg")

# ================================================================================================ SERVICES
PAGE = "services.html"


def items(rows, cls=""):
    return f'<ul class="items {cls}">' + "".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a, b in rows) + "</ul>"


services = opener("Services", "Interiors, <em>start to finish</em>", "Whether you are refreshing a commercial property or designing a welcoming home, we capture your vision and turn it into a space that is practical, elegant and yours.", "res-43", pos="55% 50%") + f'''
<div class="svc-flow">
<nav class="jump" aria-label="Services on this page"><div class="wrap">{"".join(f'<a href="#{a}"><b>{i + 1:02d}</b>{t}</a>' for i, (a, t, d) in enumerate(SERVICES))}</div></nav>
<section class="svc sec" id="residential" aria-labelledby="res-h">
  <div class="wrap grid">
    {fig("res-12", "r-45", "(max-width: 860px) 100vw, 50vw", "Bedroom with an upholstered bed, geometric wardrobe and study desk", cls="svc__pic", where="residential", pos="62% 50%")}
    <div class="svc__text">
      {kicker("01", "Residential")}
      <h2 id="res-h">Homes, <em>room by room</em></h2>
      <p class="lead">Your home should reflect your personality, lifestyle and comfort. From modern apartments to luxury villas, we design timeless spaces with warmth, elegance and practicality in every corner.</p>
      {items(RES)}
      {go("contact.html?type=Full+home+interiors", "Plan your home with us")}
    </div>
  </div>
</section>
<section class="svc sec dark" id="commercial" aria-labelledby="com-h">
  <div class="wrap grid">
    <div class="svc__head">
      {kicker("02", "Commercial")}
      <h2 id="com-h">Workplaces, shops <em>and hospitality</em></h2>
      <p class="lead">Every workplace, retail space or hospitality venue should look impressive and also improve productivity, customer engagement and the overall experience.</p>
      {go("contact.html?type=Office+interiors", "Discuss a commercial project")}
    </div>
    <div class="svc__list">{items(COM, "items--1")}</div>
  </div>
</section>
<section class="svc sec parch" id="specialized" aria-labelledby="spec-h">
  <div class="wrap">
    <div class="shead">{kicker("03", "Specialised")}<h2 id="spec-h">Specialised <em>interior solutions</em></h2><p>Good design comes from communication. Our specialised services focus on commercial fit-outs, combining creative design with technical knowledge of construction standards.</p></div>
    {items(SPEC, "items--3")}
  </div>
</section>
<section class="svc svc--flip sec" id="turnkey" aria-labelledby="turn-h">
  <div class="wrap grid">
    {fig("res-33", "r-45", "(max-width: 860px) 100vw, 50vw", "Grey modular kitchen with glass-fronted wall cabinets", cls="svc__pic", where="turnkey")}
    <div class="svc__text">
      {kicker("04", "Turnkey")}
      <h2 id="turn-h">One studio <em>answers for it</em></h2>
      <p class="lead">We don't hand over drawings and walk away. Quantity surveying, procurement, project planning, site management and quality control are all ours, so one studio answers for the result.</p>
      {go("process.html", "See all ten stages")}
    </div>
  </div>
</section>
</div>'''
page("services.html", "Interior Design Services | Atwood Dsigns", "Residential interiors, commercial interiors, specialised interior solutions and turnkey delivery from Atwood Dsigns, Hyderabad.", services, og_image=P + "res-40.jpg")

# ================================================================================================ PROCESS
PAGE = "process.html"
process = opener("Process", "From first conversation <em>to handover</em>", "Our design process captures exactly what you want; our execution process makes sure it is built that way. Here is what happens at each of the ten stages.", "res-24", pos="68% 50%") + f'''
{journey("01", detailed=True, more=False, title="Five of design, <em>five of execution</em>")}
<section class="why sec parch" aria-labelledby="why-h">
  <div class="wrap grid">
    {fig("res-31", "r-43", "(max-width: 860px) 100vw, 50vw", "Bedroom with full-height fitted wardrobes", cls="why__pic", where="why one team")}
    <div class="why__text">
      {kicker("02", "One team")}
      <h2 id="why-h">Why one team <em>matters</em></h2>
      <p class="lead">When the people who design your space also manage its construction, nothing gets lost between the drawing and the site.</p>
      <p>Our designers visit the site while work is in progress, and a committed site supervisor manages day-to-day activities, monitors materials and resolves problems as they arise.</p>
    </div>
  </div>
</section>'''
page("process.html", "Our Design and Build Process | Atwood Dsigns", "The ten stages of the Atwood Dsigns design and execution process, from concept design to quality control.", process, og_image=P + "res-24.jpg")

# ================================================================================================ IDEAS
PAGE = "ideas.html"


def idea_block(a, t, ps, pf, ty, key, feature=False):
    paras = "".join(f"<p>{p}</p>" for p in ps)
    plan = f'Plan your {t if t.startswith("TV") else t.lower()}'
    acts = go(f"contact.html?type={ty}", plan) + (go(f"portfolio.html#{pf}", "See them in the portfolio") if pf else "")
    text = f'<div class="idea__text"><h2 id="{a}-h">{em_last(t, 1)}</h2>{paras}<div class="idea__actions">{acts}</div></div>'
    if feature:
        return f'<article class="idea idea--feature" id="{a}" aria-labelledby="{a}-h">{ph(key, "r-43", "(max-width: 899px) 100vw, 58vw", where=t)}{text}</article>'
    if key:
        return f'<article class="idea" id="{a}" aria-labelledby="{a}-h">{ph(key, "r-45", "(max-width: 700px) 100vw, 45vw", where=t)}{text}</article>'
    return f'<article class="idea idea--text" id="{a}" aria-labelledby="{a}-h">{text}</article>'  # no studio photograph of this room yet


_first, *_rest = IDEAS
ideas = plain("Ideas", "Ideas, <em>room by room</em>", "How we think about the rooms people ask us about most, shown with rooms we have designed and built.") + f'''
<section class="sec" style="padding-top:0" aria-label="Rooms">
  <div class="wrap">
    <nav class="chips ideas-nav" aria-label="Rooms on this page">{"".join(f'<a href="#{a}">{apos(t)}</a>' for a, t, *_ in IDEAS)}</nav>
    {idea_block(_first[0], _first[1], _first[6], _first[4], _first[5], IDEA_PHOTO[_first[0]], feature=True)}
    <div class="ideas">{"".join(idea_block(a, t, ps, pf, ty, IDEA_PHOTO[a]) for a, t, b, d, pf, ty, ps in _rest)}</div>
  </div>
</section>'''
page("ideas.html", "Interior Ideas, Room by Room | Atwood Dsigns", "Living room, TV unit, kids' bedroom, modular kitchen, bedroom and bathroom ideas from Atwood Dsigns, Hyderabad.", ideas, og_image=P + "res-37.jpg")

# ================================================================================================ PORTFOLIO
PAGE = "portfolio.html"
counts = {c: sum(1 for _, cc, _ in CARDS if cc == c) for c, _ in CATS}
counts["all"] = len(CARDS)
gallery = ""
for title, cat, keys in CARDS:
    lead = keys[0]
    photos = "|".join(f"{PHOTOS[k][0]}::{PHOTOS[k][1]}" for k in keys)
    for k in keys[1:]:
        USED.setdefault(k, set()).add("portfolio.html: viewer sequence")
    more = f'<span class="more" aria-hidden="true">{len(keys)} photographs</span>' if len(keys) > 1 else ""
    label = f"{title}, {CAT_ONE[cat].lower()}" + (f", {len(keys)} photographs" if len(keys) > 1 else "")
    pic = ph(lead, "", "(max-width: 960px) 50vw, 66vw", where="card")
    if more:
        pic = pic[:-len("</div>")] + more + "</div>"
    gallery += f'''<a class="card" href="{PHOTOS[lead][0]}" data-cursor="Open" data-cat="{cat}" data-photos="{photos}" aria-label="{label}">{pic}<h2>{apos(title)}</h2><span class="card__meta">{apos(CAT_ONE[cat])}</span></a>'''
chips = "".join(f'<button type="button" data-filter="{c}" aria-pressed="{"true" if c == "all" else "false"}">{n}<small>{counts[c]}</small></button>' for c, n in CATS)
STORY = {  # (main photograph, a second view): each project's strongest frame and one that adds to it
    "project-space-kids-bedroom": ("res-21", "res-20"), "project-dining-bar": ("res-11", "res-08"), "project-open-kitchen": ("res-30", "res-07")}


def story(n, pr):
    flip = " story-case--flip" if n % 2 else ""
    main, sub = STORY[pr["slug"]]
    first = pr["overview"].split(". ")[0].rstrip(".") + "."
    return f'''<article class="story-case{flip}" data-cursor="View">
      {ph(main, "story-case__main", "(max-width: 899px) 100vw, 66vw", where="portfolio projects", alt="")}
      {ph(sub, "story-case__sub", "(max-width: 899px) 45vw, 25vw", where="portfolio projects", alt="")}
      <div class="story-case__text"><b>Project {n + 1:02d}</b><h3><a href="{pr["slug"]}.html">{em_last(pr["title"])}</a></h3><p>{first}</p><p>{apos(pr["cat"])} &middot; {len(pr["photos"])} photographs</p></div>
    </article>'''


cases = "".join(story(n, pr) for n, pr in enumerate(PROJECTS))
portfolio = plain("Portfolio", "Rooms we have <em>designed and built</em>", f"Kitchens, bedrooms, kids' rooms, living spaces and entrances across Hyderabad: {len(CARDS)} rooms, each with every photograph we have of it.") + f'''
<section class="sec dark" aria-labelledby="pfp-h">
  <div class="wrap">
    <div class="shead">{kicker("01", "Projects")}<h2 id="pfp-h">Photographed <em>in depth</em></h2><p>Spaces documented room by room, with notes on what went into each.</p></div>
    <div class="stories">{cases}</div>
  </div>
</section>
<section class="rooms" aria-labelledby="pf-h">
  <div class="wrap" style="padding-top:var(--sec)"><div class="shead" style="margin-bottom:var(--s6)">{kicker("02", "Every room")}<h2 id="pf-h">The <em>rooms</em></h2><p>Choose a room to see it full size, with every photograph of that space.</p></div></div>
  <div class="filterbar"><div class="wrap"><div class="chips" role="group" aria-label="Filter by room type">{chips}</div><p class="count" aria-hidden="true"><b data-count>{len(CARDS)}</b> rooms</p></div></div>
  <div class="wrap">
    <p class="sr-only" role="status" id="filter-status"></p>
    <div class="gallery">{gallery}</div>
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
    seq, halves = "", 0
    for k, kind in pr["seq"]:
        if k == pr["lead"]:
            continue  # the lead photograph already opens the page
        if kind == "wide":
            seq += f'<figure class="ps ps--wide">{ph(k, "r-32", "(max-width: 1320px) 100vw, 1320px", where="project sequence")}<figcaption class="cap">{PHOTOS[k][1]}</figcaption></figure>'
        else:
            lower = " ps--lower" if halves % 2 else ""  # the second of each pair hangs a little lower
            halves += 1
            seq += f'<figure class="ps ps--half{lower}">{ph(k, "r-45", "(max-width: 860px) 100vw, 50vw", where="project sequence")}<figcaption class="cap">{PHOTOS[k][1]}</figcaption></figure>'
    seq_html = f'<section class="sec" style="padding-top:0" aria-label="Photographs"><div class="wrap pseq">{seq}</div></section>' if seq else ""
    body = f'''<article aria-labelledby="pr-h">
<section class="phero">
  {ph(pr["lead"], "", "100vw", lazy=False, where="lead photograph", img_extra=' fetchpriority="high"')}
  <div class="phero__text">{crumbs(("portfolio.html", "Portfolio"), f"Project {n + 1:02d}")}<h1 id="pr-h">{em_last(pr["title"])}</h1></div>
</section>
<div class="wrap"><dl class="pfacts">
  <div><dt>Room</dt><dd>{apos(pr["cat"])}</dd></div>
  <div><dt>Photographs</dt><dd>{len(pr["photos"])}</dd></div>
  <div><dt>Studio</dt><dd>Atwood Dsigns</dd></div>
  <div><dt>Scope</dt><dd>Design and build</dd></div>
</dl></div>
<section class="pover sec" aria-labelledby="ov-h">
  <div class="wrap grid">
    <div class="pover__k">{kicker("", "Overview")}<h2 class="sr-only" id="ov-h">Overview</h2></div>
    <div class="pover__text">
      <p class="statement">{pr["overview"]}</p>
      <h3>In the room</h3>
      {items(pr["seen"])}
      <p class="pnote">Notes describe what is visible in the photographs.</p>
    </div>
  </div>
</section>
{seq_html}
</article>
<section class="pplan sec parch" aria-labelledby="nx-h">
  <div class="wrap grid">
    <h2 id="nx-h">Planning a room <em>like this?</em></h2>
    <div class="pplan__text">
      <p class="lead">Tell us about your space and we will walk you through how we would design and build it.</p>
      <div class="actions"><a class="btn" href="contact.html?type={pr["contact"]}">Plan a similar room {ARR}</a>{go(f"portfolio.html#{pr['filter']}", f"More {CAT_NAME[pr['filter']].lower()}")}</div>
    </div>
  </div>
</section>
<a class="pnext" href="{nxt["slug"]}.html" data-cursor="Next">{ph(nxt["card"], "", "100vw", where="next project", alt="", pos=nxt["card_pos"])}<span class="pnext__text"><span>Next project</span><strong>{em_last(nxt["title"])}</strong><small>{apos(nxt["cat"])} &middot; {len(nxt["photos"])} photographs</small></span></a>'''
    page(PAGE, f"{pr['title']} | Atwood Dsigns", f"{pr['title']} by Atwood Dsigns, an interior design and build studio in Hyderabad: photographs and notes on the materials, joinery and lighting.", body,
         closing=False, og_image=PHOTOS[pr["lead"]][0], section="portfolio.html", over=True)

# ================================================================================================ JOURNAL
PAGE = "journal.html"


def post_card(p, h="h2"):
    pic = cms.ph(p["cover"] or p["hero"], "r-32", "(max-width: 600px) 100vw, (max-width: 960px) 50vw, 33vw", alt="") if (p["cover"] or p["hero"]) else ""
    return f'''<article class="post" data-cursor="Read">{pic}<p class="meta">{post_meta(p)}</p><{h}><a href="{post_href(p)}">{esc(p["title"])}</a></{h}><p>{esc(p["excerpt"])}</p></article>'''


def ld(*objs):
    """JSON-LD blocks; "</" is escaped so text from the CMS can't close the script element."""
    data = [json.dumps(o, ensure_ascii=False).replace("</", "<\\/") for o in objs]
    return "".join(f'\n<script type="application/ld+json">{d}</script>' for d in data)


def og(img):
    """A 1200 x 630 crop around the Studio hotspot, for WhatsApp, Facebook and LinkedIn previews."""
    h = img.get("hotspot") or {}
    return f'{img["url"]}?w=1200&h=630&fit=crop&crop=focalpoint&fp-x={h.get("x", .5):.3f}&fp-y={h.get("y", .5):.3f}&auto=format'


feature = ""
if JOURNAL:
    f0 = JOURNAL[0]
    pic = cms.ph(f0["cover"] or f0["hero"], "r-32", "(max-width: 860px) 100vw, 66vw", lazy=False) if (f0["cover"] or f0["hero"]) else ""
    feature = f'''<article class="feature-post">{pic}<div class="feature-post__text"><p class="meta">{post_meta(f0)}</p><h2><a href="{post_href(f0)}">{esc(f0["title"])}</a></h2><p>{esc(f0["excerpt"])}</p></div></article>'''
journal = plain("Journal", "Notes from <em>the studio</em>", "On designing homes and workplaces that work: residential, sustainable and commercial interiors.") + f'''
<section class="sec" style="padding-top:0" aria-label="Articles"><div class="wrap">{feature}<div class="posts">{"".join(post_card(p) for p in JOURNAL[1:])}</div></div></section>'''
page("journal.html", "Journal | Atwood Dsigns", "Articles from Atwood Dsigns on residential, sustainable and commercial interior design.", journal,
     head_extra=ld({"@context": "https://schema.org", "@type": "Blog", "name": "Journal | Atwood Dsigns", "url": SITE + "journal/",
                    "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": SITE + post_href(p).replace(".html", "/"),
                                  "datePublished": p["date"].isoformat()} for p in JOURNAL]}))

for p in JOURNAL:
    PAGE = post_href(p)
    url = SITE + PAGE.replace(".html", "/")
    body_html, faqs = cms.render_body(p["body"], SITE)
    by = esc(p["author"] or "Atwood Dsigns") + (f", {esc(p['author_role'])}" if p["author"] and p["author_role"] else "")
    hero = f'''<div class="wrap article-hero">{cms.ph(p["hero"], "r-169", "(max-width: 1320px) 100vw, 1320px", lazy=False, extra=' fetchpriority="high"')}</div>''' if p["hero"] else ""
    same = [q for q in JOURNAL if q is not p and set(q["categories"]) & set(p["categories"])]
    more = (same + [q for q in JOURNAL if q is not p and q not in same])[:3]
    related = f'''<section class="sec parch" aria-labelledby="more-h"><div class="wrap">
  <div class="shead">{kicker("", "Keep reading")}<h2 id="more-h">More from <em>the journal</em></h2></div>
  <div class="posts">{"".join(post_card(q, "h3") for q in more)}</div>
</div></section>''' if more else ""
    body = f'''<article aria-labelledby="post-h">
<header class="ahead">
  <div class="wrap">
    {crumbs(("journal.html", "Journal"), esc(p["category"]))}
    <h1 id="post-h">{esc(p["title"])}</h1>
    <p class="lead">{esc(p["excerpt"])}</p>
    <p class="meta">{post_meta(p)} &middot; {p["read"]} &middot; {by}</p>
  </div>
</header>
{hero}
<div class="wrap"><div class="article__body">
{body_html}
</div></div>
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
contact = f'''<section class="reach" aria-labelledby="contact-h">
  <div class="wrap grid">
    <div class="reach__intro">
      {crumbs("Contact")}
      <h1 id="contact-h">Start with a <em>conversation</em></h1>
      <p class="lead">Whether you have a question, need expert advice or are ready to transform your space, we're here to help. The first consultation is free.</p>
      <div class="routes">
        <a class="route" href="{TEL}"><span>Call</span><b>{PHONE}</b>{ARR}</a>
        <a class="route" href="{WA}" target="_blank" rel="noopener"><span>WhatsApp</span><b>Message the studio</b>{ARR}</a>
        <a class="route" href="mailto:{EMAIL}"><span>Email</span><b>{EMAIL}</b>{ARR}</a>
      </div>
      <div class="reach__steps">
        <h2>What happens next</h2>
        <ol class="next-steps">
          <li>Tell us about your space and what you have in mind.</li>
          <li>We meet you for a free consultation, at our studio in Kokapet or at your site.</li>
          <li>We develop design concepts for your approval, then manage the execution through to handover.</li>
        </ol>
      </div>
    </div>
    <div class="reach__form">
      <form class="form" id="enquiry" novalidate>
        <h2>Book a free <em>consultation</em></h2>
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
        <div class="actions"><button class="btn" type="submit">Send by email</button><button class="btn btn--line" type="button" data-whatsapp>Send on WhatsApp</button></div>
        <p class="form-note">Both open your email or WhatsApp app with your details filled in, ready to send. What you type is kept on this device until you send it.</p>
        <div class="form-status" role="status" aria-live="polite"></div>
      </form>
    </div>
  </div>
</section>
<section aria-label="Map"><div class="wrap" style="padding-bottom:var(--sec)">
  <p class="kicker"><b>{ADDR_SHORT.split(",")[0]}</b>{", ".join(ADDR_SHORT.split(",")[1:]).strip()} &middot; <a href="{MAPS}" target="_blank" rel="noopener" style="color:inherit">Open in Maps</a></p>
  <iframe class="map" title="Map showing Atwood Dsigns in Kokapet, Hyderabad" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=E-Infra%20Tower%2C%20Brindavan%20Colony%2C%20Kokapet%2C%20Hyderabad%20500075&z=15&output=embed"></iframe>
</div></section>'''
page("contact.html", "Contact and Free Consultation | Atwood Dsigns", "Book a free interior design consultation with Atwood Dsigns in Kokapet, Hyderabad. Call +91 90001 81212 or message us on WhatsApp.", contact, closing=False)

# ================================================================================================ manifest
KIND = {"studio": "Studio photograph", "supplied": "Photograph supplied by the studio (November 2026)", "library": "Library image (previous website, most likely stock)"}
lines = ["# Photograph manifest", "",
         "Generated by `tools/build.py` from its `PHOTOS` table. To replace a picture, change its entry there and rebuild.", "",
         "Studio photographs are the ones the studio uploaded of its own finished rooms (February 2026). Library images came with the",
         "previous website and are most likely stock; they are not shown anywhere that would present them as the studio's work.",
         "Run `python3 tools/webp.py` after adding photographs, so the pages can serve WebP copies.", "",
         "| Key | File | Kind | Focal point | Shows | Used on |", "|---|---|---|---|---|---|"]
for k, (src, desc, kind, pos) in PHOTOS.items():
    lines.append(f"| {k} | `{src}` | {KIND[kind]} | {pos} | {desc} | {'; '.join(sorted(USED.get(k, []))) or 'not used'} |")
lines += ["", "## Held back from the site", "", "| File | Reason |", "|---|---|"]
lines += [f"| {k} | {r} |" for k, r in HELD_BACK.items()]
with open(os.path.join(OUT, "ASSETS.md"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
print("built")
