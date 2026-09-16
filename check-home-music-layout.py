import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 page=browser.new_page(viewport={'width':1440,'height':900})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8767/index.html',wait_until='domcontentloaded')
 page.locator('.home-bgm iframe').wait_for(timeout=25000)
 geometry=page.evaluate('''() => {
  const music=document.querySelector('.home-bgm');
  const wafer=document.querySelector('.wafer-hero');
  const contact=document.querySelector('#contact');
  const a=music.getBoundingClientRect(), b=wafer.getBoundingClientRect(), c=contact.getBoundingClientRect();
  return {position:getComputedStyle(music).position, width:a.width, height:a.height, waferBottom:b.bottom, musicTop:a.top, musicBottom:a.bottom, contactTop:c.top};
 }''')
 print(json.dumps(geometry))
 assert geometry['position'] not in ['fixed','absolute'],geometry
 assert geometry['musicTop']>=geometry['waferBottom']-1,geometry
 assert geometry['musicBottom']<=geometry['contactTop']+1,geometry
 for width in [390,768,1024]:
  page.set_viewport_size({'width':width,'height':844})
  page.wait_for_timeout(200)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
 assert not errors,errors
 print('Player occupies its own section, never overlaps wafer/contact, and fits mobile/tablet.')
 browser.close()
