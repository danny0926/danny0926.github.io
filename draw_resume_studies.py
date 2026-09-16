from pathlib import Path
from html import escape
OUT=Path(__file__).parent/'assets'/'resume'
def t(x,y,s,size=20,c='#e5eeea'):
 return f'<text x="{x}" y="{y}" font-family="Microsoft JhengHei,Arial,sans-serif" font-size="{size}" fill="{c}">{escape(s)}</text>'
def r(x,y,w,h,c='#1c2627',stroke='#344746',rad=12):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rad}" fill="{c}" stroke="{stroke}"/>'
def ln(x,y,u,v):return f'<path d="M{x} {y} L{u} {v}" stroke="#344746" fill="none"/>'
def base(title,sub):return r(0,0,1200,760,'#12191a','#12191a',22)+t(48,58,'01 / 實作內容',16,'#8ee1c5')+t(48,105,title,30)+t(48,137,sub,17,'#a9b9b2')
def results(title):return ln(48,466,1152,466)+t(48,510,'02 / '+title,16,'#8ee1c5')
def stat(x,value,label,extra):return t(x,581,value,37,'#8ee1c5')+t(x,625,label,21)+t(x,663,extra,17,'#a9b9b2')
def save(k,title,s):
 (OUT/f'{k}-illustration.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760" role="img"><title>{escape(title)}</title>'+s+'</svg>',encoding='utf-8')

s=base('企業 AI Agent：把自然語言問題接上實際資料','由我獨立完成架構、MCP 工具、資料整合、應用與部署。下列查詢為示意。')
s+=r(48,168,524,264)+r(596,168,556,264)
s+=t(72,207,'使用者問題與 SQL 查詢',22)+t(72,251,'「各機台今天有多少筆量測紀錄？」',20,'#8ee1c5')
for i,l in enumerate(['SELECT equipment_id, COUNT(*)','FROM measurements','WHERE measured_at >= :today','GROUP BY equipment_id;']):s+=t(72,296+i*28,l,19,'#a9b9b2')
s+=t(620,207,'MCP 資料庫工具',22)+t(620,247,'提供受控操作，取得真實查詢結果',20,'#8ee1c5')
s+=t(620,294,'機台',18)+t(855,294,'量測筆數',18)
for i,(a,b) in enumerate([('EQ-A','120'),('EQ-B','86'),('EQ-C','104')]):
 y=330+i*33;s+=ln(620,y-22,1120,y-22)+t(620,y,a,19)+t(855,y,b,19)
s+=results('上線與使用成果')+stat(48,'約 80 人次／日','每日使用人次直接統計','已進入工程師日常工作')+stat(650,'獨立完成','架構、整合、實作與上線','工具查詢資料，模型整理回覆')
save('agent','企業 AI Agent 實作與上線成果',s)

s=base('Wafer Map：從原始數值判讀，定位異常分布','先釐清資料表示方式，再以數值與製程規則建立攔檢判斷。晶圓資料為示意。')
s+=r(48,168,524,264)+r(596,168,556,264)+t(72,205,'die 分布與異常區域',22)
for y in range(-5,6):
 for x in range(-5,6):
  if x*x+y*y<=27:s+=r(233+x*17,292+y*17,13,13,'#d7a480' if x>2 and abs(y)<4 else '#659f89','none',1)
s+=t(357,281,'異常集中區',18,'#d7a480')+t(357,315,'保留空間分布',17,'#a9b9b2')+t(357,345,'回看原始數值',17,'#a9b9b2')
s+=t(620,205,'判讀方法與持續研究',22)
for y,a,b in [(252,'資料表示','避免影像轉換引入人為表示差異'),(317,'既有方案','原始數值與製程規則'),(382,'隨機森林','持續進行特徵工程與模型實驗')]:
 s+=t(620,y,a,17,'#8ee1c5')+t(743,y,b,18)
s+=results('專案成果')+stat(48,'約 99%','既有判讀表現','涵蓋攔檢與放行判斷')+stat(650,'NT$ 3 億','立案預估專案效益','由產線工程師於申請時估算')
save('wafer','Wafer Map 自動攔檢方法與成果',s)

s=base('STDF：不只轉出數值，也保留量測資料的意義','客製化 Python 開源轉檔系統，完整提取公司使用欄位，再以 Cython 加速。')
s+=r(48,168,1104,264)+t(72,208,'新舊系統交叉比對：缺失值與量測旗標',22)
for x,a in [(72,'情況'),(325,'量測值'),(513,'其他欄位／旗標'),(844,'轉檔後判讀')]:s+=t(x,251,a,18,'#8ee1c5')
for i,row in enumerate([('一般量測','有數值','量測有效','保留量測結果'),('真正缺失','未提供','欄位與旗標共同確認','標記缺失'),('量測異常','不可直接採用','存在故障／異常紀錄','保留異常意義')]):
 y=300+i*49;s+=ln(72,y-25,1125,y-25)
 for x,a in zip([72,325,513,844],row):s+=t(x,y,a,19)
s+=results('交付與系統替代')+stat(48,'Cython','加速大量資料處理','客製欄位，核對新舊輸出')+stat(435,'6 個月','上線後未需修改或進版','穩定接手既有轉檔工作')+stat(819,'約 600 萬／年','原系統維運成本','提出替代方案的成本背景')
save('stdf','STDF 缺失值處理與交付成果',s)

s=base('TTT-Discover：在單卡上完成 Alpha 挖掘實驗','共用模型權重進行本地產碼與 LoRA 更新，以驗證結果判斷候選因子。')
s+=r(48,168,524,264)+r(596,168,556,264)+t(72,209,'生成與更新，共享一份 base 權重',22)
s+=r(79,240,459,65,'#314d45','#81bca8')+t(109,281,'Qwen2.5-Coder-7B + LoRA',24)
s+=t(79,346,'產碼：本地 Coder 生成 Alpha 程式',19)+t(79,388,'更新：開啟 train step，進行 40 輪實驗',19)
s+=t(620,209,'候選 Alpha 的驗證重點',22)
for y,a,b in [(260,'程式檢查','能執行，且輸出形式有效'),(323,'退化解檢查','排除恆等於 1 等假因子'),(386,'walk-forward','以樣本外 Sharpe 重新排名')]:s+=t(620,y,a,18,'#8ee1c5')+t(784,y,b,18)
s+=results('記憶體與固定 16 個 idea 的批次實驗')
for x,title,rows,maxv,unit in [(48,'共享權重 / 4-bit',[('兩份模型',18.82),('共享模型',13.63)],24,'GiB'),(650,'產碼、驗證與評分完成時間',[('併發 1',39.52),('併發 16',5.34)],45,'秒')]:
 s+=t(x,555,title,21)
 for i,(a,v) in enumerate(rows):
  y=604+i*58;s+=t(x,y+7,a,18)+r(x+107,y-15,v/maxv*267,26,'#7fc8ad','none',3)+t(x+390,y+7,f'{v:.2f} {unit}',18)
s+=t(48,724,'節省 5.19 GiB 的 PyTorch allocated 峰值',18,'#8ee1c5')+t(650,724,'完成時間中位數：加速約 7.4 倍',18,'#8ee1c5')
save('ttt','TTT-Discover 單卡實作與量測結果',s)
