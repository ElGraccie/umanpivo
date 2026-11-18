"""Bake classic / autumn / winter layers from the existing generated scene pieces."""
import re, sys, os
from bakelib import browser, shot, save

SRC = {'classic': 'out_sunset', 'autumn': 'out_autumn', 'winter': 'out_winter'}
OUTDIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 't'))

RAYS = ("conic-gradient(from 8deg,transparent 0 7deg,rgba(255,226,170,.2) 10deg,transparent 15deg 22deg,rgba(255,226,170,.13) 25deg,transparent 31deg 47deg,"
        "rgba(255,226,170,.2) 51deg,transparent 58deg 80deg,rgba(255,226,170,.12) 84deg,transparent 90deg 140deg,rgba(255,226,170,.1) 146deg,transparent 154deg 205deg,"
        "rgba(255,226,170,.12) 211deg,transparent 218deg 250deg,rgba(255,226,170,.16) 256deg,transparent 262deg 292deg,rgba(255,226,170,.2) 297deg,transparent 304deg 330deg,"
        "rgba(255,226,170,.14) 335deg,transparent 342deg)")

CFG = {
 'classic': dict(
    far='blur(3.5px)', mid='blur(2.5px)',
    halo='radial-gradient(circle,rgba(255,226,160,.85) 0,rgba(255,190,110,.5) 13%,rgba(255,150,80,.24) 28%,rgba(255,130,70,.08) 44%,rgba(255,120,60,0) 60%)',
    disc='radial-gradient(circle,#fffdf0 0,#fff3c8 36%,#ffe19a 62%,rgba(255,206,120,.85) 80%,rgba(255,180,90,0) 100%)',
    bokeh='radial-gradient(circle,rgba(255,206,130,.14) 0,rgba(255,206,130,.2) 62%,rgba(255,226,170,.42) 88%,rgba(255,226,170,0) 100%)',
    tb='radial-gradient(ellipse 150px 100% at 60% 0,rgba(255,214,160,.4),transparent 72%),radial-gradient(ellipse 150px 14px at 53% 24%,rgba(255,206,130,.34),transparent 72%),radial-gradient(ellipse 200px 18px at 74% 46%,rgba(255,206,130,.26),transparent 72%)',
    tbl='none', shade_extra=''),
 'autumn': dict(
    far='blur(5px) saturate(.85)', mid='blur(4.5px) saturate(.82)',
    halo='radial-gradient(circle,rgba(255,214,150,.85) 0,rgba(255,170,90,.52) 13%,rgba(255,130,60,.26) 28%,rgba(240,100,50,.09) 44%,rgba(240,100,50,0) 60%)',
    disc='radial-gradient(circle,#fffbea 0,#ffeab8 34%,#ffc77a 62%,rgba(255,170,90,.85) 80%,rgba(255,150,70,0) 100%)',
    bokeh='radial-gradient(circle,rgba(255,190,100,.16) 0,rgba(255,180,90,.22) 62%,rgba(255,210,140,.46) 88%,rgba(255,210,140,0) 100%)',
    tb='radial-gradient(ellipse 150px 100% at 60% 0,rgba(255,214,160,.4),transparent 72%),radial-gradient(ellipse 150px 14px at 53% 24%,rgba(255,206,130,.34),transparent 72%),radial-gradient(ellipse 200px 18px at 74% 46%,rgba(255,206,130,.26),transparent 72%)',
    tbl='none', shade_extra=''),
 'winter': dict(
    far='blur(5px)', mid='blur(3.6px)',
    halo='radial-gradient(circle,rgba(255,232,200,.85) 0,rgba(255,196,160,.5) 13%,rgba(244,160,150,.24) 28%,rgba(220,140,160,.09) 44%,rgba(200,130,170,0) 60%)',
    disc='radial-gradient(circle,#fffdf6 0,#fff1dc 34%,#ffd6b4 62%,rgba(255,190,150,.85) 80%,rgba(255,170,130,0) 100%)',
    bokeh='radial-gradient(circle,rgba(230,240,255,.12) 0,rgba(230,240,255,.18) 62%,rgba(255,244,230,.4) 88%,rgba(255,244,230,0) 100%)',
    tb='radial-gradient(ellipse 150px 100% at 60% 0,rgba(255,226,200,.34),transparent 72%),radial-gradient(ellipse 150px 14px at 53% 24%,rgba(255,226,200,.28),transparent 72%),radial-gradient(ellipse 200px 18px at 74% 46%,rgba(255,226,200,.22),transparent 72%)',
    tbl='saturate(.72) brightness(.96)', shade_extra=''),
}

SNOWDUST = ("radial-gradient(ellipse 170px 11px at 8% 4%,rgba(248,252,255,.78),transparent 72%),radial-gradient(ellipse 230px 12px at 27% 3%,rgba(248,252,255,.7),transparent 72%),"
  "radial-gradient(ellipse 160px 10px at 47% 4%,rgba(248,252,255,.6),transparent 72%),"
  "radial-gradient(2px 2px at 12% 40%,#fff,transparent),radial-gradient(1.6px 1.6px at 22% 62%,#fff,transparent),radial-gradient(2px 2px at 41% 30%,#fff,transparent),"
  "radial-gradient(1.6px 1.6px at 33% 80%,#fff,transparent),radial-gradient(2px 2px at 5% 56%,#fff,transparent),radial-gradient(1.6px 1.6px at 47% 74%,#fff,transparent)")

def grab(s, pat):
    m = re.search(pat, s, re.S)
    assert m, pat
    return m.group(0)

def bake(b, name):
    c = CFG[name]; d = SRC[name]; out = f'{OUTDIR}/{name}'
    sc = open(f'{d}/scene.html').read(); tab = open(f'{d}/table.html').read(); br = open(f'{d}/branch.html').read(); sh = open(f'{d}/shade.html').read()
    defs = grab(sc, r'<svg width="0".*?</svg>')
    far = grab(sc, r'<svg class="land far".*?</svg>'); mid = grab(sc, r'<svg class="land mid".*?</svg>')
    fga = grab(sc, r'<svg class="fgA".*?</svg>'); fgb = grab(sc, r'<svg class="fgB".*?</svg>')
    bok = grab(sc, r'<div class="bokeh">.*?</div>')
    sizes = {}
    # ---- far / mid : 1600x520 frame, 40px margin for blur
    M = 40
    for key, svg, flt, sc_ in (('far', far, c['far'], .5), ('mid', mid, c['mid'], .62)):
        html = defs + f'<div style="position:absolute;left:{M}px;top:{M}px;width:1600px;height:520px">' + svg.replace('class="land', 'style="display:block;width:1600px;height:520px;overflow:visible;filter:%s" class="land' % flt, 1) + '</div>'
        im = shot(b, html, 1600, 520, margin=M)
        sizes[key] = save(im, f'{out}/{key}.webp', scale=sc_, q=72, aq=80)
    # ---- fgA / fgB : 1600x900
    for key, svg, flt, sc_ in (('fga', fga, 'blur(11px)', .4), ('fgb', fgb, 'blur(4.5px)', .6)):
        html = '<div style="position:absolute;left:60px;top:60px;width:1600px;height:900px">' + svg.replace('class="fg', 'style="display:block;width:1600px;height:900px;overflow:visible;filter:%s" class="fg' % flt, 1) + '</div>'
        im = shot(b, html, 1600, 900, margin=60)
        sizes[key] = save(im, f'{out}/{key}.webp', scale=sc_, q=70, aq=78)
    # ---- bokeh : frame 1600x810 inside a 1600x950 hero-like box (th=190, lh=540)
    bkcss = ('.bokeh{position:absolute;inset:0}.bk{position:absolute;border-radius:50%%;background:%s;filter:blur(.8px)}' % c['bokeh'])
    html = '<style>' + bkcss + '</style><div style="position:relative;width:1600px;height:950px;--th:190px;--lh:540px">' + bok + '</div>'
    im = shot(b, html, 1600, 810)
    sizes['bok'] = save(im, f'{out}/bok.webp', scale=.5, q=72, aq=80)
    # ---- sun : 1700 square
    S = 1700
    sun = (f'<div style="position:relative;width:{S}px;height:{S}px">'
           f'<div style="position:absolute;inset:0;border-radius:50%;opacity:.8;filter:blur(7px);background:{RAYS};-webkit-mask-image:radial-gradient(circle,#000 5%,transparent 68%);mask-image:radial-gradient(circle,#000 5%,transparent 68%)"></div>'
           f'<div style="position:absolute;left:50%;top:50%;width:1598px;height:1598px;margin:-799px 0 0 -799px;border-radius:50%;background:{c["halo"]};opacity:.94"></div>'
           f'<div style="position:absolute;left:50%;top:50%;width:470px;height:470px;margin:-235px 0 0 -235px;border-radius:50%;background:{c["disc"]};filter:blur(2px)"></div>'
           f'<div style="position:absolute;left:50%;top:50%;width:1300px;height:7px;margin:-3.5px 0 0 -650px;border-radius:50%;background:radial-gradient(ellipse at center,rgba(255,236,190,.65) 0,rgba(255,210,140,.22) 38%,transparent 70%);filter:blur(3px)"></div></div>')
    im = shot(b, sun, S, S)
    sizes['sun'] = save(im, f'{out}/sun.webp', scale=.45, q=72, aq=80, noise=.4)
    # ---- table 1600x190 (+ lying leaves, highlights, lip, snow dust)
    tcss = ('.t{position:relative;width:1600px;height:190px;overflow:hidden;isolation:isolate}.t>svg.tbl{position:absolute;inset:0;width:100%%;height:100%%;display:block;filter:%s}'
            '.t .lay{position:absolute;z-index:2;height:auto;opacity:.92;filter:blur(.5px) drop-shadow(1px 2px 2px rgba(10,3,0,.55))}'
            '.t .tb{position:absolute;inset:0;z-index:1;mix-blend-mode:screen;background:%s}'
            '.t .sd{position:absolute;inset:0;z-index:2;background:%s}'
            '.t .lip{position:absolute;left:0;right:0;top:0;height:3px;z-index:3;background:linear-gradient(90deg,rgba(255,200,130,.12),rgba(255,222,170,.8) 60%%,rgba(255,200,130,.12));filter:blur(.5px)}') % (c['tbl'], c['tb'], SNOWDUST if name == 'winter' else 'none')
    html = '<style>' + tcss + '</style><div class="t">' + tab + '<div class="tb"></div><div class="sd"></div><div class="lip"></div></div>'
    im = shot(b, html, 1600, 190)
    sizes['table'] = save(im, f'{out}/table.webp', q=80, opaque=True)
    # ---- tshade : 640x190, blurred, faded in from the left
    m = re.search(r'<svg class="tshade".*?</svg>', sh, re.S).group(0)
    m = m.replace('class="tshade"', 'style="display:block;width:640px;height:190px;filter:blur(3.5px)"')
    im = shot(b, '<div style="position:absolute;left:20px;top:20px">' + m + '</div>', 640, 190, margin=20)
    sizes['tshade'] = save(im, f'{out}/tshade.webp', scale=.6, q=70, aq=76)
    # ---- branch : 980x215 + 30px margin
    B = 30
    c1 = grab(br, r'<svg class="c1".*?</svg>'); c2 = grab(br, r'<svg class="c2".*?</svg>')
    c1 = c1.replace('class="c1"', 'style="position:absolute;inset:0;width:980px;height:215px;display:block;overflow:hidden;filter:blur(2.6px) drop-shadow(0 0 10px rgba(255,150,60,.35));-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 16%);mask-image:linear-gradient(90deg,transparent 0,#000 16%)"')
    c2 = c2.replace('class="c2"', 'style="position:absolute;inset:0;width:980px;height:215px;display:block;overflow:hidden;filter:blur(10px)"')
    html = f'<div style="position:absolute;left:{B}px;top:{B}px;width:980px;height:215px">' + c1 + c2 + '</div>'
    im = shot(b, html, 980 + 2 * B, 215 + 2 * B)
    sizes['branch'] = save(im, f'{out}/branch.webp', q=82, aq=88)
    tot = sum(v[0] for v in sizes.values())
    print(name, {k: (v[0] // 1024, v[1]) for k, v in sizes.items()}, 'TOTAL KB', tot // 1024)

if __name__ == '__main__':
    names = sys.argv[1:] or list(SRC)
    with browser() as b:
        for n in names:
            bake(b, n)
