(() => {
  const page = document.querySelector('.music-page');
  if (!page) return;
  const choices = [...page.querySelectorAll('[data-select]')];
  const panels = [...page.querySelectorAll('.record-spread')];
  const status = page.querySelector('.selection-status');
  const playback = page.querySelector('.playback-status');
  const bgm = page.querySelector('.bgm-toggle');
  let wantMusic = true;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const players = new Map();
  let playing = null;
  let apiPromise;
  function syncDisc() {
    page.classList.toggle('is-rotating', playing === page.dataset.record && !reducedMotion.matches);
    playback.textContent = playing === page.dataset.record ? '播放中' : '尚未播放';
    bgm.textContent = playing === page.dataset.record ? 'Ⅱ 暫停背景音樂' : '▶ 開啟背景音樂';
  }
  function loadAPI() {
    if (window.YT?.Player) return Promise.resolve();
    if (!apiPromise) apiPromise = new Promise((resolve, reject) => {
      const previous = window.onYouTubeIframeAPIReady;
      window.onYouTubeIframeAPIReady = () => { previous?.(); resolve(); };
      const script = document.createElement('script');
      script.src = 'https://www.youtube.com/iframe_api';
      script.onerror = () => { apiPromise = undefined; reject(new Error('YouTube 連線失敗')); };
      document.head.append(script);
    });
    return apiPromise;
  }
  page.querySelectorAll('.youtube-load').forEach(button => {
    button.addEventListener('click', async () => {
      const panel = button.closest('.record-spread');
      const message = panel.querySelector('.player-message');
      button.disabled = true;
      message.textContent = '正在連接 YouTube…';
      try {
        await loadAPI();
        const player = new YT.Player(panel.querySelector('.youtube-mount'), {
          width: '100%', height: '100%', videoId: button.dataset.video,
          playerVars: { autoplay: 1, playsinline: 1, loop: 1, playlist: button.dataset.video, origin: location.origin },
          events: {
            onReady: event => {
              button.hidden = true;
              event.target.setVolume(35);
              message.textContent = '正在啟動背景音樂…';
              if (wantMusic && page.dataset.record === panel.id) event.target.playVideo();
              else event.target.pauseVideo();
            },
            onAutoplayBlocked: () => {
              message.textContent = '點「開啟背景音樂」即可開始聆聽。';
              playback.textContent = '點一下開啟聲音';
            },
            onStateChange: event => {
              if (event.data === YT.PlayerState.PLAYING) {
                if (page.dataset.record !== panel.id) { event.target.pauseVideo(); return; }
                players.forEach((other, id) => { if (id !== panel.id) other.pauseVideo?.(); });
                playing = panel.id; message.textContent = '播放中';
              } else if (playing === panel.id) {
                playing = null;
                message.textContent = event.data === YT.PlayerState.ENDED ? '播放完畢' : '已暫停或正在載入';
              }
              syncDisc();
            },
            onError: () => {
              if (playing === panel.id) playing = null;
              message.textContent = '這支影片目前無法在網站播放，請使用下方 YouTube 連結。';
              syncDisc();
            }
          }
        });
        players.set(panel.id, player);
      } catch {
        message.textContent = '無法連接 YouTube，請重試或使用下方連結。'; button.disabled = false;
      }
    });
  });
  function selectRecord(id, announce = true) {
    if (!panels.some(panel => panel.id === id)) return;
    if (id !== page.dataset.record) { players.forEach(player => player.pauseVideo?.()); playing = null; }
    page.dataset.record = id;
    choices.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.select === id)));
    panels.forEach(panel => { panel.hidden = panel.id !== id; });
    if (announce) status.textContent = id === 'pieces' ? '已選擇 Pieces，星街すいせい。' : '已選擇 blan_，Arika。';
    syncDisc();
    if (wantMusic) {
      const player = players.get(id);
      if (player?.playVideo) player.playVideo();
      else {
        const load = page.querySelector('#' + id + ' .youtube-load');
        if (!load.disabled) load.click();
      }
    }
  }
  bgm.addEventListener('click', () => {
    const player = players.get(page.dataset.record);
    if (playing === page.dataset.record) { wantMusic = false; player?.pauseVideo(); }
    else {
      wantMusic = true;
      if (player?.playVideo) { player.unMute(); player.playVideo(); }
      else {
        const button = page.querySelector('#' + page.dataset.record + ' .youtube-load');
        if (!button.disabled) button.click();
      }
    }
  });
  choices.forEach((button, index) => {
    button.addEventListener('click', () => selectRecord(button.dataset.select));
    button.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % choices.length;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + choices.length) % choices.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = choices.length - 1;
      if (next === undefined) return;
      event.preventDefault(); choices[next].focus(); selectRecord(choices[next].dataset.select);
    });
  });
  reducedMotion.addEventListener('change', syncDisc);
  window.addEventListener('hashchange', () => selectRecord(location.hash.slice(1)));
  selectRecord(location.hash === '#blan' ? 'blan' : 'pieces', false);
})();
