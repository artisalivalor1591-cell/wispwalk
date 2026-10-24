from h import *
async def main():
  async with async_playwright() as p:
    b,ctx,pg,errs=await mk(p,ls={'ttu_intro':'1'})
    await pg.goto(URL+'?reset=1');await pg.wait_for_timeout(1500)
    await pg.tap('#agree');await pg.tap('#sxGo');await pg.wait_for_timeout(1000)
    await pg.tap('#sxStep [data-h=public]');await pg.wait_for_timeout(400);await pg.tap('#stGo');await pg.wait_for_timeout(2500)
    mp=await pg.evaluate("(()=>{const m=[...document.querySelectorAll('.leaflet-container')].filter(e=>e.getClientRects().length);return m.map(e=>e.id)})()");print('maps',mp)
    el=await pg.query_selector('#'+mp[0]);await el.scroll_into_view_if_needed();await pg.wait_for_timeout(600)
    bb=await el.bounding_box();print(bb)
    cx,cy=bb['x']+bb['width']/2,bb['y']+bb['height']/2
    pts=[(cx-80,cy-60),(cx+80,cy-60),(cx+80,cy+60),(cx-80,cy+60)]
    for x,y in pts: await pg.touchscreen.tap(x,y);await pg.wait_for_timeout(400)
    await pg.screenshot(path='08_draw_polygon.png')
    poly=await pg.evaluate("(()=>{try{return JSON.stringify(typeof pts!=='undefined'?pts:null)}catch(e){return 'err'}})()");print('pts var',poly)
    print('pts',await pg.evaluate("JSON.stringify(drawPts)"))
    await pg.tap('text=Done');await pg.wait_for_timeout(800);await pg.screenshot(path='08_after_done.png')
    await pg.tap('#sxGo');await pg.wait_for_timeout(1000);await pg.screenshot(path='08_permission_dialog.png')
    print(await vis(pg)[-12:] if False else '')
    v=await vis(pg);print('\n'.join(v[-12:]))
    await pg.click('text=Yes, I have permission');await pg.wait_for_timeout(4000);await pg.screenshot(path='08_hunt_started.png')
    r=await pg.evaluate("""(()=>{const P=drawPts,pin=S&&S.pin;if(!pin)return 'nopin '+JSON.stringify(Object.keys(S||{}));const x=pin.lng??pin[0],y=pin.lat??pin[1];let c=false;for(let i=0,j=P.length-1;i<P.length;j=i++){const a=P[i],b=P[j];if((a[1]>y)!=(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])c=!c}return JSON.stringify({pin,inside:c,P})})()""");print(r)
    print(errs)
asyncio.run(main())
