(() => {
  const counter = document.querySelector('#traffic-counter');
  if (!counter) return;
  if (location.hostname !== 'danny0926.github.io') {
    counter.querySelector('.traffic-value').textContent = '本機預覽不計入';
    return;
  }
  const image = new Image();
  image.alt = '首頁今日與累計瀏覽次數';
  image.height = 20;
  image.referrerPolicy = 'no-referrer';
  image.onload = () => counter.querySelector('.traffic-value').replaceChildren(image);
  image.onerror = () => {counter.querySelector('.traffic-value').textContent = '暫時無法載入';};
  image.src = 'https://hits.sh/danny0926.github.io.svg?view=today-total&style=flat-square&label=VIEWS&color=397967&labelColor=1b2026';
})();
