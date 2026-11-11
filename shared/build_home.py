"""Static semantic homepage sections, mapped to inspected Figma nodes."""
from pathlib import Path
import json
from build_pages import ROOT,asset,document,unavailable

SECTIONS=json.loads((ROOT/'docs/source/home-section-map.json').read_text())
def a(folder,name,alt='',css=''):
    matches=list((ROOT/'shared/assets'/folder).glob(name+'.*'))
    assert len(matches)==1,(folder,name)
    return asset(folder,matches[0].name,alt,css)

def home_brand(folder):
    return f'<span class="home-brand"><span class="home-wordmark">{a(folder,"imgCurvedHighlight")}JWV</span><span class="home-brand-line">STREAMING{a(folder,"imgPlayEmblem")}</span><small>POWERED BY JWV DEV</small></span>'

def header(slug):
    theme=slug.rsplit('-',1)[1];f=slug+'-hero';signed='signed-in' in slug
    other=slug[:-4]+'light' if theme=='dark' else slug[:-5]+'dark'
    destinations=[('Home','#main'),('Live Games','#live-streams' if signed else '../home-signed-in-'+theme+'/index.html#live-streams'),('Sports','#sports'),('Replays','#replays' if signed else '../home-signed-in-'+theme+'/index.html#replays')]
    nav=''.join(f'<a href="{href}"'+(' aria-current="page"' if label=='Home' else '')+'>'+label+'</a>' for label,href in destinations)
    nav+=unavailable('Schedule','A schedule screen is not supplied in Design Ready.','home-nav-unavailable')
    account=unavailable('','Profile menu is blocked: no profile or account-menu design is supplied.','home-profile',a(f,'imgUser')).replace('<button ','<button aria-label="Profile unavailable" ',1) if signed else f'<a class="home-button blue compact" href="../login-{theme}/index.html">Sign Up / Log In</a>'
    return f'''<header class="home-header"><a href="../{slug}/index.html" aria-label="JWV Streaming home">{home_brand(f)}</a><button class="home-menu-toggle home-button" data-home-menu aria-controls="home-navigation" aria-expanded="false">Menu</button><nav class="home-nav" id="home-navigation" aria-label="Main">{nav}</nav><div class="home-header-controls"><label class="home-search">{a(f,'imgSearch01')}<span class="sr-only">Search sports and matches</span><input type="search" placeholder="Search for anything" data-home-search></label><a class="home-theme" href="../{other}/index.html" aria-label="Switch to {'light' if theme=='dark' else 'dark'} theme"><span class="theme-track" aria-hidden="true"></span>Dark</a>{account}<a class="home-button compact" href="../register-broadcaster-{theme}/index.html">Start Broadcasting.</a></div></header>'''

def stores(folder):
    return '<div class="store-links">'+''.join(unavailable('',label+' link is not supplied in the Figma prototype. No external destination has been guessed.','store-badge',a(folder,img,label)).replace('<button ','<button aria-label="'+label+' unavailable" ',1) for label,img in [('Download on the App Store','imgGroup41'),('Get it on Google Play','imgGroup44')])+'</div>'

def public_hero(slug):
    theme=slug.rsplit('-',1)[1];f=slug+'-hero'
    def service(label,img,css):return f'<span class="network-service {css}">{a(f,img)}<span>{label}</span></span>'
    network=f'''<div class="network-art" role="img" aria-label="JWV streams connect with YouTube, Google Drive, OneDrive, Dropbox and iCloud"><div class="network-lines">{asset('home-artwork','8292-3265.svg',css='network-left')}{asset('home-artwork','8292-3293.svg',css='network-right')}</div>{asset('home-artwork','8292-3330.svg',css='network-brand')}{service('Youtube','imgLayer2','network-youtube')}{service('Google Drive','imgGroup','network-drive')}{service('OneDrive','imgOnedriveSeeklogo1','network-onedrive')}{service('Drobox','imgColor','network-dropbox')}{service('Icloud','imgAppleIcloudSeeklogo1','network-icloud')}</div>'''
    return f'''<section class="public-hero" aria-labelledby="hero-title"><div class="hero-backdrop">{a(f,'img05AutoOrderV2')}</div><div class="public-hero-title">{stores(f)}<h1 id="hero-title">Watch Free on Samsung, LG TV,<br> Fire TV, Roku and Google TV</h1></div>{network}<div class="hero-actions"><a class="home-button" href="../home-signed-in-{theme}/index.html#live-streams">{a(f,'imgPlay')}Watch Live</a><a class="home-button blue" href="../register-user-{theme}/index.html">Get Started {a(f,'imgArrowRight02')}</a></div></section>'''

def find_stream(slug):
    f=slug+'-find'
    return f'''<section class="find-stream" aria-label="How to find a stream"><div class="find-intro"><span class="feature-icon">{a(f,'imgSearch01')}</span><div><h2>Find a live stream easily.</h2><p>Once you’re signed in, use Search or browse in 3 simple steps.</p></div></div><ol><li><a href="#sports">Choose a sport</a></li><li>{unavailable('Find a channel','Channel browsing has no supplied destination design.','find-step')}</li><li>{unavailable('Pick a game','Game details and playback destinations are not supplied.','find-step')}</li></ol></section>'''

def carousel_controls(folder,target):
    next_icon=a(folder,'imgChevronRight1' if (ROOT/'shared/assets'/folder/'imgChevronRight1.svg').exists() else 'imgChevronRight')
    return f'<div class="carousel-controls"><button type="button" data-scroll="-1" data-track="{target}" aria-label="Previous items" class="previous">{next_icon}</button><button type="button" data-scroll="1" data-track="{target}" aria-label="Next items">{next_icon}</button></div>'

def categories(slug):
    f=slug+'-categories';names=['HOCKEY','BASEBALL','VOLLEYBALL','SOCCER','football','Hockey'];items=[]
    for i,name in enumerate(names):
        picture=a(f,'imgCategoryImage'+(str(i) if i else ''),name+' category')
        badge='<span class="coming-soon">Coming Soon</span>' if i in [1,2,3,4] else unavailable('','Sport channel browsing is not supplied in Design Ready.','category-action',a(f,'imgArrowUpRight01')).replace('<button ','<button aria-label="Browse '+name+' unavailable" ',1)
        items.append(f'<article class="category-card" data-home-item="{name.lower()}">{picture}{badge}<h3>{name}</h3></article>')
    return f'''<section class="home-section categories" id="sports"><header class="home-section-heading"><div><h2>Explore by Category</h2><p>From the rink to the field, find the sports you love</p></div>{carousel_controls(f,'category-track')}</header><div class="carousel-track category-track" id="category-track">{''.join(items)}</div><p class="home-no-results" data-home-empty hidden>No sports or matches match this search.</p></section>'''

def devices(slug):
    f=slug+'-devices';light=slug.endswith('light')
    if light:
        chips=''.join('<span>'+a(f,img,label)+'</span>' for label,img in [('Roku TV','imgImage2'),('Google TV','imgGoogleTvSeeklogo1'),('Fire TV','imgImage1'),('Android TV','imgImage3'),('LG webOS','imgImage4'),('Samsung','imgSamsungLogoPng12951')])+'<span>Web TV</span>'
    else:chips=''.join('<span>'+s+'</span>' for s in ['Web','Fire TV','Google TV','Roku','Android TV','LG webOS','Samsung TV'])
    return f'''<section class="home-section devices" id="devices"><header class="split-heading"><div><p class="section-eyebrow">APPLICATIONS &amp; DEVICES</p><h2>Your game. On your<br><em>favorite screen</em>.</h2></div><p>Whether you’re at home or on the go, your family can watch live games and replays on the devices they already use.</p></header><div class="device-layout"><div class="device-card"><div><p class="device-kicker">{a(f,'imgMonitor')}WATCH ANYWHERE</p><h3>From the rink to your living room.</h3><p>Viewers watch free online or through supported TV and streaming applications. Easy access for parents, grandparents and fans.</p><div class="device-chips">{chips}</div></div><div><p class="mobile-label">Watch On Mobile</p>{stores(f)}</div></div><figure class="device-photo">{a(f,'imgImage','Family watching a JWV football broadcast at home')}<figcaption>ONE STREAM. MORE WAYS TO WATCH.</figcaption></figure></div></section>'''

BENEFITS=[('Broadcast from any device','Live stream your team’s games without complicated equipment or setup.','imgComputerPhoneSync'),('Save to YouTube automatically','Your live streams can be automatically saved to YouTube for free.','imgYoutube'),('Free cloud storage','Save streams automatically to Dropbox, Google Drive, iCloud or OneDrive for free.','imgCloud'),('Free for viewers','Parents, relatives and fans can watch your live streams at no cost.','imgHouseHeart'),('Watch on your favorite TV','Enjoy games online, on Fire TV, Google TV, Roku, Android TV, LG webOS and Samsung TV.','imgComputer'),('Only $ per minute',"No monthly fee. Pay only for the time you’re actually live streaming.",'imgDollarCircle')]
def spotlight_heading(slug):
    theme=slug.rsplit('-',1)[1]
    icon=a(slug+('-showcase' if 'signed-in' in slug else '-benefits'),'imgRss')
    return f'''<header class="spotlight-heading"><div><span class="home-tag">MADE FOR EVERY GAME DAY</span><h2>Put Every Game in the Spotlight</h2><p>From the first whistle to the final buzzer, bring youth sports to life with seamless live streaming.<br>Connect teams, families, and fans wherever they are.</p></div><div class="hero-actions"><a class="home-button" href="../register-broadcaster-{theme}/index.html">{icon}Start Broadcasting</a><a class="home-button white" href="#devices">See How It Works</a></div></header>'''
def benefits(slug):
    f=slug+'-benefits'
    head='''<header class="split-heading"><div><p class="section-eyebrow">WHY JWV STREAMING</p><h2>Everything you need.<br>Nothing you don't.</h2></div><p>Simple streaming for teams, clubs, parents and fans, with clear pricing and convenient automatic saves.</p></header>''' if slug.endswith('light') else spotlight_heading(slug)
    cards=''.join(f'<article class="benefit-card"><div><span class="feature-icon">{a(f,icon)}</span><span class="benefit-number">{i+1:02}</span></div><h3>{title}</h3><p>{desc}</p></article>' for i,(title,desc,icon) in enumerate(BENEFITS))
    return f'<section class="home-section benefits" id="benefits">{head}<div class="benefit-grid">{cards}</div></section>'

def footer(slug):
    f=slug+'-footer';theme=slug.rsplit('-',1)[1];signed='signed-in' in slug;prefix='' if signed else '../home-signed-in-'+theme+'/index.html'
    explores=''.join(f'<a href="{prefix}{href}">{label}</a>' for label,href in [('Trendings','#trending'),('Live Matches','#live-streams'),('Upcoming Streams','#trending'),('Replays','#replays')])
    legal=''.join(unavailable(label,label+' has no supplied page design.','footer-link') for label in ['Privacy Policy','Terms of Service'])
    return f'''<footer class="home-footer"><div class="footer-panel"><div class="footer-top"><div class="footer-about"><a href="#main" aria-label="JWV Streaming home">{home_brand(f)}</a><p>JWV Streaming offers live and on-demand sport broadcast, connecting fans clubs and broadcasters with seamless<br>streaming experiences worldwide.</p></div><nav aria-label="Explore"><h2>Explore</h2>{explores}</nav><nav aria-label="JWV Streaming HQ"><h2>JWV Streaming HQ</h2>{unavailable('About Us','About Us has no supplied page design.','footer-link')}<a href="#devices">How It Works</a><a href="../register-broadcaster-{theme}/index.html">Start Broadcasting</a></nav><div class="footer-contact"><h2>Contact Us</h2><p>{a(f,'imgCall02')}+1 (701) 215-1010</p><p>{a(f,'imgMail01')}info@jwvstreaming.com</p><p>{a(f,'imgLocation01')}Grand Forks, ND, 58201<br>United States</p></div></div><div class="footer-bottom"><p>© 2026 JWV Streaming. All Right Reserved</p><div>{legal}</div></div></div></footer>'''

def build_public():
    for slug,node in [('home-light','8291:1011'),('home-dark','8307:8678')]:
        content=header(slug)+'<main id="main">'+public_hero(slug)+find_stream(slug)+categories(slug)+devices(slug)+benefits(slug)+'</main>'+footer(slug)
        document(slug,'Watch and broadcast sports',content,body_class='home-page '+slug.rsplit('-',1)[1],node=node,extra_css='<link rel="stylesheet" href="../shared/home.css">')

PLAYBACK_BLOCK='No playable media or game-details design is supplied. This is a local sample state; no live connection, playback, reminder or broadcast has started.'

def play_button(folder,icon='imgPlay',label='Play unavailable',css='round-play'):
    return unavailable('',PLAYBACK_BLOCK,css,a(folder,icon)).replace('<button ','<button aria-label="'+label+'" ',1)

def signed_hero(slug):
    f=slug+'-hero';theme=slug.rsplit('-',1)[1];light=theme=='light'
    controls=unavailable('Watch Live',PLAYBACK_BLOCK,'home-button',a(f,'imgPlay'))+f'<a class="home-button muted" href="../register-broadcaster-{theme}/index.html">{a(f,"imgRss")}Start Broadcasting</a>'
    dots='<div class="hero-slide-controls">'+unavailable('‹','Other featured hero slide states are not supplied.','slide-arrow')+''.join('<span class="slide-dot'+(' selected' if i==2 else '')+'"></span>' for i in range(6))+unavailable('›','Other featured hero slide states are not supplied.','slide-arrow')+'</div>'
    feature=f'''<article class="signed-feature"><div class="signed-feature-photo">{a(f,'imgFeaturedMatch' if light else 'imgHockeyPlayers3','Two youth hockey players facing off')}</div><div class="signed-feature-copy"><span class="match-status live">● LIVE NOW</span><h1>BOSTON BRUINS vs DALLAS STARS</h1><h2>FIH Hockey World Cup 2026 | U18</h2><p>Experience the thrill as the Boston Bruins take on the Dallas Stars in a high-stakes youth hockey championship. Stay tuned for every exciting play.</p><div class="feature-bottom"><div class="hero-actions">{controls}</div>{dots}</div></div></article>'''
    highlight=[]
    names=[('EAGLES VS PHOENIX','Hockey','FIH USA Cup','LIVE NOW'),('BROWNS VS CLOTS','Volleyball','Volleyball League' if light else 'Volleyball Nations League','LIVE NOW'),('UNITED FC VS RIVERSIDE','Soccer','Youth Soccer League','REPLAY'),('GIANTS VS RAMS','Football','IFAF USA Awards','UPCOMING | NOV 16, 19:30'),('JAGUARS VS JETS','Baseball','IFAF USA Awards','UPCOMING | NOV 20, 16:00')]
    for i,(title,sport,league,state) in enumerate(names):
        photo=a(f,'imgImage'+(str(i) if i else ''),title)
        cls='live' if i<2 else 'replay' if i==2 else 'upcoming'
        icon='imgNotification01' if i>2 else 'imgPlay1'
        highlight.append(f'<article class="highlight-match" data-home-item="{title} {sport}">{photo}<div><span class="match-status {cls}">● {state}</span><h3>{title}</h3><p>{sport} • {league}</p></div>{play_button(f,icon,"Watch "+title+" unavailable" if i<3 else "Set reminder unavailable")}</article>')
    return f'<section class="signed-hero" id="live-streams">{feature}<aside class="highlights"><h2>HIGHLIGHT MATCHES</h2><div>{"".join(highlight)}</div></aside></section>'

def trending(slug):
    f=slug+'-trending';items=[]
    matches=[('BLUE JACKETS VS TITANS','Hockey','FIH Hockey World Cup 2026','LIVE NOW','9.8K'),('BILLS VS RAVENS','Football','IFAF World Championship','UPCOMING | OCT 26, 18:30','1.2K'),('THUNDER VS FURY','Volleyball','Volleyball America’s Cup','REPLAY','2.6K'),('ORIOLES VS RED SOX','Baseball','World Baseball Classic','LIVE NOW','4.7K'),('NORTHSIDE WOLF VS LAKESHORE FALCON','Hockey','U16','LIVE NOW','2.3K')]
    for i,(title,sport,league,state,views) in enumerate(matches):
        photo=a(f,'imgMatchCard'+(str(i) if i else ''),title)
        logos=''.join(a(f,'imgTeamLogo'+(str(j) if j else '')) for j in [i*2,i*2+1])
        if i==4:
            items.append(f'''<article class="trending-card compact-match" data-home-item="Northside Wolf Lakeshore Falcon Hockey">{photo}<span class="match-status live">● LIVE NOW</span><span class="trending-views">{a(f,'imgView')}{views}</span><div class="compact-match-details"><p>Hockey <span>•</span> U16</p><h3>Northside Wolf vs. Lakeshore Falcon</h3><div class="compact-match-teams"><span>{a(f,'imgTeamLogo8')}Wolves</span><b>VS</b><span>{a(f,'imgTeamLogo9')}Falcon</span></div></div></article>''')
            continue
        stateclass='upcoming' if i==1 else 'replay' if i==2 else 'live'
        items.append(f'''<article class="trending-card {'large' if i==0 else ''}" data-home-item="{title} {sport}">{photo}<span class="match-status {stateclass}">● {state}</span><span class="trending-views">{a(f,'imgBookmark02' if i==1 else 'imgView')}{views}</span><div class="match-teams">{logos}</div><div class="trending-caption"><h3>{title}</h3><p>{sport} • {league}</p></div>{play_button(f,'imgNotification01' if i==1 else 'imgPlay','Open '+title+' unavailable')}</article>''')
    return f'<section class="home-section trending" id="trending"><header class="home-section-heading"><div><h2>Trending Now</h2><p>Catch the games and highlights everyone is watching</p></div>{carousel_controls(f,"trending-track")}</header><div class="carousel-track" id="trending-track">'+''.join(items)+'</div></section>'

def continue_watching(slug):
    f=slug+'-continue';items=[]
    for i in range(2):
        picture=a(f,'imgImage'+('1' if i else ''),'Soccer replay' if i==0 else 'Baseball replay')
        progress='<div class="replay-progress"><span></span></div>'
        items.append(f'''<article class="replay-card" data-home-item="United FC Riverside Soccer"><div class="replay-image">{picture}{progress}<span class="replay-time">01:42:21</span></div><div class="replay-copy"><span class="match-status replay">● REPLAY</span><h3>UNITED FC VS RIVERSIDE</h3><h4>Soccer • Youth Soccer League</h4><p>Relive the best moments as United FC takes on Riverside in an exciting U16 league match.</p><p class="replay-meta">{a(f,'imgClock01')}42 min left <span>|</span> {a(f,'imgCalendar03')}Oct 23, 2026</p>{unavailable('Watch Live' if slug.endswith('light') and i==0 else 'Resume',PLAYBACK_BLOCK,'home-button',a(f,'imgPlay'))}</div></article>''')
    return f'<section class="home-section continue-section" id="replays"><header class="home-section-heading"><div><h2>Continue Watching</h2><p>Pick up where you left off with the games and highlights you’re currently watching</p></div>{carousel_controls(f,"replay-track")}</header><div class="carousel-track" id="replay-track">'+''.join(items)+'</div></section>'

def showcase(slug):
    f=slug+'-showcase'
    content=f'''<article class="broadcast-showcase"><div class="broadcast-image">{a(f,'imgContainer','Youth hockey broadcast preview')}<span class="match-status live">● LIVE NOW</span><span class="broadcast-time">{a(f,'imgLiveStatus')}Stream Live <strong>00:28:44</strong></span><div class="broadcast-controls"><span>34:05</span><input type="range" min="0" max="100" value="54" aria-label="Local preview timeline" data-preview-timeline><span>57:45</span>{unavailable('',PLAYBACK_BLOCK,'video-icon',a(f,'imgVolume02')).replace('<button ','<button aria-label="Audio unavailable" ',1)}<button type="button" class="video-icon" data-preview-fullscreen aria-label="Expand static broadcast preview">{a(f,'imgFullscreen')}</button></div></div><div class="broadcast-caption"><div><h3>NORTHSIDE VS LAKESHORE</h3><p>Relive the thrilling showdown between the Northside Wolves and the Lakeshore Falcons in this intense youth hockey match. Watch every goal, save, and moment of drama as these two fierce rivals battle on the ice.</p></div><p class="broadcast-details">{a(f,'imgWifi01')}8.2 Mbps <span>|</span>{a(f,'imgUser02')}2.3K <span>|</span>{a(f,'img4K')}HD</p></div></article>'''
    return f'<section class="home-section showcase-section">{spotlight_heading(slug)}{content}</section>'

def features(slug):
    f=slug+'-features';rows=[]
    data=[('Stream on Any Device','Broadcast directly from your phone, tablet, or computer.','imgMonitor'),('Free Automatic Storage','Save streams to YouTube, Dropbox, Google Drive, iCloud, or OneDrive.','imgCloudUpload'),('Watch Anywhere for Free','Watch live streams for free online or on Fire TV, Google TV, Roku, Android TV, LG webOS, and Samsung TV.','imgTv01'),('Only 10¢ per Minute',"No monthly fee. Pay only for the time you’re live.",'imgDollarCircle')]
    for i,(title,desc,icon) in enumerate(data):rows.append(f'<article class="feature-detail {"selected" if i==0 else ""}">{a(f,icon)}<h3>{title}</h3><p>{desc}</p></article>')
    return f'''<section class="home-section feature-section" id="devices"><header><h2>Everything You Need. Nothing You Don't.</h2><p>Simple, affordable streaming for teams, families, and fans.</p></header><div class="feature-layout"><figure>{a(f,'imgImage','Watching sport on a phone and television')}</figure><div>{''.join(rows)}</div></div></section>'''

def cta(slug):
    f=slug+'-cta'
    return f'''<section class="home-cta"><div class="cta-photo">{a(f,'imgAmericanFootballPlayerNeonStyle3','Football players in a stadium')}</div><div class="cta-copy"><span class="home-tag">STAY CLOSE TO THE GAME</span><h2>NEVER MISS A MOMENT OF THE GAME.</h2><p>Catch live youth sports, relive your favorite matches, and stay connected to every game, wherever you are.</p><div class="hero-actions"><a class="home-button" href="#live-streams">{a(f,'imgNext')}Start Watching</a><a class="home-button white" href="#sports">Explore Sport</a></div></div></section>'''

def build_signed():
    for slug,node in [('home-signed-in-dark','8212:33'),('home-signed-in-light','8212:3267')]:
        content=header(slug)+'<main id="main">'+signed_hero(slug)
        if slug.endswith('light'):content+=find_stream(slug)
        content+=categories(slug)+trending(slug)+continue_watching(slug)+showcase(slug)+features(slug)+cta(slug)+'</main>'+footer(slug)
        content+='<p class="sample-state-note">Local sample of the designed signed-in state. No user is authenticated; matches, viewing history, pricing and connection indicators are source examples.</p>'
        document(slug,'Sports home — local sample',content,body_class='home-page signed-home '+slug.rsplit('-',1)[1],node=node,extra_css='<link rel="stylesheet" href="../shared/home.css">')

if __name__=='__main__':
    build_public()
    build_signed()
