from h import *
async def flow(p,tag,h,geo=True):
    b,ctx,pg,errs=await mk(p,geo=geo,ls={'ttu_intro':'1'})
    await pg.goto(URL+'?reset=1');await pg.wait_for_timeout(1500)
    await pg.tap('#agree');await pg.tap('#sxGo');await pg.wait_for_timeout(1000)
    if h: await pg.tap(f'#sxStep [data-h={h}]');await pg.wait_for_timeout(400)
    await pg.screenshot(path=f'09_{tag}_a.png')
    await pg.tap('#stGo');await pg.wait_for_timeout(8000);await pg.screenshot(path=f'09_{tag}_b.png')
    v=await vis(pg);print(tag,'\n  '+'\n  '.join(v[-8:]));print(' errs',errs)
    return b,pg
async def main():
  async with async_playwright() as p:
    await flow(p,'denied',None,geo=False)
    await flow(p,'wander','wander')
    b,pg=await flow(p,'else','else')
    b,ctx,pg,errs=await mk(p)
    await pg.goto('https://artisalivalor1591-cell.github.io/trail-trade-up/');await pg.wait_for_timeout(4000);print('REDIRECT ->',pg.url)
asyncio.run(main())
