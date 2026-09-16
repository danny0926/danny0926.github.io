import fs from 'node:fs';
for (const path of ['voice.html', 'dist/voice.html']) {
  if (!fs.existsSync(path)) continue;
  const original = fs.readFileSync(path, 'utf8');
  const updated = original.replace(/<section\b[^>]*\bid="recent"[^>]*>[\s\S]*?<\/section>/, '').replace(/<a\b[^>]*href="#recent"[^>]*>[\s\S]*?<\/a>/g, '');
  fs.writeFileSync(path, updated, 'utf8');
  console.log(`${path}: recent section ${updated.includes('id="recent"') ? 'still present' : 'removed'}`);
}
