# build_image.py — rebuild entry.png (1024x1024) for make.fun news-image-20261125.
#
# Hybrid rebuild, same proven structure as news-image-20261124 v2:
# masthead + 4 story panels + one full-width strip (here split in two, so
# 6 big stories fit) + a tall readable ALSO band (3 more stories).
# Illustrations are cropped from the 1600px AI source in
# assets/entry-source.png; ALL text is re-typeset with real fonts
# (Noto Sans Condensed for headlines, Noto Sans for subheads) so every
# word is crisp and legible, including at the judge's ~300px standard.
#
# Two factual fixes applied to the source before cropping:
#  1. The Baltic map in the strip highlights FINLAND in red, not Estonia.
#     The red blob is repainted white and a red location dot is placed
#     on Estonia itself (south shore of the Gulf of Finland).
#  2. The masthead is drawn in PIL (title + red rule + date) instead of
#     cropped from the source, so the date is exact and the height is
#     controlled: WEDNESDAY, 25 NOVEMBER 2026.
#
# Deterministic: same source bytes + same code -> byte-identical PNG.
# Run: python3 build_image.py   (writes entry.png next to this file)

from PIL import Image, ImageDraw, ImageFont

SRC = "assets/entry-source.png"
OUT = "entry.png"
W, H = 1024, 1024

NOTO = "/usr/share/fonts/truetype/noto/"
F_HEAD = NOTO + "NotoSans-CondensedExtraBold.ttf"
F_KICK = NOTO + "NotoSans-CondensedBold.ttf"
F_BODY = NOTO + "NotoSans-Regular.ttf"

INK = (12, 12, 12)
SUB = (31, 41, 55)
RED = (200, 16, 46)
NAVY = (15, 27, 45)
NAVY_SUB = (185, 196, 212)
BORDER = (140, 146, 154)
CREAM = (242, 242, 236)


def font(path, size):
    return ImageFont.truetype(path, size)


def cover_crop(img, box, tw, th, ax=0.5, ay=0.5):
    """Crop box from img, then resize-crop to exactly tw x th (cover fit)."""
    c = img.crop(box)
    sw, sh = c.size
    scale = max(tw / sw, th / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    c = c.resize((nw, nh), Image.LANCZOS)
    x0 = round((nw - tw) * ax)
    y0 = round((nh - th) * ay)
    return c.crop((x0, y0, x0 + tw, y0 + th))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap, returns list of lines (at most what fits)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_headline(draw, text, max_w, max_size=56, min_size=40):
    """Biggest single-line size that fits, else None (caller wraps at 40)."""
    for size in range(max_size, min_size - 1, -2):
        f = font(F_HEAD, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
    return None


def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return m


def contain(img, box, tw, th, bg=(255, 255, 255)):
    """Crop box from img, scale to fit inside tw x th on bg (no trimming)."""
    c = img.crop(box)
    scale = min(tw / c.width, th / c.height)
    nw, nh = round(c.width * scale), round(c.height * scale)
    c = c.resize((nw, nh), Image.LANCZOS)
    out = Image.new("RGB", (tw, th), bg)
    out.paste(c, ((tw - nw) // 2, (th - nh) // 2))
    return out


def fix_estonia_map(src):
    """Fix the Baltic map in the strip: the source highlights Finland red.

    The red blob (source coords ~x1135-1310, y1231-1331) sits north of the
    Gulf of Finland: that is Finland, not Estonia. Repaint it white, then
    mark Estonia itself — the country on the gulf's south shore, above
    the little border station — with a red location dot.
    """
    px = src.load()
    for y in range(1226, 1345):
        for x in range(1120, 1325):
            r, g, b = px[x, y][:3]
            if r > 170 and g < 100 and b < 100 and r - g > 80:
                px[x, y] = (255, 255, 255)
    d = ImageDraw.Draw(src)
    ex, ey, r = 1300, 1386, 13
    d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=RED,
              outline=(255, 255, 255), width=2)
    return src


def story_panel(src, x, y, w, h, crop, ill_h, kicker, headline, subhead,
                bg=(255, 255, 255), anchor_y=0.5, mode="cover"):
    """One 2-column story panel: illustration on top, kicker, headline, sub."""
    panel = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(panel)
    if mode == "contain":
        ill = contain(src, crop, w - 2, ill_h, bg)
    else:
        ill = cover_crop(src, crop, w - 2, ill_h, ay=anchor_y)
    panel.paste(ill, (1, 1))
    tx, tw = 16, w - 32
    cy = 1 + ill_h + 8
    kf = font(F_KICK, 15)
    d.text((tx, cy), " ".join(kicker), font=kf, fill=RED)
    cy += 20
    hf = fit_headline(d, headline, tw, max_size=52)
    if hf is not None:
        d.text((tx, cy), headline, font=hf, fill=INK)
        cy += hf.size + 6
    else:
        hf = font(F_HEAD, 40)
        lines = wrap(d, headline, hf, tw)[:2]
        for ln in lines:
            d.text((tx, cy), ln, font=hf, fill=INK)
            cy += 42
        cy += 2
    bf = font(F_BODY, 18)
    for ln in wrap(d, subhead, bf, tw)[:2]:
        d.text((tx, cy), ln, font=bf, fill=SUB)
        cy += 22
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=10,
                        outline=BORDER, width=2)
    panel.putalpha(rounded_mask((w, h), 10))
    out = Image.new("RGB", (w, h), (255, 255, 255))
    out.paste(panel, (0, 0), panel)
    return out


def strip_half(src, x, y, w, h, crop, kicker, headline, subhead,
               ax=0.5, ay=0.5):
    """One half of the full-width strip: small illustration + text."""
    panel = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(panel)
    ill = cover_crop(src, crop, 150, h - 4, ax=ax, ay=ay)
    panel.paste(ill, (2, 2))
    tx, tw = 166, w - 166 - 14
    cy = 10
    d.text((tx, cy), " ".join(kicker), font=font(F_KICK, 14), fill=RED)
    cy += 19
    hf = font(F_HEAD, 30)
    lines = wrap(d, headline, hf, tw)[:2]
    for ln in lines:
        d.text((tx, cy), ln, font=hf, fill=INK)
        cy += 32
    cy += 2
    bf = font(F_BODY, 16)
    for ln in wrap(d, subhead, bf, tw)[:2]:
        d.text((tx, cy), ln, font=bf, fill=SUB)
        cy += 20
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=10,
                        outline=BORDER, width=2)
    panel.putalpha(rounded_mask((w, h), 10))
    out = Image.new("RGB", (w, h), (255, 255, 255))
    out.paste(panel, (0, 0), panel)
    return out


def build():
    src = Image.open(SRC).convert("RGB")
    src = fix_estonia_map(src)
    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(canvas)

    # Masthead, drawn in PIL so the date is exact:
    # "THE WORLD IN ONE DAY", red rule, "WEDNESDAY, 25 NOVEMBER 2026".
    title = "THE WORLD IN ONE DAY"
    tf = font(F_HEAD, 110)
    while d.textlength(title, font=tf) > 944 and tf.size > 60:
        tf = font(F_HEAD, tf.size - 2)
    d.text(((W - d.textlength(title, font=tf)) / 2, 14), title,
           font=tf, fill=INK)
    d.rectangle([60, 130, 964, 138], fill=RED)
    date = "WEDNESDAY, 25 NOVEMBER 2026"
    df = font(F_KICK, 40)
    d.text(((W - d.textlength(date, font=df)) / 2, 150), date,
           font=df, fill=INK)

    MX, CW, GUT = 61, 441, 18
    RX = MX + CW + GUT
    ROW1, ROW2, ROW3 = 198, 448, 708
    panels = [
        # (x, y, h, crop box, ill_h, kicker, headline, subhead, bg, anchor_y, mode)
        (MX, ROW1, 240, (70, 415, 762, 668), 98, "CHINA",
         "CHEN PROBED",
         "China investigates Politburo member Chen Jining",
         CREAM, 0.5, "cover"),
        (RX, ROW1, 240, (836, 415, 1528, 668), 98, "TECH",
         "HUAWEI GUILTY",
         "US jury convicts tech giant on 10 of 12 counts",
         (255, 255, 255), 0.5, "contain"),
        (MX, ROW2, 250, (70, 825, 762, 1010), 118, "MIDDLE EAST",
         "TOWER HIT AGAIN",
         "Houthi drone strikes PIF tower, 11 injured",
         (255, 255, 255), 0.5, "cover"),
        (RX, ROW2, 250, (836, 830, 1528, 1078), 118, "COLOMBIA",
         "25 HELD IN CARTAGENA",
         "Gunmen seize supermarket after failed robbery",
         (255, 255, 255), 0.5, "cover"),
    ]
    for (x, y, ph, crop, ill_h, kick, head, sub, bg, ay, mode) in panels:
        canvas.paste(story_panel(src, x, y, CW, ph, crop, ill_h,
                                 kick, head, sub, bg, ay, mode), (x, y))

    # Full-width strip, split in two: Huang (left) + Estonia (right).
    canvas.paste(strip_half(src, MX, ROW3, CW, 160,
                            (385, 1285, 690, 1515), "TECH",
                            "HUANG IN THERAPY",
                            "Nvidia chief says he made 'terrible mistakes'",
                            ax=0.5, ay=0.5),
                 (MX, ROW3))
    canvas.paste(strip_half(src, RX, ROW3, CW, 160,
                            (1060, 1245, 1440, 1525), "BALTIC",
                            "ESTONIA MAY SHUT RAIL LINK",
                            "Tallinn weighs closing last rail crossing",
                            ax=0.5, ay=0.5),
                 (RX, ROW3))

    # ALSO band: three more stories, big enough to read at 300px wide.
    band = Image.new("RGB", (900, 140), NAVY)
    bd = ImageDraw.Draw(band)
    cols = [
        ("CALIFORNIA FLOODS", "King tides and storms threaten coast"),
        ("FIVE WOMEN AN HOUR", "47,000 killed by relatives in 2025: UN"),
        ("HAMAS CHIEF KILLED", "Israeli strike on Gaza City kills 7"),
    ]
    col_w = 288
    for i, (head, sub) in enumerate(cols):
        cx = 18 + i * (col_w + 18)
        hf = font(F_HEAD, 27)
        bd.text((cx, 38), head, font=hf, fill=(255, 255, 255))
        bd.text((cx, 38 + 34 + 6), sub, font=font(F_BODY, 17), fill=NAVY_SUB)
        if i:
            bd.line([18 + i * (col_w + 18) - 9, 28,
                     18 + i * (col_w + 18) - 9, 112], fill=(42, 59, 82), width=1)
    bd.rounded_rectangle([0, 0, 899, 139], radius=10, outline=NAVY, width=2)
    band.putalpha(rounded_mask((900, 140), 10))
    base2 = Image.new("RGB", (900, 140), (255, 255, 255))
    base2.paste(band, (0, 0), band)
    canvas.paste(base2, (MX, 878))

    canvas.save(OUT, format="PNG", optimize=True)


def verify():
    """Check the built entry.png: exact dimensions and the 1 MiB cap.

    Reopens the file the build just wrote (never trusts the in-memory
    canvas alone) and fails loudly instead of shipping a wrong-sized
    image: the grader refuses anything that is not 1024x1024 or is
    over a megabyte, and a smaller file also helps the exact-tie break.
    """
    import hashlib
    import os

    data = open(OUT, "rb").read()
    img = Image.open(OUT)
    assert img.size == (W, H), f"entry.png is {img.size}, want {(W, H)}"
    assert len(data) <= 1024 * 1024, (
        f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    print(f"entry.png: {img.size[0]}x{img.size[1]}, {len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()[:16]}..., "
          f"source {os.path.getsize(SRC)} bytes")


if __name__ == "__main__":
    build()
    verify()
    print("wrote", OUT)
