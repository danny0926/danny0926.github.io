import json
from pathlib import Path
from bs4 import BeautifulSoup

page = Path('drinks.html')
soup = BeautifulSoup(page.read_text(encoding='utf-8-sig'), 'html.parser')
images = json.loads(Path('assets/drinks/sources.json').read_text(encoding='utf-8'))
bottles = soup.select('.bottle')
mapping = [0,1,2,3,None,4,5]
for bottle, image_index in zip(bottles, mapping):
 figure = soup.new_tag('figure', attrs={'class':'bottle-photo'})
 if image_index is not None:
  record = images[image_index]
  figure.append(soup.new_tag('img', attrs={'src':'assets/drinks/'+record['file'], 'alt':bottle.h3.get_text()+' 商品照片', 'loading':'lazy', 'decoding':'async'}))
  source = soup.new_tag('a', attrs={'href':record['source'], 'target':'_blank', 'rel':'noopener noreferrer', 'class':'photo-credit', 'aria-label':bottle.h3.get_text()+' 圖片來源'})
  source.string = '圖片來源 ↗'
  figure.append(source)
 else:
  figure['class'] = 'bottle-photo bottle-photo-pending'
  label = soup.new_tag('span')
  label.string = '捨得酒'
  figure.append(label)
  subtitle = soup.new_tag('small')
  subtitle.string = '瓶款照片待補'
  figure.append(subtitle)
 bottle.insert(0, figure)
 body = soup.new_tag('div', attrs={'class':'bottle-body'})
 for node in list(bottle.contents):
  if node != figure:
   body.append(node.extract())
 bottle.append(body)
for section in soup.select('.drink-section'):
 entries = section.select('.bottle')
 if entries:
  grid = soup.new_tag('div', attrs={'class':'bottle-grid'})
  entries[0].insert_before(grid)
  for entry in entries:
   grid.append(entry.extract())
soup.select_one('link[href^="drinks.css"]')['href']='drinks.css?v=20260916cards'
note = soup.select_one('.collection-note')
note.string = '每一瓶的品飲筆記與故事，之後慢慢補上。'
page.write_text(str(soup), encoding='utf-8')
print('Created seven drink cards with six verified product photos.')
