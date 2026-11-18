"""Soft glows without CSS `filter`.

iOS 26.4 Safari draws a spurious black square in the top-left corner of the page when an element that is
below the first screen has a CSS `filter` (WebKit bug 314999). The square is as large as the filter outset
(blur(90px) -> 253px). So the page must not use `filter` on anything that can be off-screen on load.
A blurred disc is a radial gradient: this module computes its exact radial profile, so the look stays the same.

A disc of radius R blurred with a Gaussian of std-dev S is radially symmetric: its value at distance r from
the centre is  f(r) = 1 - Q1(r/S, R/S)  (Marcum Q), computed here by numerical integration. The gradient box
reaches R + 3S from the centre, where f is < 0.2% of the peak, so the box edge is invisible.
"""
import re
import numpy as np
from scipy.special import ive

SIGMA = 90.0                                  # blur(90px) of the section orbs
ORB_D = {'a': 460, 'b': 420, 'c': 440}        # diameters (px) of the three orbs in the lines section
REACH = 3.0                                   # the gradient box extends this many sigmas beyond the disc edge


def profile(ratio, n=21):
    """[(position 0..1 from the centre to the box edge, value 0..1)] of a Gaussian-blurred disc; ratio = R / sigma."""
    edge = ratio + REACH
    s = np.linspace(0, ratio, 6001)
    out = []
    for i in range(n):
        rho = i / (n - 1)
        r = rho * edge
        # integral over the disc of the 2D Gaussian: exp(-(r^2+s^2)/2) * I0(r*s) = exp(-(r-s)^2/2) * ive(0, r*s)
        v = np.trapezoid(np.exp(-(r - s) ** 2 / 2) * ive(0, r * s) * s, s)
        out.append((rho, float(v)))
    return out


def num(x):
    t = ('%.3f' % x).rstrip('0').rstrip('.')
    return t if t else '0'


def pos(rho):
    return '0' if rho == 0 else '%s%%' % num(rho * 100)


def gradient(color, alpha, ratio, n=21):
    """radial-gradient() equal to a disc of opacity `alpha` blurred as above. `color` is 'r,g,b' or 'var(--x)'."""
    stops = ['rgba(%s,%s) %s' % (color, num(alpha * v), pos(rho)) for rho, v in profile(ratio, n)]
    return 'radial-gradient(closest-side,' + ','.join(stops) + ')'


def rgba_parts(c):
    m = re.match(r'rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+))?\s*\)', c)
    r, g, b = (int(float(m.group(i))) for i in (1, 2, 3))
    a = float(m.group(4)) if m.group(4) else 1.0
    return r, g, b, a


def orb_ratio(key):
    return ORB_D[key] / 2 / SIGMA


def orb_side(key):
    """side (px) of the square that carries the orb gradient"""
    return int(round(2 * (ORB_D[key] / 2 + REACH * SIGMA)))


def orb(key, rgba, n=21):
    """gradient for orb 'a' | 'b' | 'c' given the colour the old blurred disc had, e.g. 'rgba(246,182,39,.32)'"""
    r, g, b, a = rgba_parts(rgba)
    return gradient('%d,%d,%d' % (r, g, b), a, orb_ratio(key), n)


def orb_geometry():
    """CSS for the three orbs: same centres as the old blurred discs, boxes enlarged so the gradient fits"""
    sa, sb, sc = (orb_side(k) for k in 'abc')
    ha, hb, hc = sa // 2, sb // 2, sc // 2
    da, db, dc = ORB_D['a'] // 2, ORB_D['b'] // 2, ORB_D['c'] // 2
    return (
        # a: was left:-120px; top:22%  (460px)  -> centre x = -120 + 230, centre y = 22% + 230
        '.lines-sec .a{width:%dpx;height:%dpx;left:%dpx;top:calc(22%% - %dpx)}\n' % (sa, sa, -120 + da - ha, ha - da) +
        # b: was left:40%; bottom:-140px (420px) -> centre x = 40% + 210, centre y = 70px above the bottom edge
        '.lines-sec .b{width:%dpx;height:%dpx;left:calc(40%% - %dpx);bottom:%dpx}\n' % (sb, sb, hb - db, -(hb - (db - 140))) +
        # c: was right:-120px; top:8% (440px) -> centre x = 100px left of the right edge, centre y = 8% + 220
        '.lines-sec .c{width:%dpx;height:%dpx;right:%dpx;top:calc(8%% - %dpx)}\n' % (sc, sc, -(hc - (dc - 120)), hc - dc))


def panel(alpha=.5, ratio=2.8, n=21):
    """glow of a category panel; colour comes from the --cr custom property ('r,g,b')"""
    return gradient('var(--cr)', alpha, ratio, n)


if __name__ == '__main__':
    print(orb_geometry())
    print(orb('a', 'rgba(246,182,39,.32)'))
    print(panel())
