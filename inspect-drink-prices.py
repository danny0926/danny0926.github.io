import requests, json, concurrent.futures, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
urls=['https://www.dutyzero.com.hk/item/p15772999','https://kikubijin.co.jp/sake/kohka/','https://kitaya.biz/shop/products/12735','https://dassai.com/product/main/23.html','https://store.shopping.yahoo.co.jp/nakamashuzo/600ml-12set']
def fetch(u):
 try:
  response=requests.get(u,timeout=25)
  s=BeautifulSoup(response.content,'html.parser');t=s.get_text(' ',strip=True)
  return {'url':u,'prices':re.findall(r'.{0,65}(?:円|HK\$|price|Price|HKD|¥).{0,80}',t),'links':[(a.get_text(' ',strip=True)[:30],urljoin(u,a.get('href',''))) for a in s.select('a') if any(k in str(a) for k in ['kohka','購入','光華','600ml'])],'imgs':[(i.get('alt',''),i.get('src','')) for i in s.select('img')][:6],'raw':re.findall(r'.{0,80}(?:salePrice|priceCurrency|15772999|og:image|\.js).{0,180}',str(s))[:12]}
 except Exception as e:return {'url':u,'error':str(e)}
for r in concurrent.futures.ThreadPoolExecutor().map(fetch,urls):print(json.dumps(r,ensure_ascii=True))
