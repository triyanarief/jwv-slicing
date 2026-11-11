// Direct browser-only QA. Inputs and persistence are handled by the calling tool.
async (page) => {
  const frames = __FRAMES__;
  const pass = __PASS__;
  const root = '/Users/triyanwibowo/Documents/Codex/jwv-slicing/qa';
  await page.route('http://127.0.0.1:8765/**', route => route.continue());
  const results = [];
  for (const frame of frames) {
    const errors = [];
    const onError = error => errors.push(error.message);
    page.on('pageerror', onError);
    const result = {page:frame.slug, node:frame.node, pass, widths:[], checkedAt:new Date().toISOString()};
    for (const width of [Math.round(frame.width),390]) {
      await page.setViewportSize({width,height:Math.ceil(frame.height)});
      await page.goto('http://127.0.0.1:8765/'+frame.slug+'/index.html');
      await page.evaluate(()=>document.fonts.ready);
      const checks = {width,tooltips:[]};
      const triggers = page.locator('[data-tooltip]');
      for (let i=0;i<await triggers.count();i++) {
        const trigger = triggers.nth(i);
        await trigger.scrollIntoViewIfNeeded();
        await trigger.hover();
        const tip=page.locator('#source-tooltip');
        const visible=await tip.isVisible();
        const geometry=await tip.evaluate(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {width:r.width,height:r.height,left:r.left,right:r.right,font:s.font,background:s.backgroundColor};});
        const expected=await trigger.getAttribute('data-tooltip');
        const textMatches=await tip.textContent()===expected;
        if(i===0)await page.screenshot({path:root+'/'+frame.slug+'/state-pass-'+pass+'-'+width+'.png',fullPage:true});
        await page.keyboard.press('Escape');
        const escapeHides=!(await tip.isVisible());
        await page.mouse.move(0,0);
        await trigger.evaluate(e=>e.blur());
        await trigger.focus();
        const keyboardShows=await tip.isVisible();
        await page.keyboard.press('Tab');
        const blurHides=!(await tip.isVisible()) || await page.locator('[data-tooltip]:focus').count()>0;
        checks.tooltips.push({label:await trigger.getAttribute('aria-label'),visible,textMatches,escapeHides,keyboardShows,blurHides,geometry});
      }
      const checkbox=page.locator('.remember input');
      if(await checkbox.count()) {
        await checkbox.hover();
        await page.waitForFunction(()=>getComputedStyle(document.querySelector('.remember input')).borderTopColor==='rgb(212, 212, 212)');
        checks.checkboxBorder=await checkbox.evaluate(e=>getComputedStyle(e).borderTopColor)==='rgb(212, 212, 212)';
        await checkbox.focus();await page.keyboard.press('Space');checks.checkboxKeyboard=await checkbox.isChecked();await page.keyboard.press('Space');
      }
      const signup=page.locator('.auth-page:not(.register-page) .auth-footer a');
      if(await signup.count()) {await signup.hover();checks.signupUnderline=await signup.evaluate(e=>getComputedStyle(e).textDecorationLine.includes('underline'));}
      const number=page.locator('.pagination-placeholder').last();
      if(await number.count()) {await number.hover();checks.paginationHover=await number.evaluate(e=>getComputedStyle(e).backgroundColor)==='rgb(250, 250, 250)';}
      await page.mouse.move(0,0);await page.keyboard.press('Escape');
      checks.noOverflow=await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
      checks.assetsLoaded=await page.evaluate(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));
      result.widths.push(checks);
    }
    result.errors=errors;
    result.passed=!errors.length&&result.widths.every(w=>Object.values(w).every(v=>v!==false)&&w.tooltips.every(t=>t.visible&&t.textMatches&&t.escapeHides&&t.keyboardShows&&t.blurHides&&t.geometry.height===34&&t.geometry.left>=0&&t.geometry.right<=w.width));
    page.off('pageerror',onError);
    results.push(result);
  }
  return results;
}
