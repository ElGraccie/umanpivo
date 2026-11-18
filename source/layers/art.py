"""Small SVG helpers shared by the art generators."""
import math

def f(v): return str(int(round(v)))
def f1(v): return '%.1f' % v

def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])

def circ(x, y, r, fill=None):
    return '<circle cx="%s" cy="%s" r="%s"%s/>' % (f(x), f(y), f(r), (' fill="%s"' % fill if fill else ''))

def leafp(x, y, a, s, fill, op=1):
    return '<path transform="translate(%s %s) rotate(%s) scale(%s)" d="M0 0C9 -15 33 -15 46 0C33 15 9 15 0 0Z" fill="%s" opacity="%s"/>' % (f1(x), f1(y), f1(a), f1(s), fill, op)

def needle(x, y, a, s, col, op=1):
    return ('<g transform="translate(%s %s) rotate(%s) scale(%s)" stroke="%s" stroke-width="3.4" stroke-linecap="round" fill="none" opacity="%s">'
            '<path d="M0 0L26 -9M0 0L31 -1M0 0L27 9M0 0L17 -15M0 0L19 15"/></g>') % (f1(x), f1(y), f1(a), f1(s * 1.7), col, op)

def stops(l):
    return ''.join('<stop offset="%s" stop-color="%s"/>' % (o, c) for o, c in l)

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rgba(h, a):
    r, g, b = hex2rgb(h)
    return 'rgba(%d,%d,%d,%s)' % (r, g, b, a)

def bauble_defs(prefix='bb'):
    cols = {
        'red':    ('#ff9aa0', '#e0323c', '#7a0f18'),
        'gold':   ('#fff0b8', '#f0b440', '#8a5a10'),
        'blue':   ('#a8c6ff', '#3b6fd8', '#142a66'),
        'silver': ('#ffffff', '#c3cde0', '#5a6784'),
        'green':  ('#b8f0c8', '#2fa862', '#0c4a2a'),
    }
    o = ''
    for k, (a, b, c) in cols.items():
        o += ('<radialGradient id="%s_%s" cx=".36" cy=".3" r=".86"><stop offset="0" stop-color="%s"/><stop offset=".38" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>' % (prefix, k, a, b, c))
    return o

def bauble(x, y, r, col, prefix='bb', thread=0):
    """Christmas ball centered at (x, y) with a cap, loop, specular highlights; optional thread going up."""
    o = ''
    if thread:
        o += '<path d="M%s %s L%s %s" stroke="#d9b052" stroke-width="1.2" opacity=".9"/>' % (f1(x), f1(y - r * 1.3 - thread), f1(x), f1(y - r * 1.3))
    o += '<rect x="%s" y="%s" width="%s" height="%s" rx="1.6" fill="#d9b052"/>' % (f1(x - r * .24), f1(y - r * 1.26), f1(r * .48), f1(r * .32))
    o += '<circle cx="%s" cy="%s" r="%s" fill="url(#%s_%s)"/>' % (f1(x), f1(y), f1(r), prefix, col)
    o += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(-38 %s %s)" fill="#fff" opacity=".78"/>' % (f1(x - r * .36), f1(y - r * .42), f1(r * .3), f1(r * .17), f1(x - r * .36), f1(y - r * .42))
    o += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(-38 %s %s)" fill="#fff" opacity=".28"/>' % (f1(x + r * .34), f1(y + r * .5), f1(r * .22), f1(r * .09), f1(x + r * .34), f1(y + r * .5))
    return o
