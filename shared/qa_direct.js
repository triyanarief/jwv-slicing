// Pure supported browser calls. Frame data is supplied outside the browser runtime.
async (page) => {
  const root = '/Users/triyanwibowo/Documents/Codex/jwv-slicing';
  const frames = __FRAMES__;
  page.setDefaultTimeout(5000);
  // Routing disables HTTP cache so captures reflect the current local files.
  await page.route("http://127.0.0.1:8765/**", route => route.continue());
  const results = [];
  for (const frame of frames) {
    const {slug,node}=frame;
    const folder = root+'/qa/'+slug;
    const errors = [], failedRequests = [], responses = [];
    const onError = e => errors.push(e.message);
    const onConsole = e => {if (e.type() === 'error') errors.push(e.text());};
    const onFailed = r => failedRequests.push({url:r.url(),error:r.failure()?.errorText});
    const onResponse = r => {if(r.status() >= 400) responses.push({url:r.url(),status:r.status()});};
    page.on('pageerror', onError);page.on('console', onConsole);page.on('requestfailed',onFailed);page.on('response',onResponse);
    const result = {slug,node,pass:2,checkedAt:new Date().toISOString(),responsive:[],interactions:{}};
    await page.goto('http://127.0.0.1:8765/'+slug+'/index.html');
    for (const width of [Number(frame.width),1440,1024,768,390]) {
      const native = result.responsive.length === 0;
      await page.setViewportSize({width:Math.round(width),height:native?Math.ceil(Number(frame.height)):982});
      await page.evaluate(async()=>{await document.fonts.ready; await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));document.activeElement?.blur();window.scrollTo(0,0);});
      const metrics = await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,missingImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.getAttribute('src')),activeDestinations:[...document.querySelectorAll('nav [aria-current="page"]')].map(e=>e.textContent.trim())}));
      result.responsive.push({native,...metrics});
      await page.screenshot({path:folder+'/'+(native?'pass-2-native.png':`pass-2-${width}.png`),fullPage:true});
    }
    const test = result.interactions;
    const menu=page.locator('[data-navigation-toggle], [data-home-menu]');
    if(await menu.count()) {
      await menu.click();test.mobileMenuOpen=await menu.getAttribute('aria-expanded')==='true';
      await page.keyboard.press('Escape');test.mobileMenuEscape=await menu.getAttribute('aria-expanded')==='false';
    }
    await page.setViewportSize({width:Math.round(Number(frame.width)),height:982});
    await page.goto('http://127.0.0.1:8765/'+slug+'/index.html');
    await page.keyboard.press('Tab');test.skipLinkFocused=await page.locator('.skip-link').evaluate(e=>document.activeElement===e);
    await page.screenshot({path:folder+'/keyboard-focus.png'});
    await page.keyboard.press('Enter');test.skipLinkTarget=await page.evaluate(()=>location.hash==='#main');
    if(await page.locator('[data-local-auth]').count()) {
      test.emptyFormRejected=await page.locator('[data-local-auth]').evaluate(f=>!f.checkValidity());
      const email=page.locator('input[type="email"]');await email.fill('invalid');test.invalidEmailRejected=await email.evaluate(e=>e.validity.typeMismatch);await email.fill('');
      const toggle=page.locator('[data-password-toggle]').first();await toggle.click();test.passwordVisibilityOn=await page.locator('input[name="password"]').getAttribute('type')==='text';await toggle.click();test.passwordVisibilityOff=await page.locator('input[name="password"]').getAttribute('type')==='password';
    }
    if(await page.locator('[data-team-search]').count()) {
      const search=page.locator('[data-team-search]');await search.fill('no-match-qa');test.teamEmptySearch=await page.locator('[data-no-results]').isVisible();await search.fill('');
      const select=page.locator('[data-age-filter]');await select.selectOption({index:1});test.ageFilter=await page.locator('[data-team]:not([hidden])').count()>0;await select.selectOption({index:0});
      await search.fill('Hawks');test.viewLinksPreserveSearch=await page.locator('[data-view-link]').evaluateAll(links=>links.every(l=>l.href.includes('search=Hawks')));await search.fill('');
    }
    if(await page.locator('[data-density]').count()) {
      const box=page.locator('[data-density]');await box.focus();await page.keyboard.press('Space');test.densityKeyboard=await page.locator('.admin-table-box').getAttribute('data-dense')!==null;await page.keyboard.press('Space');
    }
    if(await page.locator('[data-home-search]').count()) {
      const next=page.locator('[data-scroll="1"]').first(), track=page.locator('#category-track');
      await next.click();await page.waitForFunction(()=>document.getElementById('category-track').scrollLeft>0);test.categoryCarousel=await track.evaluate(e=>e.scrollLeft>0);
      const search=page.locator('[data-home-search]');await search.fill('no-match-qa');test.homeEmptySearch=await page.locator('[data-home-item]:not([hidden])').count()===0;test.homeEmptyMessage=await page.locator('[data-home-empty]').isVisible();await search.fill('');
    }
    if(await page.locator('[data-preview-timeline]').count()) {
      const range=page.locator('[data-preview-timeline]');await range.focus();const before=await range.inputValue();await page.keyboard.press('ArrowRight');test.previewTimelineKeyboard=Number(await range.inputValue())>Number(before);
      await page.locator('[data-preview-fullscreen]').click();await page.waitForFunction(()=>!!document.fullscreenElement);test.staticPreviewFullscreen=await page.evaluate(()=>!!document.fullscreenElement);if(test.staticPreviewFullscreen)await page.evaluate(()=>document.exitFullscreen());
    }
    if(await page.locator('[data-dashboard-search]').count()) {
      const search=page.locator('[data-dashboard-search]');await search.fill('no-match-qa');test.dashboardSearch=await page.locator('[data-dashboard-record]:not([hidden])').count()===0;await search.fill('');
    }
    if(await page.locator('[data-wallet-search]').count()) {
      const search=page.locator('[data-wallet-search]');await search.fill('no-match-qa');test.walletEmptySearch=await page.locator('[data-wallet-empty]').isVisible();await search.fill('Test Club');test.walletMatch=await page.locator('[data-wallet-record]:not([hidden])').count()===1;await search.fill('');
      await page.locator('a[href="#club-broadcasters"]').click();test.manageWalletsAnchor=page.url().endsWith('#club-broadcasters');
    }
    const linkChecks=await page.evaluate(async()=>{const links=[...new Set([...document.querySelectorAll('a[href]')].map(a=>a.href))];return await Promise.all(links.map(async url=>{if(!url.startsWith(location.origin))return {url,external:true};const r=await fetch(url);await r.text();return {url,status:r.status};}));});
    result.linkChecks=linkChecks;test.localLinksResolve=linkChecks.every(l=>l.status===200);
    result.unavailableControls=await page.locator('[data-unavailable]').evaluateAll(items=>items.map(e=>({label:e.getAttribute('aria-label')||e.textContent.trim(),reason:e.dataset.unavailable,ariaDisabled:e.getAttribute('aria-disabled')})));
    const theme=page.locator('a[aria-label*="theme"],a[aria-label="Switch theme"]').first();
    if(await theme.count()){const target=await theme.getAttribute('href');await theme.click();test.themeNavigation=page.url().includes(target.replace('../','').split('#')[0]);}
    await page.screenshot({path:folder+'/interaction-end.png',fullPage:true});
    result.errors=errors;result.failedRequests=failedRequests;result.httpErrors=responses;
    result.passed=result.responsive.every(r=>r.documentWidth<=r.width&&r.missingImages.length===0)&&Object.values(test).every(v=>v!==false)&&!errors.length&&!failedRequests.length&&!responses.length;

    results.push(result);
    page.off('pageerror',onError);page.off('console',onConsole);page.off('requestfailed',onFailed);page.off('response',onResponse);
  }
  return results;
}
