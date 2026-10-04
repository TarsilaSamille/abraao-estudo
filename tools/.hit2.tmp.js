const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch({channel:'chrome'});
const p=await b.newPage({viewport:{width:1400,height:1000}});
await p.goto('file://'+path.resolve(process.argv[2]),{waitUntil:'domcontentloaded'});
await p.waitForTimeout(2000);
const r=await p.evaluate(()=>{
  const el=document.getElementById('lang-en'); const bb=el.getBoundingClientRect();
  const cx=bb.left+bb.width/2, cy=bb.top+bb.height/2;
  const st=document.elementsFromPoint(cx,cy).slice(0,4).map(e=>e.tagName.toLowerCase()+'.'+String(e.className||'').slice(0,24)+'#'+(e.id||'-'));
  const rp=document.getElementById('reading-progress');
  return {rect:[Math.round(cx),Math.round(cy),Math.round(bb.width),Math.round(bb.height)],
    empilha:st,
    barra: rp?{z:getComputedStyle(rp).zIndex,h:getComputedStyle(rp).height}:'sem'};
});
console.log(JSON.stringify(r,null,1));
await b.close();})();
