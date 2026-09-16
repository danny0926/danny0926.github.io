(() => {
  const tracks = [
    { title: 'Pieces · 星街すいせい', video: 'gidBYApkqhI' },
    { title: 'blan_ · Arika', video: 'pr8jE4Rh81M' }
  ];
  const hero = document.querySelector('.wafer-hero');
  if (!hero) return;
  const box = document.createElement('section');
  box.id = 'home-music';
  box.className = 'home-bgm';
  box.setAttribute('aria-labelledby', 'bgm-title');
  box.innerHTML = `<div class="bgm-deck">
    <div class="bgm-heading"><span class="bgm-kicker">ON THE RECORD / 02</span><a href="jpop.html">音樂收藏 ↗</a></div>
    <h2 id="bgm-title">此刻的背景音。</h2>
    <label class="bgm-track-label" for="bgm-track">正在聽<select id="bgm-track">${tracks.map((t, i) => `<option value="${i}">${t.title}</option>`).join('')}</select></label>
    <div class="bgm-controls"><button type="button" disabled aria-label="播放背景音樂">連線中…</button><label for="bgm-volume">音量 <input id="bgm-volume" type="range" min="0" max="100" value="35"/><output for="bgm-volume">35%</output></label></div>
    <p class="bgm-message" role="status">正在連接 YouTube…</p>
  </div><div class="bgm-screen"><div id="home-youtube"></div></div>`;
  hero.after(box);
  const select = box.querySelector('select');
  const button = box.querySelector('button');
  const volume = box.querySelector('input');
  const output = box.querySelector('output');
  const message = box.querySelector('.bgm-message');
  let player;
  let ready = false;
  let isPlaying = false;
  let waitingForGesture = true;
  let autoplayTimer;
  const blockedMessage = '瀏覽器尚未允許自動播放；點一下頁面或按播放，即可開始。';

  function update(playing) {
    isPlaying = playing;
    box.classList.toggle('is-playing', playing);
    button.textContent = playing ? 'Ⅱ 暫停' : '▶ 播放';
    button.setAttribute('aria-label', playing ? '暫停背景音樂' : '播放背景音樂');
  }
  function play() {
    player.unMute();
    player.playVideo();
  }
  function init() {
    if (player) return;
    player = new YT.Player('home-youtube', {
      width: '100%', height: '100%', videoId: tracks[0].video,
      playerVars: { autoplay: 1, playsinline: 1, origin: location.origin },
      events: {
        onReady: event => {
          ready = true;
          button.disabled = false;
          update(false);
          event.target.getIframe().title = '首頁音樂 · YouTube 播放器';
          event.target.setVolume(Number(volume.value));
          message.textContent = '正在嘗試自動播放…';
          event.target.playVideo();
          autoplayTimer = setTimeout(() => {
            if (waitingForGesture && !isPlaying) message.textContent = blockedMessage;
          }, 4000);
        },
        onStateChange: event => {
          update(event.data === YT.PlayerState.PLAYING);
          if (event.data === YT.PlayerState.PLAYING) {
            waitingForGesture = false;
            clearTimeout(autoplayTimer);
            message.textContent = '播放中 · ' + tracks[Number(select.value)].title;
          } else if (event.data === YT.PlayerState.PAUSED) {
            waitingForGesture = false;
            message.textContent = '已暫停 · 隨時接著聽。';
          } else if (event.data === YT.PlayerState.BUFFERING) {
            message.textContent = '正在載入歌曲…';
          } else if (event.data === YT.PlayerState.ENDED) {
            event.target.playVideo();
          }
        },
        onAutoplayBlocked: () => {
          update(false);
          waitingForGesture = true;
          message.textContent = blockedMessage;
        },
        onError: () => {
          clearTimeout(autoplayTimer);
          waitingForGesture = false;
          update(false);
          message.textContent = '這首歌暫時無法播放，請切換另一首試試。';
        }
      }
    });
  }
  button.addEventListener('click', () => {
    if (!ready) return;
    waitingForGesture = false;
    clearTimeout(autoplayTimer);
    if (isPlaying) player.pauseVideo();
    else play();
  });
  select.addEventListener('change', () => {
    if (!ready) return;
    waitingForGesture = false;
    clearTimeout(autoplayTimer);
    message.textContent = '正在切換歌曲…';
    player.unMute();
    player.loadVideoById(tracks[Number(select.value)].video);
  });
  volume.addEventListener('input', () => {
    output.value = volume.value + '%';
    if (ready) player.setVolume(Number(volume.value));
  });
  // Retry blocked autoplay on a real user gesture; an explicit pause stays paused.
  function firstGesture(event) {
    if (!ready || !waitingForGesture || box.contains(event.target)) return;
    if (event.type === 'keydown' && !['Enter', ' '].includes(event.key)) return;
    play();
  }
  document.addEventListener('click', firstGesture);
  document.addEventListener('keydown', firstGesture);
  if (window.YT?.Player) init();
  else {
    const previousReady = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => { previousReady?.(); init(); };
    const script = document.createElement('script');
    script.src = 'https://www.youtube.com/iframe_api';
    script.onerror = () => { message.textContent = '無法連接 YouTube，請重新整理再試。'; };
    document.head.append(script);
  }
})();
