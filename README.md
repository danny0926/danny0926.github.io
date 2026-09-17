# Danny's Lab

個人網站、履歷、夏吉ゆうこ聲優手帖與 J-POP 音樂頁。原生 HTML、CSS、JavaScript，不需要安裝套件。

目前僅在本機開發與預覽；不再部署至 GPT／Sites 網域。

## 本機預覽

在此目錄執行：

```powershell
python -m http.server 8767 --bind 127.0.0.1
```

開啟 http://127.0.0.1:8767/ 。聲優專題位於 `/voice.html`。

## 修改內容

- `index.html`：首頁、專案摘要、個人介紹。
- `app.js`：專案詳情、研究筆記、首頁互動。
- `voice.html`：喜歡夏吉的理由、千砂、演出與作品。
- `voice.js`：作品頁籤、影片載入、主題切換。
- `resume.html`：完整 HTML 履歷，含列印樣式。近期職稱與專案狀態以此頁為準，既有 PDF 保留原檔。
- `jpop.html`：第一輯探索選曲，尚未宣稱為 Danny 的個人最愛排行。
- `page.js`：新頁面的主題與列印功能。
- `style.css`、`extended.css`：共用樣式、手機排版與各專題樣式。
- `assets/`：圖片與履歷。

網站以朋友網站的終端機／ASCII 氛圍為視覺參考，程式碼重新製作。

執行 `python build_static.py` 可將網站檔案同步到本機 `dist/`。來源檔保留在根目錄；不會上傳或部署。

## 素材與資料來源

- 夏吉肖像、出演資料：[賢プロダクション](https://www.kenproduction.co.jp/talent/202)。肖像權利屬原權利人。
- ray 演出與縮圖：[THE FIRST TAKE 官方影片](https://www.youtube.com/watch?v=5DXqEa-7-Wg)。影片採 YouTube 嵌入，按播放才載入。
- 本頁為非官方個人手帖；喜歡的理由為 Danny 的個人觀感。
- 外景節目圖片與簡介：[アーケードでいきましょう](https://www.openrec.tv/user/yuko_natsuyoshi)。官方 X：[akms_staff](https://x.com/akms_staff)。
- 近期動畫圖片：[超かぐや姫！](https://www.cho-kaguyahime.com/)、[ヤニねこ](https://yanineko-anime.com/)、[グロウアップショウ](https://growupshow.com/)、[花ざかりの君たちへ](https://hanakimi-anime.com/character/02.html)、[笑顔のたえない職場です。](https://www.egatae.com/)。圖片權利屬各作品原權利人；各卡片提供原始官方連結。
- Arika：[官方介紹](https://arika.bitfan.id/contents/menu/71138)；うたごえはミルフィーユ：[官方網站](https://utamille.com/)。
- J-POP 文字封面為網站原創排版，並非唱片原封面。歌曲卡片連到官方作品頁。

影片與外部音樂入口需要網路。複製信箱功能在 localhost／HTTPS 可使用，瀏覽器不支援時提供提示。


## GitHub Pages

https://danny0926.github.io/

Push to main automatically builds and deploys the static site through .github/workflows/pages.yml.


## Drinks admin

Open https://danny0926.github.io/admin/. Create a fine-grained GitHub token for danny0926.github.io only, with Contents read/write. Enter it in the admin page, never commit or send the token in chat. The token stays in tab memory. Edit entries, save drafts, then publish. JSON and uploaded images are committed together and trigger Pages deployment. Drafts are not persistent; export JSON before leaving (keep original unuploaded images separately). Canonical drinks data lives in data/drinks.json; drinks.html remains a fallback snapshot.
