from pathlib import Path
from bs4 import BeautifulSoup
import re
ROOT=Path(__file__).parent
p=ROOT/'index.html';home=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
source=(ROOT/'app.js').read_text(encoding='utf-8')
entries={m.group(1):(m.group(2),m.group(3)) for m in re.finditer(r"(\w+):\{title:'([^']*)',body:`(.*?)`\}",source,re.S)}
def make_page(file,title,active,content):
 shell=BeautifulSoup((ROOT/'drinks.html').read_text(encoding='utf-8'),'html.parser')
 shell.title.string=title+' — Danny Wang'
 for a in shell.select('header nav a'):
  a.attrs.pop('aria-current',None)
  if a.get_text()==active:a['aria-current']='page'
 main=shell.main;main.clear()
 for node in list(BeautifulSoup(content,'html.parser').contents):main.append(node)
 for sheet in ['project-media.css','content-pages.css']:
  shell.head.append(shell.new_tag('link',href=sheet+'?v=20260916clean',rel='stylesheet'))
 (ROOT/file).write_text(str(shell),encoding='utf-8')
work=home.select_one('#work')
projects='<span class="eyebrow mono">PROJECTS / 做過的事</span><h1>從問題開始，<br/>做到實際交付。</h1><p class="personal-lead">工作、研究與個人實作。<a href="resume.html">查看完整履歷 ↗</a></p>'
for button in work.select('[data-project]'):
 key=button['data-project'];title,body=entries[key]
 projects+=f'<article class="content-entry" id="{key}"><h2>{title}</h2><div class="project-content">{body}</div></article>'
recognition=home.select_one('#recognition')
if recognition:projects+=str(recognition)
make_page('projects.html','Projects','Projects',projects)
notes='<span class="eyebrow mono">JOURNAL / 我的筆記</span><h1>把當時的想法，<br/>留給以後的自己。</h1><p class="personal-lead">研究裡的觀察，還有生活中想記下來的事。</p>'
for key in ['representation','batch','trace']:
 title,body=entries[key];notes+=f'<article class="content-entry" id="{key}"><h2>{title}</h2>{body}</article>'
make_page('journal.html','Journal','Journal',notes)
for section in home.select('main section'):
 if section.get('id') not in ['home','contact']:section.decompose()
for dialog in home.select('dialog'):dialog.decompose()
for script in home.select('script[src]'):
 if script['src'].split('?')[0]=='app.js':script['src']='page.js'
 if script['src'].split('?')[0]=='wafer-home.js':script['src']='wafer-home.js?v=20260916clean'
p.write_text(str(home),encoding='utf-8')
for file in ['index.html','resume.html','voice.html','jpop.html','journal.html','drinks.html','projects.html']:
 q=ROOT/file;s=q.read_text(encoding='utf-8').replace('href="index.html#work"','href="projects.html"');q.write_text(s,encoding='utf-8')
print('Home simplified; project stories and research notes preserved in dedicated pages.')
