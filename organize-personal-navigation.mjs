import fs from 'node:fs';
const entries=[['Home','index.html'],['Projects','index.html#work'],['Journal','journal.html'],['Music','jpop.html'],['VoiceActors','voice.html'],['Drinks','drinks.html']];
function nav(current){return '<nav aria-label="主要導覽">'+entries.map(([label,href])=>`<a href="${href}"${label===current?' aria-current="page"':''}>${label}</a>`).join('')+'</nav>';}
const home=fs.readFileSync('index.html','utf8');
const originalHeader=home.match(/<header\b[^>]*class="[^"]*site-header[^\"]*"[^>]*>[\s\S]*?<\/header>/)?.[0];
if(!originalHeader)throw new Error('Header not found');
function header(current){return originalHeader.replace(/<nav\b[\s\S]*?<\/nav>/,nav(current));}
function page(title,current,body){return `<!DOCTYPE html>
<html lang="zh-Hant" data-theme="dark"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>${title} — Danny Wang</title><link rel="stylesheet" href="style.css"/><link rel="stylesheet" href="extended.css"/><link rel="stylesheet" href="wafer-theme.css"/><link rel="stylesheet" href="personal-navigation.css?v=20260916nav"/><script defer src="page.js"></script></head><body class="personal-page">${header(current)}<main class="personal-content">${body}</main><footer class="site-footer"><a href="index.html">DANNY.W / PERSONAL WAFER</a><a href="resume.html">CV / 完整履歷 ↗</a><span>© 2026 DANNY WANG</span></footer></body></html>`;}
fs.writeFileSync('journal.html',page('Journal','Journal',`<span class="eyebrow mono">JOURNAL / 王邦彥的筆記</span><h1>把當時的想法，<br/>留給以後的自己。</h1><p class="personal-lead">研究裡的觀察，還有生活中想記下來的事。</p><section class="personal-entries"><a href="index.html#notes"><span class="mono">01 / 資料與模型</span><h2>在選模型之前，先想想資料長什麼樣。</h2><p>從 Wafer Map 的數值與影像表示，回頭思考模型實際看見的資料。</p><span>閱讀研究筆記 ↗</span></a><a href="index.html#notes"><span class="mono">02 / 單卡實驗</span><h2>併發增加，為什麼不會等比例變快？</h2><p>固定一批 idea，記錄批次產碼的速度與硬體取捨。</p><span>閱讀研究筆記 ↗</span></a><a href="index.html#notes"><span class="mono">03 / 研究記憶</span><h2>失敗的實驗，也值得留下一個位置。</h2><p>保存假說、改動與結果，讓下一輪研究能接續。</p><span>閱讀研究筆記 ↗</span></a></section>`),'utf8');
fs.writeFileSync('drinks.html',page('Drinks','Drinks',`<span class="eyebrow mono">DRINKS / 飲酒筆記</span><h1>喝過的酒，<br/>也記得那天的事。</h1><p class="personal-lead">想記下酒的味道，也想記下在哪裡、和誰一起喝。</p><section class="drink-unwritten"><span class="mono">FIRST ENTRY</span><h2>第一杯，等我慢慢寫。</h2><p>酒名、照片、品飲感受，以及會不會想再喝。</p></section>`),'utf8');
for(const [file,current] of [['index.html','Home'],['resume.html',null],['voice.html','VoiceActors'],['jpop.html','Music'],['journal.html','Journal'],['drinks.html','Drinks']]){
 let html=fs.readFileSync(file,'utf8');
 html=html.replace(/(<header\b[^>]*class="[^"]*site-header[^\"]*"[^>]*>[\s\S]*?)<nav\b[\s\S]*?<\/nav>/,(match,prefix)=>prefix+nav(current));
 if(!html.includes('personal-navigation.css'))html=html.replace('</head>','<link href="personal-navigation.css?v=20260916nav" rel="stylesheet"/></head>');
 fs.writeFileSync(file,html,'utf8');
}
console.log('Six navigation entries unified; Journal and Drinks created locally.');
