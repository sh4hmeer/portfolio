/* Tri-City dashboard copies for the walkthrough. window.Dash renders the 4 boards (HVF / Vision /
   OCT / Doctors-Lounge) and exposes a director API the game engine drives. Phase 2 = boards + render;
   Phase 3 = the .stage()/.reset() choreography. */
(function(){
"use strict";
const root=document.getElementById('dash'); if(!root) return;
const el=(tag,cls,html)=>{const d=document.createElement(tag); if(cls)d.className=cls; if(html!=null)d.innerHTML=html; return d;};
const now=()=>performance.now();
const mmss=ms=>{const s=Math.max(0,Math.floor(ms/1000));return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');};

/* ---- people ---- */
const HERO={name:'DOE, Jordan', dob:'1959-04-22', reason:'gl w/u · optos · HVF · VA · OCT', dr:'Husayn', hero:true};
const POOL=[
  {name:'MENSAH, Rita',  dob:'1951-08-02', reason:'cataract eval',     dr:'Manreet'},
  {name:'KOVAL, Andriy', dob:'1968-12-19', reason:'retina f/u',        dr:'Nimesh'},
  {name:'PATEL, Sunil',  dob:'1972-05-30', reason:'DR screening',      dr:'Tarek'},
  {name:'NGUYEN, Mai',   dob:'1985-03-14', reason:'glaucoma suspect',  dr:'Husayn'},
  {name:"O'BRIEN, Sean", dob:'1948-11-09', reason:'post-op day 1',     dr:'John'},
  {name:'SANTOS, Lia',   dob:'1990-07-21', reason:'field defect',      dr:'Manreet'},
  {name:'HABIB, Omar',   dob:'1963-02-27', reason:'IOP check',         dr:'Nimesh'},
  {name:'ROY, Pierre',   dob:'1957-09-05', reason:'optic disc photo',  dr:'Tarek'},
];
// give each a stable starting wait so timers read like a real busy board
POOL.forEach((p,i)=>p.wait=(6+i*3)*60*1000);
const DOCS=['Manreet','Nimesh','Husayn','Tarek','John'];

/* ---- state ---- */
let stamp=now();                       // base; reset() rebases
const t0=p=> stamp - (p.wait||0) - (p._sit||0);  // virtual start so elapsed = real-since-placed + base wait
let hero=null;                         // {board, zone, idx} or null — set by the director
function freshHero(){ HERO.wait=8*60*1000; HERO._enter=now(); return HERO; }

/* boards hold copies of pool slices so the hero can be inserted/removed without disturbing fillers */
const B={};
function buildState(){
  hero=null;
  B.hvf   ={ boxes:[{lab:'HVF 1',desc:'furthest from door',p:null},{lab:'HVF 2',desc:'middle',p:POOL[4]},{lab:'HVF 3',desc:'closest to door',p:null}],
             queue:[POOL[0],POOL[3],POOL[6]] };
  B.vision={ rooms:[{lab:'Vision 1',p:null},{lab:'Vision 2',p:POOL[1]},{lab:'Vision 3',p:null},{lab:'Vision 4',p:POOL[7]}],
             docs:[POOL[2],POOL[5]], queue:[POOL[0],POOL[6]] };
  B.oct   ={ rooms:[{lab:'Room 1',desc:'corner',p:POOL[5]},{lab:'Room 2',desc:'beside med room',p:null},{lab:'Room 3',desc:'no optos',p:null}],
             docs:[POOL[3],POOL[1],POOL[7]], queue:[POOL[2],POOL[4]] };
  B.lounge={ docs:DOCS.map((n,i)=>({name:n, sched:2+i%3, here:1+(i%2), hvf:i%2, oct:(i+1)%2, wait:i%3, billed:3+i%4, billedAt:['2:58','3:04','2:41','3:11','2:49'][i]})) };
}

/* ---- DOM skeleton ---- */
const boards={}; let cursor, drag, dimDash, beaconEls=[];
// focus dimming: dim the half that ISN'T the action so a first-time viewer knows where to look
const dimGameEl=()=>document.getElementById('dimGame');
function focusGame(){ const g=dimGameEl(); if(dimDash)dimDash.classList.add('on'); if(g)g.classList.remove('on'); }
function focusDash(){ const g=dimGameEl(); if(g)g.classList.add('on'); if(dimDash)dimDash.classList.remove('on'); }
function focusNone(){ const g=dimGameEl(); if(g)g.classList.remove('on'); if(dimDash)dimDash.classList.remove('on'); }
function topbar(brand){
  const t=el('div','d-top');
  t.appendChild(el('div','d-brand', brand+' <span class="d-dim">· Tri-City</span>'));
  t.appendChild(el('div','d-spacer'));
  t.appendChild(el('div','d-pill','Mon Jun 16'));
  const ck=el('div','d-clock'); const bc=el('span','d-beacon'); beaconEls.push(bc);
  ck.appendChild(bc); const tm=el('span'); tm.dataset.clock='1'; ck.appendChild(tm); t.appendChild(ck);
  return t;
}
function makeBoard(name,brand){
  const bd=el('div','board board-'+name); bd.id='board-'+name;
  bd.appendChild(topbar(brand));
  const body=el('div','d-body'); bd.appendChild(body);
  bd._body=body; boards[name]=bd; root.appendChild(bd);
}
function init(){
  ['hvf','HVF Board','vision','Vision Board','oct','OCT Board','lounge',"Doctors' Lounge"]
    .reduce((a,v,i)=>{ if(i%2===0)a.push([v]); else a[a.length-1].push(v); return a; },[])
    .forEach(([n,b])=>makeBoard(n,b));
  cursor=el('div','d-cursor');
  cursor.innerHTML='<svg width="22" height="22" viewBox="0 0 22 22"><path d="M3 2 L3 18 L7.5 13.5 L10.5 20 L13 19 L10 12.5 L17 12.5 Z" fill="#f6f8fc" stroke="#0e1116" stroke-width="1.2" stroke-linejoin="round"/></svg>';
  drag=el('div','d-drag');
  dimDash=el('div','dim'); dimDash.id='dimDash';
  root.appendChild(cursor); root.appendChild(drag); root.appendChild(dimDash);
  buildState(); renderAll(); tick(); setInterval(tick,1000);
}

/* ---- card / box builders ---- */
function card(p,kind,opts){ opts=opts||{};
  const d=el('div','d-card '+(kind||'')+(p.hero?' hero':'')+(opts.ghost?' ghost':''));
  d.innerHTML=`<div class="d-r1"><span class="d-name">${p.name}</span><span class="d-dob">DOB ${p.dob}</span></div>
    <div class="d-reason">${p.reason}</div>
    <div class="d-r3"><span class="d-dr">→ Dr. ${p.dr}</span><span class="d-timer ${kind==='yellow'?'':''}" data-ts="${tEpoch(p)}">00:00</span></div>`;
  return d;
}
function roomBox(r,accent,doneLabel,rk){
  let d;
  if(!r.p){ d=el('div','d-room empty');
    d.innerHTML=`<div class="d-rlabel">${r.lab}${r.desc?` <small>${r.desc}</small>`:''}</div><div>Drop a patient here</div>`; }
  else{ d=el('div','d-room occ '+accent+(r.p.hero?' hero':''));
    // the hero's room timer is driven by the game's clinical clock (so it can spin fast + freeze); others tick real-time
    const tAttr = r.p.hero ? '' : ` data-ts="${tEpoch(r.p)}"`;
    d.innerHTML=`<div class="d-rlabel">${r.lab}${r.desc?` <small>${r.desc}</small>`:''}</div>
      <div class="d-slot"><div class="d-name">${r.p.name}</div><div class="d-meta">${r.p.reason} · → Dr. ${r.p.dr}</div>
        <div class="d-acts"><span class="d-rm">Remove</span><span class="d-t"${tAttr}>00:00</span><span class="d-done">${doneLabel||'Done'}</span></div></div>`; }
  if(rk)d.dataset.rk=rk; return d;
}
function docRow(p){
  const d=el('div','d-doc');
  d.innerHTML=`<div><div class="d-dn">${p.name.split(',')[0]}</div><div class="d-dl">${p.reason}</div></div><div class="d-badge">1</div>`;
  return d;
}
// virtual epoch ts (ms, performance clock) a card's timer counts up from
function tEpoch(p){ return (p._ts!=null)? p._ts : (now() - (p.wait||0)); }

/* ---- renderers ---- */
function colHead(title,count){ const h=el('div','d-colhead',title); if(count!=null)h.appendChild(el('span','d-cnt','('+count+')')); return h; }
function listCol(title,count,nodes){ const c=el('div','d-col'); c.appendChild(colHead(title,count)); const l=el('div','d-list'); nodes.forEach(n=>l.appendChild(n)); c.appendChild(l); return c; }

function renderHVF(){ const b=B.hvf, body=boards.hvf._body; body.innerHTML='';
  const boxes=el('div','d-col'); boxes.appendChild(colHead('HVF Machines'));
  const bl=el('div','d-list'); b.boxes.forEach((r,i)=>bl.appendChild(roomBox(r,'green','HVF done','hvf-'+i))); boxes.appendChild(bl);
  const q=b.queue.map(p=>card(p,'green'));
  body.appendChild(boxes);
  body.appendChild(listCol('Greens needing HVF',b.queue.length,q));
}
function renderVision(){ const b=B.vision, body=boards.vision._body; body.innerHTML='';
  body.appendChild(listCol('Waiting for Dr',b.docs.length,b.docs.map(p=>card(p,'purple'))));
  const rooms=el('div','d-col'); rooms.appendChild(colHead('Vision Rooms'));
  const rl=el('div','d-list'); b.rooms.forEach((r,i)=>rl.appendChild(roomBox(r,'blue','Done','vision-'+i))); rooms.appendChild(rl);
  body.appendChild(rooms);
  body.appendChild(listCol('Greens · Here',b.queue.length,b.queue.map(p=>card(p,'green'))));
}
function renderOCT(){ const b=B.oct, body=boards.oct._body; body.innerHTML='';
  body.appendChild(listCol('Waiting for Dr',b.docs.length,b.docs.map(docRow)));
  const rooms=el('div','d-col'); rooms.appendChild(colHead('OCT Rooms'));
  const rl=el('div','d-list'); b.rooms.forEach((r,i)=>rl.appendChild(roomBox(r,'blue','Done','oct-'+i))); rooms.appendChild(rl);
  body.appendChild(rooms);
  body.appendChild(listCol('Ready for OCT',b.queue.length,b.queue.map(p=>card(p,'yellow'))));
}
function renderLounge(){ const b=B.lounge, body=boards.lounge._body; body.innerHTML='';
  b.docs.forEach(d=>{
    const c=el('div','d-loungecard');
    c.appendChild(el('div','d-lh',`<b>${d.name}</b><span>billed ${d.billedAt}</span>`));
    const stats=el('div','d-stats');
    const mk=(cls,k,v)=>{const s=el('div','d-stat '+cls+(v>0?' on':''));s.innerHTML=`<div class="d-sv">${v}</div><div class="d-sk">${k}</div>`;return s;};
    stats.appendChild(mk('sched','sched',d.sched)); stats.appendChild(mk('here','here',d.here)); stats.appendChild(mk('hvf','hvf',d.hvf));
    stats.appendChild(mk('oct','oct',d.oct)); stats.appendChild(mk('wait','wait',d.wait)); stats.appendChild(mk('billed','billed',d.billed));
    c.appendChild(stats); body.appendChild(c);
  });
}
function renderAll(){ renderHVF(); renderVision(); renderOCT(); renderLounge(); tick(); }
const RENDER={hvf:renderHVF,vision:renderVision,oct:renderOCT,lounge:renderLounge};

/* ---- per-second tick: clocks + card timers ---- */
function tick(){
  const d=new Date(); const hh=((d.getHours()+11)%12+1), clk=hh+':'+String(d.getMinutes()).padStart(2,'0');
  root.querySelectorAll('[data-clock]').forEach(e=>e.textContent=clk);
  const t=now();
  root.querySelectorAll('[data-ts]').forEach(e=>{ const ts=+e.getAttribute('data-ts'); const el2=e;
    const ms=t-ts; el2.textContent=mmss(ms);
    el2.classList.remove('amber','red'); const m=ms/60000; if(m>=15)el2.classList.add('red'); else if(m>=10)el2.classList.add('amber');
  });
}

/* ---- show / pulse ---- */
let current=null;
function show(name){ Object.values(boards).forEach(b=>b.classList.remove('show')); if(boards[name]){boards[name].classList.add('show');current=name;} }
function pulse(){ beaconEls.forEach(b=>{b.classList.remove('pulse');void b.offsetWidth;b.classList.add('pulse');}); }

/* ---- director: fake cursor + per-stage choreography ---- */
const rrect=()=>root.getBoundingClientRect();
function center(elm){const r=elm.getBoundingClientRect(),R=rrect();return {x:r.left-R.left+r.width/2,y:r.top-R.top+r.height/2};}
function setPos(elm,x,y){elm.style.left=x+'px';elm.style.top=y+'px';}
function renderCurrent(){ (RENDER[current]||renderAll)(); tick(); }
function heroCardEl(){ return boards[current]?boards[current].querySelector('.d-card.hero'):null; }
function rkEl(rk){ return boards[current]?boards[current].querySelector('[data-rk="'+rk+'"]'):null; }
function heroEpochNow(){ HERO._ts=now(); }   // (re)start the hero's visible timer at 00:00

// room timer sync: while the hero is in a room, his card timer tracks the game's (rapid) clinical clock
let clockSecs=0; const heroRoom={active:false,start:0};
function roomEnter(){ heroRoom.active=true; heroRoom.start=clockSecs; }
function roomLeave(){ heroRoom.active=false; }
function clock(s){ clockSecs=s; if(!heroRoom.active) return;
  const t=boards[current]&&boards[current].querySelector('.d-room.hero .d-t');
  if(t) t.textContent=mmss(Math.max(0,clockSecs-heroRoom.start)*1000); }

// drag the hero card from its current list spot into room `rk` — slow + pronounced. mutate() commits state.
function dragHeroToRoom(rk,kind,mutate,done){
  focusDash(); renderCurrent();
  const src=heroCardEl(), tgt=rkEl(rk);
  if(!src||!tgt){ heroEpochNow(); mutate(); renderCurrent(); done&&done(); return; }
  const s=center(src), t=center(tgt);
  drag.className='d-drag'+(kind==='yellow'?' yellow':'');
  drag.innerHTML=`<div class="d-name">${HERO.name}</div><div class="d-reason">${HERO.reason}</div>`;
  setPos(cursor,s.x-3,s.y-2); setPos(drag,s.x-16,s.y+6); cursor.style.opacity='1';
  setTimeout(()=>{ cursor.classList.add('down'); src.style.visibility='hidden'; drag.style.opacity='1'; },600); // hover, then grab
  setTimeout(()=>{ setPos(cursor,t.x-3,t.y-2); setPos(drag,t.x-16,t.y+6); },1000);                              // slow glide (2.2s)
  setTimeout(()=>{ drag.style.opacity='0'; cursor.classList.remove('down');
    heroEpochNow(); mutate(); renderCurrent(); pulse();
    setTimeout(()=>cursor.style.opacity='0',500); done&&done();
  },1000+2200+300);   // ~3.5s total
}
// move the cursor to a room's Done button, "click", then commit + re-render
function clickDone(rk,mutate,done){
  focusDash();
  const tgt=rkEl(rk);
  if(!tgt){ mutate(); renderCurrent(); done&&done(); return; }
  const btn=tgt.querySelector('.d-done')||tgt, t=center(btn);
  setPos(cursor,t.x-3,t.y-2); cursor.style.opacity='1';
  setTimeout(()=>cursor.classList.add('down'),2300);   // glide to the button (2.2s), then press
  setTimeout(()=>{ cursor.classList.remove('down'); mutate(); renderCurrent(); pulse(); done&&done(); },2650);
  setTimeout(()=>cursor.style.opacity='0',3150);
}
const rmFromQueue=q=>{const i=q.indexOf(HERO); if(i>=0)q.splice(i,1);};
const firstEmpty=rooms=>{const i=rooms.findIndex(r=>!r.p); return i<0?0:i;};

/* flow order is fixed: 0 here(checkin) · 1 here(wait) · 2 hvf · 3 here(post-hvf) · 4 vision ·
   5 octwait · 6 oct · 7 drwait · 8 doctor · 9 billed · 10 exit  */
function stage(idx,key,leg){
  pulse();
  switch(idx){
    case 0: { focusDash(); show('hvf'); rmFromQueue(B.hvf.queue); B.hvf.queue.unshift(HERO); heroEpochNow(); renderCurrent();
      const hc=heroCardEl(); if(hc) hc.classList.add('reveal');   // slow first appearance so the viewer locks onto him
      break; }
    case 1: break; // seated beat — hero waits in the HVF queue, timer ticking
    case 2: { roomEnter(); const bi=firstEmpty(B.hvf.boxes);
      dragHeroToRoom('hvf-'+bi,'green',()=>{ rmFromQueue(B.hvf.queue); B.hvf.boxes[bi].p=HERO; }); break; }
    case 3: { const bi=B.hvf.boxes.findIndex(r=>r.p===HERO);
      clickDone('hvf-'+(bi<0?0:bi),()=>{ roomLeave(); if(bi>=0)B.hvf.boxes[bi].p=null; },()=>{
        setTimeout(()=>{ show('vision'); B.vision.queue.unshift(HERO); heroEpochNow(); renderCurrent(); },1000); }); break; }
    case 4: { roomEnter(); dragHeroToRoom('vision-0','green',()=>{ rmFromQueue(B.vision.queue); B.vision.rooms[0].p=HERO; }); break; }
    case 5: { const ri=B.vision.rooms.findIndex(r=>r.p===HERO);
      clickDone('vision-'+(ri<0?0:ri),()=>{ roomLeave(); if(ri>=0)B.vision.rooms[ri].p=null; },()=>{
        setTimeout(()=>{ show('oct'); B.oct.queue.unshift(HERO); heroEpochNow(); renderCurrent(); },1000); }); break; }
    case 6: { roomEnter(); const ri=firstEmpty(B.oct.rooms);
      dragHeroToRoom('oct-'+ri,'yellow',()=>{ rmFromQueue(B.oct.queue); B.oct.rooms[ri].p=HERO; }); break; }
    case 7: { const ri=B.oct.rooms.findIndex(r=>r.p===HERO);
      clickDone('oct-'+(ri<0?0:ri),()=>{ roomLeave(); if(ri>=0)B.oct.rooms[ri].p=null; },()=>{
        setTimeout(()=>{ show('lounge'); const d=B.lounge.docs.find(x=>x.name===HERO.dr); if(d)d.wait++; renderCurrent(); },1000); }); break; }
    case 8: { const d=B.lounge.docs.find(x=>x.name===HERO.dr); pulse(); renderCurrent(); break; }
    case 9: { const d=B.lounge.docs.find(x=>x.name===HERO.dr); if(d){ if(d.wait>0)d.wait--; d.billed++; } renderCurrent(); break; }
    default: break;
  }
}

window.Dash={ show, render:n=>{(RENDER[n]||renderAll)();}, renderAll, pulse, stage, focusGame, focusDash, focusNone, clock, roomLeave,
  reset:()=>{ HERO._ts=null; clockSecs=0; heroRoom.active=false; if(cursor)cursor.style.opacity='0'; if(drag)drag.style.opacity='0'; focusNone(); buildState(); renderAll(); show('hvf'); } };
init(); show('hvf');
})();
