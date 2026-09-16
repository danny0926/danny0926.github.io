import fs from 'node:fs';
for (const name of ['index.html', 'resume.html', 'voice.html', 'jpop.html']) {
  const original = fs.readFileSync(name, 'utf8');
  const updated = original.replace(/(<nav\b[\s\S]*?<\/nav>)/g, nav => nav.replace(/(<a\b[^>]*href="voice\.html"[^>]*>)夏吉手帖(<\/a>)/g, '$1Voice Actor$2'));
  fs.writeFileSync(name, updated, 'utf8');
  console.log(`${name}: navigation updated`);
}
