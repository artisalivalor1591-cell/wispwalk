import asyncio,json,sys
from playwright.async_api import async_playwright
URL='https://artisalivalor1591-cell.github.io/wispwalk/'
GEO={'latitude':44.43601,'longitude':-89.41313,'accuracy':10}
async def mk(p,geo=True,ls=None):
    b=await p.chromium.launch()
    d=dict(p.devices['Pixel 7']);ctx=await b.new_context(**d,geolocation=GEO,permissions=['geolocation'] if geo else [])
    if ls: await ctx.add_init_script("if(!sessionStorage.__i){sessionStorage.__i=1;"+''.join(f"localStorage.setItem({json.dumps(k)},{json.dumps(v)});" for k,v in ls.items())+"}")
    pg=await ctx.new_page();errs=[]
    pg.on('console',lambda m: m.type in('error','warning') and errs.append(m.type+': '+m.text))
    pg.on('pageerror',lambda e: errs.append('PAGEERROR: '+str(e)))
    return b,ctx,pg,errs
async def vis(pg):
    return await pg.evaluate("""()=>[...document.querySelectorAll('button,a,h1,h2,h3,p,small,b,label,span')].filter(e=>{const r=e.getBoundingClientRect();const s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!='hidden'&&s.opacity!='0'&&e.children.length==0&&e.innerText.trim()}).map(e=>e.tagName+(e.id?'#'+e.id:'')+': '+e.innerText.trim().slice(0,120))""")
OVL="""()=>{const L=[...document.querySelectorAll('body *')].filter(e=>{if(![...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim()))return false;const r=e.getBoundingClientRect();const s=getComputedStyle(e);return r.width>0&&r.height>0&&r.bottom>0&&r.top<innerHeight&&s.visibility!='hidden'&&+s.opacity>0.05&&e.closest('[aria-hidden=true]')==null});
const out=[];const vis=e=>{let x=e;while(x&&x!==document.body){const s=getComputedStyle(x);if(+s.opacity<0.05||s.visibility=='hidden'||s.display=='none')return false;x=x.parentElement}return true};
const V=L.filter(vis);
for(const e of V){const r=e.getBoundingClientRect();if(r.right>innerWidth+1||r.left<-1)out.push('OFFSCREEN-X '+e.tagName+' "'+e.innerText.slice(0,40)+'" '+Math.round(r.left)+'..'+Math.round(r.right));if(e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflow!='visible')out.push('CLIP '+e.innerText.slice(0,40))}
for(let i=0;i<V.length;i++)for(let j=i+1;j<V.length;j++){const a=V[i],b=V[j];if(a.contains(b)||b.contains(a))continue;const r=a.getBoundingClientRect(),q=b.getBoundingClientRect();const ix=Math.min(r.right,q.right)-Math.max(r.left,q.left),iy=Math.min(r.bottom,q.bottom)-Math.max(r.top,q.top);if(ix>4&&iy>4)out.push('OVERLAP "'+a.innerText.slice(0,30)+'" x "'+b.innerText.slice(0,30)+'" '+Math.round(ix)+'x'+Math.round(iy))}
return [...new Set(out)]}"""
THEMES=['haunted','golden','winter','story','spring','summer']
def prof(fan): return json.dumps({"v":1,"name":"","av":"🧭","move":"walk","rad":0.5,"fit":3,"acc":"","zt":[],"fan":fan,"hist":[],"walkedM":0,"xp":0,"badges":[]})
