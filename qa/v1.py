from h import *
import sys
U=sys.argv[1];ths=sys.argv[2].split(',')
async def one(p,th):
    b,ctx,pg,errs=await mk(p,ls={'ttu_profile_theme':th,'ttu_profile_v1':prof(False),'ttu_intro':'1'})
    SS=lambda n:pg.screenshot(path=f'shots_v/{th}_{n}.png')
    await pg.goto(U+'?reset=1');await pg.wait_for_timeout(1200);await pg.goto(U);await pg.wait_for_timeout(2500)
    await SS('1begin')
    await pg.tap('#agree');await pg.tap('#sxGo');await pg.wait_for_timeout(1200);await SS('2wizard')
    await pg.tap('#sxStep [data-h=public]');await pg.wait_for_timeout(300);await pg.tap('#stGo');await pg.wait_for_timeout(1800);await SS('3draw')
    dm=await (await pg.query_selector('#drawmap')).bounding_box()
    for fx,fy in [(.3,.3),(.7,.3),(.7,.7),(.3,.7)]:
        await pg.touchscreen.tap(dm['x']+dm['width']*fx,dm['y']+dm['height']*fy);await pg.wait_for_timeout(300)
    await SS('4drawn')
    await pg.tap('#drawGo');await pg.wait_for_timeout(1200);await SS('5perm')
    await pg.evaluate("document.querySelector('#askbtns button').click()");await pg.wait_for_timeout(6000);await SS('6hunt')
    pin=await pg.evaluate("S.pin");await ctx.set_geolocation({'latitude':pin['lat'],'longitude':pin['lng'],'accuracy':5});await pg.wait_for_timeout(3000)
    await pg.evaluate("(document.getElementById('hxClaim')||document.getElementById('claim')).click()");await pg.wait_for_timeout(2500);await SS('7win')
    print(th,'OVLwin',await pg.evaluate(OVL))
    print(th,'prize',await pg.evaluate("document.getElementById('wloot')?.innerText.replace(/\\n+/g,' | ')"))
    await pg.wait_for_timeout(9000)
    fb=await pg.query_selector('#fbCard')
    if fb: await pg.evaluate("document.getElementById('fbCard').scrollIntoView()");await pg.wait_for_timeout(800);await SS('8feedback')
    print(th,'fb',fb is not None,errs);await b.close()
async def main():
  async with async_playwright() as p:
    await asyncio.gather(*[one(p,t) for t in ths])
asyncio.run(main())
