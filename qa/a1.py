from h import *
async def main():
  async with async_playwright() as p:
    b,ctx,pg,errs=await mk(p)
    await pg.goto(URL+'?reset=1');await pg.wait_for_timeout(2500)
    await pg.screenshot(path='01_intro_card1.png')
    print('\n'.join(await vis(pg)))
    print('SKIP present:', await pg.evaluate("document.body.innerText.toLowerCase().includes('skip')"))
    for i in range(3):
      await pg.click('#inNext');await pg.wait_for_timeout(900);await pg.screenshot(path=f'01_intro_after{i+1}.png')
    print('---- start');print('\n'.join(await vis(pg)))
    print(errs)
asyncio.run(main())
