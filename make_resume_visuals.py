from pathlib import Path
from html import escape
out=Path(__file__).parent/'assets'/'resume'
def text(x,y,s,size=18,color='#dce7e3',mono=False):
 return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-family="{ "Consolas,monospace" if mono else "Arial,sans-serif"}">{escape(s)}</text>'
def rect(x,y,w,h,fill='#1b2828',stroke='#344846',r=10):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'
def save(name,title,body):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="540" viewBox="0 0 1100 540" role="img"><title>{escape(title)} — illustrative mockup</title>'+rect(0,0,1100,540,'#121b1c','#121b1c',0)+text(38,42,title,15,'#8ce2c5',True)+text(858,42,'ILLUSTRATIVE MOCKUP',12,'#aabbb5',True)+body+'</svg>'
 (out/f'{name}-illustration.svg').write_text(s,encoding='utf-8')
# Agent: a product screen, not an architecture diagram.
b=rect(38,72,220,420)+text(62,110,'ENGINEERING ASSISTANT',15,'#8ce2c5')
for y,s in [(163,'Production query'),(213,'Measurement summary'),(263,'Lot investigation')]: b+=text(62,y,s,16)
b+=text(62,453,'MCP DATABASE TOOLS',13,'#8ce2c5',True)+rect(280,72,782,420)+rect(310,110,710,70,'#293d37')+text(334,152,'Summarize recent measurement anomalies.',21)
b+=text(310,224,'ANSWER',13,'#8ce2c5',True)+text(310,262,'Grouped by equipment and measurement type.',21)
for i,(s,v) in enumerate([('Equipment A','Flag review'),('Equipment B','Value distribution'),('Equipment C','Lot comparison')]):
 y=291+i*46;b+=rect(310,y,710,38,'#172222','#2b403b',4)+text(330,y+25,s,16)+text(640,y+25,v,16,'#abc6bc')
b+=rect(310,442,710,30,'#162522','#3d6556',5)+text(330,463,'Query completed · results organized for review',14,'#8ce2c5')
save('agent','AI AGENT / WORKSPACE',b)
# Wafer maps: visual comparison with synthetic die data.
b=text(58,98,'REFERENCE MAP',17)+text(580,98,'ANOMALY REVIEW',17)
for offset,bad in [(40,False),(565,True)]:
 b+=f'<circle cx="{offset+224}" cy="294" r="177" fill="#172627" stroke="#405a57" stroke-width="2"/>'
 for y in range(-6,7):
  for x in range(-6,7):
   if x*x+y*y<=39:
    color='#5eb99e' if not bad or not (x>2 and y>-3 and y<4) else '#e99b81'
    b+=rect(offset+224+x*24-10,294+y*24-10,20,20,color,color,2)
 b+=text(offset+45,495,'SYNTHETIC DIE DATA',12,'#aabbb5',True)
b+=rect(942,128,117,73,'#3c2d29','#9c705f')+text(955,158,'REVIEW',13,'#efb59d')+text(955,184,'EDGE BAND',12,'#efb59d')
save('wafer','WAFER MAP / INSPECTION VIEW',b)
# STDF: output review table.
b=text(48,106,'OUTPUT CONSISTENCY REVIEW',24)+text(48,141,'Illustrative records · customized fields and measurement flags',17,'#aabbb5')
cols=[48,232,428,650,869];heads=['RECORD','LEGACY OUTPUT','NEW OUTPUT','FLAG / MEANING','CHECK']
for x,h in zip(cols,heads):b+=text(x,196,h,13,'#8ce2c5',True)
rows=[('TEST_001','1.248','1.248','VALID','MATCH'),('TEST_002','0.976','0.976','VALID','MATCH'),('TEST_003','--','--','MISSING','MATCH'),('TEST_004','--','--','MEAS. FAULT','MATCH')]
for i,row in enumerate(rows):
 y=216+i*54;b+=rect(40,y,1015,45,'#192627','#314340',4)
 for x,v in zip(cols,row):b+=text(x,y+29,v,17,'#8ce2c5' if v=='MATCH' else '#dce7e3',True)
b+=text(48,476,'DATA MEANING PRESERVED',17,'#8ce2c5',True)+text(590,476,'Cython · customized field extraction',17,'#aabbb5')
save('stdf','STDF / DATA REVIEW',b)
# TTT: code and evaluated candidates side-by-side. No arrows.
b=rect(38,80,520,410)+text(60,115,'ALPHA CANDIDATE / CODE',14,'#8ce2c5',True)
for i,line in enumerate(['def alpha(data):','    signal = rolling_rank(','        data["feature"], window=20','    )','    return normalize(signal)']):b+=text(64,163+i*33,line,18,'#b6cbd9',True)
b+=text(64,420,'LOCAL CODER + LoRA',16,'#8ce2c5',True)+text(64,453,'Candidate code shown for illustration',14,'#aabbb5')
b+=rect(582,80,480,410)+text(606,115,'EXPERIMENT NOTEBOOK',14,'#8ce2c5',True)
for i,(a,c) in enumerate([('Generation','16 fixed ideas'),('Code evaluation','39.52 s → 5.34 s'),('Shared weights','18.82 → 13.63 GiB'),('Validation','Walk-forward + checks')]):
 y=151+i*72
 b+=text(606,y,a,16,'#aabbb5')+text(606,y+31,c,22,'#8ce2c5')
save('ttt','TTT-DISCOVER / ALPHA EXPERIMENT',b)
# WorldQuant: a research desk with real summary metrics and illustrative cards.
b=''
for x,n,l in [(38,'04','TAIWAN RANK'),(385,'24,072','BACKTESTS'),(732,'44','SUBMITTED ALPHAS')]:
 b+=rect(x,80,330,117)+text(x+22,129,n,38,'#8ce2c5',True)+text(x+22,166,l,13,'#aabbb5',True)
b+=text(38,239,'24/7 AGENT RESEARCH DESK',20)+text(740,239,'TREE-STRUCTURED MEMORY',13,'#8ce2c5',True)
for i,(h,s,n) in enumerate([('HYPOTHESIS','Volume / price interaction','Saved rationale + expression'),('EXPERIMENT','Candidate backtest review','Saved metrics + observations'),('RESEARCH MEMORY','Next investigation notes','Parent context + alternatives')]):
 x=38+i*347;b+=rect(x,267,330,211)+text(x+20,302,h,14,'#8ce2c5',True)+text(x+20,346,s,18)+text(x+20,386,n,15,'#aabbb5')
 for j in range(3):b+=rect(x+20,413+j*14,260-j*40,5,'#49685d','#49685d',2)
save('worldquant','WORLDQUANT / RESEARCH WORKSPACE',b)
