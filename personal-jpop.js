(() => {
  const page = document.querySelector('.music-page');
  if (!page) return;
  const choices = [...page.querySelectorAll('[data-select]')];
  const panels = [...page.querySelectorAll('.record-spread')];
  const rotation = page.querySelector('.rotation-control');
  const rotationLabel = rotation.querySelector('.rotation-label');
  const status = page.querySelector('.selection-status');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let rotating = !reducedMotion.matches;
  function setRotation() {
    page.classList.toggle('is-rotating', rotating && !reducedMotion.matches);
    rotation.hidden = reducedMotion.matches;
    rotationLabel.textContent = rotating ? '停止轉動' : '開始轉動';
  }
  function selectRecord(id, announce = true) {
    if (!panels.some(panel => panel.id === id)) return;
    page.dataset.record = id;
    choices.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.select === id)));
    panels.forEach(panel => { panel.hidden = panel.id !== id; });
    if (announce) status.textContent = id === 'pieces' ? '已選擇 Pieces，星街すいせい。' : '已選擇 blan_，Arika。';
  }
  choices.forEach((button, index) => {
    button.addEventListener('click', () => selectRecord(button.dataset.select));
    button.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % choices.length;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + choices.length) % choices.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = choices.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      choices[next].focus();
      selectRecord(choices[next].dataset.select);
    });
  });
  rotation.addEventListener('click', () => { rotating = !rotating; setRotation(); });
  reducedMotion.addEventListener('change', () => {
    if (reducedMotion.matches) rotating = false;
    setRotation();
  });
  window.addEventListener('hashchange', () => selectRecord(location.hash.slice(1)));
  selectRecord(location.hash === '#blan' ? 'blan' : 'pieces', false);
  setRotation();
})();
