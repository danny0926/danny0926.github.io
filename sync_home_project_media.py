from pathlib import Path
from bs4 import BeautifulSoup
import re
ROOT=Path(__file__).parent
resume=BeautifulSoup((ROOT/'resume.html').read_text(encoding='utf-8'),'html.parser')
images={Path(i['src'].split('?')[0]).stem.replace('-illustration',''):i['src'] for i in resume.select('img[src*="-illustration.svg"]')}
labels={'agent':'企業 AI Agent：MCP 查詢與上線成果','wafer':'Wafer Map：判讀方法與專案成果','stdf':'STDF：缺失值、量測旗標與系統交付','ttt':'TTT-Discover：單卡實作與實驗比較','worldquant':'WorldQuant：24/7 Agent 與樹狀研究記憶'}
p=ROOT/'app.js';js=p.read_text(encoding='utf-8')
for key,src in images.items():
 pattern=re.compile(r'('+key+r":\{title:.*?body:`)(.*?)(`\},)",re.S)
 match=pattern.search(js)
 if not match:raise RuntimeError(key)
 body=re.sub(r'<figure.*?</figure>','',match.group(2),flags=re.S)
 metric=re.search(r'<p class="detail-metric">.*?</p>',body,re.S)
 pos=metric.end() if metric else body.index('</p>')+4
 figure=f'<figure class="detail-figure detail-diagram"><img src="{src}" alt="{labels[key]}" loading="lazy"><figcaption>{labels[key]}</figcaption></figure>'
 js=js[:match.start(2)]+body[:pos]+figure+body[pos:]+js[match.end(2):]
js=js.replace('CORNING TAIWAN ? SUMMER INTERN TEAM','CORNING TAIWAN · SUMMER INTERN TEAM').replace('GAT + D3QN ? STATIC ENVIRONMENT RESULTS','GAT + D3QN · STATIC ENVIRONMENT RESULTS')
p.write_text(js,encoding='utf-8')
p=ROOT/'index.html';s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
for key,src in images.items():
 row=s.select_one(f'.wafer-project-row[data-project="{key}"]')
 if 'has-thumb' not in row['class']:row['class'].append('has-thumb')
 im=row.select_one('.project-thumb')
 if not im:
  im=s.new_tag('img');im['class']=['project-thumb'];row.find('span').insert_after(im)
 im['src']=src;im['alt']=labels[key];im['loading']='lazy'
 row['aria-label']='閱讀'+labels[key]+'完整專案'
for script in s.select('script[src]'):
 if script['src'].split('?')[0]=='app.js':script['src']='app.js?v=20260916j'
for l in s.select('link[href]'):
 if l['href'].split('?')[0]=='project-media.css':l['href']='project-media.css?v=20260916j'
p.write_text(str(s),encoding='utf-8')
print('Synced five project images from resume to home details and list.')
