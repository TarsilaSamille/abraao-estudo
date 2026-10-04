const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch({channel:'chrome'});
for(const f of process.argv.slice(2)){
const p=await b.newPage({viewport:{width:1400,height:1000}});
await p.goto('file://'+path.resolve(f),{waitUntil:'domcontentloaded'});await p.waitForTimeout(2200);
const r=await p.evaluate(()=>{
  const el=document.getElementById('lang-en'); const b=el.getBoundingClientRect();
  const cx=b.left+b.width/2, cy=b.top+b.height/2;
  const top=document.elementFromPoint(cx,cy);
  const stack=document.elementsFromPoint(cx,cy).slice(0,4).map(e=>e.tagName.toLowerCase()+'.'+((e.className||'').toString().slice(0,26))+'#'+(e.id||'-'));
  const cs=getComputedStyle(el); const rp=document.getElementById('reading-progress');
  return {rect:{x:Math.round(cx),y:Math.round(cy),w:Math.round(b.width),h:Math.round(b.height)},
    vis:cs.visibility, disp:cs.display, pe:cs.pointerEvents,
    topEl: top? top.tagName.toLowerCase()+'#'+(top.id||'-')+'.'+((top.className||'').toString().slice(0,30)) : null,
    empilha: stack,
    progressZ: rp?getComputedStyle(rp).zIndex+' h='+getComputedStyle(rp).height : 'sem barra'};
});
console.log(f); console.log(' ',JSON.stringify(r));
await p.close();}
await b.close();})();
