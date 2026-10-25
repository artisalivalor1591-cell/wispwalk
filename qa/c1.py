from h import *
U=sys.argv[1]
async def main():
  async with async_playwright() as p:
    b,ctx,pg,errs=await mk(p,ls={'ttu_profile_theme':'golden','ttu_profile_v1':prof(False)})
    SS=lambda n:pg.screenshot(path=f'coach/coach_{n}.png')
    await pg.goto(U+'?reset=1');await pg.wait_for_timeout(1200);await pg.evaluate("localStorage.removeItem('ttu_intro');localStorage.removeItem('ttu_profile_coach')");await pg.goto(U);await pg.wait_for_timeout(2000)
    for k in range(3):
        await SS(f'intro{k+1}');await pg.tap('#inNext');await pg.wait_for_timeout(700)
    await pg.wait_for_timeout(9000);await SS('idle_begin')
    await pg.tap('#agree');await pg.tap('#sxGo');await pg.wait_for_timeout(1200);await SS('wizard')
    await pg.wait_for_timeout(9000);await SS('idle_wizard')
    await pg.tap('#sxStep [data-h=public]');await pg.wait_for_timeout(300);await pg.tap('#stGo');await pg.wait_for_timeout(1800)
    dm=await (await pg.query_selector('#drawmap')).bounding_box()
    for fx,fy in [(.3,.3),(.7,.3),(.7,.7),(.3,.7)]:
        await pg.touchscreen.tap(dm['x']+dm['width']*fx,dm['y']+dm['height']*fy);await pg.wait_for_timeout(300)
    await pg.tap('#drawGo');await pg.wait_for_timeout(1200)
    await pg.evaluate("document.querySelector('#askbtns button').click()");await pg.wait_for_timeout(5000)
    for k in range(4):
        await SS(f'tip{k+1}');await pg.tap('#coach');await pg.wait_for_timeout(1200)
    print('coachdone',await pg.evaluate("localStorage.getItem('ttu_profile_coach')"))
    await pg.wait_for_timeout(9000);await SS('idle_hunt')
    await pg.goto(U+'?reset=1');await pg.wait_for_timeout(1500)
    print('after reset',await pg.evaluate("[localStorage.getItem('ttu_profile_coach'),localStorage.getItem('ttu_intro')]"))
    print(errs);await b.close()
asyncio.run(main())
