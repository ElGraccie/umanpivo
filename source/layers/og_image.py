"""Share picture for Google/Telegram/Viber/Facebook (1200x630): the summer hero of the clean site, no watermark.
Usage: python3 source/layers/og_image.py   (needs the clean build: python3 source/build_site.py --clean /tmp/x/index.html)"""
import os, sys, subprocess, tempfile, time, io, shutil
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
tmp = tempfile.mkdtemp()
subprocess.run([sys.executable, os.path.join(ROOT, 'source', 'build_site.py'), '--clean', os.path.join(tmp, 'index.html')], check=True, stdout=subprocess.DEVNULL)
os.symlink(os.path.join(ROOT, 't'), os.path.join(tmp, 't'))
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8791', '--bind', '127.0.0.1', '--directory', tmp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(.8)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--disable-gpu'])
        ctx = b.new_context(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
        ctx.add_init_script("try{sessionStorage.setItem('adult','1');localStorage.setItem('up-theme2','classic');localStorage.setItem('up-fx-test','on')}catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8791/index.html'); pg.wait_for_timeout(3500)
        pg.add_style_tag(content='.themes,.hero .plate,.hero .acts{display:none!important}')
        pg.wait_for_timeout(400)
        im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
        b.close()
finally:
    srv.terminate(); shutil.rmtree(tmp, ignore_errors=True)
out = os.path.join(ROOT, 'og-image.jpg')
im.save(out, quality=86, optimize=True, progressive=True)
print(out, im.size, os.path.getsize(out) // 1024, 'KB')
