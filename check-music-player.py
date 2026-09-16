from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True)
 page=browser.new_page(viewport={'width':1280,'height':900})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8767/jpop.html',wait_until='networkidle')
 assert not page.locator('body').evaluate('(el)=>el.classList.contains("is-rotating")')
 page.locator('#pieces .youtube-load').click()
 try:
  page.locator('#pieces iframe').wait_for(timeout=20000)
  print('Pieces: YouTube iframe loaded.')
 except Exception:
  print('Pieces message:',page.locator('#pieces .player-message').inner_text())
 page.locator('[data-select="blan"]').click()
 page.locator('#blan .youtube-load').click()
 try:
  page.locator('#blan iframe').wait_for(timeout=20000)
  print('blan_: YouTube iframe loaded.')
 except Exception:
  print('blan message:',page.locator('#blan .player-message').inner_text())
 page.wait_for_timeout(3000)
 print('Messages:',page.locator('.player-message').all_inner_texts())
 assert not errors,errors
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 print('No JavaScript errors; mobile width fits.')
 browser.close()
