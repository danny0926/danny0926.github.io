from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).parent
p=ROOT/'voice.html';s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
def fragment(html):return BeautifulSoup(html,'html.parser')
note=s.select_one('.personal-note')
note.h2.clear();note.h2.append('先記住角色，');note.h2.append(s.new_tag('br'));note.h2.append('再驚訝原來也是她。')
copy=note.select_one('.personal-note-copy');copy.clear()
for node in list(fragment('''<p>現在的聲優，往往不只需要配音，也要唱歌、上節目、站上舞台。外貌、舞台魅力與各式各樣的才藝，都成為大家認識一位聲優的入口。但對我來說，最讓我在意的，始終是她能不能用聲音，讓角色真正活起來。</p><p>夏吉ゆうこ就是這樣讓我著迷的人。我覺得她的配音實力，在新生代裡很突出。同一位聲優，能讓不同角色擁有自己的語氣、節奏與情緒；有時候沒先看出演名單，我甚至不會立刻認出那是她的聲音。</p><span class="mono">— DANNY / 我的聲優手帖</span>''').contents):copy.append(node)
fav=s.select_one('.favorite-role');paras=fav.find_all('p');paras[-1].clear();paras[-1].append('千砂是我的第一順位。她的聲音帶著親密與黏人的一面，讓每句話都像是在對你說。對，就是那隻讓我想替她多留一頁的「甜點貓」。')
arc=s.select_one('#arcade .reading-copy');old=arc.find_all('p',recursive=False)
texts=['一個跟著夏吉尋找「喜歡」的外景綜藝。走進感興趣的地方，體驗想做的事情，讓好奇心決定這一趟要往哪裡走。','她喜歡喝酒，剛好也和我的興趣相符。我尤其喜歡早期節目裡，她偷偷喝上一口的樣子：有點調皮，又很自在，實在很可愛。比起刻意維持形象，我更喜歡那些不經意流露出來的反應。','現在我比較少在公開場合看到那麼奔放的她，但在自己的番組裡，仍然能遇見那份自由。看她出門探索、聊天，認真享受自己喜歡的事情，對我來說，也是認識夏吉很重要的一部分。','吸引我的，還有我感受到的反差：鏡頭前很放得開，鏡頭之外給我的印象卻是安安靜靜的。角色之外的她，又是另一種吸引力。']
for e in old:e.decompose()
links=arc.select_one('.arcade-links')
for text in texts:
 e=s.new_tag('p');e.string=text;e['class']=['fan-note'];links.insert_before(e)
grid=s.select_one('#animation .voice-role-grid')
card=fragment('''<article class="voice-role"><figure class="character-art"><img alt="ヤニねこ：動畫官方角色立繪" loading="lazy" src="assets/characters/yanineko.webp"/></figure><span class="mono">ANIMATION / DANNY'S NOTE</span><h3>ヤニねこ</h3><p class="role-work">ヤニねこ / 尼古貓貓</p><p>我喜歡她在這個角色裡自由、多變的演出。和千砂的親密、かぐや的活潑放在一起聽，更能感受到她塑造角色的幅度。</p><a class="character-source" href="https://yanineko-anime.com/#anchor-chara" rel="noopener noreferrer" target="_blank">官方角色圖片與配音資料 ↗</a></article>''').article
if not grid.find('img',src='assets/characters/yanineko.webp'):grid.find('article').insert_after(card)
for card in s.select('#animation .voice-role'):
 name=card.h3.get_text()
 if name=='かぐや':card.select('p')[-1].string='我喜歡かぐや開朗活潑的聲音。語氣裡那股往前衝的能量，讓角色不只是熱鬧，也讓我想跟著她一起走進故事。'
 if name=='サーシャ・ネクロン':card.select('p')[-1].string='我聽見的是身為姐姐的責任感。和千砂的親密語氣相比，她在這裡讓角色站得更穩，也讓我更注意到演技的差異。'
for card in s.select('#game .voice-role'):
 if 'カズサ' in card.h3.get_text():card.select('p')[-1].string='我的最愛。親密、黏人的語氣，讓我先記住了這隻「甜點貓」，再開始追著夏吉的其他作品聽。'
roles=s.select_one('#roles');roles.select_one('.section-heading > p').string='語氣、節奏與情緒各有自己的樣子。這些角色，讓我一次次驚訝於她的聲音。'
closing=s.new_tag('p');closing['class']=['voice-personal-closing'];closing.string='最初讓我停下來的是角色，讓我一直想看下去的，則是她本人。'
roles.append(closing)
link=s.new_tag('link',href='voice-notes.css?v=20260916m',rel='stylesheet');s.head.append(link)
p.write_text(str(s),encoding='utf-8')
print('Personal notes integrated; official Yani Neko character added.')
