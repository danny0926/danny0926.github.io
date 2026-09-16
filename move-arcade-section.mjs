import fs from 'node:fs';
for (const path of ['voice.html', 'dist/voice.html']) {
  if (!fs.existsSync(path)) continue;
  let html = fs.readFileSync(path, 'utf8');
  const block = html.match(/<section\b[^>]*\bid="arcade"[^>]*>[\s\S]*?<\/section>/)?.[0];
  if (!block) throw new Error(`Missing arcade section in ${path}`);
  html = html.replace(block, '');
  const roles = /<section\b[^>]*\bid="roles"[^>]*>/;
  if (!roles.test(html)) throw new Error(`Missing roles section in ${path}`);
  html = html.replace(roles, match => block + match);
  fs.writeFileSync(path, html, 'utf8');
  console.log(`${path}: arcade moved before roles`);
}
