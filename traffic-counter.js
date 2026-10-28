(() => {
  const counter = document.querySelector('#traffic-counter');
  if (!counter) return;

  const value = counter.querySelector('.traffic-value');
  const status = counter.querySelector('.traffic-status');
  const restoreLink = counter.querySelector('.traffic-restore');
  if (location.hostname !== 'danny0926.github.io') {
    value.textContent = '本機預覽不計入';
    return;
  }

  const excludeMode = new URLSearchParams(location.search).get('exclude');
  const explicitlyExcluding = excludeMode === '1';
  const explicitlyRestoring = excludeMode === '0';
  const storageKey = 'danny0926-traffic-counter-excluded';
  let excluded = false;
  let persistenceSucceeded = false;

  if (explicitlyExcluding) {
    excluded = true;
    try {
      localStorage.setItem(storageKey, '1');
      persistenceSucceeded = true;
    } catch {
      // The explicit query still excludes this visit even when storage is blocked.
    }
  } else if (explicitlyRestoring) {
    try {
      localStorage.removeItem(storageKey);
      persistenceSucceeded = true;
    } catch {
      // Count this explicit restore visit, but keep the query so it can be retried.
    }
  } else {
    try {
      excluded = localStorage.getItem(storageKey) === '1';
    } catch {
      // Without a readable preference, keep the default counting behavior.
    }
  }

  if ((explicitlyExcluding || explicitlyRestoring) && persistenceSucceeded) {
    const cleanUrl = new URL(location.href);
    cleanUrl.searchParams.delete('exclude');
    history.replaceState(history.state, '', `${cleanUrl.pathname}${cleanUrl.search}${cleanUrl.hash}`);
  }

  const setStatus = (message) => {
    if (!status) return;
    status.textContent = message;
    status.hidden = !message;
  };

  if (excluded) {
    value.textContent = '';
    setStatus(explicitlyExcluding && !persistenceSucceeded
      ? '此瀏覽器本次不計入（無法儲存設定）'
      : '此瀏覽器不計入');
    if (restoreLink) {
      const restoreUrl = new URL(location.href);
      restoreUrl.searchParams.set('exclude', '0');
      restoreLink.href = `${restoreUrl.pathname}${restoreUrl.search}${restoreUrl.hash}`;
      restoreLink.hidden = false;
    }
    return;
  }

  if (explicitlyRestoring && !persistenceSucceeded) {
    setStatus('本次恢復計數，無法清除儲存設定');
  }

  const image = new Image();
  image.alt = '首頁今日與累計瀏覽次數';
  image.height = 20;
  image.referrerPolicy = 'no-referrer';
  image.onload = () => value.replaceChildren(image);
  image.onerror = () => { value.textContent = '暫時無法載入'; };
  image.src = 'https://hits.sh/danny0926.github.io.svg?view=today-total&style=flat-square&label=VIEWS&color=397967&labelColor=1b2026';
})();
