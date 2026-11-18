"""Seasonal look for everything below the hero: section grounds, paper patterns, scalloped edges and the
decorative strip above the catalogue (autumn leaves / winter icicles / New Year garland).
Everything is CSS + tiny inline SVG tiles, no extra requests, nothing animated except the garland twinkle."""
import math, urllib.parse, random


def q(svg):
    return 'url("data:image/svg+xml;utf8,%s")' % urllib.parse.quote(svg, safe=" /:=,;'()*!~._-")


def f(x):
    return ('%.1f' % x).rstrip('0').rstrip('.')


# ------------------------------------------------------------------ outline icons (same hand as the base barley/hop pattern)
def maple():
    return ('<path d="M0 -26L6 -14L14 -18L12 -6L24 -10L18 2L26 6L10 12L12 20L2 16L2 28L-2 28L-2 16L-12 20L-10 12L-26 6L-18 2L-24 -10L-12 -6L-14 -18L-6 -14Z"/>'
            '<path d="M0 28V-8M0 8L-14 -2M0 8L14 -2M0 -2L-9 -12M0 -2L9 -12"/>')


def leaf():
    return ('<path d="M0 -26C16 -16 18 6 0 28C-18 6 -16 -16 0 -26Z"/>'
            '<path d="M0 -26V36M0 -8L-9 -16M0 -8L9 -16M0 4L-11 -6M0 4L11 -6M0 14L-8 6M0 14L8 6"/>')


def snow(r=22):
    arm = 'M0 0V-%d' % r
    for rr, w in ((r * .5, 5), (r * .72, 4)):
        arm += 'M0 -%s L-%d -%s M0 -%s L%d -%s' % (f(rr), w, f(rr + w), f(rr), w, f(rr + w))
    return ''.join('<g transform="rotate(%d)"><path d="%s"/></g>' % (a, arm) for a in range(0, 360, 60))


def spark():
    return '<path d="M0 -17Q2 -2 17 0Q2 2 0 17Q-2 2 -17 0Q-2 -2 0 -17Z"/>'


def bauble():
    return ('<circle cx="0" cy="6" r="13"/><path d="M-4 -7H4V-3H-4Z"/><path d="M0 -7V-12Q0 -16 4 -16"/>'
            '<path d="M-13 3Q0 10 13 3"/>')


def fir():
    n = 'M0 -30V32'
    for y, w in ((-22, 9), (-13, 12), (-4, 14), (6, 12), (16, 9)):
        n += 'M0 %d l-%d 6M0 %d l%d 6' % (y, w, y, w)
    return '<path d="%s"/>' % n


def tile(groups, sw=1.6):
    """groups: [(stroke, opacity, [(icon, x, y, rot, scale)...])]"""
    out = ''
    for stroke, op, items in groups:
        out += '<g fill="none" stroke="%s" stroke-opacity="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round">' % (stroke, op, sw)
        for ic, x, y, r, s in items:
            out += '<g transform="translate(%s %s) rotate(%s) scale(%s)">%s</g>' % (x, y, r, s, ic)
        out += '</g>'
    return "<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240' viewBox='0 0 240 240'>%s</svg>" % out


PAT = {
    'autumn': q(tile([('#8a4a1c', '.21', [(maple(), 56, 62, -20, 1), (leaf(), 176, 150, 28, .95), (maple(), 196, 44, 24, .62), (leaf(), 44, 190, -30, .72)])])),
    'winter': q(tile([('#4f7088', '.24', [(snow(24), 58, 62, 8, 1), (snow(22), 178, 150, 30, .92), (snow(20), 198, 44, 0, .62), (snow(20), 44, 190, 18, .7)]),
                      ('#4f7088', '.26', [('<circle r="1.8" fill="#4f7088"/>', x, y, 0, 1) for x, y in ((118, 36), (124, 118), (22, 118), (110, 214), (226, 110), (152, 70), (84, 150))])])),
    'newyear': q(tile([('#a9781f', '.34', [(spark(), 58, 62, 0, 1.05), (spark(), 196, 46, 0, .6), (spark(), 112, 130, 0, .5)]),
                       ('#8b2f3b', '.24', [(bauble(), 176, 150, 12, .9), (fir(), 44, 190, -26, .78)]),
                       ('#4f7088', '.22', [(snow(20), 122, 214, 10, .6)])])),
}

# scalloped edge, shape only: colour comes from the CSS (mask)
SCAL = q("<svg xmlns='http://www.w3.org/2000/svg' width='260' height='30' viewBox='0 0 260 30'><g fill='#000'><rect width='260' height='8'/>"
         "<circle cx='14' cy='8' r='12'/><circle cx='46' cy='6' r='9'/><circle cx='70' cy='8' r='15'/><circle cx='104' cy='5' r='8'/>"
         "<circle cx='128' cy='8' r='13'/><circle cx='160' cy='6' r='10'/><circle cx='190' cy='8' r='16'/><circle cx='224' cy='5' r='9'/>"
         "<circle cx='246' cy='8' r='12'/></g></svg>")


# ------------------------------------------------------------------ decoration strips
def leaf_fill(col, dark, kind):
    """small filled leaf in its own coordinates (about 52 units long)"""
    if kind == 'maple':
        body = '<path d="M0 -26L6 -14L14 -18L12 -6L24 -10L18 2L26 6L10 12L12 20L2 16L2 28L-2 28L-2 16L-12 20L-10 12L-26 6L-18 2L-24 -10L-12 -6L-14 -18L-6 -14Z"/>'
        vein = '<path d="M0 28V-10M0 8L-14 -2M0 8L14 -2M0 -2L-9 -12M0 -2L9 -12"/>'
    else:
        body = '<path d="M0 -26C16 -16 18 6 0 28C-18 6 -16 -16 0 -26Z"/>'
        vein = '<path d="M0 -26V36M0 -8L-9 -16M0 -8L9 -16M0 4L-11 -6M0 4L11 -6M0 14L-8 6M0 14L8 6"/>'
    return ('<g fill="%s" stroke="%s" stroke-opacity=".55" stroke-width="1.3" stroke-linejoin="round">%s</g>'
            '<g fill="none" stroke="%s" stroke-opacity=".5" stroke-width="1.2" stroke-linecap="round">%s</g>') % (col, dark, body, dark, vein)


def leaves_strip():
    items = [(40, 28, -35, .9, '#c8481f', 'maple'), (118, 40, 25, .62, '#e0a52e', 'leaf'), (196, 24, -12, .78, '#d9772b', 'maple'),
             (292, 42, 42, .6, '#8a4a1c', 'leaf'), (372, 26, -26, .92, '#b83a1d', 'maple'), (462, 38, 14, .7, '#e0a52e', 'maple'),
             (548, 22, -42, .66, '#d9772b', 'leaf'), (638, 40, 32, .8, '#c8481f', 'leaf')]
    g = ''.join('<g transform="translate(%d %d) rotate(%d) scale(%s)">%s</g>' % (x, y, r, s, leaf_fill(c, '#5a2a0e', k)) for x, y, r, s, c, k in items)
    return q("<svg xmlns='http://www.w3.org/2000/svg' width='720' height='84' viewBox='0 0 720 84'>%s</svg>" % g)


def icicles_strip():
    xs = [20, 64, 98, 150, 188, 236, 280, 330, 374, 420, 466, 520, 566, 610]
    ln = [30, 46, 22, 58, 34, 48, 24, 56, 32, 44, 22, 52, 36, 26]
    wd = [13, 16, 11, 17, 13, 16, 11, 17, 14, 15, 11, 16, 14, 11]
    g = ('<defs><linearGradient id="i" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".96"/>'
         '<stop offset="1" stop-color="#b9daef" stop-opacity=".88"/></linearGradient></defs>')
    for x, l, w in zip(xs, ln, wd):
        g += ('<path d="M%s 0Q%s %s %s %sQ%s %s %s 0Z" fill="url(#i)" stroke="#86adc6" stroke-opacity=".75" stroke-width="1"/>'
              '<path d="M%s 4L%s %s" stroke="#fff" stroke-opacity=".95" stroke-width="1.3" stroke-linecap="round"/>') % (
            f(x - w / 2), f(x - w / 4), f(l * .55), f(x), f(l), f(x + w / 4), f(l * .55), f(x + w / 2), f(x - w / 6), f(x - w / 10), f(l * .62))
    return q("<svg xmlns='http://www.w3.org/2000/svg' width='640' height='72' viewBox='0 0 640 72'>%s</svg>" % g)


BULB = ['#e0434f', '#f2b632', '#4a86e6', '#3fa66a', '#e86fa3']


def garland_parts():
    W, H = 360, 78
    P0, C, P2 = (0, 6), (180, 60), (360, 6)

    def pt(t):
        return ((1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * C[0] + t * t * P2[0], (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * C[1] + t * t * P2[1])
    ts = [.1, .3, .5, .7, .9]
    wire = '<path d="M0 6Q180 60 360 6" fill="none" stroke="#25332c" stroke-width="1.7" stroke-linecap="round"/>'
    bulbs, halos = '', []
    for i, t in enumerate(ts):
        x, y = pt(t)
        col = BULB[i % len(BULB)]
        cy = y + 13
        bulbs += ('<path d="M%s %sV%s" stroke="#25332c" stroke-width="1.3"/><rect x="%s" y="%s" width="5" height="4.5" rx="1" fill="#3a463f"/>'
                  '<ellipse cx="%s" cy="%s" rx="5.4" ry="7.4" fill="%s"/><ellipse cx="%s" cy="%s" rx="1.6" ry="2.6" fill="#fff" fill-opacity=".55"/>') % (
            f(x), f(y), f(y + 4), f(x - 2.5), f(y + 3.5), f(x), f(cy), col, f(x - 1.8), f(cy - 2.6))
        halos.append((x, cy, col))

    def layer(idx):
        defs, body = '<defs>', ''
        for k, (x, cy, col) in enumerate(halos):
            if k not in idx:
                continue
            defs += '<radialGradient id="g%d"><stop offset="0" stop-color="%s" stop-opacity=".75"/><stop offset=".45" stop-color="%s" stop-opacity=".28"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (k, col, col, col)
            body += '<circle cx="%s" cy="%s" r="19" fill="url(#g%d)"/>' % (f(x), f(cy), k)
        return q("<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d' viewBox='0 0 %d %d'>%s</defs>%s</svg>" % (W, H, W, H, defs, body))
    base = q("<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d' viewBox='0 0 %d %d'>%s%s</svg>" % (W, H, W, H, wire, bulbs))
    return base, layer({0, 2, 4}), layer({1, 3})


# ------------------------------------------------------------------ per-season parameters
SEASONS = {
    'autumn': dict(
        deep='#130d08', sand='#f1dcb6', hop='#8a4a1c', lines='#1a110a 0%,#26190f 50%,#130d08 100%',
        orb=('rgba(240,140,40,.34)', 'rgba(190,70,40,.30)', 'rgba(230,170,40,.30)'),
        paper='#e8c98f', about=('#e5d6ac', '#d6c18c'), visit=('#efd9b0', '#f1dfbd'),
        deepglow=('rgba(232,140,30,.20)', 'rgba(150,60,30,.26)'), footer='#17100b', hover='138,74,28,.5'),
    'winter': dict(
        deep='#0b121b', sand='#e8eff4', hop='#2f5f86', lines='#0e1620 0%,#15212f 50%,#0b121b 100%',
        orb=('rgba(110,165,230,.32)', 'rgba(214,120,160,.22)', 'rgba(140,205,230,.26)'),
        paper='#d6e3ec', about=('#d5e2ea', '#c4d6e3'), visit=('#e8eef2', '#eef3f6'),
        deepglow=('rgba(120,170,230,.16)', 'rgba(80,120,170,.24)'), footer='#0f1822', hover='60,100,140,.42'),
    'newyear': dict(
        deep='#080d20', sand='#f5e8d0', hop='#8b2f3b', lines='#0a1028 0%,#111b40 50%,#080d20 100%',
        orb=('rgba(255,196,80,.28)', 'rgba(214,60,80,.26)', 'rgba(90,120,220,.26)'),
        paper='#ecd6ad', about=('#efe1c3', '#e3cf9f'), visit=('#f5e8d0', '#f3e3c3'),
        deepglow=('rgba(255,196,80,.18)', 'rgba(80,100,200,.24)'), footer='#0b1024', hover='150,40,60,.36'),
}


def css():
    out = ['/* ===== seasonal inner design (generated by inner.py) ===== */',
           'html[data-theme]{--scal:%s}' % SCAL,
           '.sdeco{display:none;position:absolute;left:0;right:0;pointer-events:none}',
           '.sdeco i{position:absolute;inset:0;background-repeat:repeat-x;background-position:0 0}']
    for th, p in SEASONS.items():
        s = 'html[data-theme=%s]' % th
        # --hf = rgb of the colour the next section (.lines-sec) starts with: the hero fades into exactly this
        first = p['lines'].split()[0].lstrip('#')
        hf = ','.join(str(int(first[i:i + 2], 16)) for i in (0, 2, 4))
        out.append('%s{--deep:%s;--sand:%s;--hop:%s;--hf:%s}' % (s, p['deep'], p['sand'], p['hop'], hf))
        out.append('%s .lines-sec{background:linear-gradient(180deg,%s)}' % (s, p['lines']))
        out.append('%s .lines-sec .a{background:%s}%s .lines-sec .b{background:%s}%s .lines-sec .c{background:%s}' % (s, p['orb'][0], s, p['orb'][1], s, p['orb'][2]))
        out.append('%s .market{background:%s,linear-gradient(180deg,%s 0%%,%s 55%%,%s 100%%);background-size:240px 240px,auto}' % (s, PAT[th], p['sand'], p['paper'], p['sand']))
        out.append('%s .about-sec{background:%s,linear-gradient(180deg,%s 0%%,%s 100%%);background-size:240px 240px,auto}' % (s, PAT[th], p['about'][0], p['about'][1]))
        out.append('%s .visit-sec{background:%s,linear-gradient(180deg,%s 0%%,%s 100%%);background-size:240px 240px,auto}' % (s, PAT[th], p['visit'][0], p['visit'][1]))
        out.append('%s .scal::before{background:var(--deep);-webkit-mask:var(--scal) 0 0/260px 30px repeat-x;mask:var(--scal) 0 0/260px 30px repeat-x}' % s)
        out.append('%s .deep::before{background:var(--sand);-webkit-mask:var(--scal) 0 0/260px 30px repeat-x;mask:var(--scal) 0 0/260px 30px repeat-x}' % s)
        out.append('%s .deep::after{background:radial-gradient(700px 420px at 85%% 20%%,%s,transparent 70%%),radial-gradient(520px 380px at 5%% 90%%,%s,transparent 70%%)}' % (s, p['deepglow'][0], p['deepglow'][1]))
        out.append('%s footer{background:%s}' % (s, p['footer']))
        out.append('%s .tabs .tab[aria-selected="true"]{background:var(--deep);border-color:var(--deep)}' % s)
        out.append('%s .card:hover{box-shadow:0 18px 36px -22px rgba(%s)}' % (s, p['hover']))
    leaves = leaves_strip()
    ice = icicles_strip()
    g0, g1, g2 = garland_parts()
    out.append('html[data-theme=autumn] .sdeco{display:block;top:-12px;height:84px;z-index:3}')
    out.append('html[data-theme=autumn] .sdeco .d0{background-image:%s;background-size:720px 84px}' % leaves)
    out.append('html[data-theme=winter] .sdeco{display:block;top:14px;height:72px;z-index:1}')
    out.append('html[data-theme=winter] .sdeco .d0{background-image:%s;background-size:640px 72px}' % ice)
    out.append('html[data-theme=newyear] .sdeco{display:block;top:14px;height:78px;z-index:1}')
    out.append('html[data-theme=newyear] .sdeco .d0{background-image:%s;background-size:360px 78px}' % g0)
    out.append('html[data-theme=newyear] .sdeco .d1{background-image:%s;background-size:360px 78px;animation:sblink 2.8s ease-in-out infinite}' % g1)
    out.append('html[data-theme=newyear] .sdeco .d2{background-image:%s;background-size:360px 78px;animation:sblink 2.8s ease-in-out -1.4s infinite}' % g2)
    out.append('@keyframes sblink{0%,100%{opacity:.2}50%{opacity:1}}')
    out.append('html[data-fx=lite] .sdeco i{animation:none!important;opacity:.7}html[data-fx=lite] .sdeco .d0{opacity:1}')
    out.append('@media (prefers-reduced-motion:reduce){.sdeco i{animation:none!important;opacity:.7}.sdeco .d0{opacity:1}}')
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    c = css()
    print(len(c), 'bytes')
