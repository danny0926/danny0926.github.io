import fs from 'node:fs';
for (const path of ['index.html','projects.html','journal.html','resume.html','jpop.html','voice.html','drinks.html']) {
  let html=fs.readFileSync(path,'utf8');
  html=html.replace(/<nav aria-label="主要導覽">[\s\S]*?<\/nav>/,nav=>{
    if(nav.includes('>CV</a>'))return nav;
    return nav.replace(/(<a\b[^>]*>Journal<\/a>)/,`$1<a href="resume.html"${path==='resume.html'?' aria-current="page"':''}>CV</a>`);
  });
  fs.writeFileSync(path,html,'utf8');
  if(!/<nav aria-label="主要導覽">[\s\S]*?>CV<\/a>/.test(html))throw new Error(`CV missing: ${path}`);
  console.log(`${path}: CV added`);
}
