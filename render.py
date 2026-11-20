#!/usr/bin/env python3
"""Build script: draw the front page of Friday 20 November 2026.

Regenerates entry.png for the make.fun bounty news-image-20261120, "Sum up
20 November's world news in one image". Reads news.json (headlines verified
against reporting dated 19-20 November 2026) and renders a 1024x1024
newspaper front page with PIL. Writes entry.png next to this script; set OUT
to override. This is NOT the entrypoint: the graded program is main.py,
which only copies the committed entry.png. Run this only to rebuild the
image (needs Pillow and Liberation fonts; DejaVu is the fallback).

Deterministic by construction: no clock, no randomness, no network, fixed
fonts. The same news.json always produces the same PNG bytes.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 245, 238)   # newsprint off-white
INK = (17, 17, 17)        # near-black ink
RED = (185, 28, 28)       # accent red
GREY = (92, 88, 80)       # deck / footer grey
HAIR = (200, 196, 186)    # hairline grey
WHITE = (255, 255, 255)

FONT_DIRS = ("/usr/share/fonts/truetype/liberation",
             "/usr/share/fonts/truetype/dejavu")


def find_font(names):
    """First existing file among the candidates, Liberation preferred."""
    for base in FONT_DIRS:
        for name in names:
            path = os.path.join(base, name)
            if os.path.exists(path):
                return path
    raise FileNotFoundError("none of %r found under %r" % (names, FONT_DIRS))


SERIF_B = find_font(["LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf"])
SERIF = find_font(["LiberationSerif-Regular.ttf", "DejaVuSerif.ttf"])
SANS_B = find_font(["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"])
SANS = find_font(["LiberationSans-Regular.ttf", "DejaVuSans.ttf"])


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, lines, x, y, font, fill, leading):
    """Draw lines top-anchored at (x, y); returns the y below the block."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill, anchor="la")
        y += leading
    return y


def story_height(draw, story, width):
    """Height of one grid story without drawing it (badge + kicker +
    headline + deck, same metrics as draw_story)."""
    tw = width - 40
    head = wrap(draw, story["headline"], fnt(SERIF_B, 24), tw)
    deck = wrap(draw, story["deck"], fnt(SERIF, 18), tw)
    return 25 + len(head) * 29 + 3 + len(deck) * 23


def draw_story(draw, story, x, y, width, index):
    """Draw one grid story at (x, y); returns the height it used."""
    top = y
    # Red number badge, kicker to its right.
    draw.ellipse([x, y + 1, x + 28, y + 29], fill=RED)
    draw.text((x + 14, y + 15), str(index + 1), font=fnt(SANS_B, 18),
              fill=WHITE, anchor="mm")
    tx, tw = x + 40, width - 40
    draw.text((tx, y), story["kicker"], font=fnt(SANS_B, 15), fill=RED,
              anchor="la")
    y += 25
    # Bold headline, then grey deck; both measured so rows never overlap.
    y = text_block(draw, wrap(draw, story["headline"], fnt(SERIF_B, 24), tw),
                   tx, y, fnt(SERIF_B, 24), INK, 29)
    y += 3
    y = text_block(draw, wrap(draw, story["deck"], fnt(SERIF, 18), tw),
                   tx, y, fnt(SERIF, 18), GREY, 23)
    return y - top


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "news.json"), encoding="utf-8") as fh:
        news = json.load(fh)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 48
    x0, x1 = mx, W - mx
    inner = x1 - x0

    # --- Masthead -------------------------------------------------------
    d.text((W // 2, 26), news["masthead"], font=fnt(SERIF_B, 92), fill=INK,
           anchor="ma")
    y = 26 + 96
    d.line([(x0, y), (x1, y)], fill=INK, width=3)
    y += 13
    d.text((x0, y), news["dateline_left"], font=fnt(SANS_B, 20), fill=INK,
           anchor="la")
    d.text((x1, y), news["dateline_right"], font=fnt(SANS_B, 20), fill=RED,
           anchor="ra")
    y += 29
    d.line([(x0, y), (x1, y)], fill=RED, width=4)
    y += 24

    # --- Lead story -----------------------------------------------------
    d.text((x0, y), news["lead"]["kicker"], font=fnt(SANS_B, 19), fill=RED,
           anchor="la")
    y += 29
    y = text_block(d, wrap(d, news["lead"]["headline"], fnt(SERIF_B, 44),
                           inner), x0, y, fnt(SERIF_B, 44), INK, 52)
    y += 6
    y = text_block(d, wrap(d, news["lead"]["deck"], fnt(SERIF, 23), inner),
                   x0, y, fnt(SERIF, 23), INK, 30)
    y += 20
    d.line([(x0, y), (x1, y)], fill=INK, width=2)
    y += 22

    # --- Story grid: 2 columns x 3 rows ---------------------------------
    # Measure each story's height first; each row takes the taller side,
    # so text can never run into the row below.
    gutter = 36
    col_w = (inner - gutter) // 2
    footer_top = H - 84
    grid_top = y
    rows = []
    for r in range(3):
        pair = news["stories"][r * 2:(r + 1) * 2]
        rows.append(max(story_height(d, st, col_w) for st in pair))
    total = sum(rows) + 2 * 26  # gaps between rows
    # If the measured grid is shorter than the space, spread the slack
    # evenly as extra row gaps so the grid fills the page nicely.
    slack = max(0, (footer_top - grid_top) - total)
    gap = 26 + slack // 2
    cy = grid_top
    for r in range(3):
        pair = news["stories"][r * 2:(r + 1) * 2]
        for i, story in enumerate(pair):
            cx = x0 + i * (col_w + gutter)
            draw_story(d, story, cx, cy, col_w, r * 2 + i)
        # Vertical hairline between the two columns.
        d.line([(x0 + col_w + gutter // 2, cy + 4),
                (x0 + col_w + gutter // 2, cy + rows[r] - 4)],
               fill=HAIR, width=1)
        cy += rows[r]
        if r < 2:
            d.line([(x0, cy + gap // 2), (x1, cy + gap // 2)],
                   fill=HAIR, width=1)
            cy += gap

    # --- Footer ---------------------------------------------------------
    fy = footer_top
    d.line([(x0, fy), (x1, fy)], fill=INK, width=2)
    fy += 12
    for line in wrap(d, news["footer"], fnt(SANS, 14), inner):
        d.text((W // 2, fy), line, font=fnt(SANS, 14), fill=GREY,
               anchor="ma")
        fy += 19
    fy += 4
    d.text((W // 2, fy), news["credit"], font=fnt(SANS, 14), fill=GREY,
           anchor="ma")

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.environ.get("OUT", os.path.join(here, "entry.png"))
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
