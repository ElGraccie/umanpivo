import random, math, os, sys
THEME=sys.argv[1]; OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)
AUT=(THEME=='autumn')
WIN=(THEME=='winter')
R=random.Random(21 if not AUT else (34 if not WIN else 58))
def f(v): return str(int(round(v)))
def f1(v): return '%.1f'%v
def circ(x,y,r,fill=None): return '<circle cx="%s" cy="%s" r="%s"%s/>'%(f(x),f(y),f(r),(' fill="%s"'%fill if fill else ''))
W,H=1600,520
SUNX=960
if WIN:
    FAR=[('0','#e4cfd8'),('.35','#aeaac6'),('1','#7e84a6')]
    MID=[('0','#eef4fb'),('.09','#a3b7cc'),('.3','#35516a'),('1','#0f1c26')]
    PAL=None
    FG='#0d1c20'; FGLIT=['#e6eef6','#c3d4e4','#f2f6fb']
    BR='#2a1e16'
    LIT=['#e4eef6','#cfdeea','#f4f8fc','#bcd0e0']
    DARK=['#17382c','#1f4636','#12302a','#1b3d33']
elif AUT:
    FAR=[('0','#e2ac7c'),('.35','#b98a6c'),('1','#8a6458')]
    MID=[('0','#f0a040'),('.09','#a8481e'),('.3','#5c2a14'),('1','#241008')]
    PAL=['#c9561f','#b03a1c','#dc9a2b','#8a3a18','#e47b26','#7a5a1e','#a02e18']
    FG='#3a140a'; FGLIT=['#c4521c','#d8782a','#a62f18']
    BR='#2c160c'
    LIT=['#e0661e','#f0922a','#c8421a','#f4b232','#b0301a','#d8a028']
    DARK=['#4a1a0c','#5c2410','#3a1608','#52200e']
else:
    FAR=[('0','#c79a8a'),('.35','#9a7a80'),('1','#6e5a68')]
    MID=[('0','#a8683a'),('.09','#5a4130'),('.3','#2f2c24'),('1','#14170f')]
    PAL=None
    FG='#0b0d08'; FGLIT=None
    BR='#0e0d09'
    LIT=['#86922f','#9d8e2b','#718028','#b09a32','#5f7424']
    DARK=['#141b0d','#1a2310','#202b13','#171e0e']
def stops(l): return ''.join('<stop offset="%s" stop-color="%s"/>'%(o,c) for o,c in l)
defs=('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
 '<filter id="rag" x="-4%" y="-12%" width="108%" height="124%"><feTurbulence type="fractalNoise" baseFrequency="0.014 0.03" numOctaves="4" seed="8" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="'+("16" if (AUT or WIN) else "34")+'" xChannelSelector="R" yChannelSelector="G"/></filter>'
 '<linearGradient id="gfar" gradientUnits="userSpaceOnUse" x1="0" y1="230" x2="0" y2="520">'+stops(FAR)+'</linearGradient>'
 '<linearGradient id="gmid" gradientUnits="userSpaceOnUse" x1="0" y1="170" x2="0" y2="520">'+stops(MID)+'</linearGradient>'
 '</defs></svg>')
def canopy(base,amp,step,rmin,rmax,ph,gap=0,pal=None):
    out=[];x=-60
    pick=(lambda: R.choice(pal)) if pal else (lambda: None)
    while x<W+60:
        t=base+amp*(math.sin(x/260+ph)*.55+math.sin(x/97+ph*2)*.3+math.sin(x/41+ph*3)*.25)
        t+=gap*math.exp(-((x-SUNX)/250)**2)
        r=R.uniform(rmin,rmax)
        out.append(circ(x,t+r*.55,r,pick()))
        out.append(circ(x+step/2,t+r*.95,r*.9,pick()))
        for _ in range(3): out.append(circ(x+R.uniform(-step,step),t+R.uniform(-4,r*.5),R.uniform(5,12),pick()))
        x+=step
    out.append('<rect x="-60" y="%s" width="%d" height="%d"%s/>'%(f(base+amp+40),W+120,H,(' fill="#3a1a0e"' if AUT else '')))
    return ''.join(out)
def land(cls,inner,fill):
    return '<svg class="land %s" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMax slice" fill="%s"><g filter="url(#rag)">%s</g></svg>'%(cls,W,H,fill,inner)
def spruce(cx,base,h,w):
    n=7;r=[];l=[]
    for i in range(n):
        y=base-h+h*(i+1)/n*0.94
        wi=w*(0.2+0.8*(i+1)/n)
        yi=base-h+h*i/n*0.94+h/n*0.28
        r+=[(cx+wi*.5,yi),(cx+wi,y)]
        l=[(cx-wi,y),(cx-wi*.5,yi)]+l
    pts=[(cx,base-h)]+r+[(cx+w*.08,base+10),(cx-w*.08,base+10)]+l
    return '<path d="M'+' L'.join('%s %s'%(f(a),f(b)) for a,b in pts)+' Z"/>'
def spruces():
    out=[];x=-40
    while x<W+60:
        dist=abs(x-SUNX)/380;k=.5+.5*min(1,dist)
        h=R.uniform(190,330)*k+30
        w=h*R.uniform(.2,.28)
        out.append(spruce(x,H+10,h,w))
        x+=R.uniform(24,52)
    out.append('<rect x="-60" y="430" width="%d" height="120"/>'%(W+120))
    return ''.join(out)
far=land('far',canopy(292,26,24,30,52,.6,gap=30),'url(#gfar)')
mid=land('mid',(spruces() if WIN else canopy(245,38,19,34,66,2.1,gap=60,pal=PAL)),'url(#gmid)')
# ---- foreground foliage + thin branches (top)
CW,CH=1600,900
def leaf(cx,cy,sz,fill=None):
    return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(%s %s %s)"%s/>'%(f(cx),f(cy),f(sz*R.uniform(.8,1.5)),f(sz*R.uniform(.35,.6)),f(R.uniform(0,180)),f(cx),f(cy),(' fill="%s"'%fill if fill else ''))
def cloud(cx,cy,rx,ry,n,sz):
    o=[]
    for _ in range(n):
        a=R.uniform(0,6.283);d=math.sqrt(R.random())**.7
        fl=R.choice(FGLIT) if (FGLIT and R.random()<.4) else None
        o.append(leaf(cx+math.cos(a)*rx*d,cy+math.sin(a)*ry*d,sz,fl))
    o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s"/>'%(f(cx),f(cy),f(rx*.8),f(ry*.78)))
    return ''.join(o)
def bez(p0,p1,p2,p3,t):
    u=1-t
    return (u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0], u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1])
def tbranch(p0,p1,p2,p3,w):
    o='<path d="M%s %s C%s %s %s %s %s %s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>'%(f(p0[0]),f(p0[1]),f(p1[0]),f(p1[1]),f(p2[0]),f(p2[1]),f(p3[0]),f(p3[1]),BR,f(w))
    for i in range(1,15):
        t=i/14;x,y=bez(p0,p1,p2,p3,t)
        for _ in range(6):
            fl=R.choice(FGLIT) if (FGLIT and R.random()<.4) else None
            o+=leaf(x+R.uniform(-26,26),y+R.uniform(-18,26),R.uniform(8,15),fl)
    return o
fgA=('<svg class="fgA" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice" fill="%s">'%(CW,CH,FG)+
  cloud(30,20,400,150,560,22)+cloud(210,150,150,80,120,18)+cloud(1590,20,430,180,600,22)+cloud(1470,200,190,100,150,18)+cloud(700,-30,170,60,100,18)+cloud(1160,-20,170,64,110,18)+'</svg>')
fgB=('<svg class="fgB" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice" fill="%s">'%(CW,CH,BR)+
  tbranch((360,70),(560,40),(760,140),(900,290),11)+tbranch((1260,60),(1170,90),(1050,170),(960,300),10)+tbranch((1560,330),(1420,330),(1260,360),(1130,400),9)+'</svg>')
# ---- bokeh
bk=''
for i in range(22):
    sz=R.uniform(16,52)
    if i%3==0: x,y=R.uniform(52,96),R.uniform(60,92)
    else: x,y=R.uniform(4,98),R.uniform(56,92)
    bk+='<i class="bk" style="left:%.1f%%;bottom:calc(var(--th) + var(--lh) * %.2f);width:%dpx;height:%dpx;opacity:%.2f;animation-delay:-%ds;animation-duration:%ds"></i>'%(x,(y-40)/48,sz,sz,R.uniform(.35,.9),R.randint(0,20),R.randint(16,30))
# ---- falling leaves (autumn only)
fall=''
if AUT:
    for i in range(9):
        c=R.choice(LIT);sz=R.uniform(16,34);bl=R.random()<.5
        fall+='<svg class="fall" viewBox="-4 -16 54 32" style="left:%.0f%%;width:%dpx;animation-duration:%ds;animation-delay:-%ds;%s"><path d="M0 0C9 -15 33 -15 46 0C33 15 9 15 0 0Z" fill="%s"/></svg>'%(R.uniform(3,97),sz,R.randint(16,30),R.randint(0,28),'filter:blur(2.5px);' if bl else '',c)
snow=''
if WIN:
    for i in range(54):
        sz=R.choice([2,2,3,3,4,5,7]);bl=sz>=5 and 'filter:blur(2px);' or ('filter:blur(.6px);' if sz>=4 else '')
        snow+='<i class="sf" style="left:%.0f%%;width:%dpx;height:%dpx;animation-duration:%ds;animation-delay:-%ds;opacity:%.2f;%s"></i>'%(R.uniform(0,100),sz,sz,R.randint(9,24),R.randint(0,24),R.uniform(.5,.95),bl)
# ---- table
TW,TH=1600,190
hs=[12*1.2**i for i in range(8)];s=sum(hs);hs=[h*TH/s for h in hs]
y=0;pl=[]
cols=['#8d6038','#7e5231','#966941','#855a37','#76492a','#916340','#7c502f','#9a6c44']
for i,h in enumerate(hs):
    pl.append('<rect x="0" y="%.1f" width="%d" height="%.1f" fill="%s"/>'%(y,TW,h,cols[(i*3+1)%len(cols)]))
    jx=R.uniform(150,TW-150)
    for jj in (jx,(jx+R.uniform(500,900))%TW):
        pl.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#241208" opacity=".5"/>'%(jj,y,1.1+i*.2,h))
    pl.append('<rect x="0" y="%.1f" width="%d" height="%.1f" fill="#1d0e06" opacity=".7"/>'%(y+h-1.4-i*.25,TW,1.4+i*.25))
    pl.append('<rect x="0" y="%.1f" width="%d" height="1" fill="#ffd9a0" opacity=".14"/>'%(y,TW))
    y+=h
table=('<svg class="tbl" viewBox="0 0 %d %d" preserveAspectRatio="none"><defs>'
 '<filter id="wg" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency="0.0018 0.2" numOctaves="5" seed="5"/><feColorMatrix type="matrix" values="0 0 0 0 .11  0 0 0 0 .05  0 0 0 0 .015  2.1 0 0 0 -.72"/></filter>'
 '<filter id="wg2" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency="0.0026 0.11" numOctaves="4" seed="17"/><feColorMatrix type="matrix" values="0 0 0 0 .86  0 0 0 0 .62  0 0 0 0 .38  1.6 0 0 0 -.78"/></filter>'
 '<linearGradient id="tsh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb86a" stop-opacity=".42"/><stop offset=".4" stop-color="#ff9a48" stop-opacity=".1"/><stop offset="1" stop-color="#140a04" stop-opacity=".8"/></linearGradient></defs>'
 '%s<rect width="%d" height="%d" filter="url(#wg)" opacity=".95"/><rect width="%d" height="%d" filter="url(#wg2)" opacity=".4"/><rect width="%d" height="%d" fill="url(#tsh)"/></svg>')%(TW,TH,''.join(pl),TW,TH,TW,TH,TW,TH)
# fallen leaves lying on the table (autumn)
lying=''
if AUT:
    for (x,y,a,sz) in [(9,48,20,34),(16,74,-35,28),(30,60,60,24),(41,82,-10,30),(53,36,140,22),(6,88,95,26)]:
        lying+='<svg class="lay" viewBox="-4 -16 54 32" style="left:%d%%;top:%d%%;width:%dpx;transform:rotate(%ddeg)"><path d="M0 0C9 -15 33 -15 46 0C33 15 9 15 0 0Z" fill="%s"/><path d="M2 0H44" stroke="rgba(40,10,0,.45)" stroke-width="1.4"/></svg>'%(x,y,sz,a,R.choice(LIT))
# droplets on bottles
dr=[]
for _ in range(26):
    x=R.uniform(22,80);yy=R.uniform(36,94);r=R.uniform(.6,1.5)
    dr.append('radial-gradient(circle at %.1f%% %.1f%%,rgba(255,255,255,.95) 0,rgba(255,255,255,.5) %.1fpx,rgba(255,255,255,0) %.1fpx)'%(x,yy,r*.7,r*1.9))
# ---- big overhanging branch (tapered, natural tip) + shade on the table
BW,BH=980,215
def leafp(x,y,a,s,fill,op=1):
    return '<path transform="translate(%s %s) rotate(%s) scale(%s)" d="M0 0C9 -15 33 -15 46 0C33 15 9 15 0 0Z" fill="%s" opacity="%s"/>'%(f1(x),f1(y),f1(a),f1(s),fill,op)
def needle(x,y,a,s,col,op=1):
    return '<g transform="translate(%s %s) rotate(%s) scale(%s)" stroke="%s" stroke-width="3.4" stroke-linecap="round" fill="none" opacity="%s"><path d="M0 0L26 -9M0 0L31 -1M0 0L27 9M0 0L17 -15M0 0L19 15"/></g>'%(f1(x),f1(y),f1(a),f1(s*1.7),col,op)
def lf(x,y,a,s,lit=True):
    if WIN:
        if lit and R.random()<.3: return needle(x,y,a,s,R.choice(LIT),.95)
        return needle(x,y,a,s,R.choice(DARK),1)
    if lit and R.random()<.45: return leafp(x,y,a,s,R.choice(LIT),.9)
    return leafp(x,y,a,s,R.choice(DARK),1)
P=[(1040,95),(790,78),(480,125),(130,140)]
N=40;left=[];right=[];pts=[]
for i in range(N+1):
    t=i/N;x,y=bez(*P,t)
    x2,y2=bez(*P,min(1,t+.01));x1,y1=bez(*P,max(0,t-.01))
    dx,dy=x2-x1,y2-y1;L=math.hypot(dx,dy) or 1
    nx,ny=-dy/L,dx/L
    w=max(1.2,13*(1-t)**1.15+1.5)
    left.append((x+nx*w,y+ny*w));right.append((x-nx*w,y-ny*w));pts.append((x,y,t))
poly=left+right[::-1]
bout=['<path d="M'+' L'.join('%s %s'%(f1(a),f1(b)) for a,b in poly)+' Z" fill="%s"/>'%BR]
bout.append('<path d="M'+' L'.join('%s %s'%(f1(a),f1(b)) for a,b in (right if right[0][1]<left[0][1] else left))+'" stroke="#ffb060" stroke-opacity=".5" stroke-width="2.2" fill="none"/>')
tips=[]
for t in (.14,.28,.42,.56,.7,.82):
    x,y=bez(*P,t);dirn=R.choice([-1,1]);ln=R.uniform(45,95)*(1-t*.45)
    ex=x-ln;ey=y+dirn*R.uniform(22,50)
    bout.append('<path d="M%s %s Q%s %s %s %s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>'%(f1(x),f1(y),f1((x+ex)/2),f1((y+ey)/2-12),f1(ex),f1(ey),BR,f1(max(2,9*(1-t)+1.5))))
    tips.append((ex,ey,t))
# end of the branch: a fan of fine twigs with a few leaves, fading out
ex0,ey0=bez(*P,1.0)
for k,(ang,ln) in enumerate([(-24,70),(8,95),(32,64),(-48,44)]):
    a=math.radians(180+ang);ex=ex0+math.cos(a)*ln;ey=ey0+math.sin(a)*ln*.9
    bout.append('<path d="M%s %s Q%s %s %s %s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>'%(f1(ex0),f1(ey0),f1((ex0+ex)/2),f1((ey0+ey)/2-6),f1(ex),f1(ey),BR,f1(2.4-k*.3)))
    tips.append((ex,ey,1.0))
for i in range(0,60):
    t=i/59;x,y=bez(*P,t)
    n=(3 if t<.55 else (2 if t<.85 else 1))+(1 if WIN else 0)
    for _ in range(n): bout.append(lf(x+R.uniform(-28,28),y+R.uniform(-22,28),R.uniform(0,360),R.uniform(.5,1.0)*(1-t*.35)))
for ex,ey,t in tips:
    for _ in range(max(2,int(10*(1-t*.7)))): bout.append(lf(ex+R.uniform(-40,32),ey+R.uniform(-24,26),R.uniform(0,360),R.uniform(.5,1.0)*(1-t*.3)))
if WIN:
    for i in range(0,60,2):
        t=i/59;x,y=bez(*P,t)
        bout.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#f3f8fd" opacity=".95"/>'%(f1(x+R.uniform(-10,10)),f1(y-8-9*(1-t)),f1(R.uniform(11,24)*(1-t*.5)),f1(R.uniform(5,9))))
main='<svg class="c1" viewBox="0 0 %d %d" preserveAspectRatio="xMaxYMax meet">%s</svg>'%(BW,BH,''.join(bout))
big=[lf(R.uniform(600,1030),R.uniform(150,260),R.uniform(100,260),R.uniform(1.8,3.0)) for _ in range(12)]
bigsvg='<svg class="c2" viewBox="0 0 %d %d" preserveAspectRatio="xMaxYMax meet">%s</svg>'%(BW,BH,''.join(big))
sh=[]
for _ in range(70):
    if WIN: sh.append(needle(R.uniform(0,640),R.uniform(-10,190),R.uniform(0,360),R.uniform(.9,2.0),'#0a0e18',R.uniform(.35,.6)))
    else: sh.append(leafp(R.uniform(0,640),R.uniform(-10,190),R.uniform(0,360),R.uniform(1.0,2.4),'#120600',R.uniform(.4,.68)))
sh.append('<path d="M700 -10C560 40 380 70 120 80" stroke="#120600" stroke-opacity=".4" stroke-width="22" fill="none" stroke-linecap="round"/>')
shade='<svg class="tshade" viewBox="0 0 640 190" preserveAspectRatio="xMaxYMid slice">%s</svg>'%''.join(sh)
open(OUT+'/scene.html','w').write(defs+far+'<div class="haze"></div>'+mid+('<div class="forestshade"></div>' if AUT else '')+'<div class="bloom"></div>'+fgB+fgA+'<div class="bokeh">'+bk+'</div>'+fall+snow)
open(OUT+'/table.html','w').write(table+lying)
open(OUT+'/drops.css','w').write(','.join(dr))
open(OUT+'/branch.html','w').write('<div class="fgC">'+main+bigsvg+'</div>')
open(OUT+'/shade.html','w').write(shade)
print(THEME,'ok')
