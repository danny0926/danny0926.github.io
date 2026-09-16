from pathlib import Path
from html import escape
from math import sin

OUT=Path(__file__).parent/'assets'/'resume'
INK='#d9e2de'; MUTED='#8eaaa0'; GREEN='#7cc7ac'; PAPER='#e4e4d7'; DARK='#15201e'
def txt(x,y,t,size=20,color=INK):
 return f'<text x="{x}" y="{y}" font-family="Microsoft JhengHei,Arial,sans-serif" font-size="{size}" fill="{color}">{escape(t)}</text>'
def rect(x,y,w,h,fill,stroke='none',r=0):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'
def line(x,y,u,v,c=MUTED,w=2):
 return f'<path d="M{x} {y} L{u} {v}" fill="none" stroke="{c}" stroke-width="{w}"/>'
def circle(x,y,r,fill,stroke='none'):
 return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def note(title,a,b,c='',metric=''):
 return txt(670,100,title,27)+line(670,122,948,122,'#3c5149',1)+txt(670,166,a,19,MUTED)+txt(670,203,b,19,MUTED)+txt(670,240,c,19,MUTED)+txt(670,301,metric,22,GREEN)
def save(key,title,b):
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 380" role="img"><title>{escape(title)}，概念插圖</title><rect width="1000" height="380" fill="#111918"/>'+b+'</svg>'
 (OUT/f'{key}-illustration.svg').write_text(svg,encoding='utf-8')

# A question slip on a working data sheet: a still life, not a product mockup.
b=rect(142,83,360,244,'#263b33')+rect(126,66,360,244,PAPER)
b+=txt(151,99,'LOT / MEASUREMENT',13,'#53685b')
for i in range(6):
 y=128+i*25;b+=line(151,y,458,y,'#b7c0b3',1)
 for j in range(5):
  b+=rect(158+j*60,y+7,24+(j%2)*13,4,'#9eab9c')
b+=rect(352,119,258,113,'#81bca4')+txt(376,156,'這批資料有什麼異常？',19,DARK)+line(376,179,582,179,'#507e69',1)+txt(376,210,'讓查詢從一句問題開始',16,'#294b3c')
b+=circle(545,268,38,'none',GREEN)+line(571,296,601,326,GREEN,6)+line(526,269,539,281,GREEN,3)+line(539,281,564,253,GREEN,3)
b+=txt(151,286,'SQL / 受控資料操作',16,'#354d40')
save('agent','企業 AI Agent',b+note('獨立建置，上線使用','自然語言提問、撰寫 SQL','MCP 提供受控資料庫操作','架構、整合、部署獨立完成','約 80 使用人次／日'))

# One large wafer, with a recognizable spatial defect pattern.
b=circle(324,188,151,'#182822','#496457')
for y in range(-7,8):
 for x in range(-7,8):
  if x*x+y*y<=48:
   anomalous=(x>=3 and -4<=y<=4)
   c='#d4a177' if anomalous else '#4d8c72'
   b+=rect(324+x*19-7,188+y*19-7,14,14,c)
b+='<path d="M311 338 L324 325 L337 338" fill="#111918" stroke="#496457"/>'
b+=circle(492,152,56,'#182822','#d4a177')
for y in range(3):
 for x in range(3):b+=rect(461+x*21,121+y*21,16,16,'#d4a177' if x else '#4d8c72')
b+=line(531,192,555,218,'#d4a177',5)
save('wafer','Wafer Map 自動攔檢',b+note('Wafer Map 自動攔檢','原始數值與製程規則判讀','隨機森林：特徵工程與實驗','立案預估效益 3 億元','判讀表現約 99%'))

# Two aligned paper outputs with the significant flag field picked out.
b=''
for x,title in [(104,'原系統'),(362,'替代系統')]:
 b+=rect(x+8,69,226,256,'#263b33')+rect(x,59,226,256,PAPER)+txt(x+22,96,title,20,'#354d40')
 for i,label in enumerate(['TEST_NUM','RESULT','TEST_FLG','PARM_FLG']):
  y=143+i*43
  if i==2:b+=rect(x+14,y-22,196,33,'#a8c7b1')
  b+=txt(x+23,y,label,15,'#53685b')+line(x+135,y-5,x+193,y-5,'#7f9383',4)
b+=circle(337,259,27,GREEN)+line(325,259,334,268,DARK,3)+line(334,268,351,248,DARK,3)
b+=txt(110,349,'缺失值 ≠ 量測異常',18,MUTED)+txt(382,349,'Python + Cython',18,GREEN)
save('stdf','STDF 轉檔資料一致性',b+note('正確接手原系統','完整提取公司所需欄位','交叉比對量測值與 flag','Cython 加速大量資料處理','上線半年，未需進版'))

# GPU silhouette and a notebook of candidate code, not dashboard blocks.
b=rect(99,205,322,106,'#273c32','#698674',6)+rect(81,217,18,81,'#839282')
for x in [188,329]:
 b+=circle(x,258,37,'#14221b','#5b7763')+circle(x,258,10,'#647f6a')
 for a in range(8):
  b+=f'<path d="M{x} 232 q18 8 13 25" transform="rotate({a*45} {x} 258)" fill="none" stroke="#54745e" stroke-width="4"/>'
b+=rect(368,64,250,230,PAPER)+txt(390,101,'α / candidate',23,'#354d40')
for i,length in enumerate([166,124,180,148,101]):b+=line(391,133+i*23,391+length,133+i*23,'#809783' if i!=2 else '#3e795d',5)
b+=txt(390,267,'walk-forward / 退化檢查',14,'#53685b')
b+=txt(110,348,'共享 base 權重 + LoRA',19,GREEN)
save('ttt','TTT-Discover Alpha 挖掘',b+note('TTT-Discover 挖掘 Alpha','本地產碼、評分與 LoRA 更新','共享權重節省 5.19 GiB','樣本外驗證與退化解檢查','批次產碼評估加速 7.4×'))

# A continuously running agent and a research-memory tree, without process arrows.
b=circle(160,164,84,'#182822','#648574')
for i in range(12):
 b+=f'<path d="M160 89 V98" transform="rotate({i*30} 160 164)" stroke="#7cc7ac" stroke-width="2"/>'
b+=txt(101,177,'24/7',40,GREEN)+txt(93,285,'Agent 自動挖掘',20)+txt(79,317,'假說、產生因子、回測',16,MUTED)
b+=rect(294,56,319,272,PAPER)+txt(319,90,'樹狀研究記憶',21,'#354d40')
for x,y,u,v in [(452,132,452,156),(363,156,542,156),(363,156,363,192),(452,156,452,192),(542,156,542,192),(363,208,363,231),(329,231,397,231),(329,231,329,255),(397,231,397,255)]:b+=line(x,y,u,v,'#718c76',2)
for x,y in [(452,121),(363,199),(452,199),(542,199),(329,263),(397,263)]:b+=circle(x,y,11,'#6b9278')
b+=txt(318,306,'每個節點：假說 / 程式 / 回測',15,'#354d40')
save('worldquant','WorldQuant Agent Alpha 研究',b+note('持續挖掘，累積研究記憶','24/7 Agent 自動研究系統','樹狀記憶延續研究與分支','24,072 次回測 · 44 個 Alpha','WorldQuant 台灣區第四名'))
