import copy,json
from pathlib import Path
from bs4 import BeautifulSoup
page=Path('drinks.html');s=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
source='https://ec.tamanohikari.co.jp/products/blacklabel'
image='https://cdn.shopify.com/s/files/1/0549/3394/6565/files/BL720_1.jpg?v=1750135936'
card=copy.deepcopy(s.select_one('.bottle'))
card.h3.string='玉乃光 · BLACK LABEL'
card.select_one('.bottle-body p').string='純米大吟釀 · 黑瓶黑盒'
card.select_one('.bottle-spec').string='720 ml'
card.select_one('img')['src']='assets/drinks/tamanohikari-black.jpg';card.select_one('img')['alt']='玉乃光 BLACK LABEL 720ml 黑色瓶身與黑色禮盒 官方商品圖片'
credit=card.select_one('.photo-credit');credit['href']=source;credit['aria-label']='玉乃光 BLACK LABEL 圖片來源'
price=card.select_one('.bottle-price a');price['href']=source;price.string='JPY ¥13,200'
card.select_one('.bottle-price small').string='含稅 · 官網 720ml／含盒版本'
grid=s.select_one('#sake .bottle-grid');grid.select('.bottle')[-1].insert_before(card)
for i,c in enumerate(s.select('.bottle'),1):c.select_one('.bottle-number').string=f'{i:02}'
s.select_one('.collection-count').contents[0].replace_with('11')
s.select_one('.drink-categories a[href="#sake"]').string='清酒 · 8';s.select_one('#sake .drink-heading span').string='SAKE / 08'
page.write_text(str(s),encoding='utf-8')
for filename,entry in [('sources.json',dict(file='tamanohikari-black.jpg',image=image,source=source)),('prices.json',['JPY ¥13,200','含稅 · 官網 720ml／含盒版本',source])]:
 path=Path('assets/drinks')/filename;data=json.loads(path.read_text(encoding='utf-8'));data.append(entry);path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print('Added verified black bottle/box photo and official JPY price.')
