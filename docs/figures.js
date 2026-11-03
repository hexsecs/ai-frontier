/* Declarative, sandbox-free interactive figures. No user-provided JavaScript executes. */
(()=>{'use strict';
const libs={
  vega:['https://cdn.jsdelivr.net/npm/vega@5.33.0/build/vega.min.js','https://cdn.jsdelivr.net/npm/vega-lite@5.23.0/build/vega-lite.min.js','https://cdn.jsdelivr.net/npm/vega-embed@6.29.0/build/vega-embed.min.js'],
  mermaid:['https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js'],
  cyto:['https://cdn.jsdelivr.net/npm/cytoscape@3.30.4/dist/cytoscape.min.js']
};
const loaded=new Map();
function load(src){if(!loaded.has(src))loaded.set(src,new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=src;s.async=true;s.onload=resolve;s.onerror=()=>reject(Error('Could not load visualization library'));document.head.appendChild(s)}));return loaded.get(src)}
async function loadAll(urls){for(const url of urls)await load(url)}
function decode(encoded){const bytes=Uint8Array.from(atob(encoded),c=>c.charCodeAt(0));return new TextDecoder().decode(bytes)}
function element(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e}
function chartToVega(c){
  const data=[];for(let i=0;i<c.labels.length;i++)for(const set of c.datasets){const value=set.data?.[i];if(typeof value==='number'&&Number.isFinite(value))data.push({category:String(c.labels[i]),series:String(set.label||'Series'),value})}
  const type=c.type==='doughnut'?'pie':c.type;
  const mark=type==='bar'?'bar':type==='line'?'line':type==='scatter'?'point':type==='pie'?'arc':'line';
  const spec={width:'container',height:Math.min(420,Math.max(250,Number(c.height)||320)),data:{values:data},mark:{type:mark,tooltip:true},encoding:{}};
  if(type==='pie'){spec.encoding={theta:{field:'value',type:'quantitative'},color:{field:'category',type:'nominal'},tooltip:[{field:'category'},{field:'value'}]};if(c.type==='doughnut')spec.mark.innerRadius=70}
  else {spec.encoding={x:{field:'category',type:'nominal',title:c.xAxis?.title||null},y:{field:'value',type:'quantitative',title:c.yAxis?.title||null,scale:{zero:true,...(Number.isFinite(c.yAxis?.min)?{domainMin:c.yAxis.min}:{}),...(Number.isFinite(c.yAxis?.max)?{domainMax:c.yAxis.max}:{})}},color:{field:'series',type:'nominal'},tooltip:[{field:'category'},{field:'series'},{field:'value'}]};if(type==='line')spec.encoding.x.type='ordinal'}
  return spec;
}
function safeVega(spec){
  const result=structuredClone(spec);
  const visit=(v,depth=0)=>{if(depth>30)throw Error('Visualization is too deeply nested');if(!v||typeof v!=='object')return;for(const [k,val] of Object.entries(v)){if(['url','href','expr','calculate','signal','on','params','usermeta'].includes(k))throw Error('Unsupported external or executable Vega-Lite property: '+k);visit(val,depth+1)}};
  visit(result);result.width='container';result.autosize={type:'fit',contains:'padding'};return result;
}
async function render(node){
  if(node.dataset.rendered)return;node.dataset.rendered='true';
  const kind=node.dataset.visual;
  const raw=decode(node.dataset.spec||'');
  const spec=kind==='mermaid'?raw:JSON.parse(raw);
  const frame=element('div','figure-canvas');node.replaceChildren(frame);
  const title=kind==='mermaid'?'Workflow diagram':String(spec.title||'Interactive '+kind+' figure');
  node.setAttribute('role','group');node.setAttribute('aria-label',title);
  if(kind==='chart'||kind==='vega-lite'){
    await loadAll(libs.vega);
    const vega=kind==='chart'?chartToVega(spec):safeVega(spec);
    await window.vegaEmbed(frame,vega,{actions:{export:true,source:false,compiled:false,editor:false},renderer:'svg',tooltip:true,theme:'dark'});
  }else if(kind==='mermaid'){
    const mermaid=(await import('https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs')).default;
    if(!window.__frontierMermaidReady){mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:'dark',flowchart:{htmlLabels:false},maxTextSize:100000});window.__frontierMermaidReady=true}
    const id='frontier-diagram-'+Math.random().toString(36).slice(2);
    const result=await mermaid.render(id,spec);frame.innerHTML=result.svg;
    const svg=frame.querySelector('svg');if(svg){svg.removeAttribute('height');svg.style.maxWidth='100%';svg.style.height='auto'}
  }else if(kind==='graph'){
    await loadAll(libs.cyto);
    const nodes=spec.nodes.map(n=>({data:{id:String(n.id),label:String(n.label||n.id),url:typeof n.url==='string'?n.url:''}}));
    const ids=new Set(nodes.map(n=>n.data.id));
    const edges=spec.edges.filter(e=>ids.has(String(e.source))&&ids.has(String(e.target))).map((e,i)=>({data:{id:'edge-'+i,source:String(e.source),target:String(e.target),label:String(e.label||'')}}));
    frame.classList.add('network-canvas');
    const cy=window.cytoscape({container:frame,elements:[...nodes,...edges],layout:{name:'cose',animate:false},style:[{selector:'node',style:{'background-color':'#9475f4',label:'data(label)',color:'#e8e8ff','font-size':12,'text-wrap':'wrap','text-max-width':110,'text-valign':'bottom','text-margin-y':9}},{selector:'edge',style:{width:1.5,'line-color':'#4b6088','target-arrow-color':'#4b6088','target-arrow-shape':'triangle','curve-style':'bezier'}}],wheelSensitivity:0.2});
    cy.on('tap','node',e=>{const url=e.target.data('url');if(url&&/^(https:\/\/|#\/)/.test(url))window.open(url,'_blank','noopener')});
    const fit=element('button','figure-fit','Fit graph');fit.type='button';fit.addEventListener('click',()=>cy.fit(undefined,30));node.append(fit);
  }else throw Error('Unsupported figure type');
  const caption=kind==='mermaid'?'Interactive workflow diagram':spec.caption;
  if(caption)node.append(element('div','figure-caption',String(caption)));
}
async function renderAll(root=document){for(const node of root.querySelectorAll('.interactive-figure')){try{await render(node)}catch(e){node.replaceChildren(element('p','figure-error','Figure unavailable: '+e.message));node.dataset.rendered='error';console.error('Figure rendering failed',e)}}}
window.FrontierFigures={renderAll};
})();
