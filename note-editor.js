(() => {
  const allowed=new Set(['P','DIV','BR','H2','H3','STRONG','B','EM','I','U','S','UL','OL','LI','BLOCKQUOTE','A','IMG']);
  const safeURL=value=>{try{return ['http:','https:'].includes(new URL(value,location.href).protocol);}catch{return false;}};
  function clean(html,previews=false){
    const source=document.createElement('template');source.innerHTML=html;
    const result=document.createElement('div');
    function copy(node,parent){
      if(node.nodeType===3){parent.append(document.createTextNode(node.textContent));return;}
      if(node.nodeType!==1||['SCRIPT','STYLE','IFRAME','OBJECT','SVG','MATH'].includes(node.tagName))return;
      if(!allowed.has(node.tagName)){node.childNodes.forEach(child=>copy(child,parent));return;}
      const out=document.createElement(node.tagName.toLowerCase());
      if(node.tagName==='IMG'){
        const src=node.getAttribute('src')||'';
        if(!src||!(safeURL(src)||previews&&/^data:image\/(png|jpeg|webp);base64,/.test(src)))return;
        out.src=src;out.alt=node.getAttribute('alt')||'筆記照片';
        if(['small','medium','full'].includes(node.dataset.size))out.dataset.size=node.dataset.size;
        if(previews&&node.dataset.upload)out.dataset.upload=node.dataset.upload;
      }
      if(node.tagName==='A'&&safeURL(node.getAttribute('href'))){out.href=node.getAttribute('href');out.target='_blank';out.rel='noopener noreferrer';}
      node.childNodes.forEach(child=>copy(child,out));parent.append(out);
    }
    source.content.childNodes.forEach(node=>copy(node,result));return result.innerHTML;
  }
  function render(parent,item){
    const content=document.createElement('div');content.className='note-content';
    if(item.notesHtml)content.innerHTML=clean(item.notesHtml);
    else {const p=document.createElement('p');p.textContent=item.notes||'這瓶酒的故事，還在等我寫下。';content.append(p);}
    for(const path of item.noteImages||[]){if(safeURL(path)){const img=document.createElement('img');img.src=path;img.alt='筆記照片';content.append(img);}}
    parent.append(content);
  }
  function editor(textarea,item,message){
    const wrapper=document.createElement('section');wrapper.className='rich-note';
    const title=document.createElement('h3');title.textContent='我的品飲筆記';
    const toolbar=document.createElement('div');toolbar.className='note-toolbar';toolbar.setAttribute('role','toolbar');toolbar.setAttribute('aria-label','筆記排版');
    const area=document.createElement('div');area.className='note-content note-editable';area.contentEditable='true';area.setAttribute('role','textbox');area.setAttribute('aria-multiline','true');area.setAttribute('aria-label','我的品飲筆記');
    const hint=document.createElement('p');hint.className='detail-muted';hint.textContent='像寫筆記一樣自由排版；在游標位置貼上或插入圖片。點選照片可調整大小或移除。';
    const initial=document.createElement('div');render(initial,item);area.innerHTML=initial.firstChild.innerHTML;
    if(!item.notes&&!item.notesHtml)area.innerHTML='<p><br></p>';
    let selection=null,selectedImage=null,pending=0;
    const uploads=new Map();
    function remember(){const sel=window.getSelection();if(sel.rangeCount&&area.contains(sel.anchorNode))selection=sel.getRangeAt(0).cloneRange();}
    area.addEventListener('keyup',remember);area.addEventListener('mouseup',remember);area.addEventListener('input',remember);
    function restore(){area.focus();const sel=window.getSelection();if(selection&&area.contains(selection.startContainer)){sel.removeAllRanges();sel.addRange(selection);}else{const range=document.createRange();range.selectNodeContents(area);range.collapse(false);sel.removeAllRanges();sel.addRange(range);}}
    function button(label,action){const b=document.createElement('button');b.type='button';b.textContent=label;b.onmousedown=e=>{e.preventDefault();remember();};b.onclick=action;toolbar.append(b);return b;}
    for(const [label,cmd,value] of [['內文','formatBlock','p'],['標題','formatBlock','h2'],['粗體','bold'],['斜體','italic'],['項目清單','insertUnorderedList'],['編號清單','insertOrderedList'],['引用','formatBlock','blockquote'],['復原','undo'],['重做','redo']])button(label,()=>{restore();document.execCommand(cmd,false,value);remember();});
    button('連結',()=>{const href=prompt('輸入連結網址（https://…）');if(!href)return;if(!safeURL(href)){message('請輸入有效的 http 或 https 網址。');return;}restore();document.execCommand('createLink',false,href);remember();});
    const upload=document.createElement('input');upload.type='file';upload.accept='image/jpeg,image/png,image/webp';upload.multiple=true;upload.hidden=true;
    button('插入圖片',()=>upload.click());
    const imageTools=document.createElement('div');imageTools.className='note-image-tools';imageTools.hidden=true;
    for(const [label,size] of [['小','small'],['中','medium'],['滿寬','full'],['移除圖片',null]]){const b=document.createElement('button');b.type='button';b.textContent=label;b.onclick=()=>{if(!selectedImage)return;if(size)selectedImage.dataset.size=size;else{selectedImage.remove();selectedImage=null;imageTools.hidden=true;}};imageTools.append(b);}
    area.onclick=e=>{selectedImage=e.target.closest('img');imageTools.hidden=!selectedImage;};
    async function add(files){
      restore();const insertion=window.getSelection().getRangeAt(0).cloneRange();pending++;area.contentEditable='false';
      try{for(const file of files){const ext={'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}[file.type];if(!ext||file.size>5*1024*1024){message('圖片需為 5 MB 以下的 JPEG、PNG 或 WebP。');continue;}
        const dataURL=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=()=>reject(Error('圖片讀取失敗，請再試一次。'));reader.readAsDataURL(file);});
        const path='assets/drinks/uploads/'+crypto.randomUUID()+'.'+ext;uploads.set(path,{path,base64:dataURL.split(',')[1]});
        const img=document.createElement('img');img.src=dataURL;img.alt=file.name||'筆記照片';img.dataset.upload=path;img.dataset.size='full';
        insertion.deleteContents();insertion.insertNode(img);insertion.setStartAfter(img);insertion.collapse(true);const p=document.createElement('p');p.append(document.createElement('br'));insertion.insertNode(p);insertion.setStart(p,0);insertion.collapse(true);selection=insertion.cloneRange();
        message('圖片已插入筆記，儲存時一起發布。');
      }}catch(e){message(e.message);}finally{pending--;area.contentEditable='true';restore();}
    }
    upload.onchange=()=>{add([...upload.files]);upload.value='';};
    area.addEventListener('paste',e=>{e.preventDefault();remember();const files=[...(e.clipboardData?.items||[])].filter(x=>x.kind==='file'&&x.type.startsWith('image/')).map(x=>x.getAsFile()).filter(Boolean);if(files.length){add(files);return;}restore();const html=e.clipboardData.getData('text/html');if(html)document.execCommand('insertHTML',false,clean(html));else document.execCommand('insertText',false,e.clipboardData.getData('text/plain'));remember();});
    area.addEventListener('dragover',e=>e.preventDefault());
    area.addEventListener('drop',e=>{e.preventDefault();if(pending)return;const caret=document.caretRangeFromPoint?.(e.clientX,e.clientY);if(caret&&area.contains(caret.startContainer))selection=caret;const files=[...(e.dataTransfer?.files||[])];if(files.length)add(files);});
    wrapper.append(title,toolbar,hint,imageTools,area,upload);textarea.parentElement.replaceWith(wrapper);
    return {get pending(){return pending;},snapshot(){const copy=area.cloneNode(true),used=[];copy.querySelectorAll('img[data-upload]').forEach(img=>{const file=uploads.get(img.dataset.upload);if(file){img.setAttribute('src',file.path);used.push(file);}img.removeAttribute('data-upload');});return {html:clean(copy.innerHTML),text:area.innerText.trim(),uploads:used};}};
  }
  window.drinkNoteEditor={render,editor};
})();
