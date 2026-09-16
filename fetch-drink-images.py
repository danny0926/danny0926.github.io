import concurrent.futures
import json
from pathlib import Path
import requests
from PIL import Image, ImageDraw

assets = Path('assets/drinks')
assets.mkdir(parents=True, exist_ok=True)
items = [
 ('dassai23.jpg', 'https://dassai.com/files/dassai-2wari3bu.jpg', 'https://dassai.com/product/main/23.html'),
 ('shiro-uguisu.jpg', 'https://makeshop-multi-images.akamaized.net/onosaketen/itemimages/000000000705_SAcJwOQ.jpg', 'https://onosaketen.jp/view/item/000000000705'),
 ('kohka.webp', 'https://kikubijin.co.jp/wp/wp-content/uploads/2025/04/DSC01943_qp-1.webp', 'https://kikubijin.co.jp/sake/kohka/'),
 ('kitaya.jpg', 'https://d2w53g1q050m78.cloudfront.net/kitayabiz/ec_assets/25cf92de36f9f90221d6b56a5a2b792b8c73d943-original.jpg', 'https://kitaya.biz/shop/products/12735'),
 ('miyanotsuru.jpg', 'https://item-shopping.c.yimg.jp/i/n/awamoriya_302', 'https://store.shopping.yahoo.co.jp/awamoriya/302.html'),
 ('zanpa-blue.png', 'https://static.wixstatic.com/media/d4e029_b4f2a330061e44e280ecb4637641f104~mv2.png', 'https://www.zanpa.co.jp/%E8%A4%87%E8%A3%BD-zanpa-white-new-1'),
]
def fetch(item):
 name, url, source = item
 response = requests.get(url, timeout=30)
 response.raise_for_status()
 (assets / name).write_bytes(response.content)
 im = Image.open(assets / name)
 im.verify()
 return dict(file=name, image=url, source=source)
records = list(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(fetch, items))
(assets / 'sources.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
sheet = Image.new('RGB', (1200, 450), '#eeeeee')
draw = ImageDraw.Draw(sheet)
for i, record in enumerate(records):
 im = Image.open(assets / record['file']).convert('RGBA')
 im.thumbnail((180, 390))
 sheet.paste(im, (i * 200 + (200-im.width)//2, 30 + (390-im.height)//2), im)
 draw.text((i * 200 + 8, 420), record['file'], fill='black')
sheet.save(assets / 'image-check.jpg')
print('Downloaded and decoded', len(records), 'bottle images.')
