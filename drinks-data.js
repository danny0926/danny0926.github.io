(() => {
  const labels = {sake:['香氣','甜感','酸感','旨味','酒體','餘韻'],beer:['麥芽','啤酒花','苦味','酒體','氣泡'],whisky:['果香','麥芽','木質','煙燻','香料'],baijiu:['香氣','甜感','酒體','酒精刺激','餘韻'],awamori:['香氣','甜感','酒體','酒精刺激','餘韻']};
  window.drinkAxes = labels;
  function node(tag, text, cls) {const e=document.createElement(tag);if(text)e.textContent=text;if(cls)e.className=cls;return e;}
  window.drinkAxisGroups = [
    ['香氣', ['香氣','果香','花香','米香／穀物香','堅果','草本','發酵／乳香','木質／橡木']],
    ['味覺', ['甜感','酸感','苦味','旨味','鹹感／礦物感','澀感']],
    ['口感', ['酒體','濃淡','順口','圓潤綿密','酒精感','刺激／辛辣','氣泡']],
    ['收尾', ['餘韻','爽脆（キレ）','乾淨','平衡']],
    ['風味特色', ['煙燻／泥煤','香料','焦糖／蜂蜜','香草','麥芽','啤酒花']]
  ];
  window.drinkAxisPool = window.drinkAxisGroups.flatMap(g => g[1]);
  const validRadar = r => Array.isArray(r) && r.length >= 3 && r.every(x => x && typeof x.label === 'string' && x.label.trim() && Number.isFinite(x.value) && x.value >= 0 && x.value <= 5);
  window.drinkRadarOf = item => {
    if (validRadar(item.radar)) return item.radar;
    const axes = labels[item.category];
    if (axes && Array.isArray(item.scores) && item.scores.length === axes.length && item.scores.every(v => Number.isFinite(v) && v >= 0 && v <= 5)) return axes.map((a, i) => ({label: a, value: item.scores[i]}));
    return null;
  };
  window.drinkRadarEditor = item => {
    const root = node('div', '', 'radar-picker'), rows = [], boxes = new Map();
    const current = window.drinkRadarOf(item) || [];
    const addRow = (label, value, checked, group = '自訂') => {
      if (!boxes.has(group)) { const g = node('div', '', 'radar-group'); g.append(node('h4', group)); const grid = node('div', '', 'radar-grid'); g.append(grid); boxes.set(group, grid); root.insertBefore(g, adder); }
      const row = node('label', '', 'radar-row'), box = node('input'), name = node('span', label), num = node('input');
      box.type = 'checkbox'; box.checked = checked; num.type = 'number'; num.min = 0; num.max = 5; num.step = 1; num.value = value; num.disabled = !checked; num.setAttribute('aria-label', label + ' 分數');
      box.onchange = () => { num.disabled = !box.checked; };
      row.append(box, name, num); boxes.get(group).append(row); rows.push({label, box, num});
    };
    const adder = node('div', '', 'radar-add'), input = node('input'), btn = node('button', '新增自訂項目');
    input.placeholder = '自訂項目，例如：蜜香'; input.maxLength = 12; btn.type = 'button';
    const add = () => { const t = input.value.trim(); if (!t || rows.some(r => r.label === t)) return; addRow(t, 0, true); input.value = ''; };
    btn.onclick = add; input.onkeydown = e => { if (e.key === 'Enter') { e.preventDefault(); add(); } };
    adder.append(input, btn); root.append(adder);
    const hint = node('p', '勾選要用的項目並填 0–5 分，至少 3 項才會畫出雷達圖。', 'detail-muted'); root.prepend(hint);
    const pool = window.drinkAxisPool, known = new Map(current.map(x => [x.label, x.value]));
    window.drinkAxisGroups.forEach(([g, list]) => list.forEach(a => addRow(a, known.get(a) ?? 0, known.has(a), g)));
    current.filter(x => !pool.includes(x.label)).forEach(x => addRow(x.label, x.value, true));
    return {el: root, value() {
      const picked = rows.filter(r => r.box.checked).map(r => ({label: r.label, value: Number(r.num.value)}));
      if (picked.length < 3) throw Error('雷達圖至少要選 3 個項目。');
      if (picked.some(x => !Number.isInteger(x.value) || x.value < 0 || x.value > 5)) throw Error('分數請填入 0～5 的整數。');
      return picked;
    }};
  };
  function radar(values, axes) {
    const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 300 280');svg.setAttribute('role','img');svg.setAttribute('aria-label',axes.map((a,i)=>a+' '+values[i]+'/5').join('，'));
    const point=(i,r)=>[150+Math.sin(i*2*Math.PI/axes.length)*r,140-Math.cos(i*2*Math.PI/axes.length)*r];
    for(let level=1;level<=5;level++){const p=document.createElementNS(ns,'polygon');p.setAttribute('points',axes.map((_,i)=>point(i,level*17).join(',')).join(' '));p.setAttribute('fill','none');p.setAttribute('stroke','#52606a');svg.append(p);}
    const p=document.createElementNS(ns,'polygon');p.setAttribute('points',values.map((v,i)=>point(i,v*17).join(',')).join(' '));p.setAttribute('fill','#7fe3c433');p.setAttribute('stroke','#7fe3c4');svg.append(p);
    axes.forEach((a,i)=>{const t=document.createElementNS(ns,'text'),[x,y]=point(i,112);t.setAttribute('x',x);t.setAttribute('y',y+4);t.setAttribute('text-anchor','middle');t.setAttribute('fill','currentColor');t.setAttribute('font-size','12');t.textContent=a+' '+values[i];svg.append(t);});return svg;
  }
  window.renderDrinkRadar = radar;
  if(!document.querySelector('.drink-categories'))return;
  fetch('data/drinks.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error();return r.json();}).then(window.renderDrinks=items=>{
    window.drinksCollection=items;
    Object.keys(labels).forEach(category=>{
      const section=document.getElementById(category),old=section.querySelector('.bottle-grid,.empty-shelf');old?.remove();const group=items.filter(x=>x.category===category);
      section.hidden=!group.length;
      section.querySelector('.drink-heading span').textContent=category.toUpperCase()+' / '+String(group.length).padStart(2,'0');
      const link=document.querySelector('.drink-categories a[href="#'+category+'"]');link.hidden=!group.length;link.replaceChildren();const categoryNames={sake:'清酒',beer:'啤酒',whisky:'威士忌',baijiu:'白酒',awamori:'燒酎・泡盛'};link.append(node('span',category.toUpperCase(),'category-code'),node('strong',categoryNames[category]),node('span',group.length+' 款收藏','category-count'));
      const grid=node('div','', 'bottle-grid');section.append(grid);
      group.forEach(item=>{
        const card=node('article','','bottle');card.dataset.drinkId=item.id;card.tabIndex=0;card.setAttribute('role','button');card.setAttribute('aria-label',item.name);const figure=node('figure','','bottle-photo'),img=node('img');
        const safeURL=v=>{try {const u=new URL(v,location.href);return ['http:','https:'].includes(u.protocol);}catch{return false;}};
        if(safeURL(item.image)){img.src=item.image;img.alt=item.name;img.loading='lazy';figure.append(img);}
        if(safeURL(item.source)){const credit=node('a','圖片來源 ↗','photo-credit');credit.href=item.source;credit.target='_blank';credit.rel='noopener noreferrer';figure.append(credit);}
        const body=node('div','','bottle-body');body.append(node('span',String(items.indexOf(item)+1).padStart(2,'0'),'bottle-number mono'),node('h3',item.name),node('p',item.description),node('span',item.spec,'bottle-spec mono'));
        body.append(node('span','DETAILS / 開啟品飲手記 ↗','bottle-open'));card.append(figure,body);grid.append(card);
      });
      if(!group.length)section.append(node('p','下一瓶的故事，留在這裡。','empty-shelf'));
    });
    const count=document.querySelector('.collection-count');if(count?.firstChild)count.firstChild.textContent=items.length;
  }).catch(()=>{/* Preserve the existing static collection on network failure. */});
})();
