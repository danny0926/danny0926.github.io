(() => {
  const labels = {sake:['香氣','甜感','酸感','旨味','酒體','餘韻'],beer:['麥芽','啤酒花','苦味','酒體','氣泡'],whisky:['果香','麥芽','木質','煙燻','香料'],baijiu:['香氣','甜感','酒體','酒精刺激','餘韻'],awamori:['香氣','甜感','酒體','酒精刺激','餘韻']};
  window.drinkAxes = labels;
  function node(tag, text, cls) {const e=document.createElement(tag);if(text)e.textContent=text;if(cls)e.className=cls;return e;}
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
      section.querySelector('.drink-heading span').textContent=category.toUpperCase()+' / '+String(group.length).padStart(2,'0');
      const link=document.querySelector('.drink-categories a[href="#'+category+'"]');link.textContent=link.textContent.split(' · ')[0]+' · '+group.length;
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
    document.querySelector('.collection-count').firstChild.textContent=items.length;
  }).catch(()=>{/* Preserve the existing static collection on network failure. */});
})();
