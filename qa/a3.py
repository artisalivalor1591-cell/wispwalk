from h import *
async def main():
  async with async_playwright() as p:
    b,ctx,pg,errs=await mk(p)
    await pg.goto(URL+'?reset=1');await pg.wait_for_timeout(1500)
    for i in range(3): await pg.click('#inNext');await pg.wait_for_timeout(700)
    await pg.wait_for_timeout(800)
    el=await pg.evaluate("""()=>{const w=document.evaluate("//*[contains(text(),'…')]",document,null,7,null);let o=[];for(let i=0;i<w.snapshotLength;i++){const e=w.snapshotItem(i);const r=e.getBoundingClientRect();if(r.height>0)o.push([e.tagName,e.id,e.className,e.parentElement.id,e.textContent.slice(0,50),Math.round(r.top),Math.round(r.bottom)])}return o}""")
    print(el)
    await pg.tap('#agree');await pg.wait_for_timeout(500)
    await pg.tap('#sxGo');await pg.wait_for_timeout(2000);await pg.screenshot(path='03_begin_step.png')
    print(await pg.evaluate("document.body.className"))
    html=await pg.evaluate("(()=>{const e=[...document.querySelectorAll('[class*=step],#sxStep,.opt')].map(e=>e.closest('div[id]')?.id);return [...new Set(e)]})()");print(html)
    print(errs)
asyncio.run(main())
