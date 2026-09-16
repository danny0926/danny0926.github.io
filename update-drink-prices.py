import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from PIL import Image

page=Path('drinks.html')
soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
bottles=soup.select('.bottle')
source='https://www.dutyzero.com.hk/item/p15772999'
remote=BeautifulSoup(requests.get(source,timeout=25).content,'html.parser')
image_url=remote.select_one('meta[property="og:image"]')['content']
response=requests.get(image_url,timeout=25);response.raise_for_status()
asset=Path('assets/drinks/shede-taian.jpg');asset.write_bytes(response.content)
Image.open(asset).verify()
figure=bottles[4].select_one('figure');figure.clear();figure['class']='bottle-photo'
figure.append(soup.new_tag('img',attrs={'src':str(asset).replace('\\','/'),'alt':'舍得酒 泰安古釀 52度 500毫升 商品照片','loading':'lazy','decoding':'async'}))
credit=soup.new_tag('a',attrs={'href':source,'class':'photo-credit','target':'_blank','rel':'noopener noreferrer'});credit.string='圖片來源 ↗';figure.append(credit)
bottles[4].h3.string='舍得酒 · 泰安古釀'
bottles[4].select_one('.bottle-body p').string='免稅通路限定 · 香港機場購入'
spec=soup.new_tag('span',attrs={'class':'bottle-spec mono'});spec.string='52% · 500 ml';bottles[4].select_one('.bottle-body').append(spec)
prices=[
 ('JPY ¥6,380','含稅 · 720ml／無盒','https://dassai.com/product/main/23.html'),
 ('JPY ¥8,800','含稅 · 720ml／2023 官方公告價','https://niwanouguisu.com/news/『しろうぐ』発売のお知らせ/'),
 ('JPY ¥22,000','含稅 · 官網現售 740ml 版本','https://kikubijin.shop-pro.jp/'),
 ('JPY ¥5,500','含稅 · 720ml','https://kitaya.biz/shop/products/12735'),
 ('官網未公開售價','免稅限定 · 500ml','https://spirit-of-china.net/zh/products/shede-founder-s-tribute-%E8%88%8D%E5%BE%97-%E6%B3%B0%E5%AE%89%E5%8F%A4%E9%85%BF'),
 ('官網未列單瓶價格','600ml · 酒造直售需詢價','https://miyanotsuru.com/order/'),
 ('JPY ¥2,150','含稅 · 官網建議售價／720ml','https://www.zanpa.co.jp/%E8%A4%87%E8%A3%BD-zanpa-white-new-1'),
]
for bottle,(amount,detail,url) in zip(bottles,prices):
 block=soup.new_tag('div',attrs={'class':'bottle-price'})
 link=soup.new_tag('a',attrs={'href':url,'target':'_blank','rel':'noopener noreferrer'});link.string=amount
 small=soup.new_tag('small');small.string=detail
 block.append(link);block.append(small);bottle.select_one('.bottle-body').append(block)
note=soup.new_tag('p',attrs={'class':'collection-note price-date'})
note.string='價格保留官網原幣別，不含運費。查核：2026.09.16。'
soup.select_one('.collection-note').insert_before(note)
soup.select_one('link[href^="drinks.css"]')['href']='drinks.css?v=20260916prices'
page.write_text(str(soup),encoding='utf-8')
records=json.loads(Path('assets/drinks/sources.json').read_text(encoding='utf-8'))
records.append(dict(file=asset.name,image=image_url,source=source))
Path('assets/drinks/sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
Path('assets/drinks/prices.json').write_text(json.dumps(prices,ensure_ascii=False,indent=2),encoding='utf-8')
print('Updated 7 price labels and exact Shede bottle photograph.')
