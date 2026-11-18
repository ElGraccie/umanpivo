import json, base64, io, urllib.parse
from bakelib import browser, shot
from PIL import Image
MARK='<path d="M115.4 115.4H0V0h115.4v115.4zM2 113.4h111.4V2H2v111.4z"/><path d="M84.8 26.3v2L71.9 72.9c-4.4 14.5-11.3 21.6-21.6 21.6-8.2 0-13.8-4.5-13.8-12.6 0-6.3 5.1-11 13.4-11.7L34.4 32.7l-3.8-4.4v-2h18.1l14 46.3-1 1.8h-4.9c-4.8 0-8.4 1.8-8.4 6.3 0 3.6 2.3 5.8 5.6 5.8 5.5 0 10.3-7.7 12.1-18.6l5.7-35.4-3.8-4.3v-1.9h16.8z"/>'
def svg(extra='', fg='#FFC72C', bg='#1b1306'):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-9 -6 133.4 130"><rect x="-9" y="-6" width="133.4" height="130" rx="22" fill="%s"/><g fill="%s">%s</g>%s</svg>'%(bg,fg,MARK,extra))
EX={
 'classic':'',
 'autumn':'<g transform="translate(96 14) rotate(28)"><path d="M0 0C10 -20 36 -20 50 0C36 20 10 20 0 0Z" fill="#e0661e"/><path d="M2 0H46" stroke="#7a2a0c" stroke-width="3" fill="none"/><path d="M-8 3L2 0" stroke="#7a2a0c" stroke-width="3.4" stroke-linecap="round"/></g>',
 'winter':'<clipPath id="cp"><rect x="-9" y="-6" width="133.4" height="130" rx="22"/></clipPath><g clip-path="url(#cp)"><path d="M-9 -6H124.4V6c-6 0-9 6-16 6-6 0-8-5-14-5-7 0-8 8-17 8-7 0-9-6-15-6-8 0-9 7-18 7-7 0-9-6-15-6-8 0-9 7-17 7-6 0-8-5-14-5-6 0-8 6-12 6z" fill="#f4f9ff"/><circle cx="104" cy="52" r="4.5" fill="#f4f9ff"/><circle cx="14" cy="96" r="3.6" fill="#f4f9ff"/><circle cx="96" cy="104" r="3" fill="#f4f9ff"/>',
 'newyear':'<g transform="translate(2 18) rotate(14 96 10)"><path d="M70 22C74 -4 98 -16 124 -8C113 0 112 10 116 22Z" fill="#d8252f"/><rect x="64" y="18" width="58" height="15" rx="7.5" fill="#fff"/><circle cx="125" cy="-9" r="8.5" fill="#fff"/></g>',
}
out={}
with browser() as b:
    sheet=Image.new('RGBA',(4*140,150),(60,60,60,255))
    for i,(k,ex) in enumerate(EX.items()):
        s=svg(ex)
        html='<div style="width:128px;height:128px">'+s.replace('<svg ','<svg width="128" height="128" ',1)+'</div>'
        im=shot(b,html,128,128)
        sheet.alpha_composite(im,(i*140+6,6))
        sm=im.resize((32,32),Image.LANCZOS)
        buf=io.BytesIO(); sm.save(buf,'PNG',optimize=True)
        out[k]={'svg':'data:image/svg+xml,'+urllib.parse.quote(s,safe="/:=' ,()"), 'png':'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()}
        sheet.alpha_composite(sm,(i*140+6,134-4)) if False else None
sheet.save('/tmp/favs.png')
json.dump(out,open('favs.json','w'))
print({k:(len(v['svg']),len(v['png'])) for k,v in out.items()})
