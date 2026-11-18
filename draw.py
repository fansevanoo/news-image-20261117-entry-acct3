"""Render the news-image-20261117 front page for account 3 (fansevanoo).

1024x1024, supersampled 2x then downsampled. All sizes below are in final
pixels; every coordinate is multiplied by S when drawing.
Usage: python3 draw.py <A|B> <output.png>
  A = navy lead panel + white cards + briefs strip
  B = cream lead panel + pale cards, no briefs strip (taller grid)
"""
import sys
from PIL import Image, ImageDraw, ImageFont

S = 2
W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

NAVY = (20, 33, 61)
NAVY2 = (27, 45, 82)
CREAM = (247, 243, 232)
PAPER = (250, 247, 238)
CARD = (255, 255, 255)
CARD_B = (232, 238, 240)
GOLD = (201, 162, 39)
GOLD_L = (224, 186, 74)
TEAL = (15, 118, 110)
SLATE = (91, 100, 114)
INK = (20, 33, 61)
RULE = (201, 162, 39)


def F(name, size):
    return ImageFont.truetype(FONT_DIR + name, int(size * S))


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_h(font):
    return int(font.size * 1.18)


def draw_wrapped(d, x, y, text, font, fill, max_w, lh=None):
    lines = wrap(d, text, font, max_w)
    h = lh if lh else text_h(font)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += h
    return y, len(lines)


def rrect(d, box, fill, outline=None, width=1, radius=10):
    d.rounded_rectangle([v * S for v in box], radius=radius * S,
                        fill=fill, outline=outline, width=width * S)


def line(d, pts, fill, width=2):
    d.line([(x * S, y * S) for x, y in pts], fill=fill, width=width * S)


def ellipse(d, box, outline=None, width=2, fill=None):
    (x0, y0), (x1, y1) = box
    d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], outline=outline,
              width=width * S, fill=fill)


# ---------------------------------------------------------------- icons
def icon_bridge(d, x, y, s, col):
    # arch bridge with a collapsed span + smoke
    d.arc([x * S, (y - s * 0.15) * S, (x + s) * S, (y + s * 0.75) * S],
          200, 340, fill=col, width=3 * S)
    line(d, [(x, y + s * 0.62), (x + s * 0.32, y + s * 0.62),
             (x + s * 0.68, y + s * 0.62), (x + s, y + s * 0.62)], col, 3)
    line(d, [(x + s * 0.32, y + s * 0.62), (x + s * 0.42, y + s * 0.78)], col, 3)
    line(d, [(x + s * 0.68, y + s * 0.62), (x + s * 0.58, y + s * 0.78)], col, 3)
    for cx, cy, r in [(0.5, 0.18, 0.09), (0.58, 0.08, 0.07), (0.42, 0.10, 0.06)]:
        ellipse(d, [(x + cx * s - r * s, y + cy * s - r * s),
                    (x + cx * s + r * s, y + cy * s + r * s)], fill=col)


def icon_drone(d, x, y, s, col):
    cx, cy = x + s * 0.5, y + s * 0.5
    ellipse(d, [(cx - s * 0.16, cy - s * 0.10), (cx + s * 0.16, cy + s * 0.10)],
            fill=col)
    for dx, dy in [(-0.32, -0.28), (0.32, -0.28), (-0.32, 0.28), (0.32, 0.28)]:
        line(d, [(cx, cy), (cx + dx * s, cy + dy * s)], col, 3)
        line(d, [(cx + dx * s - s * 0.14, cy + dy * s),
                 (cx + dx * s + s * 0.14, cy + dy * s)], col, 3)
    for r in (0.30, 0.44):
        d.arc([(cx - r * s) * S, (cy - r * s) * S, (cx + r * s) * S,
               (cy + r * s) * S], 200, 340, fill=col, width=2 * S)


def icon_gate(d, x, y, s, col):
    # tent / open gate for aid access
    line(d, [(x + s * 0.08, y + s * 0.85), (x + s * 0.5, y + s * 0.12),
             (x + s * 0.92, y + s * 0.85)], col, 3)
    line(d, [(x + s * 0.30, y + s * 0.85), (x + s * 0.5, y + s * 0.48),
             (x + s * 0.70, y + s * 0.85)], col, 3)
    line(d, [(x + s * 0.5, y + s * 0.55), (x + s * 0.5, y + s * 0.85)], col, 3)
    line(d, [(x + s * 0.58, y + s * 0.70), (x + s * 0.92, y + s * 0.70)], col, 3)
    line(d, [(x + s * 0.82, y + s * 0.60), (x + s * 0.92, y + s * 0.70),
             (x + s * 0.82, y + s * 0.80)], col, 3)


def icon_hub(d, x, y, s, col):
    # building + location pin
    d.rectangle([x * S, (y + s * 0.30) * S, (x + s * 0.62) * S,
                 (y + s * 0.88) * S], outline=col, width=3 * S)
    for wx in (0.12, 0.30, 0.48):
        d.rectangle([(x + wx * s) * S, (y + s * 0.44) * S,
                     (x + (wx + 0.08) * s) * S, (y + s * 0.56) * S], fill=col)
    px, py = x + s * 0.78, y + s * 0.30
    ellipse(d, [(px - s * 0.13, py - s * 0.13), (px + s * 0.13, py + s * 0.13)],
            fill=col)
    line(d, [(px - s * 0.10, py + s * 0.10), (px, py + s * 0.34),
             (px + s * 0.10, py + s * 0.10)], col, 3)


def icon_chart(d, x, y, s, col):
    line(d, [(x + s * 0.10, y + s * 0.15), (x + s * 0.10, y + s * 0.88),
             (x + s * 0.92, y + s * 0.88)], col, 3)
    bars = [(0.22, 0.55), (0.40, 0.40), (0.58, 0.48), (0.76, 0.28)]
    for bx, bh in bars:
        d.rectangle([(x + bx * s) * S, (y + (0.88 - bh) * s) * S,
                     (x + (bx + 0.12) * s) * S, (y + s * 0.88) * S], fill=col)
    line(d, [(x + s * 0.18, y + s * 0.30), (x + s * 0.85, y + s * 0.18)], col, 3)
    line(d, [(x + s * 0.72, y + s * 0.18), (x + s * 0.85, y + s * 0.18),
             (x + s * 0.85, y + s * 0.31)], col, 3)


def icon_cross(d, x, y, s, col):
    ellipse(d, [(x, y), (x + s, y + s)], outline=col, width=3 * S)
    cx, cy = x + s * 0.5, y + s * 0.5
    d.rectangle([(cx - s * 0.09) * S, (cy - s * 0.26) * S,
                 (cx + s * 0.09) * S, (cy + s * 0.26) * S], fill=col)
    d.rectangle([(cx - s * 0.26) * S, (cy - s * 0.09) * S,
                 (cx + s * 0.26) * S, (cy + s * 0.09) * S], fill=col)


def globe(d, cx, cy, r, line_col, dot_cols):
    ellipse(d, [(cx - r, cy - r), (cx + r, cy + r)], outline=line_col, width=4)
    d.ellipse([(cx - r * 0.42) * S, (cy - r) * S, (cx + r * 0.42) * S,
               (cy + r) * S], outline=line_col, width=3 * S)
    d.ellipse([(cx - r) * S, (cy - r * 0.42) * S, (cx + r) * S,
               (cy + r * 0.42) * S], outline=line_col, width=3 * S)
    line(d, [(cx - r, cy), (cx + r, cy)], line_col, 3)
    pts = [(-0.55, -0.45), (0.10, -0.62), (0.62, -0.10)]
    drawn = []
    for fx, fy in pts:
        px, py = cx + fx * r, cy + fy * r
        drawn.append((px, py))
        ellipse(d, [(px - 9, py - 9), (px + 9, py + 9)], fill=dot_cols[len(drawn) - 1])
    for i in range(len(drawn) - 1):
        x1, y1 = drawn[i]
        x2, y2 = drawn[i + 1]
        line(d, [(x1, y1), (x2, y2)], line_col, 3)


# ---------------------------------------------------------------- data
LEAD = ("DIPLOMACY",
        "Trump, Xi and Putin to hold first three-way summit",
        "Trilateral meeting confirmed for Thursday in Shenzhen. "
        "Trump arrives in Manila for the ASEAN summit first.")

SECONDARY = [
    ("UKRAINE WAR", "Ukraine strikes Crimean Bridge again",
     "A section of the road bridge collapses; Russia hits Kyiv bridges.", icon_bridge),
    ("GULF / IRAN", "Iran fires drones at US radar",
     "Bahrain says all drones were intercepted, no damage.", icon_drone),
    ("GAZA", "West urges Israel to open Gaza crossings",
     "UK, Australia, Canada and Italy call for rapid aid access.", icon_gate),
    ("EUROPE", "Five EU states plan Rwanda return hub",
     "First transfers in 2027; rights groups object.", icon_hub),
    ("ECONOMY / TECH", "Xi and Carney agree new tariff cuts",
     "China cuts duties on C$400m of pork and seafood.", icon_chart),
    ("HEALTH", "Measles cases highest since 1991",
     "Thirteen babies born with congenital measles in the US.", icon_cross),
]

BRIEFS = [
    ("Hormuz", "Third US carrier, USS Theodore Roosevelt, joins the Gulf force."),
    ("Japan", "Tokyo scrambles fighters as suspected Russian jets enter its airspace."),
    ("Estonia", "Crossings to Russia close 1 December after a foiled bomb plot."),
    ("Pentagon", "Fails its audit for a ninth year; $4.8 trillion unverified."),
]

# Variant C trims the secondary detail lines so each fits two lines at 20px.
DETAILS_C = [
    "Bridge span collapses; Russia hits Kyiv bridges.",
    "Bahrain says all drones intercepted, no damage.",
    "UK, Australia, Canada and Italy urge aid access.",
    "First transfers in 2027; rights groups object.",
    "China cuts duties on C$400m of pork and seafood.",
    "Thirteen babies born with congenital measles in US.",
]

BRIEFS_TICKER = ("Hormuz: third US carrier joins Gulf force \u00b7 "
                 "Japan: jets scrambled over Russian airspace \u00b7 "
                 "Estonia: Russia border closes 1 December \u00b7 "
                 "Pentagon: ninth failed audit in a row")

FOOTER_C = ("Every story happened or was first reported on Tuesday 17 November 2026. "
            "Sources: Reuters \u00b7 Al Jazeera \u00b7 CNN \u00b7 NPR \u00b7 AP. "
            "Original drawings.")

FOOTER = ("Every story happened or was first reported on Tuesday 17 November 2026. "
          "Disputed claims are attributed. Sources: Reuters \u00b7 Al Jazeera \u00b7 "
          "CNN \u00b7 NPR \u00b7 AP. Original drawings.")


def render(variant, out_path):
    img = Image.new("RGB", (W * S, H * S), CREAM)
    d = ImageDraw.Draw(img)

    is_c = (variant == "C")
    f_mast = F("DejaVuSerif-Bold.ttf", 60)
    f_date = F("DejaVuSerif-Bold.ttf", 34)
    f_kick = F("DejaVuSans-Bold.ttf", 19)
    f_lead = F("DejaVuSerif-Bold.ttf", 46 if is_c else 42)
    f_lead_det = F("DejaVuSans.ttf", 24 if is_c else 23)
    f_head = F("DejaVuSans-Bold.ttf", 27)
    f_det = F("DejaVuSans.ttf", 20)
    f_brief_h = F("DejaVuSans-Bold.ttf", 16)
    f_brief = F("DejaVuSans.ttf", 19)
    f_foot = F("DejaVuSans.ttf", 15)

    mast_h = 118 if is_c else 120
    lead_top = 128 if is_c else 132
    lead_bot = 472 if is_c else 512
    grid_top = 482 if is_c else 524
    cell_h = 204 if is_c else 190
    cell_w, gap = 318, 12
    card_fill = CARD if variant in ("A", "C") else CARD_B

    # ---- masthead (full-bleed navy band)
    d.rectangle([0, 0, W * S, mast_h * S], fill=NAVY)
    t = "WORLD NEWS"
    d.text(((W - d.textlength(t, font=f_mast) / S) / 2 * S, 6 * S),
           t, font=f_mast, fill=CREAM)
    t2 = "TUESDAY 17 NOVEMBER 2026"
    d.text(((W - d.textlength(t2, font=f_date) / S) / 2 * S, 72 * S),
           t2, font=f_date, fill=GOLD_L)
    line(d, [(24, mast_h), (1000, mast_h)], GOLD, 3)

    lead_navy = (variant in ("A", "C"))
    lead_bg = NAVY if lead_navy else CREAM
    lead_fg = CREAM if lead_navy else NAVY
    lead_det_col = (226, 220, 200) if lead_navy else SLATE
    lead_line = GOLD_L if lead_navy else GOLD

    # ---- lead panel
    rrect(d, (24, lead_top, 1000, lead_bot), fill=lead_bg,
          outline=GOLD if not lead_navy else None, width=2, radius=12)
    kicker, headline, detail = LEAD
    d.text((52 * S, (lead_top + 22) * S), kicker,
           font=F("DejaVuSans-Bold.ttf", 24), fill=lead_line)
    line(d, [(52, lead_top + 58), (140, lead_top + 58)], lead_line, 3)
    y, _ = draw_wrapped(d, 52 * S, (lead_top + 72) * S, headline, f_lead,
                        lead_fg, 540 * S, lh=int(f_lead.size * 1.16))
    y += 12 * S
    draw_wrapped(d, 52 * S, y, detail, f_lead_det, lead_det_col, 540 * S,
                 lh=int(f_lead_det.size * 1.3))
    # globe illustration, right side of the lead panel
    globe(d, 800, lead_top + 175, 140, lead_line,
          [GOLD_L, TEAL, CREAM if lead_navy else NAVY])

    # ---- secondary grid: 3 cols x 2 rows
    for i, (kick, head, det, icon) in enumerate(SECONDARY):
        if is_c:
            det = DETAILS_C[i]
        col, row = i % 3, i // 3
        x0 = 24 + col * (cell_w + gap)
        y0 = grid_top + row * (cell_h + gap)
        rrect(d, (x0, y0, x0 + cell_w, y0 + cell_h), fill=card_fill,
              outline=(200, 205, 210), width=1, radius=10)
        # icon in the kicker row, left
        icon(d, x0 + 14, y0 + 12, 34, TEAL)
        d.text(((x0 + 56) * S, (y0 + 16) * S), kick, font=f_kick, fill=TEAL)
        # headline, full card width
        y, _ = draw_wrapped(d, (x0 + 14) * S, (y0 + 56) * S, head, f_head,
                            INK, (cell_w - 28) * S, lh=int(27 * 1.16 * S))
        draw_wrapped(d, (x0 + 14) * S, y + 4 * S, det, f_det, SLATE,
                     (cell_w - 28) * S, lh=int(20 * 1.22 * S))

    y_cur = grid_top + 2 * cell_h + gap

    # ---- briefs strip (variant A: numbered list; variant C: ticker)
    if variant == "A":
        d.text((24 * S, (y_cur + 2) * S), "ALSO ON TUESDAY 17 NOVEMBER",
               font=f_brief_h, fill=NAVY)
        y_cur += 24
        for j in range(0, 4, 2):
            for k, (place, text) in enumerate(BRIEFS[j:j + 2]):
                bx = 24 + k * 492
                num = str(16 + j + k)
                ellipse(d, [(bx, y_cur), (bx + 22, y_cur + 22)], fill=TEAL)
                tw = d.textlength(num, font=f_brief_h)
                d.text(((bx + 11) * S - tw / 2, (y_cur + 2) * S), num,
                       font=f_brief_h, fill=CREAM)
                d.text(((bx + 30) * S, (y_cur + 1) * S),
                       place + ": " + text, font=f_brief, fill=INK)
            y_cur += 24
        y_cur += 4
    elif is_c:
        d.text((24 * S, (y_cur + 2) * S), "ALSO ON TUESDAY 17 NOVEMBER",
               font=f_brief_h, fill=NAVY)
        draw_wrapped(d, 24 * S, (y_cur + 22) * S, BRIEFS_TICKER, f_brief,
                     INK, 976 * S, lh=int(19 * 1.25 * S))
        y_cur += 22 + 2 * int(19 * 1.25) + 6

    # ---- footer
    foot_text = FOOTER_C if is_c else FOOTER
    line(d, [(24, y_cur), (1000, y_cur)], GOLD, 2)
    draw_wrapped(d, 24 * S, (y_cur + 8) * S, foot_text, f_foot, SLATE,
                 976 * S, lh=int(15 * 1.3 * S))

    img = img.resize((W, H), Image.LANCZOS)
    img.save(out_path, "PNG")
    print("wrote", out_path, img.size)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
