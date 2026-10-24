from h import *
import time
async def main():
  async with async_playwright() as p:
    b,ctx,pg,errs=await mk(p,ls={'ttu_intro':'1'})
    await pg.goto(URL+'?reset=1');await pg.wait_for_timeout(1500)
    await pg.tap('#agree');await pg.tap('#sxGo');await pg.wait_for_timeout(1000)
    await pg.tap('#sxStep [data-d=medium]');await pg.tap('#stGo')
    t0=time.time()
    for i in range(30):
      v=await pg.evaluate("[typeof cmpBear!=='undefined'?cmpBear:'u', document.getElementById('needle')?.style.display, document.getElementById('temp')?.textContent, !!window.__wispC]")
      print(round(time.time()-t0,1),v)
      if v[0] not in (None,'u'): break
      await pg.wait_for_timeout(1000)
    await ctx.set_geolocation({'latitude':44.4362,'longitude':-89.4130,'accuracy':8});
    t0=time.time()
    for i in range(20):
      v=await pg.evaluate("[cmpBear,document.getElementById('needle')?.style.display,document.getElementById('temp')?.textContent,!!window.__wispC]")
      print('after move',round(time.time()-t0,1),v)
      if v[0] is not None: break
      await pg.wait_for_timeout(500)
    await pg.screenshot(path='06_medium_after_geo.png')
    print(errs)
asyncio.run(main())
