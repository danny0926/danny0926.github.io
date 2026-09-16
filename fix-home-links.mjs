import fs from 'node:fs';
const path='wafer-home.jsx';
let source=fs.readFileSync(path,'utf8');
source=source.replace('href="#work">用文字瀏覽全部專案 ↓','href="projects.html">瀏覽全部專案 ↗');
fs.writeFileSync(path,source,'utf8');
