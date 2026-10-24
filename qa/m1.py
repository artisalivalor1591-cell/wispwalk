from h import *
import sys
async def run(p,th,fan):
    tag=f'{th}_{"fan" if fan else "norm"}'
    b,ctx,pg,errs=await mk(p,ls={'ttu_profile_theme':th,'ttu_profile_v1':prof(fan)})
    R=[]
    await pg.goto(URL+'?reset=1');await pg.wait_for_timeout(1600)
    for i in range(3):
      await pg.screenshot(path=f'shots_m/{tag}_intro{i+1}.png');R+=[f'intro{i+1}: '+x for x in await pg.evaluate(OVL)]
      R.append('introtext: '+(await pg.evaluate("document.querySelector('#sxIntro')?.innerText.replace(/\\n+/g,' | ')")))
      await pg.click('#inNext');await pg.wait_for_timeout(700)
    await pg.wait_for_timeout(700)
    for k in range(4):
      R.append('line: '+await pg.evaluate("document.querySelector('#sxGo').parentElement.innerText.replace(/\\n+/g,' | ').slice(0,200)"))
      R+=[f'start{k}: '+x for x in await pg.evaluate(OVL)]
      await pg.screenshot(path=f'shots_m/{tag}_start{k}.png');await pg.wait_for_timeout(3500)
    await pg.tap('#agree');await pg.tap('#sxGo');await pg.wait_for_timeout(1500)
    R+=['begin: '+x for x in await pg.evaluate(OVL)];await pg.screenshot(path=f'shots_m/{tag}_begin.png')
    R.append('begintext: '+await pg.evaluate("document.querySelector('#sxStep').innerText.replace(/\\n+/g,' | ')"))
    for mv in ['walk','drive','combo']:
      await pg.tap(f'#sxStep [data-mv={mv}]');await pg.wait_for_timeout(500)
      R.append(f'mv {mv}: '+await pg.evaluate("document.querySelector('#sxStep').innerText.replace(/\\n+/g,' | ')"))
      R+=[f'mv {mv}: '+x for x in await pg.evaluate(OVL)]
      await pg.screenshot(path=f'shots_m/{tag}_mv_{mv}.png')
      for mi in await pg.evaluate("[...document.querySelectorAll('#sxStep [data-mi]')].map(e=>e.dataset.mi)"):
        await pg.tap(f'#sxStep [data-mi="{mi}"]');await pg.wait_for_timeout(250)
        R+=[f'mv {mv} mi {mi}: '+x for x in await pg.evaluate(OVL)]
      if await pg.query_selector('#sxStep [data-cu]'):
        await pg.tap('#sxStep [data-cu]');await pg.wait_for_timeout(500);await pg.screenshot(path=f'shots_m/{tag}_mv_{mv}_custom.png')
        R.append(f'custom {mv}: '+await pg.evaluate("document.querySelector('#sxStep').innerText.replace(/\\n+/g,' | ')"))
        R+=[f'custom {mv}: '+x for x in await pg.evaluate(OVL)]
    R+=errs
    await b.close();open(f'shots_m/{tag}.txt','w').write('\n'.join(R));print(tag,'done',len(errs))
async def main():
  async with async_playwright() as p:
    r=await asyncio.gather(*[run(p,t,f) for t in THEMES for f in (False,True)],return_exceptions=True);print([str(x)[:300] for x in r])
asyncio.run(main())
