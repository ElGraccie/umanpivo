"""Helpers for baking SVG/CSS layers into transparent WebP files with headless Chrome."""
import io, os, re, random
from contextlib import contextmanager
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright

@contextmanager
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--disable-gpu'])
        try:
            yield b
        finally:
            b.close()

def shot(browser_, html, w, h, margin=0, wait=120):
    """Render html (body is transparent) and return RGBA PIL image of the w*h box at (margin, margin)."""
    pg = browser_.new_page(viewport={'width': int(w + 2 * margin), 'height': int(h + 2 * margin)})
    try:
        pg.set_content('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent}</style></head><body>' + html + '</body></html>')
        pg.wait_for_timeout(wait)
        png = pg.screenshot(clip={'x': margin, 'y': margin, 'width': w, 'height': h}, omit_background=True)
    finally:
        pg.close()
    return Image.open(io.BytesIO(png)).convert('RGBA')

def add_noise(im, sigma=1.1, seed=3):
    """Tiny noise on opaque-ish pixels so wide smooth gradients do not band after lossy encoding."""
    a = np.asarray(im).astype(np.float32)
    rng = np.random.default_rng(seed)
    n = rng.normal(0, sigma, a.shape[:2] + (1,)).astype(np.float32)
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255)
    return Image.fromarray(a.astype(np.uint8), 'RGBA')

def save(im, path, scale=1.0, q=76, aq=82, noise=0, opaque=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if scale != 1.0:
        im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    if noise:
        im = add_noise(im, noise)
    if opaque:
        im = im.convert('RGB')
        im.save(path, 'WEBP', quality=q, method=6)
    else:
        im.save(path, 'WEBP', quality=q, alpha_quality=aq, method=6)
    return os.path.getsize(path), im.size
