"""Assemble the themed site: base index.html (v10) + new hero, theme manager and baked layers."""
import json, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))   # <repo>/source
BASE = f'{HERE}/base/index.html'                   # базова сторінка (v10): каталог, BeerBox, фото
SRC = f'{HERE}/src'                                # CSS/JS шапки, теми, favicon-и
OUT = os.path.dirname(HERE)                        # корінь репозиторію: сюди пишеться index.html, тут лежить t/
s = open(BASE, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:70], s.count(old))
    s = s.replace(old, new)

def rd(name):
    return open(f'{SRC}/{name}', encoding='utf-8').read()

THEMES = {
    'spring':  {'n': 'Весна',    'l': 'sun far mid fga fgb bok table tshade branch'},
    'classic': {'n': 'Літо', 'l': 'sun far mid fga fgb bok table tshade branch'},
    'autumn':  {'n': 'Осінь',    'l': 'sun far mid fga fgb bok table tshade branch'},
    'winter':  {'n': 'Зима',     'l': 'sun far mid fga fgb bok table tshade branch'},
    'newyear': {'n': 'Новий рік', 'l': 'sun far mid fga fgb bok table tshade branch garland gl1 gl2 gl3 bgl1 bgl2'},
}
# only list layers that really exist on disk
for t, v in THEMES.items():
    have = [k for k in v['l'].split() if os.path.exists(f'{OUT}/t/{t}/{k}.webp')]
    v['l'] = ' '.join(have)

# ------------------------------------------------------------------ particles
def snow(n=28, seed=5):
    R = random.Random(seed); o = []
    for i in range(n):
        sz = R.choice([2, 2, 3, 3, 4, 5, 6, 8])
        o.append('<i style="--l:%d%%;--s:%dpx;--t:%ds;--dl:-%ds;--o:%.2f;--sw:%dpx"></i>' % (R.randint(0, 100), sz, R.randint(9, 22), R.randint(0, 22), R.uniform(.5, .95), R.choice([-44, -26, 26, 44])))
    return '<div class="fx fx-snow">' + ''.join(o) + '</div>'

def leaves(n=9, seed=34):
    R = random.Random(seed); cols = ['#e0661e', '#f0922a', '#c8421a', '#f4b232', '#b0301a', '#d8a028']; o = []
    for i in range(n):
        o.append('<svg viewBox="-4 -16 54 32" style="left:%.0f%%;width:%dpx;animation-duration:%ds;animation-delay:-%ds"><path d="M0 0C9 -15 33 -15 46 0C33 15 9 15 0 0Z" fill="%s"/></svg>' % (R.uniform(3, 97), R.uniform(16, 34), R.randint(16, 30), R.randint(0, 28), R.choice(cols)))
    return '<div class="fx fx-leaves">' + ''.join(o) + '</div>'

def petals(n=12, seed=303):
    """spring: blossom petals drifting down"""
    R = random.Random(seed); cols = ['#fbe2ea', '#f6c4d4', '#ffffff', '#f2aec4', '#fde9ef']; o = []
    for i in range(n):
        o.append('<svg viewBox="-12 -9 24 18" style="left:%.0f%%;width:%dpx;animation-duration:%ds;animation-delay:-%ds"><path d="M-11 0C-7 -9 6 -9 11 -2C7 1 7 3 11 3C5 9 -7 8 -11 0Z" fill="%s"/></svg>' % (
            R.uniform(2, 98), R.uniform(10, 18), R.randint(14, 26), R.randint(0, 26), R.choice(cols)))
    return '<div class="fx fx-petals">' + ''.join(o) + '</div>'

def fireflies(n=9, seed=12):
    R = random.Random(seed); o = []
    for i in range(n):
        def d(): return '%dpx' % R.randint(-70, 70)
        o.append('<i style="--x:%d%%;--y:%.2f;--s:%dpx;--t:%ds;--b:%ds;--dl:-%ds;--ax:%s;--ay:%s;--bx:%s;--by:%s;--cx:%s;--cy:%s"></i>' % (
            R.randint(6, 94), R.uniform(.04, .7), R.choice([14, 18, 22, 28]), R.randint(12, 22), R.randint(3, 7), R.randint(0, 20), d(), d(), d(), d(), d(), d()))
    return '<div class="fx fx-fly">' + ''.join(o) + '</div>'

def stars_css_and_html(seed=77):
    R = random.Random(seed)
    def layer(n, big):
        g = []
        for _ in range(n):
            x, y = R.uniform(1, 99), R.uniform(1, 52)
            r = R.uniform(1.0, 1.7) if not big else R.uniform(1.6, 2.4)
            g.append('radial-gradient(%.1fpx %.1fpx at %.1f%% %.1f%%,rgba(255,255,255,%.2f),transparent)' % (r, r, x, y, R.uniform(.7, 1)))
        return ','.join(g)
    css = ('.fx-stars i{inset:0 0 40% 0}.fx-stars .s1{background:@A@;animation:tw 4.5s ease-in-out infinite alternate}'
           '.fx-stars .s2{background:@B@;animation:tw 6s ease-in-out -2s infinite alternate}@keyframes tw{from{opacity:.25}to{opacity:1}}').replace('@A@', layer(34, False)).replace('@B@', layer(16, True))
    return css, '<div class="fx fx-stars"><i class="s1"></i><i class="s2"></i></div>'

def fireworks_css_and_html():
    def burst(col, r1=64, r2=108, n=16):
        import math
        sh = []
        for i in range(n):
            a = 2 * math.pi * i / n
            sh.append('%dpx %dpx 2px 1px %s' % (round(math.cos(a) * r1), round(math.sin(a) * r1), col))
        for i in range(n):
            a = 2 * math.pi * (i + .5) / n
            sh.append('%dpx %dpx 2px 0 %s' % (round(math.cos(a) * r2), round(math.sin(a) * r2), col))
        return ','.join(sh)
    css = ('.fx-fw .fw{width:5px;height:5px;border-radius:50%;opacity:0;animation:fw 8s ease-out var(--dl) infinite}'
           '.fx-fw .f1{left:86%;top:29%;--dl:-1s;background:#ffd66b;box-shadow:' + burst('#ffd66b') + '}'
           '.fx-fw .f2{left:50%;top:15%;--dl:-4.5s;background:#ff8fc4;box-shadow:' + burst('#ff8fc4', 52, 90, 14) + '}'
           '.fx-fw .f3{left:96%;top:47%;--dl:-6.5s;background:#8fe3ff;box-shadow:' + burst('#8fe3ff', 48, 82, 14) + '}'
           '@keyframes fw{0%{transform:scale(.1);opacity:0}3%{opacity:1}34%{transform:scale(1.08);opacity:.85}46%{transform:scale(1.14);opacity:0}100%{transform:scale(1.14);opacity:0}}')
    return css, '<div class="fx fx-fw"><i class="fw f1"></i><i class="fw f2"></i><i class="fw f3"></i></div>'

st_css, st_html = stars_css_and_html()
fw_css, fw_html = fireworks_css_and_html()

# ------------------------------------------------------------------ markup
def L(key, cls, d=None, extra=''):
    return '<img class="ly %s" data-l="%s"%s alt="" decoding="async" draggable="false" hidden%s>' % (cls, key, (' data-d="%s"' % d) if d is not None else '', extra)

SKY = ('<div class="sky" aria-hidden="true"><div class="sk"></div><div class="cl c1"></div><div class="cl c2"></div>'
       + st_html + fw_html
       + L('sun', 'sun', 6) + L('far', 'far', 5) + '<div class="haze"></div>' + L('mid', 'mid', 11) + '<div class="fshade"></div><div class="bloom"></div>'
       + L('fgb', 'fgb', 14) + L('fga', 'fga', 18) + L('bok', 'bok', 9)
       + leaves() + petals() + snow() + fireflies()
       + L('garland', 'garland', 12) + L('gl1', 'gl', 12) + L('gl2', 'gl', 12) + L('gl3', 'gl', 12)
       + '<div class="mist"></div><div class="table">' + L('table', 'tbl') + L('tshade', 'tshade') + '</div>'
       + '<div class="vig"></div></div>')
rep('<div class="sky" aria-hidden="true"><div class="ec"><i class="corona"></i><i class="limb"></i><i class="moon"></i></div><i class="dust"></i></div>', SKY)
rep('<header class="hero">', '<header class="hero" id="hero">')
KICK = '<p class="kick" id="kick"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 1.5l2.6 6.9 7.4.4-5.8 4.6 2 7.1L12 16.5 5.8 20.5l2-7.1L2 8.8l7.4-.4z" fill="#ffd66b"/></svg><span></span></p>'
rep('<h1>Пиво, сидр і лимонад <em>з Умані</em></h1>', KICK + '<h1>Пиво, сидр і лимонад <em>з Умані</em></h1>')

SWITCH = ('<div class="themes" role="group" aria-label="Тема оформлення"><span class="th-l">Тема</span>'
          '<button type="button" data-th="spring">Весна</button><button type="button" data-th="classic">Літо</button><button type="button" data-th="autumn">Осінь</button>'
          '<button type="button" data-th="winter">Зима</button><button type="button" data-th="newyear">Новий рік</button>'
          '<button type="button" data-th="auto">Авто</button></div>')
FGC = '<div class="fgC" data-d="22">' + L('branch', '') + L('bgl1', 'bgl') + L('bgl2', 'bgl') + '</div>'
js = rd('theme.js').replace('%THEMES%', json.dumps(THEMES, ensure_ascii=False))
rep('<div role="listitem"><b>Магазини</b><span>Щодня з 10:00 до 22:00</span></div>\n      </div>\n    </div>\n    <div class="stage" id="stage"><div class="floor"></div></div>\n  </div>\n</header>',
    '<div role="listitem"><b>Магазини</b><span>Щодня з 10:00 до 22:00</span></div>\n      </div>\n      ' + SWITCH + '\n    </div>\n    <div class="stage" id="stage"><div class="beams"></div></div>\n  </div>\n  ' + FGC + '\n</header>\n<script>' + js + '</script>')

# bottle: shadow offset var, and the old pointer parallax goes away (new engine lives in theme.js)
rep("--ar:'+(AR[p.ph]||.3)+'\">'", "--ar:'+(AR[p.ph]||.3)+';--sx:'+(((parseFloat(h[2])-56)/30)*24).toFixed(1)+'px;--o:'+Math.max(-1,Math.min(1,Math.round((parseFloat(h[2])-50)/19)))+'\">'")
a = s.index('  /* pointer parallax: bottles turn slightly')
b = s.index('  var L=[')
s = s[:a] + s[b:]

# lazy photo decoding: the base site turned all ~390 product photos into blob URLs at startup (~100 ms desktop,
# ~650 ms on a phone-class CPU). Same IMG[...] reads now convert a photo only when somebody actually asks for it.
rep("(function(){try{Object.keys(IMG).forEach(function(k){var s=IMG[k],i=s.indexOf(','),b=atob(s.slice(i+1)),a=new Uint8Array(b.length);for(var j=0;j<b.length;j++)a[j]=b.charCodeAt(j);IMG[k]=URL.createObjectURL(new Blob([a],{type:'image/webp'}))})}catch(e){}})();",
    "(function(){try{Object.keys(IMG).forEach(function(k){var s=IMG[k],v;Object.defineProperty(IMG,k,{configurable:true,enumerable:true,get:function(){if(v===undefined){try{var i=s.indexOf(','),b=atob(s.slice(i+1)),a=new Uint8Array(b.length);for(var j=0;j<b.length;j++)a[j]=b.charCodeAt(j);v=URL.createObjectURL(new Blob([a],{type:'image/webp'}))}catch(e){v=s}}return v}})})}catch(e){}})();")

# ------------------------------------------------------------------ css
drops = open(f'{SRC}/drops.css').read()
css = rd('hero.css').replace('%DROPS%', drops) + '\n' + rd('themes.css')
ny = rd('newyear.css') if os.path.exists(f'{SRC}/newyear.css') else ''
css = css.replace('/*NEWYEAR*/', ny + st_css + fw_css)
import inner
css += '\n' + inner.css()
rep('</style>', css + '</style>')
rep('<div class="market scal">', '<div class="market scal"><div class="sdeco" aria-hidden="true"><i class="d0"></i><i class="d1"></i><i class="d2"></i></div>')

# ------------------------------------------------------------------ head: favicons, early theme
head = ('<link rel="icon" href="favicon.ico" sizes="48x48"><link rel="icon" type="image/svg+xml" href="favicon.svg"><link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">'
        '<link rel="apple-touch-icon" href="apple-touch-icon.png"><meta name="theme-color" content="#1b1306">'
        '<meta http-equiv="Content-Security-Policy" content="object-src \'none\'; base-uri \'self\'; form-action \'none\'">'
        '<meta name="referrer" content="strict-origin-when-cross-origin">'
        '<script>(function(){var d=document.documentElement,t="classic",p="auto";try{p=localStorage.getItem("up-theme2")||"auto"}catch(e){}'
        'if(p==="auto"){var z=["Europe/Kyiv","Europe/Kiev"],o=null,i;for(i=0;i<z.length&&!o;i++){try{o={};new Intl.DateTimeFormat("en-US",{timeZone:z[i],year:"numeric",month:"numeric",day:"numeric"}).formatToParts(new Date()).forEach(function(q){if(q.type!=="literal")o[q.type]=+q.value});if(!(o.month&&o.day))o=null}catch(e){o=null}}'
        'if(!o){var n=new Date();o={month:n.getMonth()+1,day:n.getDate()}}var m=o.month,x=o.day;t=((m===12&&x>=30)||(m===1&&x<=5))?"newyear":(m===12||m===1||m===2)?"winter":(m>=9&&m<=11)?"autumn":(m>=3&&m<=5)?"spring":"classic"}'
        'else if(/^(spring|classic|autumn|winter|newyear)$/.test(p))t=p;d.setAttribute("data-theme",t)})()</script>')
rep('<title>Уманьпиво. Концепт сайту</title>', '<title>Уманьпиво. Концепт сайту</title>' + head)

os.makedirs(OUT, exist_ok=True)
open(f'{OUT}/index.html', 'w', encoding='utf-8').write(s)
print('built', len(s) // 1024, 'KB;', {t: len(v['l'].split()) for t, v in THEMES.items()})
