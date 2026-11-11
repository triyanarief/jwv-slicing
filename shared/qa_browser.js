// Browser QA for local static pages. No external submissions or credentials.
async (page) => {
  const fs = await import('node:fs');
  const path = await import('node:path');
  const root = '/Users/triyanwibowo/Documents/Codex/jwv-slicing';
  const batch = JSON.parse(fs.readFileSync(path.join(root, 'qa/current-batch.json'), 'utf8'));
  const inventory = JSON.parse(fs.readFileSync(path.join(root, 'docs/status/figma-inventory.json'), 'utf8'));
  const results = [];
  for (const slug of batch) {
    const folder = path.join(root, 'qa', slug);
    fs.mkdirSync(folder, {recursive:true});
    const html = fs.readFileSync(path.join(root, slug, 'index.html'), 'utf8');
    const node = html.match(/data-figma-node="([^"]+)"/)[1];
    const frame = inventory.screen_candidates.find(f => f.id === node);
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
      await page.screenshot({path:path.join(folder, native?'pass-2-native.png':`pass-2-${width}.png`),fullPage:true});
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
      await page.locator('[data-preview-fullscreen]').click();test.staticPreviewFullscreen=await page.evaluate(()=>!!document.fullscreenElement);if(test.staticPreviewFullscreen)await page.evaluate(()=>document.exitFullscreen());
    }
    if(await page.locator('[data-dashboard-search]').count()) {
      const search=page.locator('[data-dashboard-search]');await search.fill('no-match-qa');test.dashboardSearch=await page.locator('[data-dashboard-record]:not([hidden])').count()===0;await search.fill('');
    }
    const blocked=page.locator('button[data-unavailable]:visible').first();
    if(await blocked.count()) {
      const dialogPromise=page.waitForEvent('dialog').then(async dialog=>{const message=dialog.message();await dialog.dismiss();return message;});await blocked.click();test.unavailableActionMessage=await dialogPromise;
    }
    const theme=page.locator('a[aria-label*="theme"],a[aria-label="Switch theme"]').first();
    if(await theme.count()){const target=await theme.getAttribute('href');await theme.click();test.themeNavigation=page.url().includes(target.replace('../','').split('#')[0]);}
    result.errors=errors;result.failedRequests=failedRequests;result.httpErrors=responses;
    result.passed=result.responsive.every(r=>r.documentWidth<=r.width&&r.missingImages.length===0)&&Object.values(test).every(v=>v!==false)&&!errors.length&&!failedRequests.length&&!responses.length;
    fs.writeFileSync(path.join(folder,'pass-2-results.json'),JSON.stringify(result,null,2));
    results.push({slug,passed:result.passed,responsive:result.responsive.map(r=>[r.width,r.documentWidth]),interactions:test,errors});
    page.off('pageerror',onError);page.off('console',onConsole);page.off('requestfailed',onFailed);page.off('response',onResponse);
  }
  return results;
}
