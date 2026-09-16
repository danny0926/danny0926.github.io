import copy
from pathlib import Path
from bs4 import BeautifulSoup

page = Path('drinks.html')
s = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
source = 'https://www.damm.com/en/beers/inedit'
if not s.select_one('#beer .bottle'):
    card = copy.deepcopy(s.select_one('.bottle'))
    card.h3.string = '西班牙金星啤酒 · Inedit Damm'
    card.select_one('.bottle-body p').string = '麥芽與小麥調和的佐餐啤酒 · 西班牙'
    card.select_one('.bottle-spec').string = '750 ml · 4.8%'
    card.select_one('img')['src'] = 'assets/drinks/inedit.png'
    card.select_one('img')['alt'] = 'Inedit Damm 金色星星、紅色瓶頸標籤的黑色酒瓶，官方圖片'
    credit = card.select_one('.photo-credit')
    credit['href'] = source
    credit['aria-label'] = 'Inedit Damm 官方圖片來源'
    price = card.select_one('.bottle-price a')
    price['href'] = 'https://shop.damm.com/es/producto/cervezainedit/84372'
    price.string = '750 ml 官網未列售價'
    card.select_one('.bottle-price small').string = '西班牙 · 不以其他容量價格換算'
    section = s.select_one('#beer')
    section.select_one('.empty-shelf').decompose()
    grid = s.new_tag('div', attrs={'class': 'bottle-grid'})
    grid.append(card)
    section.append(grid)
s.select_one('#beer .drink-heading span').string = 'BEER / 01'
s.select_one('.drink-categories a[href="#beer"]').string = '啤酒 · 1'
s.select_one('.collection-count').contents[0].replace_with('12')
for i, card in enumerate(s.select('.bottle'), 1):
    card.select_one('.bottle-number').string = f'{i:02}'
page.write_text(str(s), encoding='utf-8')
p = Path('wafer-home.jsx')
p.write_text(p.read_text(encoding='utf-8').replace('11 款收藏 / 飲酒筆記', '12 款收藏 / 飲酒筆記'), encoding='utf-8')
