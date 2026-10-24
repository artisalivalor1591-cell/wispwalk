from h import *
async def main():
  async with async_playwright() as p:
    b,ctx,pg,errs=await mk(p)
    await pg.goto(URL+'?reset=1');await pg.wait_for_timeout(1500)
    for i in range(3): await pg.click('#inNext');await pg.wait_for_timeout(700)
    await pg.wait_for_timeout(800)
    for k in range(6):
      info=await pg.evaluate("""()=>{const s=document.querySelector('#sxSug');const r=s.getBoundingClientRect();const ch=[...s.querySelectorAll('*')].map(e=>{const q=e.getBoundingClientRect();return [e.tagName,e.innerText.slice(0,40),Math.round(q.top),Math.round(q.bottom),Math.round(q.left),Math.round(q.right)]});const g=document.querySelector('#sxGo').getBoundingClientRect();return {sug:[r.top,r.bottom],ch,go:[g.top,g.bottom,getComputedStyle(document.querySelector('#sxGo')).display,getComputedStyle(document.querySelector('#sxGo')).opacity]}}""")
      print(info);await pg.screenshot(path=f'02_start_line_{k}.png');await pg.wait_for_timeout(4000)
    print(await pg.evaluate("document.querySelector('#sxAgree').innerHTML.slice(0,500)"))
    print(errs)
asyncio.run(main())
