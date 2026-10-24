from h import *
import sys
th=sys.argv[1] if len(sys.argv)>1 else 'haunted';fan=len(sys.argv)>2
async def main():
  async with async_playwright() as p:
    b,ctx,pg,errs=await mk(p,ls={'ttu_profile_theme':th,'ttu_profile_v1':prof(fan),'ttu_intro':'1'})
    tg=f'{th}_{"fan" if fan else "norm"}';SS=lambda n:pg.screenshot(path=f'shots_h/{tg}_{n}.png')
    await pg.goto(URL+'?reset=1&star=1');await pg.wait_for_timeout(1500)
    await pg.goto(URL+'?star=1');await pg.wait_for_timeout(1500)
    await pg.tap('#agree');await pg.tap('#sxGo');await pg.wait_for_timeout(1000)
    await pg.tap('#sxStep [data-d=medium]');await pg.wait_for_timeout(300);await pg.tap('#stGo');await pg.wait_for_timeout(6000)
    await SS('hunt');print('hunting', await pg.evaluate("document.body.className"))
    S=await pg.evaluate("({pin:S.pin,diff:S.diff,zone:S.zone&&S.zone.n,start:S.start})");print(S)
    # wisp tap
    bb=await (await pg.query_selector('#wspC')).bounding_box();await pg.touchscreen.tap(bb['x']+bb['width']/2,bb['y']+bb['height']/2);await pg.wait_for_timeout(400);await SS('wisp_tap')
    r=await pg.evaluate("(()=>{const r=document.querySelector('#wspC').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()")
    await pg.mouse.move(r[0]-60,r[1]+60);await pg.mouse.down()
    for i in range(10): await pg.mouse.move(r[0]-60+i*3,r[1]+60-i*3);await pg.wait_for_timeout(50)
    print('follow translate', await pg.evaluate("document.querySelector('#wspC').style.translate"));await SS('wisp_follow');await pg.mouse.up()
    print('anim', await pg.evaluate("Object.keys(TTU_WPLAY.Q)"))
    await pg.evaluate("TTU_WPLAY.Q.twirl(document.querySelector('#wspC'))");await pg.wait_for_timeout(500);await SS('wisp_spin')
    for k in ['decoy','mirage']:
      await pg.evaluate(f"TTU_TRICK.tick('{k}')");await pg.wait_for_timeout(800);await SS('trick_'+k)
      ex=await pg.query_selector('#wspX');print(k,'X present',ex is not None, await pg.evaluate("TTU_TRICK.state()"))
      if ex: await pg.evaluate("document.querySelector('#wspX').click()");await pg.wait_for_timeout(500)
      print(k,'msg:',await pg.evaluate("document.querySelector('#wspMsg')?.innerText"));await SS('trick_'+k+'_after')
    await pg.wait_for_timeout(1000)
    print('acc text', await pg.evaluate("document.getElementById('acc').textContent"))
    await ctx.set_geolocation({'latitude':44.4362,'longitude':-89.4130,'accuracy':8});await pg.wait_for_timeout(1500)
    await pg.evaluate("TTU_TRICK.tick('detour')");await pg.wait_for_timeout(1000);await SS('detour_offer')
    print('detour', await pg.evaluate("JSON.stringify(TTU_TRICK.state())"), await pg.evaluate("document.querySelector('#wspMsg')?.innerText"))
    print('OVL',await pg.evaluate(OVL))
    links=await pg.evaluate("[...document.querySelectorAll('#wspMsg a')].map(a=>a.textContent)");print('links',links)
    D=await pg.evaluate("JSON.stringify(S.detour||null)");print('S.detour',D)
    if links:
      await pg.evaluate("document.querySelector('#wspMsg a').click()");await pg.wait_for_timeout(800);await SS('detour_follow');print('after follow',await pg.evaluate("document.querySelector('#wspMsg')?.innerText"),await pg.evaluate("JSON.stringify(S.detour)"))
      dp=await pg.evaluate("S.detour&&S.detour.pin")
      if dp:
        await ctx.set_geolocation({'latitude':dp['lat'],'longitude':dp['lng'],'accuracy':5});await pg.wait_for_timeout(4000);await SS('detour_reward')
        print('reward msg',await pg.evaluate("document.querySelector('#wspMsg')?.innerText"),'| toast',await pg.evaluate("document.querySelector('#msT')?.innerText"))
    # star
    print('star api',await pg.evaluate("Object.keys(TTU_STAR)"))
    await pg.evaluate("TTU_STAR.fly()");await pg.wait_for_timeout(700);await SS('star_fly')
    st=await pg.query_selector('#sStar');print('star el',st is not None)
    if st:
      bb=await st.bounding_box();print(bb)
      if bb: await pg.touchscreen.tap(bb['x']+48,bb['y']+48)
      await pg.wait_for_timeout(1500);await SS('star_caught');print('star caught', await pg.evaluate("localStorage.getItem('ttu_star_caught')"), await pg.evaluate("document.body.innerText.match(/.{0,80}(star|Star).{0,80}/g)?.slice(0,5)"))
    pin=await pg.evaluate("S.pin");await ctx.set_geolocation({'latitude':pin['lat'],'longitude':pin['lng'],'accuracy':5});await pg.wait_for_timeout(3000)
    await SS('at_pin');print('claim disabled', await pg.evaluate("[document.getElementById('claim').disabled, document.getElementById('hxClaim')?.disabled]"))
    await pg.evaluate("(document.getElementById('hxClaim')||document.getElementById('claim')).click()");await pg.wait_for_timeout(2500);await SS('win')
    print('WIN TEXT',await pg.evaluate("document.body.className"),await pg.evaluate("[...document.querySelectorAll('#msT,#reveal,#win,#shRow,#fbCard')].map(e=>e.id+': '+e.innerText.replace(/\\n+/g,' | ').slice(0,600))"))
    print('OVLwin',await pg.evaluate(OVL))
    await pg.wait_for_timeout(5000);await SS('win_later');print('toast later',await pg.evaluate("document.querySelector('#msT')?.innerText"))
    async with pg.expect_download(timeout=8000) as dl:
      await pg.evaluate("document.getElementById('shGo')&&document.getElementById('shGo').click()")
    d=await dl.value;await d.save_as(f'shots_h/{tg}_sharecard.png');print('share msg',await pg.evaluate("document.getElementById('shMsg')?.innerText"))
    fb=await pg.query_selector('#fbCard');print('fbCard', fb is not None, fb and await pg.evaluate("document.getElementById('fbCard').innerText"))
    if fb:
      await pg.evaluate("document.getElementById('fbCard').scrollIntoView()");await SS('feedback')
    print(errs)
asyncio.run(main())
