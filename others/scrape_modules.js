const { chromium } = require('/Users/macbook/.hermes/hermes-agent/apps/desktop/node_modules/playwright');
const fs = require('fs');

const SLUGS = ["heaven-and-earth","adam-to-noah","jacob","joseph","exodus-overview-carmen-imes",
 "ezekiel","jonah","messianic-torah","1-corinthians-lucy-peppiatt","ephesians",
 "introduction-to-the-hebrew-bible","art-of-biblical-words"];

const EXTRACT = () => {
  function findClass(o){if(!o||typeof o!=='object')return null;
    if(o.__typename==='Class'&&o.modules&&o.modules.nodes)return o;
    for(const k in o){const r=findClass(o[k]);if(r)return r;}return null;}
  const cls=findClass(window.__remixContext);if(!cls)return null;
  const mods=cls.modules.nodes.map(m=>{const sess=(m.sessions&&m.sessions.nodes)?m.sessions.nodes.map(s=>s.position||s.number):[];
    return {pos:m.position,title:m.title,desc:m.description,first:sess[0],last:sess[sess.length-1],n:sess.length};});
  return {title:cls.title,scripture:cls.scripture,description:cls.description,mods};
};

(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage();
  const out={};
  for(const slug of SLUGS){
    try{
      await p.goto(`https://bibleproject.com/classroom/${slug}/`,{waitUntil:'networkidle',timeout:45000});
      await p.waitForTimeout(1200);
      const data=await p.evaluate(EXTRACT);
      out[slug]=data;
      console.error(`OK ${slug}: ${data?data.mods.length+' modules':'NULL'}`);
    }catch(e){console.error(`ERR ${slug}: ${e.message}`);out[slug]=null;}
  }
  fs.writeFileSync('/tmp/course_modules.json',JSON.stringify(out,null,2));
  await b.close();
  console.error('WROTE /tmp/course_modules.json');
})();
