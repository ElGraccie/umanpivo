/* hero themes + light-weight motion: runs right after the hero markup so layer files start loading early */
(function(){
  var D=document.documentElement,hero=document.getElementById('hero'),stage=document.getElementById('stage');
  if(!hero||!stage)return;
  var LS={get:function(k,d){try{return localStorage.getItem(k)||d}catch(e){return d}},set:function(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
  var T=%THEMES%;
  var FAV=%FAV%;
  var imgs={},cur=D.getAttribute('data-theme')||'classic';
  [].forEach.call(hero.querySelectorAll('img[data-l]'),function(i){imgs[i.getAttribute('data-l')]=i});
  /* seasons follow Kyiv time: autumn 1 Sep, winter 1 Dec, New Year 30 Dec - 5 Jan */
  function kyivDate(){
    var z=['Europe/Kyiv','Europe/Kiev'],i,o;
    for(i=0;i<z.length;i++){
      try{o={};new Intl.DateTimeFormat('en-US',{timeZone:z[i],year:'numeric',month:'numeric',day:'numeric'}).formatToParts(new Date()).forEach(function(p){if(p.type!=='literal')o[p.type]=+p.value});
        if(o.year&&o.month&&o.day)return o}catch(e){}
    }
    var n=new Date();return {year:n.getFullYear(),month:n.getMonth()+1,day:n.getDate()}
  }
  function autoTheme(){var k=kyivDate(),m=k.month,x=k.day;
    if((m===12&&x>=30)||(m===1&&x<=5))return 'newyear';
    if(m===12||m===1||m===2)return 'winter';
    if(m>=9&&m<=11)return 'autumn';
    return 'classic'}
  var pref=LS.get('up-theme2','auto');if(pref!=='auto'&&!T[pref])pref='auto';
  function resolve(p){return p==='auto'?autoTheme():p}
  /* ---- buttons ---- */
  var btns=[].slice.call(hero.querySelectorAll('[data-th]')),fxb=hero.querySelector('[data-fxb]');
  function sync(){
    btns.forEach(function(b){var on=b.getAttribute('data-th')===pref;b.setAttribute('aria-pressed',on?'true':'false');
      if(b.getAttribute('data-th')==='auto')b.title='За датою (Київ), зараз: '+T[autoTheme()].n});
    if(fxb)fxb.setAttribute('aria-pressed',lite?'false':'true');
  }
  /* ---- layers ---- */
  function load(t,cb){
    var keys=T[t].l.split(' '),n=keys.length,done=0,fired=false;
    function fin(){if(!fired){fired=true;cb()}}
    keys.forEach(function(k){var im=new Image();im.onload=im.onerror=function(){if(++done===n)fin()};im.src='t/'+t+'/'+k+'.webp'});
    setTimeout(fin,3500);
  }
  function paint(t){
    var keys=T[t].l.split(' ');
    D.setAttribute('data-theme',t);
    Object.keys(imgs).forEach(function(k){
      var im=imgs[k];
      if(keys.indexOf(k)<0){im.hidden=true;im.classList.remove('in');im.removeAttribute('src');return}
      var u='t/'+t+'/'+k+'.webp';
      im.hidden=false;
      if(im.getAttribute('src')!==u){im.classList.remove('in');im.onload=function(){im.classList.add('in')};im.src=u}
      if(im.complete&&im.naturalWidth)im.classList.add('in');
    });
    var f=FAV[t];if(f){var a=document.getElementById('fav-svg'),b=document.getElementById('fav-png');if(a)a.href=f.svg;if(b)b.href=f.png}
    cur=t;
  }
  function apply(p,first){
    pref=p;if(!first)LS.set('up-theme2',p);sync();
    var t=resolve(p);
    if(first){paint(t);return}
    if(t===cur)return;
    hero.classList.add('swap');
    var t0=Date.now();
    load(t,function(){setTimeout(function(){paint(t);requestAnimationFrame(function(){hero.classList.remove('swap')})},Math.max(0,210-(Date.now()-t0)))});
  }
  btns.forEach(function(b){b.addEventListener('click',function(){apply(b.getAttribute('data-th'))})});
  /* ---- effects: full / lite ---- */
  var fxPref=LS.get('up-fx','auto'),lite=false;
  function calcLite(){
    if(fxPref==='off')return true;
    if(fxPref==='on')return false;
    var c=navigator.connection||{};
    return !!((window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches)||c.saveData||(navigator.deviceMemory&&navigator.deviceMemory<=2)||(navigator.hardwareConcurrency&&navigator.hardwareConcurrency<=2))
  }
  function setFx(){lite=calcLite();D.setAttribute('data-fx',lite?'lite':'full');sync();if(lite)reset()}
  if(fxb)fxb.addEventListener('click',function(){fxPref=lite?'on':'off';LS.set('up-fx',fxPref);setFx()});
  /* ---- pointer parallax: one rAF loop, transforms only, stops when settled ---- */
  var layers=[].map.call(hero.querySelectorAll('[data-d]'),function(el){return{el:el,d:parseFloat(el.getAttribute('data-d'))||0}});
  var fine=window.matchMedia&&matchMedia('(pointer:fine)').matches;
  var tx=0,ty=0,cx=0,cy=0,raf=0,lastPx=9,seen=true;
  function step(){
    cx+=(tx-cx)*.14;cy+=(ty-cy)*.14;
    if(Math.abs(tx-cx)<.003)cx=tx;
    if(Math.abs(ty-cy)<.003)cy=ty;
    for(var i=0;i<layers.length;i++)layers[i].el.style.transform='translate3d('+(-cx*layers[i].d).toFixed(2)+'px,0,0)';
    if(Math.abs(cx-lastPx)>.004||cx===0){stage.style.setProperty('--px',cx.toFixed(3));lastPx=cx}
    raf=(cx!==tx||cy!==ty)?requestAnimationFrame(step):0;
  }
  function reset(){tx=ty=cx=cy=0;if(raf){cancelAnimationFrame(raf);raf=0}
    for(var i=0;i<layers.length;i++)layers[i].el.style.transform='';stage.style.setProperty('--px',0);lastPx=9}
  if(fine){
    hero.addEventListener('pointermove',function(e){
      if(lite||!seen)return;
      var r=hero.getBoundingClientRect();
      tx=((e.clientX-r.left)/r.width-.5)*2;ty=((e.clientY-r.top)/r.height-.5)*2;
      if(!raf)raf=requestAnimationFrame(step);
    },{passive:true});
    hero.addEventListener('pointerleave',function(){tx=ty=0;if(!lite&&!raf)raf=requestAnimationFrame(step)});
  }
  /* ---- pause animations while the hero is off screen or the tab is hidden ---- */
  function pause(off){hero.classList.toggle('off',off)}
  if('IntersectionObserver' in window){new IntersectionObserver(function(es){seen=es[0].isIntersecting;pause(!seen||document.hidden)},{threshold:0}).observe(hero)}
  document.addEventListener('visibilitychange',function(){pause(document.hidden||!seen)});
  /* hero height for the falling particles */
  function size(){hero.style.setProperty('--H',hero.offsetHeight+'px')}
  size();if(window.ResizeObserver)new ResizeObserver(size).observe(hero);else addEventListener('resize',size);
  var kick=document.querySelector('#kick span');
  if(kick){var kd=kyivDate();kick.textContent='З Новим '+(kd.month>=7?kd.year+1:kd.year)+' роком'}
  setFx();apply(pref,true);
  /* left open over midnight (Kyiv): follow the calendar */
  setInterval(function(){if(pref==='auto'&&!document.hidden){var t=resolve('auto');if(t!==cur)apply('auto')}},60000);
})();
