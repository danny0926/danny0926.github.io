(() => {
  const tracks = [{id:'gidBYApkqhI',title:'Pieces',artist:'星街すいせい'},{id:'pr8jE4Rh81M',title:'blan_',artist:'Arika'}];
  const channel = new BroadcastChannel('danny-music');
  let index = 0, player, ready = false;
  function report() {
    const playing = ready && player.getPlayerState() === 1;
    channel.postMessage({type:'status',title:tracks[index].title,playing});
    document.querySelector('#status').textContent = playing ? '播放中 · 保留這個視窗即可繼續聽。' : '按播放開始聽音樂。';
  }
  function action(name) {
    if (!ready) return;
    if (name === 'toggle') player.getPlayerState() === 1 ? player.pauseVideo() : player.playVideo();
    else {
      index = (index + (name === 'previous' ? -1 : 1) + tracks.length) % tracks.length;
      document.querySelector('#title').textContent = tracks[index].title;
      document.querySelector('#artist').textContent = tracks[index].artist;
      player.loadVideoById(tracks[index].id);
    }
  }
  channel.onmessage = ({data}) => {if (data.action) action(data.action);};
  document.querySelector('#controls').addEventListener('click', e => {const b=e.target.closest('button');if(b)action(b.dataset.action);});
  window.onYouTubeIframeAPIReady = () => {
    player = new YT.Player('video', {videoId:tracks[index].id,playerVars:{autoplay:1,playsinline:1,origin:location.origin},events:{
      onReady:()=>{ready=true;player.setVolume(35);player.playVideo();report();},
      onStateChange:e=>{if(e.data===0)action('next');report();},
      onError:()=>{document.querySelector('#status').textContent='這首歌曲目前無法播放，請切換下一首。';},
      onAutoplayBlocked:()=>{document.querySelector('#status').textContent='請按播放，開始聽音樂。';}
    }});
  };
  window.addEventListener('beforeunload',()=>channel.postMessage({type:'status',title:tracks[index].title,playing:false}));
})();
