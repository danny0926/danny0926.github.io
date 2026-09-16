import copy,json
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from PIL import Image
path=Path('drinks.html');s=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
source='https://shop.tatenokawa.com/shop/products/4511802017807'
url='https://d2w53g1q050m78.cloudfront.net/shoptatenokawaco/ec_assets/a279bd65175e102751158750ff04bc5fc6cf204e-original.png'
asset=Path('assets/drinks/tatenokawa18.png');r=requests.get(url,timeout=25);r.raise_for_status();asset.write_bytes(r.content);Image.open(asset).verify()
card=copy.deepcopy(s.select_one('.bottle'))
card.h3.string='楯野川 · 十八（じゅうはち）'
card.select_one('.bottle-body p').string='純米大吟醸 · 雪女神 · 精米步合 18%'
card.select_one('.bottle-spec').decompose()
card.select_one('img')['src']='assets/drinks/tatenokawa18.png';card.select_one('img')['alt']='楯野川 純米大吟醸 十八 官方商品照片'
credit=card.select_one('.photo-credit');credit['href']=source;credit['aria-label']='楯野川十八 圖片來源'
price=card.select_one('.bottle-price a');price['href']=source;price.string='JPY ¥19,800'
card.select_one('.bottle-price small').string='含稅 · 官網 720ml／含盒版本'
s.select_one('#sake .bottle-grid').append(card)
for i,c in enumerate(s.select('.bottle'),1):c.select_one('.bottle-number').string=f'{i:02}'
s.select_one('.collection-count').contents[0].replace_with('10')
s.select_one('.drink-categories a[href="#sake"]').string='清酒 · 7';s.select_one('#sake .drink-heading span').string='SAKE / 07'
path.write_text(str(s),encoding='utf-8')
p=Path('assets/drinks/sources.json');data=json.loads(p.read_text(encoding='utf-8'));data.append(dict(file=asset.name,image=url,source=source));p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print('Added Tatenokawa 18. Collection: 10.')
