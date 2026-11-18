"""Static tab icon (the Уманьпиво mark) as real files next to index.html.
Data-URL favicons swapped by JS per theme disappear in Safari, so the icon is one set of files for every theme."""
import io, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from bakelib import browser, shot
from PIL import Image
from favs_mark import svg
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
s = svg()
open(f'{ROOT}/favicon.svg', 'w').write(s)
with browser() as b:
    big = shot(b, '<div style="width:512px;height:512px">' + s.replace('<svg ', '<svg width="512" height="512" ', 1) + '</div>', 512, 512)
for n, name in ((32, 'favicon-32.png'), (180, 'apple-touch-icon.png'), (192, 'icon-192.png')):
    im = big.resize((n, n), Image.LANCZOS)
    if name == 'apple-touch-icon.png':      # iOS draws its own rounded corners: give it a full square
        bg = Image.new('RGBA', (n, n), (27, 19, 6, 255)); bg.alpha_composite(im); im = bg
    im.save(f'{ROOT}/{name}', optimize=True)
big.resize((48, 48), Image.LANCZOS).save(f'{ROOT}/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
print({f: os.path.getsize(f'{ROOT}/{f}') for f in ('favicon.svg', 'favicon-32.png', 'apple-touch-icon.png', 'icon-192.png', 'favicon.ico')})
