import json
from pathlib import Path

p = Path('data/drinks.json')
items = json.loads(p.read_text(encoding='utf-8'))
summaries = {
    'sake-1': '使用山田錦，精米步合 23%。\n酒藏描述為華麗香氣與如蜂蜜般的甜感。',
    'sake-2': '以取得專利的技術，呈現剛榨取清酒的新鮮風味。\n二割三分系列的純米大吟釀。',
    'sake-3': '酒藏描述為華麗香氣、平衡的甜感。\n飲後有持續的餘韻。',
    'sake-4': '福岡縣山口酒造場，以山田錦釀製。\n以袋吊雫搾方式取酒，通路形容口感細緻、透明。',
    'sake-5': '酒藏定位為品牌頂級酒款。\n描述為馥郁香氣、豐富甜感與乾淨且持續的餘韻。',
    'sake-6': '使用糸島產山田錦。\n2013 年獲 IWC 日本酒部門 Champion Sake。',
    'sake-7': '使用 100% 雄町米，精米步合 35%。\n官方標示酒精濃度為 15%。',
    'sake-8': '使用雪女神米，精米步合 18%。\n酒藏強調細緻風味與原料米旨味的呈現。',
    'baijiu-1': '香港機場免稅通路的泰安古釀版本。\n通路標示為 52 度、500 毫升。',
    'awamori-1': '石垣島宮良的仲間酒造釀製。\n酒造描述為芳醇香氣與柔和甜感。',
    'awamori-2': '調和 60% 的五年古酒，酒精濃度 30%。\n官方描述為甕貯藏風味與熟成帶來的香氣、厚度。\n藍色酒瓶以沖繩的海與天空為設計意象。',
    'beer-1': '由 Damm 釀酒團隊與 Ferran Adrià、elBulli 侍酒師團隊共同開發。\n結合大麥麥芽與小麥啤酒，加入芫荽、甘草與橙皮。\n定位為搭配餐食的啤酒，酒精濃度 4.8%。',
}
for item in items:
    item.setdefault('officialSummary', summaries.get(item['id'], ''))
    item.setdefault('officialSource', item['source'])
    if item['id'] == 'awamori-1':
        item['officialSource'] = 'https://miyanotsuru.com/'
    if item['id'] in ('sake-4', 'baijiu-1'):
        item['informationLabel'] = 'PRODUCT NOTES / 通路資訊摘要'
p.write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
