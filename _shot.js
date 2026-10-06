const { chromium } = require('playwright');
const path=require('path');
(async()=>{
  const f=process.argv[2], out=process.argv[3], full=process.argv[4]==='full';
  const b=await chromium.launch({channel:'chrome'});
  const p=await b.newPage({viewport:{width:1400,height:1000}});
  await p.goto('file://'+path.resolve(f),{waitUntil:'networkidle'});
  await p.waitForTimeout(600);
  await p.screenshot({path:out, fullPage:full});
  console.log('ok',out);
  await b.close();
})();
