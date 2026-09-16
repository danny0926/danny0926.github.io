from pathlib import Path
from bs4 import BeautifulSoup
p=Path(__file__).parent/'resume.html'
s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
for image in s.select('img[src*="-illustration.svg"]'):
 image['src']=image['src'].split('?')[0]+'?v=20260916h'
wq=s.select('#independent .cv-entry')[1]
wq.h3.string='WorldQuant / 24/7 Agent Alpha 挖掘'
wq.p.clear()
wq.p.append('建立 24/7 自動運作的 Agent Alpha 挖掘系統，串接研究假說、因子生成與回測。以樹狀研究記憶保存各分支的假說、程式、回測結果與後續方向，讓下一輪探索延續既有成果。累計 24,072 次回測、44 個已提交 Alpha，取得 WorldQuant 台灣區第四名。')
p.write_text(str(s),encoding='utf-8')
