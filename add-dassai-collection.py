import copy,json
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from PIL import Image

page=Path('drinks.html')
soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
grid=soup.select_one('#sake .bottle-grid')
template=grid.select_one('.bottle')
records=json.loads(Path('assets/drinks/sources.json').read_text(encoding='utf-8'))
prices=json.loads(Path('assets/drinks/prices.json').read_text(encoding='utf-8'))
anchor=template
for title,description,slug,filename,amount in [
 ('獺祭 · 早田','二割三分 · 純米大吟釀','hayata','dassai-hayata.jpg','JPY ¥14,300'),
 ('獺祭 · 三割九分','純米大吟釀','39','dassai39.jpg','JPY ¥3,080')
]:
 source=f'https://dassai.com/product/main/{slug}.html'
 remote=BeautifulSoup(requests.get(source,timeout=25).content,'html.parser')
 im=remote.select_one('main img')
 image_url=urljoin(source,im['src'])
 data=requests.get(image_url,timeout=25);data.raise_for_status()
 asset=Path('assets/drinks')/filename;asset.write_bytes(data.content);Image.open(asset).verify()
 card=copy.deepcopy(template)
 card.h3.string=title
 card.select_one('.bottle-body p').string=description
 card.select_one('.bottle-spec').decompose()
 photo=card.select_one('img');photo['src']='assets/drinks/'+filename;photo['alt']=title+' 商品照片'
 credit=card.select_one('.photo-credit');credit['href']=source;credit['aria-label']=title+' 圖片來源'
 price=card.select_one('.bottle-price a');price.string=amount;price['href']=source
 card.select_one('.bottle-price small').string='含稅 · 官網 720ml 版本'
 anchor.insert_after(card);anchor=card
 records.append(dict(file=filename,image=image_url,source=source))
 prices.append([amount,'含稅 · 官網 720ml 版本',source])
for index,card in enumerate(soup.select('.bottle'),1):
 card.select_one('.bottle-number').string=f'{index:02}'
count=soup.select_one('.collection-count')
count.contents[0].replace_with('09')
soup.select_one('.drink-categories a[href="#sake"]').string='清酒 · 6'
soup.select_one('#sake .drink-heading span').string='SAKE / 06'
soup.select_one('link[href^="drinks.css"]')['href']='drinks.css?v=20260916nine'
page.write_text(str(soup),encoding='utf-8')
Path('assets/drinks/sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
Path('assets/drinks/prices.json').write_text(json.dumps(prices,ensure_ascii=False,indent=2),encoding='utf-8')
print('Added two official Dassai photos and prices. Collection: 9, sake: 6.')
