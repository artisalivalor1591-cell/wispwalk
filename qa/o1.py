from h import *
U=sys.argv[1];ths=sys.argv[2].split(',')
CHK="""()=>{const v=e=>e&&e.classList.contains('on')&&+getComputedStyle(e).opacity>0.05;const f=document.getElementById('fct'),t=[document.getElementById('coach'),document.getElementById('idleH')].filter(v);return v(f)&&t.length?'BOTH':''}"""
async def one(p,th,small):
    b,ctx,pg,errs=await mk(p,ls={'ttu_profile_theme':th,'ttu_profile_v1':prof(False),'ttu_intro':'1'})
    if small: await pg.set_viewport_size({'width':360,'height':640})
    tag=f"{th}_{'s' if small else 'p'}";SS=lambda n:pg.screenshot(path=f'coach/overlap_{tag}_{n}.png')
    bad=[]
    async def watch(ms):
        for _ in range(ms//400):
            r=await pg.evaluate(CHK)
            if r: bad.append(r)
            await pg.wait_for_timeout(400)
    await pg.goto(U+'?reset=1');await pg.wait_for_timeout(1200);await pg.evaluate("localStorage.removeItem('ttu_profile_coach')");await pg.goto(U);await pg.wait_for_timeout(2000)
    await pg.tap('#agree');await pg.tap('#sxGo');await pg.wait_for_timeout(1200)
    await pg.tap('#sxStep [data-h=public]');await pg.wait_for_timeout(300);await pg.tap('#stGo');await pg.wait_for_timeout(1800)
    dm=await (await pg.query_selector('#drawmap')).bounding_box()
    for fx,fy in [(.3,.3),(.7,.3),(.7,.7),(.3,.7)]:
        await pg.touchscreen.tap(dm['x']+dm['width']*fx,dm['y']+dm['height']*fy);await pg.wait_for_timeout(300)
    await pg.evaluate("document.getElementById('drawGo').click()");await pg.wait_for_timeout(1200)
    await pg.evaluate("document.querySelector('#askbtns button').click()");await watch(6000);await SS('1tip')
    for k in range(4):
        await pg.evaluate("document.getElementById('coach')&&document.getElementById('coach').click()");await watch(1200)
    await watch(4000);await SS('2fact')
    await watch(9000);await SS('3idle_or_fact')
    await watch(12000);await SS('4later')
    print(tag,'BOTH' if bad else 'ok',len(errs),errs[:2]);await b.close()
async def main():
  async with async_playwright() as p:
    await asyncio.gather(*[one(p,t,s) for t in ths for s in (True,False)])
asyncio.run(main())
