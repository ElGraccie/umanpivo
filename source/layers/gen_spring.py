"""Spring theme (1 March - 31 May): blossoming orchard in soft morning light. Generates SVG art and bakes every layer to WebP.
Same frames and file names as the other themes, so the hero CSS needs no changes."""
import random, math, sys, os
from bakelib import browser, shot, save
from art import f, f1, bez, circ, stops, rgba, leafp

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 't', 'spring'))
R = random.Random(315)
W, H = 1600, 520
SUNX = 960

FAR = [('0', '#c4dbd9'), ('.35', '#a3c2b6'), ('1', '#7fa38d')]                 # far green hills in the daylight haze
MID = [('0', '#f4dce6'), ('.08', '#b9c98e'), ('.3', '#5f8a4c'), ('1', '#22381f')]   # sunlit orchard, green shade below
GREENS = ['#6f9a4e', '#86ad57', '#5c8642', '#9cbc63', '#4f7a3c']
PINKS = ['#f6c4d4', '#f9d7e2', '#efa9c0', '#fbe6ee', '#ffffff', '#e894b0']
BR = '#4a3026'          # bark
LEAF = ['#7fb04f', '#93c25a', '#6a9a44', '#a9cf6c']

defs = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        '<filter id="rag" x="-4%" y="-12%" width="108%" height="124%"><feTurbulence type="fractalNoise" baseFrequency="0.014 0.03" numOctaves="4" seed="8" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="12" xChannelSelector="R" yChannelSelector="G"/></filter>'
        '<linearGradient id="gfar" gradientUnits="userSpaceOnUse" x1="0" y1="230" x2="0" y2="520">' + stops(FAR) + '</linearGradient>'
        '<linearGradient id="gmid" gradientUnits="userSpaceOnUse" x1="0" y1="170" x2="0" y2="520">' + stops(MID) + '</linearGradient>'
        '</defs></svg>')


def canopy(base, amp, step, rmin, rmax, ph, gap=0, pal=None, pal_p=0):
    out = []; x = -60
    while x < W + 60:
        t = base + amp * (math.sin(x / 260 + ph) * .55 + math.sin(x / 97 + ph * 2) * .3 + math.sin(x / 41 + ph * 3) * .25)
        t += gap * math.exp(-((x - SUNX) / 250) ** 2)
        r = R.uniform(rmin, rmax)
        pk = lambda: (R.choice(pal) if pal and R.random() < pal_p else None)
        out.append(circ(x, t + r * .55, r, pk()))
        out.append(circ(x + step / 2, t + r * .95, r * .9, pk()))
        for _ in range(3):
            out.append(circ(x + R.uniform(-step, step), t + R.uniform(-4, r * .5), R.uniform(5, 12), pk()))
        x += step
    out.append('<rect x="-60" y="%s" width="%d" height="%d"/>' % (f(base + amp + 40), W + 120, H))
    return ''.join(out)


def land(inner, gid):
    return '<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMax slice" fill="url(#%s)"><g filter="url(#rag)">%s</g></svg>' % (W, H, gid, inner)


far = land(canopy(292, 26, 24, 30, 52, .6, gap=30), 'gfar')
# blossoming trees in the orchard: pink and white crowns among green ones
def crowns():
    """blossoming tree crowns standing out of the green orchard: soft clusters of pink and white"""
    out = []; x = -20
    cols = ['#f4c9d8', '#f9dde6', '#fdf0f4', '#eab0c4', '#f7d2de']
    while x < W + 40:
        base = 245 + 38 * (math.sin(x / 260 + 2.1) * .55 + math.sin(x / 97 + 4.2) * .3) + 60 * math.exp(-((x - SUNX) / 250) ** 2)
        rx, ry = R.uniform(46, 78), R.uniform(30, 46)
        cy = base - ry * .2
        for _ in range(26):
            a = R.uniform(0, 6.283); d = math.sqrt(R.random())
            out.append(circ(x + math.cos(a) * rx * d, cy + math.sin(a) * ry * d, R.uniform(9, 20), R.choice(cols)))
        x += R.uniform(110, 190)
    return ''.join(out)


mid = land(canopy(245, 38, 19, 34, 66, 2.1, gap=60) + crowns(), 'gmid')


# ---------------- blossom
def blossom(x, y, r, rot, col, op=1, center=True):
    o = '<g transform="translate(%s %s) rotate(%s)" opacity="%s">' % (f1(x), f1(y), f1(rot), op)
    for k in range(5):
        o += '<ellipse cx="0" cy="%s" rx="%s" ry="%s" transform="rotate(%d)" fill="%s"/>' % (f1(-r * .52), f1(r * .42), f1(r * .55), k * 72, col)
    if center:
        o += '<circle r="%s" fill="#f7d36a"/>' % f1(r * .2)
        for k in range(6):
            a = math.radians(k * 60 + 15)
            o += '<circle cx="%s" cy="%s" r="%s" fill="#c4572c"/>' % (f1(math.cos(a) * r * .3), f1(math.sin(a) * r * .3), f1(max(.6, r * .06)))
    return o + '</g>'


def bud(x, y, r, rot):
    return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(%s %s %s)" fill="#e47fa2"/>' % (f1(x), f1(y), f1(r * .45), f1(r * .7), f1(rot), f1(x), f1(y))


def petal(x, y, s, rot, col, op=1):
    return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(%s %s %s)" fill="%s" opacity="%s"/>' % (f1(x), f1(y), f1(s), f1(s * .62), f1(rot), f1(x), f1(y), col, op)


# ---------------- foreground: soft blossom clouds at the top (fga) and thin flowering twigs (fgb)
CW, CH = 1600, 900


def bloom_cloud(cx, cy, rx, ry, n, sz):
    o = ['<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#e7a9be"/>' % (f(cx), f(cy), f(rx * .8), f(ry * .78))]
    for _ in range(n):
        a = R.uniform(0, 6.283); d = math.sqrt(R.random()) ** .7
        x, y = cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d
        if R.random() < .22:
            o.append(petal(x, y, sz * R.uniform(.7, 1.1), R.uniform(0, 180), R.choice(GREENS)))
        else:
            o.append(blossom(x, y, sz * R.uniform(.7, 1.2), R.uniform(0, 72), R.choice(PINKS), center=False))
    return ''.join(o)


def twig(p0, p1, p2, p3, w):
    o = '<path d="M%s %s C%s %s %s %s %s %s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (
        f(p0[0]), f(p0[1]), f(p1[0]), f(p1[1]), f(p2[0]), f(p2[1]), f(p3[0]), f(p3[1]), BR, f(w))
    for i in range(1, 15):
        t = i / 14; x, y = bez(p0, p1, p2, p3, t)
        for _ in range(4):
            if R.random() < .25:
                o += petal(x + R.uniform(-22, 22), y + R.uniform(-16, 20), R.uniform(8, 13), R.uniform(0, 180), R.choice(LEAF))
            else:
                o += blossom(x + R.uniform(-24, 24), y + R.uniform(-18, 22), R.uniform(9, 15), R.uniform(0, 72), R.choice(PINKS))
    return o


fgA = ('<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice">' % (CW, CH)
       + bloom_cloud(30, 20, 400, 150, 420, 22) + bloom_cloud(210, 150, 150, 80, 90, 18) + bloom_cloud(1590, 20, 430, 180, 460, 22)
       + bloom_cloud(1470, 200, 190, 100, 110, 18) + bloom_cloud(700, -30, 170, 60, 80, 18) + bloom_cloud(1160, -20, 170, 64, 84, 18) + '</svg>')
fgB = ('<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice">' % (CW, CH)
       + twig((360, 70), (560, 40), (760, 140), (900, 290), 9) + twig((1260, 60), (1170, 90), (1050, 170), (960, 300), 8)
       + twig((1560, 330), (1420, 330), (1260, 360), (1130, 400), 7) + '</svg>')


# ---------------- bokeh: sunlit petals out of focus (frame 1600x810)
def bokeh():
    o = []
    cols = ['#ffffff', '#ffe3ec', '#f7c2d4', '#fff1c8', '#dff0c0']
    for i in range(30):
        col = R.choice(cols)
        x = R.uniform(42, 98) if R.random() < .6 else R.uniform(3, 60)
        y = R.uniform(70, 640)
        sz = R.choice([14, 18, 24, 30, 38, 46, 56]) * R.uniform(.9, 1.15)
        bg = 'radial-gradient(circle,%s 0,%s 60%%,%s 86%%,%s 100%%)' % (rgba(col, .2), rgba(col, .28), rgba(col, .55), rgba(col, 0))
        o.append('<i style="position:absolute;left:%.0fpx;top:%.0fpx;width:%.0fpx;height:%.0fpx;border-radius:50%%;opacity:%.2f;background:%s;filter:blur(.8px)"></i>' % (
            x / 100 * 1600 - sz / 2, y, sz, sz, R.uniform(.4, .9), bg))
    return '<div style="position:relative;width:1600px;height:810px">' + ''.join(o) + '</div>'


# ---------------- table: light oak in morning sun, a few fallen petals
def table():
    TW, TH = 1600, 190
    hs = [12 * 1.2 ** i for i in range(8)]; s = sum(hs); hs = [h * TH / s for h in hs]
    y = 0; pl = []
    cols = ['#a9794a', '#9c6c40', '#b38452', '#a27348', '#94653b', '#ad7d4d', '#9a6a3f', '#b98a58']
    for i, h in enumerate(hs):
        pl.append('<rect x="0" y="%.1f" width="%d" height="%.1f" fill="%s"/>' % (y, TW, h, cols[(i * 3 + 1) % len(cols)]))
        jx = R.uniform(150, TW - 150)
        for jj in (jx, (jx + R.uniform(500, 900)) % TW):
            pl.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#3a2010" opacity=".45"/>' % (jj, y, 1.1 + i * .2, h))
        pl.append('<rect x="0" y="%.1f" width="%d" height="%.1f" fill="#2a160a" opacity=".6"/>' % (y + h - 1.4 - i * .25, TW, 1.4 + i * .25))
        pl.append('<rect x="0" y="%.1f" width="%d" height="1" fill="#fff0d8" opacity=".2"/>' % (y, TW))
        y += h
    pet = ''.join(petal(R.uniform(20, 1580), R.uniform(10, 180), R.uniform(4, 8), R.uniform(0, 180), R.choice(['#fbe0e9', '#f4c3d3', '#ffffff']), R.uniform(.7, .95)) for _ in range(46))
    return ('<svg style="position:absolute;inset:0;width:100%%;height:100%%;display:block" viewBox="0 0 %d %d" preserveAspectRatio="none"><defs>'
            '<filter id="wg" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency="0.0018 0.2" numOctaves="5" seed="5"/><feColorMatrix type="matrix" values="0 0 0 0 .16  0 0 0 0 .08  0 0 0 0 .03  2.1 0 0 0 -.72"/></filter>'
            '<filter id="wg2" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency="0.0026 0.11" numOctaves="4" seed="17"/><feColorMatrix type="matrix" values="0 0 0 0 .95  0 0 0 0 .8  0 0 0 0 .6  1.6 0 0 0 -.78"/></filter>'
            '<linearGradient id="tsh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2dc" stop-opacity=".4"/><stop offset=".4" stop-color="#ffd8b0" stop-opacity=".1"/><stop offset="1" stop-color="#2a1608" stop-opacity=".72"/></linearGradient></defs>'
            '%s<rect width="%d" height="%d" filter="url(#wg)" opacity=".9"/><rect width="%d" height="%d" filter="url(#wg2)" opacity=".4"/><rect width="%d" height="%d" fill="url(#tsh)"/>%s</svg>') % (
        TW, TH, ''.join(pl), TW, TH, TW, TH, TW, TH, pet)


TB = ('radial-gradient(ellipse 160px 100% at 60% 0,rgba(255,244,220,.36),transparent 72%),radial-gradient(ellipse 220px 16px at 74% 40%,rgba(255,214,226,.24),transparent 72%),'
      'radial-gradient(ellipse 160px 14px at 52% 24%,rgba(255,236,200,.22),transparent 72%)')


# ---------------- dappled shadow of the blossoming branch on the table
def tshade():
    sh = []
    for _ in range(60):
        sh.append(blossom(R.uniform(0, 640), R.uniform(-10, 190), R.uniform(9, 18), R.uniform(0, 72), '#2a1408', R.uniform(.3, .5), center=False))
    sh.append('<path d="M700 -10C560 40 380 70 120 80" stroke="#2a1408" stroke-opacity=".38" stroke-width="18" fill="none" stroke-linecap="round"/>')
    return '<svg viewBox="0 0 640 190" preserveAspectRatio="xMaxYMid slice" style="display:block;width:640px;height:190px;filter:blur(3.5px)">@@</svg>'.replace('@@', ''.join(sh))


# ---------------- the blossoming branch over the table (frame 980x215)
BW, BH = 980, 215


def branch():
    rr = random.Random(41)
    P = [(1040, 95), (790, 78), (480, 125), (130, 140)]
    N = 40; left = []; right = []
    for i in range(N + 1):
        t = i / N; x, y = bez(*P, t)
        x2, y2 = bez(*P, min(1, t + .01)); x1, y1 = bez(*P, max(0, t - .01))
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = max(1.2, 11 * (1 - t) ** 1.15 + 1.4)
        left.append((x + nx * w, y + ny * w)); right.append((x - nx * w, y - ny * w))
    poly = left + right[::-1]
    out = ['<path d="M' + ' L'.join('%s %s' % (f1(a), f1(b)) for a, b in poly) + ' Z" fill="%s"/>' % BR]
    out.append('<path d="M' + ' L'.join('%s %s' % (f1(a), f1(b)) for a, b in (right if right[0][1] < left[0][1] else left)) + '" stroke="#e8c2a8" stroke-opacity=".45" stroke-width="2" fill="none"/>')
    tips = []
    for t in (.12, .26, .4, .54, .68, .8, .9):
        x, y = bez(*P, t); dirn = rr.choice([-1, 1]); ln = rr.uniform(45, 95) * (1 - t * .45)
        ex = x - ln; ey = y + dirn * rr.uniform(22, 54)
        out.append('<path d="M%s %s Q%s %s %s %s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (
            f1(x), f1(y), f1((x + ex) / 2), f1((y + ey) / 2 - 12), f1(ex), f1(ey), BR, f1(max(1.8, 7 * (1 - t) + 1.4))))
        tips.append((ex, ey, t))
    ex0, ey0 = bez(*P, 1.0)
    for k, (ang, ln) in enumerate([(-24, 64), (8, 86), (32, 58)]):
        a = math.radians(180 + ang); ex = ex0 + math.cos(a) * ln; ey = ey0 + math.sin(a) * ln * .9
        out.append('<path d="M%s %s Q%s %s %s %s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (
            f1(ex0), f1(ey0), f1((ex0 + ex) / 2), f1((ey0 + ey) / 2 - 6), f1(ex), f1(ey), BR, f1(2.2 - k * .3)))
        tips.append((ex, ey, 1.0))
    flowers = []
    def cluster(x, y, n, scale):
        for _ in range(n):
            r = rr.uniform(9, 15) * scale
            px, py = x + rr.uniform(-30, 26), y + rr.uniform(-24, 22)
            c = rr.random()
            if c < .16:
                out.append(leafp(px, py, rr.uniform(0, 360), rr.uniform(.34, .5) * scale, rr.choice(LEAF)))
            elif c < .26:
                flowers.append(bud(px, py, r, rr.uniform(-40, 40)))
            else:
                flowers.append(blossom(px, py, r, rr.uniform(0, 72), rr.choice(['#fde8ef', '#f9d3df', '#ffffff', '#f4bccd', '#fbe0e8'])))
    for i in range(0, 46):
        t = i / 45; x, y = bez(*P, t)
        cluster(x, y - 4, 2 if t < .7 else 1, 1 - t * .3)
    for ex, ey, t in tips:
        cluster(ex, ey, max(3, int(9 * (1 - t * .6))), 1 - t * .25)
    dd = ('<defs><radialGradient id="pg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#f3b7ca"/></radialGradient></defs>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" style="position:absolute;inset:0;overflow:hidden">%s%s</svg>' % (
        BW, BH, BW, BH, dd, ''.join(out) + ''.join(flowers))
    big = [blossom(rr.uniform(600, 1030), rr.uniform(150, 260), rr.uniform(26, 40), rr.uniform(0, 72), rr.choice(['#f6c9d7', '#fbe2ea', '#ffffff']), center=False) for _ in range(9)]
    bigsvg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" style="position:absolute;inset:0;overflow:hidden;filter:blur(10px)">%s</svg>' % (BW, BH, BW, BH, ''.join(big))
    return svg, bigsvg


SUN_DISC = 'radial-gradient(circle at 46% 42%,#ffffff 0,#fffbe8 40%,#fff3c4 66%,rgba(255,240,180,.9) 82%,rgba(255,236,170,0) 100%)'
SUN_HALO = 'radial-gradient(circle,rgba(255,252,236,.95) 0,rgba(255,246,206,.55) 12%,rgba(255,240,190,.24) 28%,rgba(255,240,200,.08) 44%,rgba(255,240,200,0) 60%)'


def main():
    sizes = {}
    with browser() as b:
        M = 40
        for key, svg, flt, sc in (('far', far, 'blur(4px)', .5), ('mid', mid, 'blur(4px)', .62)):
            html = defs + '<div style="position:absolute;left:%dpx;top:%dpx;width:1600px;height:520px">' % (M, M) + svg.replace('<svg ', '<svg style="display:block;width:1600px;height:520px;overflow:visible;filter:%s" ' % flt, 1) + '</div>'
            sizes[key] = save(shot(b, html, 1600, 520, margin=M), OUT + '/%s.webp' % key, scale=sc, q=72, aq=80)
        for key, svg, flt, sc in (('fga', fgA, 'blur(11px)', .4), ('fgb', fgB, 'blur(4.5px)', .6)):
            html = '<div style="position:absolute;left:60px;top:60px;width:1600px;height:900px">' + svg.replace('<svg ', '<svg style="display:block;width:1600px;height:900px;overflow:visible;filter:%s" ' % flt, 1) + '</div>'
            sizes[key] = save(shot(b, html, 1600, 900, margin=60), OUT + '/%s.webp' % key, scale=sc, q=70, aq=78)
        sizes['bok'] = save(shot(b, bokeh(), 1600, 810), OUT + '/bok.webp', scale=.5, q=74, aq=82)
        S = 1700
        sun = ('<div style="position:relative;width:%dpx;height:%dpx">' % (S, S)
               + '<div style="position:absolute;left:50%%;top:50%%;width:1598px;height:1598px;margin:-799px 0 0 -799px;border-radius:50%%;background:%s"></div>' % SUN_HALO
               + '<div style="position:absolute;left:50%%;top:50%%;width:400px;height:400px;margin:-200px 0 0 -200px;border-radius:50%%;background:%s;filter:blur(2px)"></div></div>' % SUN_DISC)
        sizes['sun'] = save(shot(b, sun, S, S), OUT + '/sun.webp', scale=.45, q=72, aq=80, noise=.4)
        tcss = ('.t{position:relative;width:1600px;height:190px;overflow:hidden;isolation:isolate}.t .tb{position:absolute;inset:0;z-index:1;mix-blend-mode:screen;background:%s}'
                '.t .lip{position:absolute;left:0;right:0;top:0;height:3px;z-index:3;background:linear-gradient(90deg,rgba(255,236,210,.2),rgba(255,244,228,.85) 60%%,rgba(255,236,210,.2));filter:blur(.5px)}') % TB
        sizes['table'] = save(shot(b, '<style>' + tcss + '</style><div class="t">' + table() + '<div class="tb"></div><div class="lip"></div></div>', 1600, 190), OUT + '/table.webp', q=80, opaque=True)
        sizes['tshade'] = save(shot(b, '<div style="position:absolute;left:20px;top:20px">' + tshade() + '</div>', 640, 190, margin=20), OUT + '/tshade.webp', scale=.6, q=70, aq=76)
        B = 30
        main_svg, bigsvg = branch()
        c1 = ('<div style="position:absolute;inset:0;filter:blur(1.4px) drop-shadow(0 0 8px rgba(255,220,235,.35));'
              '-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 16%);mask-image:linear-gradient(90deg,transparent 0,#000 16%)">' + main_svg + '</div>')
        wrap = lambda inner: '<div style="position:absolute;left:%dpx;top:%dpx;width:980px;height:215px">%s</div>' % (B, B, inner)
        sizes['branch'] = save(shot(b, wrap(c1 + bigsvg), 980 + 2 * B, 215 + 2 * B), OUT + '/branch.webp', q=82, aq=88)
    print({k: (v[0] // 1024, v[1]) for k, v in sizes.items()}, 'TOTAL KB', sum(v[0] for v in sizes.values()) // 1024)


if __name__ == '__main__':
    main()
