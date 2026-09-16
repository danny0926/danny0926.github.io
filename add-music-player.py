from pathlib import Path
from bs4 import BeautifulSoup
path=Path('jpop.html')
soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
status=soup.new_tag('span',attrs={'class':'playback-status mono','role':'status'});status.string='尚未播放'
soup.select_one('.rotation-control').replace_with(status)
for ident,video,title in [('pieces','gidBYApkqhI','Pieces'),('blan','pr8jE4Rh81M','blan_')]:
 panel=soup.select_one('#'+ident)
 section=soup.new_tag('section',attrs={'class':'song-player','aria-label':title+' YouTube 播放器'})
 frame=soup.new_tag('div',attrs={'class':'youtube-frame'})
 frame.append(soup.new_tag('div',attrs={'class':'youtube-mount','id':'youtube-'+ident}))
 button=soup.new_tag('button',attrs={'class':'youtube-load','data-video':video});button.string='▶ 在這裡聽 '+title
 frame.append(button)
 message=soup.new_tag('p',attrs={'class':'player-message','role':'status'});message.string='YOUTUBE / 點一下載入播放器'
 section.append(frame);section.append(message)
 panel.select_one('.listen-link').insert_before(section)
soup.select_one('script[src^="personal-jpop.js"]')['src']='music-youtube.js?v=20260916play'
soup.select_one('link[href^="personal-jpop.css"]')['href']='personal-jpop.css?v=20260916play'
path.write_text(str(soup),encoding='utf-8')
