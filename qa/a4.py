from h import *
async def main():
  async with async_playwright() as p:
    b,ctx,pg,errs=await mk(p)
    await pg.goto(URL+'?reset=1');await pg.wait_for_timeout(1500)
    for i in range(3): await pg.click('#inNext');await pg.wait_for_timeout(700)
    await pg.tap('#agree');await pg.tap('#sxGo');await pg.wait_for_timeout(1200)
    await pg.tap('#stGo');
    for t in [2,5,10]:
      await pg.wait_for_timeout(t*1000);await pg.screenshot(path=f'04_hunt_{t}s.png')
    print(await pg.evaluate("document.body.className"), await pg.evaluate("document.body.innerText.replace(/\\n+/g,' | ').slice(0,1500)"))
    print(await pg.evaluate("JSON.stringify(Object.keys(localStorage))"))
    # start fresh via top-right button
    print('resetAll visible', await pg.is_visible('#resetAll'))
    await pg.evaluate("resetAll()");await pg.wait_for_timeout(3000)
    await pg.screenshot(path='05_after_start_fresh.png')
    print('intro after fresh:', await pg.query_selector('#sxIntro') is not None, await pg.evaluate("localStorage.getItem('ttu_intro')"))
    await pg.reload();await pg.wait_for_timeout(2500);print('intro after reload:', await pg.query_selector('#sxIntro') is not None)
    print(errs)
asyncio.run(main())
