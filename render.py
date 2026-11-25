#!/usr/bin/env python3
"""THE WORLD — Wednesday 25 November 2026: 35 stories, 9 regions.
Stdlib-only newspaper renderer. Draws the whole front page with a tiny
built-in 5x7 bitmap font and vector primitives, then writes entry.png.
No third-party imports: only struct, zlib, random, math, os, sys.
"""
import math
import os
import random
import struct
import sys
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 230)
PAPER2 = (238, 231, 212)
INK = (22, 22, 26)
INK_SOFT = (74, 74, 78)
RED = (176, 32, 32)
BLUE = (30, 70, 130)
NAVY = (16, 30, 62)
NAVY2 = (24, 46, 92)
GOLD = (198, 150, 60)
TEAL = (32, 120, 110)
ORANGE = (210, 110, 40)
GREEN = (46, 140, 70)
SKY = (126, 168, 208)
SKY2 = (198, 214, 232)
SEA = (44, 96, 140)
SEA2 = (26, 66, 104)
SAND = (226, 208, 170)
WHITE = (252, 250, 246)
GREY = (150, 148, 140)
DARK = (30, 30, 34)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows of 5 chars, '#' = on, '.' = off. Uppercase + digits +
# punctuation only; all text is rendered in caps.
FONT = {
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'K': ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'Q': (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    'X': ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    'Y': ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    '0': (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    '2': (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    '3': (".###.", "#...#", "....#", "..##.", "....#", "#...#", ".###."),
    '4': ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    '5': ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '6': (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    '7': ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    '8': (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    '9': (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    '.': (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ',': (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ':': (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ';': (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '?': (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    '-': (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    '+': (".....", "..#..", "..#..", ".###.", "..#..", "..#..", "....."),
    '%': ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.#.#", "#..##"),
    '$': ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    '/': ("....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."),
    '(': ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ')': (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    '&': (".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    '=': (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '*': (".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."),
}

_glyph_cache = {}


def _glyph_stamp(ch, scale, color):
    """Return (width, [(mask_int, stamp_int, nbytes), ...]) for one glyph.

    mask has 0xFF where the glyph is on, 0x00 elsewhere; stamp holds the
    color there. Blitting composites (canvas & ~mask) | stamp so the
    paper behind the glyph survives (off pixels are NOT painted black).
    """
    key = (ch, scale, color)
    hit = _glyph_cache.get(key)
    if hit is not None:
        return hit
    rows = FONT.get(ch, FONT[' '])
    w = 5 * scale
    px = bytes(color)
    on = b'\xff\xff\xff'
    off = b'\x00\x00\x00'
    out_rows = []
    for r in range(7):
        line = rows[r]
        mask_row = bytearray()
        stamp_row = bytearray()
        for c in range(5):
            if line[c] == '#':
                mask_row += on * scale
                stamp_row += px * scale
            else:
                mask_row += off * scale
                stamp_row += off * scale
        m = int.from_bytes(bytes(mask_row), 'big')
        s = int.from_bytes(bytes(stamp_row), 'big')
        out_rows.extend([(m, s, len(mask_row))] * scale)
    stamp = (w, out_rows)
    _glyph_cache[key] = stamp
    return stamp


def text_width(s, scale):
    return len(s) * 6 * scale - scale


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, base):
        self.w = w
        self.h = h
        self.buf = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, base)

    def _off(self, x, y):
        return (y * self.w + x) * 3

    def fill_rect(self, x, y, w, h, color):
        x = max(0, x)
        y = max(0, y)
        w = min(w, self.w - x)
        h = min(h, self.h - y)
        if w <= 0 or h <= 0:
            return
        row = bytes(color) * w
        for yy in range(y, y + h):
            o = self._off(x, yy)
            self.buf[o:o + w * 3] = row

    def set_px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = self._off(x, y)
            self.buf[o:o + 3] = bytes(color)

    def hline(self, x0, x1, y, color, thick=1):
        if x0 > x1:
            x0, x1 = x1, x0
        self.fill_rect(x0, y, x1 - x0 + 1, thick, color)

    def vline(self, x, y0, y1, color, thick=1):
        if y0 > y1:
            y0, y1 = y1, y0
        self.fill_rect(x, y0, thick, y1 - y0 + 1, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.fill_rect(x0 - thick // 2, y0 - thick // 2, thick, thick, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def ring(self, cx, cy, r, color, thick=2):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            dx2 = int(math.sqrt(max(0, (r - thick) * (r - thick) - dy * dy))) if r - thick > 0 else 0
            self.fill_rect(cx - dx, cy + dy, dx - dx2, 1, color)
            self.fill_rect(cx + dx2 + 1, cy + dy, dx - dx2, 1, color)

    def poly(self, pts, color):
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    t = (y - y0) / (y1 - y0) if y1 != y0 else 0
                    xs.append(int(x0 + t * (x1 - x0)))
            if len(xs) >= 2:
                xs.sort()
                self.fill_rect(xs[0], y, xs[-1] - xs[0] + 1, 1, color)

    def grad_rect(self, x, y, w, h, c1, c2, vertical=True, dither=True):
        """Per-row interpolated fill; alternating rows shift by 1 in one
        channel so the PNG stays high-entropy (rich file, paper feel)."""
        for i in range(h if vertical else w):
            t = i / max(1, (h - 1) if vertical else (w - 1))
            c = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
            if dither and i % 2 == 1:
                c = (min(255, c[0] + 1), c[1], max(0, c[2] - 1))
            if vertical:
                self.fill_rect(x, y + i, w, 1, c)
            else:
                self.fill_rect(x + i, y, 1, h, c)

    def speckle(self, x, y, w, h, n, seed, colors, size=2):
        rnd = random.Random(seed)
        for _ in range(n):
            px = x + rnd.randrange(w)
            py = y + rnd.randrange(h)
            c = rnd.choice(colors)
            s = rnd.choice((1, 1, size))
            self.fill_rect(px, py, s, s, c)

    def stipple(self, x, y, w, h, color, step=4, seed=11):
        """Regular faint dot grid — texture that also fattens the PNG."""
        rnd = random.Random(seed)
        for yy in range(y, y + h, step):
            for xx in range(x, x + w, step):
                if rnd.random() < 0.55:
                    self.set_px(xx, yy, color)

    def grain(self, fraction, amp, seed):
        """Deterministic fine paper grain: a fraction of pixels get a small
        random delta in one channel. Subtle to the eye, high entropy to
        the compressor — the file stays rich without looking dirty."""
        rnd = random.Random(seed)
        w, h = self.w, self.h
        buf = self.buf
        n = int(w * h * fraction)
        for _ in range(n):
            x = rnd.randrange(w)
            y = rnd.randrange(h)
            o = (y * w + x) * 3 + rnd.randrange(3)
            v = buf[o] + rnd.randint(-amp, amp)
            buf[o] = 0 if v < 0 else (255 if v > 255 else v)

    # ------------------------------------------------------------ text
    def draw_text(self, s, x, y, scale, color):
        s = s.upper()
        cx = x
        for ch in s:
            w, rows = _glyph_stamp(ch, scale, color)
            x0 = max(0, cx)
            x1 = min(self.w, cx + w)
            if x1 > x0:
                drop_l = (x0 - cx) * 3
                keep = (x1 - x0) * 3
                for i, (mask, stamp, nb) in enumerate(rows):
                    yy = y + i
                    if 0 <= yy < self.h:
                        o = self._off(x0, yy)
                        cur = int.from_bytes(
                            self.buf[o:o + keep], 'big')
                        m = int.from_bytes(
                            mask.to_bytes(nb, 'big')[drop_l:drop_l + keep],
                            'big')
                        st = int.from_bytes(
                            stamp.to_bytes(nb, 'big')[drop_l:drop_l + keep],
                            'big')
                        new = (cur & ~m) | st
                        self.buf[o:o + keep] = new.to_bytes(keep, 'big')
            cx += 6 * scale
        return cx

    def draw_text_center(self, s, cx, y, scale, color):
        w = text_width(s, scale)
        return self.draw_text(s, cx - w // 2, y, scale, color)

    def draw_text_right(self, s, x, y, scale, color):
        w = text_width(s, scale)
        return self.draw_text(s, x - w, y, scale, color)

    def draw_wrapped(self, s, x, y, max_w, scale, color, line_h=None):
        if line_h is None:
            line_h = 7 * scale + 3
        words = s.upper().split(' ')
        lines = []
        cur = ''
        for wd in words:
            trial = (cur + ' ' + wd).strip()
            if text_width(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        yy = y
        for ln in lines:
            self.draw_text(ln, x, yy, scale, color)
            yy += line_h
        return yy


# ---------------------------------------------------------------- PNG out
def write_png(cv, path):
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)
        raw += cv.buf[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 6)

    def chunk(typ, data):
        c = struct.pack('>I', len(data)) + typ + data
        c += struct.pack('>I', zlib.crc32(typ + data) & 0xffffffff)
        return c

    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', comp)
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)

# ---------------------------------------------------------------- scenes
def draw_map(cv, x, y, w, h):
    cv.grad_rect(x, y, w, h, SEA, SEA2, vertical=True)
    # faint latitude lines
    for i in range(1, 4):
        yy = y + i * h // 4
        cv.hline(x, x + w - 1, yy, (90, 140, 180), 1)
    land = SAND
    dark = (196, 172, 128)
    # schematic continents (stylised blobs, newspaper-map style)
    cv.poly([(x + 40, y + 22), (x + 150, y + 14), (x + 168, y + 44),
             (x + 130, y + 78), (x + 70, y + 76), (x + 36, y + 52)], land)
    cv.poly([(x + 205, y + 58), (x + 248, y + 56), (x + 244, y + 96),
             (x + 214, y + 100), (x + 200, y + 78)], land)
    cv.poly([(x + 448, y + 12), (x + 498, y + 10), (x + 500, y + 34),
             (x + 462, y + 40), (x + 444, y + 26)], land)
    cv.poly([(x + 462, y + 44), (x + 522, y + 42), (x + 516, y + 92),
             (x + 478, y + 96), (x + 458, y + 66)], land)
    cv.poly([(x + 540, y + 8), (x + 760, y + 6), (x + 800, y + 36),
             (x + 720, y + 76), (x + 600, y + 66), (x + 546, y + 40)], land)
    cv.poly([(x + 800, y + 74), (x + 862, y + 72), (x + 856, y + 94),
             (x + 806, y + 96)], land)
    cv.speckle(x, y, w, h, 260, 42, [dark, (210, 190, 150), (120, 160, 190)], 2)
    marks = [
        (120, 52, "NVIDIA", 12, -4), (492, 26, "POLAND", 12, -4),
        (640, 52, "HORMUZ", 12, -4), (540, 52, "GAZA", -40, 8),
        (668, 62, "INDIA", 12, -4), (462, 20, "UK", 12, -4),
        (700, 48, "NEPAL", 12, -4),
    ]
    for mx, my, lab, dx, dy in marks:
        cv.circle(x + mx, y + my, 4, RED)
        cv.ring(x + mx, y + my, 7, RED, 1)
        cv.draw_text(lab, x + mx + dx, y + my + dy, 1, INK)
    cv.draw_text("WORLD MAP - WHERE THE NEWS HAPPENED", x + 4, y + h - 11, 1, WHITE)


def draw_chart_scene(cv, x, y, w, h):
    cv.grad_rect(x, y, w, h, NAVY, NAVY2, vertical=True)
    # grid lines
    for i in range(1, 5):
        yy = y + i * h // 5
        cv.hline(x, x + w - 1, yy, (52, 74, 120), 1)
    pts = [(x + 20, y + h - 40), (x + 90, y + h - 52), (x + 160, y + h - 44),
           (x + 230, y + h - 86), (x + 300, y + h - 104), (x + 370, y + h - 150),
           (x + 440, y + h - 168), (x + w - 24, y + 30)]
    # area under the line
    area = pts + [(x + w - 24, y + h - 16), (x + 20, y + h - 16)]
    cv.poly(area, (30, 90, 60))
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], GREEN, 3)
    for px, py in pts:
        cv.circle(px, py, 3, GOLD)
    # chip at lower left
    cx, cy = x + 26, y + h - 78
    cv.fill_rect(cx, cy, 74, 52, (20, 20, 26))
    cv.fill_rect(cx + 6, cy + 6, 62, 40, (44, 64, 110))
    for k in range(5):
        cv.fill_rect(cx - 6, cy + 10 + k * 9, 6, 3, GOLD)
        cv.fill_rect(cx + 74, cy + 10 + k * 9, 6, 3, GOLD)
    cv.draw_text("NVDA", cx + 14, cy + 18, 2, WHITE)
    cv.speckle(x, y, w, h, 200, 7, [(70, 100, 150), (120, 150, 200)], 2)


def draw_jet_scene(cv, x, y, w, h):
    cv.grad_rect(x, y, w, h, (232, 140, 60), (30, 40, 90), vertical=True)
    cv.circle(x + w - 70, y + 26, 16, (250, 220, 160))
    # jet silhouette
    cv.poly([(x + 60, y + 60), (x + 190, y + 46), (x + 230, y + 58),
             (x + 190, y + 66), (x + 120, y + 78), (x + 90, y + 88),
             (x + 70, y + 72)], INK)
    cv.poly([(x + 110, y + 60), (x + 130, y + 34), (x + 142, y + 60)], INK)
    # missile trails
    for i, ty in enumerate((y + 20, y + 44, y + 68)):
        cv.line(x + 250, ty, x + w - 30, ty + 12, WHITE, 2)
        cv.circle(x + w - 26, ty + 12, 3, RED)
    # radar arcs
    for r in (18, 30, 42):
        cv.ring(x + 40, y + h - 20, r, (200, 220, 240), 2)
    cv.speckle(x, y, w, h, 120, 9, [(240, 180, 120), (90, 110, 150)], 2)


def draw_sea_scene(cv, x, y, w, h):
    cv.grad_rect(x, y, w, h, SKY2, SEA, vertical=True)
    # waves
    for i in range(4):
        yy = y + h - 18 - i * 12
        for xx in range(x + 6, x + w - 6, 26):
            cv.line(xx, yy, xx + 13, yy - 3, (200, 225, 240), 2)
    # three tankers
    for ti, tx in enumerate((x + 16, x + w // 2 - 60, x + w - 150)):
        ty = y + h - 58 + ti * 6
        cv.poly([(tx, ty), (tx + 128, ty), (tx + 118, ty + 22),
                 (tx + 10, ty + 22)], (40, 40, 46))
        cv.fill_rect(tx + 14, ty - 16, 52, 16, (150, 60, 50))
        cv.fill_rect(tx + 72, ty - 16, 30, 16, (60, 110, 70))
        cv.fill_rect(tx + 106, ty - 26, 8, 26, (90, 90, 96))
        cv.circle(tx + 108, ty - 30, 3, ORANGE)
    # mines with spikes
    for mx, my in ((x + 60, y + 34), (x + w - 90, y + 26), (x + w // 2, y + 18)):
        cv.circle(mx, my, 7, INK)
        for a in range(0, 360, 45):
            ex = mx + int(11 * math.cos(math.radians(a)))
            ey = my + int(11 * math.sin(math.radians(a)))
            cv.line(mx, my, ex, ey, INK, 2)
    cv.speckle(x, y, w, h, 140, 13, [(180, 210, 230), (30, 70, 110)], 2)


def mini_scene(cv, kind, x, y, w, h):
    cv.grad_rect(x, y, w, h, SKY2, (214, 226, 238), vertical=True)
    if kind == 'tariff':
        cv.fill_rect(x + 14, y + h - 22, 40, 22, (120, 90, 60))
        cv.fill_rect(x + 14, y + h - 26, 40, 4, (90, 64, 40))
        cv.line(x + 70, y + h - 8, x + 70, y + 8, RED, 3)
        cv.poly([(x + 58, y + 16), (x + 70, y + 4), (x + 82, y + 16)], RED)
    elif kind == 'down':
        pts = [(x + 8, y + 10), (x + 30, y + 18), (x + 52, y + 14),
               (x + 74, y + 30), (x + w - 10, y + h - 10)]
        for i in range(len(pts) - 1):
            cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], RED, 3)
        cv.draw_text("$83", x + w - 34, y + 4, 1, RED)
    elif kind == 'chip':
        cv.fill_rect(x + w // 2 - 20, y + 6, 40, 30, INK)
        cv.fill_rect(x + w // 2 - 12, y + 13, 24, 16, (44, 64, 110))
        for k in range(4):
            cv.fill_rect(x + w // 2 - 26, y + 10 + k * 7, 6, 3, GOLD)
            cv.fill_rect(x + w // 2 + 20, y + 10 + k * 7, 6, 3, GOLD)
    elif kind == 'gaza':
        cv.fill_rect(x + 12, y + 12, 30, h - 12, (110, 104, 96))
        cv.fill_rect(x + 48, y + 20, 24, h - 20, (140, 134, 124))
        for i in range(3):
            cv.circle(x + 60 + i * 8, y + 8 - i * 2, 5, (180, 180, 180))
        cv.fill_rect(x + 12, y + h - 4, 70, 4, INK)
    elif kind == 'climate':
        cv.circle(x + w // 2, y + h // 2, 16, TEAL)
        cv.poly([(x + w // 2 - 4, y + 6), (x + w // 2 + 6, y + 18),
                 (x + w // 2 - 2, y + 26), (x + w // 2 + 8, y + h - 6),
                 (x + w // 2 - 8, y + h - 6)], (20, 60, 54))
        cv.line(x + 10, y + 4, x + w - 10, y + h - 4, RED, 2)
    elif kind == 'gta':
        for i, bh in enumerate((26, 34, 22, 30)):
            bx = x + 10 + i * 18
            cv.fill_rect(bx, y + h - bh, 14, bh, (60, 70, 96))
            cv.fill_rect(bx + 3, y + h - bh + 4, 3, 3, GOLD)
            cv.fill_rect(bx + 8, y + h - bh + 9, 3, 3, GOLD)
        cv.fill_rect(x + w - 34, y + 6, 26, 14, RED)
        cv.draw_text("VI", x + w - 28, y + 9, 1, WHITE)
    elif kind == 'ballot':
        cv.fill_rect(x + w // 2 - 18, y + 14, 36, 22, (150, 120, 70))
        cv.fill_rect(x + w // 2 - 18, y + 10, 36, 5, (120, 94, 52))
        cv.line(x + w // 2 - 8, y + 4, x + w // 2 + 2, y + 12, RED, 2)
        cv.line(x + w // 2 + 2, y + 12, x + w // 2 + 14, y - 2, RED, 2)
    elif kind == 'mountain':
        cv.poly([(x + 4, y + h - 4), (x + 30, y + 8), (x + 56, y + h - 4)], (90, 100, 120))
        cv.poly([(x + 40, y + h - 4), (x + 66, y + 16), (x + 92, y + h - 4)], (120, 130, 150))
        cv.poly([(x + 24, y + 8), (x + 30, y + 14), (x + 36, y + 8),
                 (x + 30, y + 4)], WHITE)
        cv.line(x + 8, y + h - 6, x + w - 8, y + h - 6, INK, 2)
    elif kind == 'derrick':
        cv.poly([(x + w // 2 - 14, y + h - 4), (x + w // 2 - 4, y + 6),
                 (x + w // 2 + 8, y + 6), (x + w // 2 + 16, y + h - 4)], (60, 60, 66))
        cv.line(x + w // 2 - 4, y + 6, x + w // 2 + 14, y + h - 4, INK, 2)
        cv.circle(x + w // 2 + 22, y + 12, 6, INK)
        cv.fill_rect(x + w // 2 + 20, y + 18, 4, 10, INK)
    elif kind == 'mic':
        cv.circle(x + w // 2, y + 14, 9, (90, 90, 96))
        cv.fill_rect(x + w // 2 - 2, y + 22, 4, 12, INK)
        cv.fill_rect(x + w // 2 - 8, y + 34, 16, 3, INK)
        cv.line(x + 8, y + 8, x + w - 8, y + 8, RED, 2)
        cv.line(x + 8, y + h - 6, x + w - 8, y + h - 6, RED, 2)


# ---------------------------------------------------------------- layout
GRID = [
    ('tariff', "TRUMP TARIFF WAVE", "NEW IMPORT DUTIES", "25 NOV"),
    ('down', "ANTHROPIC SLIDES", "BELOW $83 IPO", "25 NOV"),
    ('chip', "HUAWEI GUILTY", "TRADE SECRETS", "25 NOV"),
    ('gaza', "GAZA CRISIS DEEPENS", "UN WARNS", "25 NOV"),
    ('climate', "CLIMATE TALKS FAIL", "COP31 NO DEAL", "25 NOV"),
    ('gta', "GTA 6 OUT NOW", "19 NOV LAUNCH", "19 NOV"),
    ('ballot', "BJP-SAD REUNITE", "PUNJAB 2027", "25 NOV"),
    ('mountain', "NEPAL QUAKE 5.6", "KOSHI SHAKEN", "25 NOV"),
    ('derrick', "IRAQ OIL STANDOFF", "KURD FIELDS", "25 NOV"),
    ('mic', "SINGER FLOGGED", "74 LASHES", "25 NOV"),
]

RAIL_LEFT = [
    "14. GIULIANI GETS MEDAL OF FREEDOM - 25 NOV",
    "15. TWO HELD OVER WILLIAM HOME BREAK-IN - 25 NOV",
    "16. DENMARK KEEPS GHETTO EVICTIONS - 25 NOV",
    "17. ISRAEL ARMY SUICIDES HIT 16-YEAR HIGH - 25 NOV",
    "18. SAUDI-LED BLOC CONDEMNS RIYADH BLAST, HOUTHIS REPORT DEAD - 25 NOV",
    "19. ZIMBABWE MAN JAILED OVER UKRAINE FIGHT - 25 NOV",
    "20. US CONSUMER CONFIDENCE IN FOCUS - 25 NOV",
    "21. SENSEX -1484, NIFTY UNDER 25400 - 25 NOV",
    "22. ENGLAND BEAT AUSTRALIA IN 2ND T20I - 25 NOV",
    "23. SOORYAVANSHI FASTEST LIST-A DOUBLE TON - 25 NOV",
    "24. NZ HOLD INDIA TO DRAW IN 1ST TEST - 25 NOV",
]
RAIL_RIGHT = [
    "25. PRIYANSH ARYA 181, 2ND-BEST T20 SCORE - 25 NOV",
    "26. VERA RUBIN FIRST IMAGES AMAZE - 25 NOV",
    "27. ASTEROID ECLIPSE: DIDYMOS-DIMORPHOS - 25 NOV",
    "28. IMPOSSIBLE STAR SYSTEM 28 LY AWAY - 25 NOV",
    "29. 12 ACROPORA CORALS REVIVED ON REEF - 25 NOV",
    "30. DAY AGAINST VIOLENCE ON WOMEN - 25 NOV",
    "31. 12000 EVACUATED AT UK CONCERT - 25 NOV",
    "32. MODI-MERZ TALK STRATEGIC TIES - 25 NOV",
    "33. INDIA SPACE ECONOMY TO $40-45B - 25 NOV",
    "34. US-QATAR STRATEGIC TALKS - 25 NOV",
    "35. TAIEX +8.99%, SANOFI $41B DEAL - 25 NOV",
]


def build():
    cv = Canvas(W, H, PAPER)
    # paper grain: full-canvas vertical gradient + faint stipple
    cv.grad_rect(0, 0, W, H, PAPER, PAPER2, vertical=True, dither=True)
    cv.stipple(0, 0, W, H, (226, 218, 196), step=5, seed=21)

    # ---- masthead
    cv.draw_text("THE WORLD", 24, 12, 6, INK)
    cv.draw_text("WEDNESDAY 25 NOVEMBER 2026", 24, 62, 2, INK_SOFT)
    cv.draw_text_right("35 STORIES", 1000, 14, 3, RED)
    cv.draw_text_right("9 REGIONS", 1000, 44, 3, INK)
    cv.draw_text_right("CHECKED 25 NOV 2026", 1000, 74, 2, INK_SOFT)
    cv.hline(24, 1000, 94, INK, 3)
    cv.hline(24, 1000, 99, INK, 1)
    # ---- stats strip
    cv.draw_text_center(
        "35 DATED STORIES - 9 REGIONS - WORLD MAP - DATE-CHECKED - SOURCES: NEWS WIRES",
        512, 106, 2, INK_SOFT)
    cv.hline(24, 1000, 124, INK, 1)

    # ---- world map band
    draw_map(cv, 24, 130, 976, 104)

    # ---- hero 1: NVIDIA
    hx, hy, hw, hh = 24, 242, 976, 206
    cv.fill_rect(hx, hy, hw, hh, NAVY)
    draw_chart_scene(cv, hx + 8, hy + 8, 520, hh - 16)
    cv.fill_rect(hx + 536, hy, 2, hh, GOLD)
    tx = hx + 552
    cv.draw_text("HUANG IS BACK", tx, hy + 12, 4, WHITE)
    cv.draw_text("+31.5%", tx, hy + 52, 5, GOLD)
    cv.draw_text("+$952B IN ONE DAY", tx + 220, hy + 62, 2, WHITE)
    cv.draw_wrapped(
        "HUANG BACK AS CEO 23 NOV AFTER 12 NOV EXIT. STOCK BEST DAY "
        "SINCE 2003. STILL -32% FROM OCT PEAK. TESTIFIES TO CONGRESS "
        "IN DEC.", tx, hy + 108, 420, 2, (226, 230, 240))
    cv.draw_text("23 NOV 2026 - CHECKED", tx, hy + hh - 22, 1, GOLD)
    cv.draw_text("MARKETS", hx + 12, hy + 12, 1, (160, 180, 210))

    # ---- heroes 2 and 3
    # hero 2: Poland
    x2, y2, w2, h2 = 24, 456, 484, 176
    cv.fill_rect(x2, y2, w2, h2, WHITE)
    cv.fill_rect(x2, y2, w2, 2, RED)
    draw_jet_scene(cv, x2 + 6, y2 + 6, w2 - 12, 92)
    cv.draw_text("MISSILES OVER POLAND", x2 + 10, y2 + 104, 3, INK)
    cv.draw_wrapped(
        "3 RUSSIAN MISSILES HIT POLAND 25 NOV. NATO JETS SCRAMBLED.",
        x2 + 10, y2 + 128, w2 - 20, 2, INK_SOFT)
    cv.draw_text("25 NOV 2026 - CHECKED", x2 + 10, y2 + h2 - 12, 1, RED)
    # hero 3: Hormuz
    x3 = 516
    cv.fill_rect(x3, y2, w2, h2, WHITE)
    cv.fill_rect(x3, y2, w2, 2, RED)
    draw_sea_scene(cv, x3 + 6, y2 + 6, w2 - 12, 92)
    cv.draw_text("MINES IN THE STRAIT", x3 + 10, y2 + 104, 3, INK)
    cv.draw_wrapped(
        "3 TANKERS HIT MINES IN HORMUZ. SHIPPING FEARS GROW, OIL ON "
        "EDGE.", x3 + 10, y2 + 128, w2 - 20, 2, INK_SOFT)
    cv.draw_text("25 NOV 2026 - CHECKED", x3 + 10, y2 + h2 - 12, 1, RED)

    # ---- grid 10
    gy = 640
    cw, ch, gap = 191, 92, 5
    for i, (kind, head, sub, date) in enumerate(GRID):
        gx = 24 + (i % 5) * (cw + gap)
        gyy = gy + (i // 5) * (ch + 8)
        cv.fill_rect(gx, gyy, cw, ch, WHITE)
        cv.fill_rect(gx, gyy, cw, 2, BLUE)
        mini_scene(cv, kind, gx + 4, gyy + 4, cw - 8, 38)
        cv.draw_wrapped(head, gx + 6, gyy + 46, cw - 12, 2, INK, line_h=16)
        cv.draw_text(sub + " - " + date, gx + 6, gyy + 82, 1, INK_SOFT)

    # ---- rail 22
    ry = 844
    cv.hline(24, 1000, ry - 6, INK, 2)
    cv.draw_text("THE REST OF THE DAY", 24, ry, 2, RED)
    yy = ry + 20
    for i, item in enumerate(RAIL_LEFT):
        cv.draw_text(item, 24, yy + i * 12, 1, INK)
    for i, item in enumerate(RAIL_RIGHT):
        cv.draw_text(item, 524, yy + i * 12, 1, INK)

    # ---- footer
    cv.hline(24, 1000, 998, INK, 2)
    cv.draw_text_center(
        "THE WORLD - WEDNESDAY 25 NOVEMBER 2026 - CHECKED 25 NOV 2026 - "
        "35 STORIES, 9 REGIONS", 512, 1006, 1, INK_SOFT)

    # final paper grain over the whole page (light, deterministic)
    cv.speckle(0, 0, W, H, 2600, 99, [(232, 224, 204), (255, 250, 238)], 1)
    cv.grain(0.10, 6, 20261125)
    return cv


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    cv = build()
    n = write_png(cv, out)
    print("wrote", out, n, "bytes")


if __name__ == "__main__":
    main()
