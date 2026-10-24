from h import *
async def main():
  async with async_playwright() as p:
    b,ctx,pg,errs=await mk(p,ls={'ttu_intro':'1'})
    await pg.goto(URL+'?reset=1');await pg.wait_for_timeout(1500)
    await pg.tap('#agree');await pg.tap('#sxGo');await pg.wait_for_timeout(1000)
    await pg.tap('#sxStep [data-h=public]');await pg.wait_for_timeout(500);await pg.screenshot(path='07_draw_option.png')
    await pg.tap('#stGo');await pg.wait_for_timeout(2500);await pg.screenshot(path='07_draw_map.png')
    print(await pg.evaluate("document.body.className"))
    print('\n'.join([x for x in await vis(pg)][-40:]))
    print(errs)
asyncio.run(main())
