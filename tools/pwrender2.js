// node pwrender2.js <dir> <out.mp4|snap:t1,t2,...> <start> <end> [fps]
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const { spawn } = require('child_process'); const path=require('path'); const fs=require('fs');
(async () => {
  const [dir, out, s0, s1, fpsS] = process.argv.slice(2);
  const fps=parseInt(fpsS||'30');
  const browser = await chromium.launch({ executablePath:'/usr/bin/google-chrome', args:['--disable-gpu','--force-device-scale-factor=1','--allow-file-access-from-files','--no-first-run','--disable-background-networking'] });
  const page = await browser.newPage({ viewport:{width:1920,height:1080} });
  page.on('pageerror', e=>console.log('PAGEERR',e.message)); page.on('console', m=>{ if(m.type()==='error') console.log('CONSOLE',m.text()); });
  await page.goto('file://'+path.resolve(dir,'index.html'));
  await page.evaluate(async()=>{await document.fonts.ready;});
  if(out.startsWith('snap:')){
    for(const ts of out.slice(5).split(',')){ const t=parseFloat(ts);
      await page.evaluate(async t=>{await window.__onSeek(t);},t); await page.waitForTimeout(50);
      await page.screenshot({path:`/tmp/snap_${t}.jpg`,type:'jpeg',quality:85}); console.log('snap',t);}
    await browser.close(); return; }
  const ff = spawn('ffmpeg',['-hide_banner','-loglevel','error','-y','-f','image2pipe','-framerate',String(fps),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',out],{stdio:['pipe','inherit','inherit']});
  const t0=parseFloat(s0), t1=parseFloat(s1); const n=Math.round((t1-t0)*fps); const st=Date.now();
  for(let i=0;i<n;i++){ const t=t0+i/fps;
    await page.evaluate(async t=>{await window.__onSeek(t);},t);
    const buf=await page.screenshot({type:'jpeg',quality:93});
    if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));
    if(i%300===0) console.log('frame',i,'/',n,((Date.now()-st)/1000).toFixed(0)+'s');
  }
  ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await browser.close();
  console.log('done',out,((Date.now()-st)/1000).toFixed(1)+'s');
})();
