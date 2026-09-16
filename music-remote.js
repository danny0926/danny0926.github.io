(() => {
  const channel = new BroadcastChannel('danny-music');
  const bar = document.createElement('div');
  bar.className = 'music-remote';
  bar.innerHTML = '<span class="music-track">MUSIC / Pieces</span><button data-action="previous" aria-label="上一首">‹</button><button data-action="toggle" aria-label="開啟音樂播放視窗">▶</button><button data-action="next" aria-label="下一首">›</button><span class="music-state" aria-live="polite">開啟音樂</span>';
  document.querySelector('.wafer-topline').append(bar);
  let musicWindow;
  bar.addEventListener('click', event => {
    const button = event.target.closest('button');
    if (!button) return;
    if (!musicWindow || musicWindow.closed) {
      musicWindow = window.open('music-player.html', 'dannyMusic', 'popup,width=560,height=460');
      bar.querySelector('.music-state').textContent = musicWindow ? '播放器已開啟' : '請允許播放視窗';
    } else channel.postMessage({action: button.dataset.action});
  });
  channel.onmessage = ({data}) => {
    if (data.type !== 'status') return;
    bar.querySelector('.music-track').textContent = 'MUSIC / ' + data.title;
    bar.querySelector('[data-action="toggle"]').textContent = data.playing ? 'Ⅱ' : '▶';
    bar.querySelector('.music-state').textContent = data.playing ? '播放中' : '已暫停';
  };
})();
