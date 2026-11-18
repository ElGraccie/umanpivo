"""New Year (night) theme: generate SVG art and bake every layer to WebP."""
import random, math, sys
from bakelib import browser, shot, save
from art import *
import bake_old as BO

import os
OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 't', 'newyear'))
R = random.Random(2027)
W, H = 1600, 520
SUNX = 960

FAR = [('0', '#7480bf'), ('.35', '#505b9c'), ('1', '#2e3672')]
MID = [('0', '#cfdcfa'), ('.08', '#8296cc'), ('.3', '#2b3b74'), ('1', '#0a1030')]
FG = '#070b1c'
FGLIT = ['#93aae0', '#7189ca', '#bccbf2']
BR = '#17110f'
NDARK = ['#10382f', '#164437', '#0c2c27', '#1a4f3e']
NLIT = ['#66a08b', '#82baa4', '#4d8872']
BCOL = ['#ff5a5f', '#ffcf6a', '#5fe09a', '#6aa8ff', '#ff8ad0', '#ffe9b0']

defs = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        '<filter id="rag" x="-4%" y="-12%" width="108%" height="124%"><feTurbulence type="fractalNoise" baseFrequency="0.014 0.03" numOctaves="4" seed="8" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="16" xChannelSelector="R" yChannelSelector="G"/></filter>'
        '<linearGradient id="gfar" gradientUnits="userSpaceOnUse" x1="0" y1="230" x2="0" y2="520">' + stops(FAR) + '</linearGradient>'
        '<linearGradient id="gmid" gradientUnits="userSpaceOnUse" x1="0" y1="170" x2="0" y2="520">' + stops(MID) + '</linearGradient>'
        '</defs></svg>')

def spruce(cx, base, h, w):
    n = 7; r = []; l = []
    for i in range(n):
        y = base - h + h * (i + 1) / n * 0.94
        wi = w * (0.2 + 0.8 * (i + 1) / n)
        yi = base - h + h * i / n * 0.94 + h / n * 0.28
        r += [(cx + wi * .5, yi), (cx + wi, y)]
        l = [(cx - wi, y), (cx - wi * .5, yi)] + l
    pts = [(cx, base - h)] + r + [(cx + w * .08, base + 10), (cx - w * .08, base + 10)] + l
    return '<path d="M' + ' L'.join('%s %s' % (f(a), f(b)) for a, b in pts) + ' Z"/>'

def spruces(hmin, hmax, smin, smax, wlo, whi, seed):
    rr = random.Random(seed); out = []; x = -40
    while x < W + 60:
        dist = abs(x - SUNX) / 380; k = .5 + .5 * min(1, dist)
        h = rr.uniform(hmin, hmax) * k + 24
        w = h * rr.uniform(wlo, whi)
        out.append(spruce(x, H + 10, h, w))
        x += rr.uniform(smin, smax)
    out.append('<rect x="-60" y="430" width="%d" height="120"/>' % (W + 120))
    return ''.join(out)

def land(inner, gid):
    return '<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMax slice" fill="url(#%s)"><g filter="url(#rag)">%s</g></svg>' % (W, H, gid, inner)

far = land(spruces(80, 170, 15, 30, .22, .3, 11), 'gfar')
mid = land(spruces(180, 320, 24, 52, .2, .28, 19), 'gmid')

def leaf(cx, cy, sz, fill=None):
    return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(%s %s %s)"%s/>' % (f(cx), f(cy), f(sz * R.uniform(.8, 1.5)), f(sz * R.uniform(.35, .6)), f(R.uniform(0, 180)), f(cx), f(cy), (' fill="%s"' % fill if fill else ''))

def cloud(cx, cy, rx, ry, n, sz):
    o = []
    for _ in range(n):
        a = R.uniform(0, 6.283); d = math.sqrt(R.random()) ** .7
        fl = R.choice(FGLIT) if R.random() < .4 else None
        o.append(leaf(cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d, sz, fl))
    o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s"/>' % (f(cx), f(cy), f(rx * .8), f(ry * .78)))
    return ''.join(o)

def tbranch(p0, p1, p2, p3, w):
    o = '<path d="M%s %s C%s %s %s %s %s %s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (f(p0[0]), f(p0[1]), f(p1[0]), f(p1[1]), f(p2[0]), f(p2[1]), f(p3[0]), f(p3[1]), BR, f(w))
    for i in range(1, 15):
        t = i / 14; x, y = bez(p0, p1, p2, p3, t)
        for _ in range(6):
            fl = R.choice(FGLIT) if R.random() < .4 else None
            o += leaf(x + R.uniform(-26, 26), y + R.uniform(-18, 26), R.uniform(8, 15), fl)
    return o

CW, CH = 1600, 900
fgA = ('<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice" fill="%s">' % (CW, CH, FG)
       + cloud(30, 20, 400, 150, 560, 22) + cloud(210, 150, 150, 80, 120, 18) + cloud(1590, 20, 430, 180, 600, 22)
       + cloud(1470, 200, 190, 100, 150, 18) + cloud(700, -30, 170, 60, 100, 18) + cloud(1160, -20, 170, 64, 110, 18) + '</svg>')
fgB = ('<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice" fill="%s">' % (CW, CH, BR)
       + tbranch((360, 70), (560, 40), (760, 140), (900, 290), 11) + tbranch((1260, 60), (1170, 90), (1050, 170), (960, 300), 10)
       + tbranch((1560, 330), (1420, 330), (1260, 360), (1130, 400), 9) + '</svg>')

# ---------------- bokeh: christmas lights out of focus (frame 1600x810)
def bokeh():
    o = []
    for i in range(40):
        col = R.choice(BCOL)
        if R.random() < .6: x = R.uniform(42, 98)
        else: x = R.uniform(3, 60)
        y = R.uniform(70, 640)
        sz = R.choice([14, 18, 24, 30, 38, 46, 56, 70]) * R.uniform(.9, 1.15)
        a = R.uniform(.45, 1.0)
        bg = 'radial-gradient(circle,%s 0,%s 62%%,%s 88%%,%s 100%%)' % (rgba(col, .12), rgba(col, .2), rgba(col, .6), rgba(col, 0))
        o.append('<i style="position:absolute;left:%.0fpx;top:%.0fpx;width:%.0fpx;height:%.0fpx;border-radius:50%%;opacity:%.2f;background:%s;filter:blur(.8px)"></i>' % (x / 100 * 1600 - sz / 2, y, sz, sz, a, bg))
    return '<div style="position:relative;width:1600px;height:810px">' + ''.join(o) + '</div>'

# ---------------- table (night wood)
def table():
    TW, TH = 1600, 190
    hs = [12 * 1.2**i for i in range(8)]; s = sum(hs); hs = [h * TH / s for h in hs]
    y = 0; pl = []
    cols = ['#6b4a3a', '#5e4132', '#745140', '#684636', '#573a2c', '#70503e', '#603f30', '#785645']
    for i, h in enumerate(hs):
        pl.append('<rect x="0" y="%.1f" width="%d" height="%.1f" fill="%s"/>' % (y, TW, h, cols[(i * 3 + 1) % len(cols)]))
        jx = R.uniform(150, TW - 150)
        for jj in (jx, (jx + R.uniform(500, 900)) % TW):
            pl.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#140a06" opacity=".5"/>' % (jj, y, 1.1 + i * .2, h))
        pl.append('<rect x="0" y="%.1f" width="%d" height="%.1f" fill="#0d0604" opacity=".7"/>' % (y + h - 1.4 - i * .25, TW, 1.4 + i * .25))
        pl.append('<rect x="0" y="%.1f" width="%d" height="1" fill="#c4d2ff" opacity=".14"/>' % (y, TW))
        y += h
    return ('<svg style="position:absolute;inset:0;width:100%%;height:100%%;display:block;filter:saturate(.8) brightness(.78)" viewBox="0 0 %d %d" preserveAspectRatio="none"><defs>'
            '<filter id="wg" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency="0.0018 0.2" numOctaves="5" seed="5"/><feColorMatrix type="matrix" values="0 0 0 0 .07  0 0 0 0 .04  0 0 0 0 .03  2.1 0 0 0 -.72"/></filter>'
            '<filter id="wg2" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency="0.0026 0.11" numOctaves="4" seed="17"/><feColorMatrix type="matrix" values="0 0 0 0 .62  0 0 0 0 .56  0 0 0 0 .6  1.6 0 0 0 -.78"/></filter>'
            '<linearGradient id="tsh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8b8ff" stop-opacity=".34"/><stop offset=".4" stop-color="#7f8ee0" stop-opacity=".08"/><stop offset="1" stop-color="#04060f" stop-opacity=".82"/></linearGradient></defs>'
            '%s<rect width="%d" height="%d" filter="url(#wg)" opacity=".95"/><rect width="%d" height="%d" filter="url(#wg2)" opacity=".4"/><rect width="%d" height="%d" fill="url(#tsh)"/></svg>') % (TW, TH, ''.join(pl), TW, TH, TW, TH, TW, TH)

TB = ('radial-gradient(ellipse 150px 100% at 60% 0,rgba(170,190,255,.32),transparent 72%),radial-gradient(ellipse 210px 16px at 74% 40%,rgba(255,190,120,.24),transparent 72%),'
      'radial-gradient(ellipse 160px 14px at 52% 24%,rgba(255,150,120,.2),transparent 72%),radial-gradient(ellipse 120px 12px at 90% 60%,rgba(120,220,170,.14),transparent 72%)')
GLITTER = ''.join('radial-gradient(%.1fpx %.1fpx at %.0f%% %.0f%%,#ffe9a8,transparent),' % (r, r, x, y) for x, y, r in
                  [(6, 36, 1.8), (13, 70, 1.5), (19, 22, 2), (28, 58, 1.6), (36, 82, 1.8), (44, 30, 1.5), (51, 66, 2), (58, 14, 1.6), (63, 48, 1.8), (71, 80, 1.5), (78, 26, 2), (86, 60, 1.6), (93, 36, 1.8), (97, 78, 1.5)])
SD = ('radial-gradient(ellipse 170px 11px at 8% 4%,rgba(248,252,255,.9),transparent 72%),radial-gradient(ellipse 230px 12px at 27% 3%,rgba(248,252,255,.82),transparent 72%),'
      'radial-gradient(ellipse 160px 10px at 47% 4%,rgba(248,252,255,.75),transparent 72%),radial-gradient(ellipse 190px 10px at 70% 4%,rgba(248,252,255,.7),transparent 72%),' + GLITTER.rstrip(','))

# ---------------- shadow of the branch on the table (needles)
def tshade():
    sh = []
    for _ in range(70):
        sh.append(needle(R.uniform(0, 640), R.uniform(-10, 190), R.uniform(0, 360), R.uniform(.9, 2.0), '#03061a', R.uniform(.38, .62)))
    sh.append('<path d="M700 -10C560 40 380 70 120 80" stroke="#03061a" stroke-opacity=".4" stroke-width="22" fill="none" stroke-linecap="round"/>')
    return '<svg viewBox="0 0 640 190" preserveAspectRatio="xMaxYMid slice" style="display:block;width:640px;height:190px;filter:blur(3.5px)">@@</svg>'.replace('@@', ''.join(sh))

# ---------------- halos for lights
def halo_defs(pref):
    o = ''
    for c in BCOL + ['#ffd98a', '#ffb347', '#7dd3ff', '#9be37a', '#ffffff']:
        o += '<radialGradient id="%s_%s"><stop offset="0" stop-color="%s" stop-opacity=".8"/><stop offset=".35" stop-color="%s" stop-opacity=".3"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (pref, c[1:], c, c, c)
    return o

def lighten(c, k=.55):
    r, g, b = hex2rgb(c)
    return '#%02x%02x%02x' % (int(r + (255 - r) * k), int(g + (255 - g) * k), int(b + (255 - b) * k))

# ---------------- garland (frame 1200x210)
GW, GH = 1200, 210
def garland():
    rr = random.Random(5)
    anchors = [(-40, 26), (300, 14), (650, 26), (1000, 14), (1250, 28)]
    sags = [96, 104, 98, 92]
    wire = 'M%s %s' % (f1(anchors[0][0]), f1(anchors[0][1])); bulbs = []
    for i in range(4):
        p0, p3 = anchors[i], anchors[i + 1]; dx = p3[0] - p0[0]
        c1 = (p0[0] + dx * .22, p0[1] + sags[i] * 1.18); c2 = (p0[0] + dx * .78, p3[1] + sags[i] * 1.18)
        wire += ' C%s %s %s %s %s %s' % (f1(c1[0]), f1(c1[1]), f1(c2[0]), f1(c2[1]), f1(p3[0]), f1(p3[1]))
        for k in range(1, 10):
            x, y = bez(p0, c1, c2, p3, k / 10)
            bulbs.append((x, y, rr.uniform(-.2, .2)))
    base = '<path d="%s" stroke="#070a16" stroke-width="2.4" fill="none"/>' % wire
    base += ''.join('<circle cx="%s" cy="%s" r="3.4" fill="#070a16"/>' % (f1(a[0]), f1(a[1])) for a in anchors[1:-1])
    sets = [[], [], []]
    for i, (x, y, tl) in enumerate(bulbs):
        col = BCOL[(i * 5 + i // 7) % 6]
        bx, by = x + tl * 14, y + 13
        g = '<rect x="%s" y="%s" width="4.4" height="7" rx="1" fill="#0e1222" transform="rotate(%s %s %s)"/>' % (f1(x - 2.2), f1(y - 1), f1(tl * 57), f1(x), f1(y))
        base += g + '<ellipse cx="%s" cy="%s" rx="5.6" ry="8.4" fill="%s" opacity=".6" transform="rotate(%s %s %s)"/>' % (f1(bx), f1(by), col, f1(tl * 57), f1(bx), f1(by))
        sets[i % 3].append('<circle cx="%s" cy="%s" r="36" fill="url(#hg_%s)"/><ellipse cx="%s" cy="%s" rx="5.8" ry="8.6" fill="%s" transform="rotate(%s %s %s)"/><ellipse cx="%s" cy="%s" rx="2.2" ry="3.4" fill="#fff" opacity=".9"/>' % (
            f1(bx), f1(by), col[1:], f1(bx), f1(by), lighten(col, .5), f1(tl * 57), f1(bx), f1(by), f1(bx - 1), f1(by - 2)))
    mk = lambda inner: '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><defs>%s</defs>%s</svg>' % (GW, GH, GW, GH, halo_defs('hg'), inner)
    return mk(base), [mk(''.join(s)) for s in sets]

# ---------------- branch (frame 980x215) with baubles and lights
BW, BH = 980, 215
def branch():
    rr = random.Random(77)
    P = [(1040, 95), (790, 78), (480, 125), (130, 140)]
    N = 40; left = []; right = []
    for i in range(N + 1):
        t = i / N; x, y = bez(*P, t)
        x2, y2 = bez(*P, min(1, t + .01)); x1, y1 = bez(*P, max(0, t - .01))
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = max(1.2, 13 * (1 - t)**1.15 + 1.5)
        left.append((x + nx * w, y + ny * w)); right.append((x - nx * w, y - ny * w))
    poly = left + right[::-1]
    out = ['<path d="M' + ' L'.join('%s %s' % (f1(a), f1(b)) for a, b in poly) + ' Z" fill="%s"/>' % BR]
    out.append('<path d="M' + ' L'.join('%s %s' % (f1(a), f1(b)) for a, b in (right if right[0][1] < left[0][1] else left)) + '" stroke="#9db4ff" stroke-opacity=".4" stroke-width="2.2" fill="none"/>')
    tips = []
    for t in (.14, .28, .42, .56, .7, .82):
        x, y = bez(*P, t); dirn = rr.choice([-1, 1]); ln = rr.uniform(45, 95) * (1 - t * .45)
        ex = x - ln; ey = y + dirn * rr.uniform(22, 50)
        out.append('<path d="M%s %s Q%s %s %s %s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (f1(x), f1(y), f1((x + ex) / 2), f1((y + ey) / 2 - 12), f1(ex), f1(ey), BR, f1(max(2, 9 * (1 - t) + 1.5))))
        tips.append((ex, ey, t))
    ex0, ey0 = bez(*P, 1.0)
    for k, (ang, ln) in enumerate([(-24, 70), (8, 95), (32, 64), (-48, 44)]):
        a = math.radians(180 + ang); ex = ex0 + math.cos(a) * ln; ey = ey0 + math.sin(a) * ln * .9
        out.append('<path d="M%s %s Q%s %s %s %s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (f1(ex0), f1(ey0), f1((ex0 + ex) / 2), f1((ey0 + ey) / 2 - 6), f1(ex), f1(ey), BR, f1(2.4 - k * .3)))
        tips.append((ex, ey, 1.0))
    def lf(x, y, a, s, lit=True):
        if lit and rr.random() < .3: return needle(x, y, a, s, rr.choice(NLIT), .95)
        return needle(x, y, a, s, rr.choice(NDARK), 1)
    for i in range(0, 60):
        t = i / 59; x, y = bez(*P, t)
        n = (3 if t < .55 else (2 if t < .85 else 1)) + 1
        for _ in range(n): out.append(lf(x + rr.uniform(-28, 28), y + rr.uniform(-22, 28), rr.uniform(0, 360), rr.uniform(.5, 1.0) * (1 - t * .35)))
    for ex, ey, t in tips:
        for _ in range(max(2, int(10 * (1 - t * .7)))): out.append(lf(ex + rr.uniform(-40, 32), ey + rr.uniform(-24, 26), rr.uniform(0, 360), rr.uniform(.5, 1.0) * (1 - t * .3)))
    for i in range(0, 60, 2):
        t = i / 59; x, y = bez(*P, t)
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#eaf1ff" opacity=".95"/>' % (f1(x + rr.uniform(-10, 10)), f1(y - 8 - 9 * (1 - t)), f1(rr.uniform(11, 24) * (1 - t * .5)), f1(rr.uniform(5, 9))))
    # lights on a wire that drapes under the branch
    pts = []
    for i in range(17):
        t = .1 + .86 * i / 16; x, y = bez(*P, t)
        pts.append((x + rr.uniform(-5, 5), y + 16 + 10 * math.sin(i * 1.7) + rr.uniform(0, 6)))
    wire = 'M' + ' L'.join('%s %s' % (f1(a), f1(b)) for a, b in pts)
    lights = '<path d="%s" stroke="#070a16" stroke-width="1.8" fill="none" stroke-linejoin="round" opacity=".9"/>' % wire
    warm = ['#ffd98a', '#ffb347', '#ff6b6b', '#7dd3ff', '#9be37a', '#fff1c8']
    sets = [[], []]
    for i, (x, y) in enumerate(pts):
        col = warm[(i * 3 + i // 5) % 6]
        lights += '<rect x="%s" y="%s" width="3.6" height="5" rx="1" fill="#0e1222"/><ellipse cx="%s" cy="%s" rx="4.6" ry="6.4" fill="%s" opacity=".62"/>' % (f1(x - 1.8), f1(y - 1), f1(x), f1(y + 6), col)
        sets[i % 2].append('<circle cx="%s" cy="%s" r="30" fill="url(#hb_%s)"/><ellipse cx="%s" cy="%s" rx="4.8" ry="6.6" fill="%s"/><ellipse cx="%s" cy="%s" rx="1.8" ry="2.6" fill="#fff" opacity=".9"/>' % (
            f1(x), f1(y + 6), col[1:], f1(x), f1(y + 6), lighten(col, .5), f1(x - .8), f1(y + 4)))
    balls = ''
    for t, col, r, th in [(.2, 'red', 19, 44), (.4, 'gold', 15, 52), (.585, 'blue', 17, 38), (.77, 'silver', 14, 30)]:
        x, y = bez(*P, t)
        balls += bauble(x + rr.uniform(-6, 6), y + th + r + 10, r, col, 'bb', thread=th + 10)
    dd = '<defs>' + bauble_defs('bb') + halo_defs('hb') + '</defs>'
    mk = lambda inner: '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" style="position:absolute;inset:0;overflow:hidden">%s%s</svg>' % (BW, BH, BW, BH, dd, inner)
    main = mk(''.join(out) + lights + balls)
    glows = [mk(''.join(s)) for s in sets]
    big = [needle(rr.uniform(600, 1030), rr.uniform(150, 260), rr.uniform(100, 260), rr.uniform(1.8, 3.0), rr.choice(NDARK)) for _ in range(12)]
    bigsvg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" style="position:absolute;inset:0;overflow:hidden;filter:blur(10px)">%s</svg>' % (BW, BH, BW, BH, ''.join(big))
    return main, glows, bigsvg

# ---------------- props on the table (frame 560x300)
def props():
    rr = random.Random(9)
    PW, PH = 560, 300
    o = '<defs>' + bauble_defs('pb') + '<filter id="bl"><feGaussianBlur stdDeviation="5"/></filter></defs>'
    # contact shadows
    o += '<ellipse cx="270" cy="268" rx="62" ry="12" fill="#02030a" opacity=".7" filter="url(#bl)"/><ellipse cx="372" cy="284" rx="46" ry="10" fill="#02030a" opacity=".7" filter="url(#bl)"/><ellipse cx="160" cy="288" rx="34" ry="8" fill="#02030a" opacity=".65" filter="url(#bl)"/>'
    # fir sprig lying at the back
    pts = [(40, 250), (150, 214), (270, 176), (410, 152), (520, 150)]
    o += '<path d="M%s" stroke="#1b1410" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % ' L'.join('%d %d' % p for p in pts)
    for i in range(46):
        t = i / 45; k = min(3, int(t * 4)); a, b = pts[k], pts[k + 1]; tt = t * 4 - k
        x, y = a[0] + (b[0] - a[0]) * tt, a[1] + (b[1] - a[1]) * tt
        for sgn in (-1, 1):
            ang = -18 + sgn * rr.uniform(38, 70)
            o += needle(x + rr.uniform(-4, 4), y + rr.uniform(-3, 3), ang, rr.uniform(.8, 1.35) * (1 - t * .25), rr.choice(NDARK + NLIT[:1]), 1)
    for i in range(0, 46, 3):
        t = i / 45; k = min(3, int(t * 4)); a, b = pts[k], pts[k + 1]; tt = t * 4 - k
        x, y = a[0] + (b[0] - a[0]) * tt, a[1] + (b[1] - a[1]) * tt
        o += '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#eef4ff" opacity=".92"/>' % (x + rr.uniform(-6, 6), y - 9, rr.uniform(8, 15), rr.uniform(3.5, 6))
    # baubles
    o += bauble(160, 262, 23, 'silver', 'pb') + bauble(270, 238, 33, 'red', 'pb') + bauble(372, 258, 27, 'gold', 'pb')
    # warm bounce light on the table under the baubles
    o += '<ellipse cx="270" cy="276" rx="54" ry="6" fill="#ff5a5f" opacity=".25" filter="url(#bl)"/><ellipse cx="372" cy="290" rx="42" ry="5" fill="#ffcf6a" opacity=".25" filter="url(#bl)"/>'
    # glitter
    for _ in range(18):
        x, y = rr.uniform(30, 520), rr.uniform(190, 295); s = rr.uniform(2.5, 6)
        o += '<path d="M%.1f %.1f l%.1f %.1f l%.1f %.1f l%.1f %.1f l%.1f %.1f l%.1f %.1f l%.1f %.1f l%.1f %.1fz" fill="#ffe9a8" opacity="%.2f"/>' % (
            x, y - s, s * .25, s * .75, s * .75, s * .25, -s * .75, s * .25, -s * .25, s * .75, -s * .25, -s * .75, -s * .75, -s * .25, s * .75, -s * .25, rr.uniform(.45, .95))
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" style="display:block">%s</svg>' % (PW, PH, PW, PH, o)

# ================================================================ bake
MOON_RAYS = ("conic-gradient(from 8deg,transparent 0 7deg,rgba(200,220,255,.14) 10deg,transparent 15deg 22deg,rgba(200,220,255,.1) 25deg,transparent 31deg 47deg,"
             "rgba(200,220,255,.14) 51deg,transparent 58deg 80deg,rgba(200,220,255,.09) 84deg,transparent 90deg 140deg,rgba(200,220,255,.08) 146deg,transparent 154deg 205deg,"
             "rgba(200,220,255,.09) 211deg,transparent 218deg 250deg,rgba(200,220,255,.12) 256deg,transparent 262deg 292deg,rgba(200,220,255,.14) 297deg,transparent 304deg 330deg,"
             "rgba(200,220,255,.1) 335deg,transparent 342deg)")
MARIA = ('radial-gradient(circle at 34% 40%,rgba(140,155,200,.34) 0,rgba(140,155,200,0) 17%),radial-gradient(circle at 58% 30%,rgba(140,155,200,.28) 0,rgba(140,155,200,0) 13%),'
         'radial-gradient(circle at 52% 62%,rgba(140,155,200,.3) 0,rgba(140,155,200,0) 19%),radial-gradient(circle at 72% 54%,rgba(140,155,200,.22) 0,rgba(140,155,200,0) 11%),')
MOON_DISC = MARIA + 'radial-gradient(circle at 42% 38%,#ffffff 0,#f3f6ff 34%,#d3defa 62%,rgba(176,196,255,.85) 80%,rgba(150,175,255,0) 100%)'
MOON_HALO = 'radial-gradient(circle,rgba(196,214,255,.8) 0,rgba(140,168,245,.42) 13%,rgba(96,118,220,.2) 28%,rgba(66,78,170,.08) 44%,rgba(44,54,140,0) 60%)'

def main():
    sizes = {}
    with browser() as b:
        M = 40
        for key, svg, flt, sc in (('far', far, 'blur(4px)', .5), ('mid', mid, 'blur(3px)', .62)):
            html = defs + '<div style="position:absolute;left:%dpx;top:%dpx;width:1600px;height:520px">' % (M, M) + svg.replace('<svg ', '<svg style="display:block;width:1600px;height:520px;overflow:visible;filter:%s" ' % flt, 1) + '</div>'
            sizes[key] = save(shot(b, html, 1600, 520, margin=M), OUT + '/%s.webp' % key, scale=sc, q=72, aq=80)
        for key, svg, flt, sc in (('fga', fgA, 'blur(11px)', .4), ('fgb', fgB, 'blur(4.5px)', .6)):
            html = '<div style="position:absolute;left:60px;top:60px;width:1600px;height:900px">' + svg.replace('<svg ', '<svg style="display:block;width:1600px;height:900px;overflow:visible;filter:%s" ' % flt, 1) + '</div>'
            sizes[key] = save(shot(b, html, 1600, 900, margin=60), OUT + '/%s.webp' % key, scale=sc, q=70, aq=78)
        sizes['bok'] = save(shot(b, bokeh(), 1600, 810), OUT + '/bok.webp', scale=.5, q=74, aq=82)
        # moon
        S = 1700
        sun = ('<div style="position:relative;width:%dpx;height:%dpx">' % (S, S)
               + '<div style="position:absolute;inset:0;border-radius:50%%;opacity:.8;filter:blur(7px);background:%s;-webkit-mask-image:radial-gradient(circle,#000 5%%,transparent 68%%);mask-image:radial-gradient(circle,#000 5%%,transparent 68%%)"></div>' % MOON_RAYS
               + '<div style="position:absolute;left:50%%;top:50%%;width:1598px;height:1598px;margin:-799px 0 0 -799px;border-radius:50%%;background:%s;opacity:.94"></div>' % MOON_HALO
               + '<div style="position:absolute;left:50%%;top:50%%;width:420px;height:420px;margin:-210px 0 0 -210px;border-radius:50%%;background:%s;filter:blur(1.6px)"></div></div>' % MOON_DISC)
        sizes['sun'] = save(shot(b, sun, S, S), OUT + '/sun.webp', scale=.45, q=72, aq=80, noise=.4)
        # table
        tcss = ('.t{position:relative;width:1600px;height:190px;overflow:hidden;isolation:isolate}.t .tb{position:absolute;inset:0;z-index:1;mix-blend-mode:screen;background:%s}'
                '.t .sd{position:absolute;inset:0;z-index:2;background:%s}'
                '.t .lip{position:absolute;left:0;right:0;top:0;height:3px;z-index:3;background:linear-gradient(90deg,rgba(170,190,255,.14),rgba(210,222,255,.85) 60%%,rgba(170,190,255,.14));filter:blur(.5px)}') % (TB, SD)
        sizes['table'] = save(shot(b, '<style>' + tcss + '</style><div class="t">' + table() + '<div class="tb"></div><div class="sd"></div><div class="lip"></div></div>', 1600, 190), OUT + '/table.webp', q=80, opaque=True)
        sizes['tshade'] = save(shot(b, '<div style="position:absolute;left:20px;top:20px">' + tshade() + '</div>', 640, 190, margin=20), OUT + '/tshade.webp', scale=.6, q=70, aq=76)
        # branch (+ glows)
        B = 30
        main_svg, glows, bigsvg = branch()
        c1 = '<div style="position:absolute;inset:0;filter:blur(1.8px) drop-shadow(0 0 10px rgba(120,150,255,.3));-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 16%);mask-image:linear-gradient(90deg,transparent 0,#000 16%)">' + main_svg + '</div>'
        wrap = lambda inner: '<div style="position:absolute;left:%dpx;top:%dpx;width:980px;height:215px">%s</div>' % (B, B, inner)
        sizes['branch'] = save(shot(b, wrap(c1 + bigsvg), 980 + 2 * B, 215 + 2 * B), OUT + '/branch.webp', q=82, aq=88)
        for i, g in enumerate(glows):
            sizes['bgl%d' % (i + 1)] = save(shot(b, wrap('<div style="position:absolute;inset:0;filter:blur(1.2px)">' + g + '</div>'), 980 + 2 * B, 215 + 2 * B), OUT + '/bgl%d.webp' % (i + 1), scale=.6, q=76, aq=85)
        # garland
        gbase, gsets = garland()
        sizes['garland'] = save(shot(b, gbase, GW, GH), OUT + '/garland.webp', q=82, aq=88)
        for i, g in enumerate(gsets):
            sizes['gl%d' % (i + 1)] = save(shot(b, g, GW, GH), OUT + '/gl%d.webp' % (i + 1), scale=.6, q=76, aq=85)
        # props
        sizes['props'] = save(shot(b, props(), 560, 300), OUT + '/props.webp', scale=.75, q=82, aq=88)
    print({k: (v[0] // 1024, v[1]) for k, v in sizes.items()}, 'TOTAL KB', sum(v[0] for v in sizes.values()) // 1024)

if __name__ == '__main__':
    main()
