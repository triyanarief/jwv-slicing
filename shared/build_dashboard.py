"""Dashboard layouts from the latest light and dark redesign frames."""
from build_pages import ROOT,asset,document,unavailable,sidebar,NAV

def dashboard_sidebar(theme):
    f='club-dashboard-'+theme
    if theme=='dark':return sidebar(f,f)
    links=[]
    for i,(label,slug,_) in enumerate(NAV):
        if slug.endswith('-dark'):slug=slug[:-4]+'light'
        elif slug=='teams-list':slug='teams-list-light'
        elif slug=='broadcasters-wallets':slug='broadcasters-wallets-light'
        icon=asset(f,'imgIcon'+(str(i) if i else '')+'.svg')
        if i==5:links.append('<p class="nav-heading light-tools">STREAMING TOOLS</p>')
        links.append(f'<a class="nav-link" href="../{slug}/index.html"'+(' aria-current="page"' if i==0 else '')+'>'+icon+label+'</a>')
    logo='<a class="light-dashboard-brand" href="../index.html"><strong>JWV</strong><span><b>STREAMING<span class="brand-green-dot">◦</span></b><small>POWERED BY JWV DEV</small></span></a>'
    return f'''<aside class="sidebar"><div class="sidebar-header">{logo}<button class="button mobile-navigation" type="button" data-navigation-toggle aria-controls="workspace-nav" aria-expanded="false">Menu</button></div><nav class="side-nav" id="workspace-nav" aria-label="Workspace"><p class="nav-heading">WORKSPACE</p>{''.join(links)}</nav><div class="sidebar-ready"><strong>Ready to go live?</strong><p>Stream your team's next big moment with JWV.</p></div><p class="sidebar-copyright">JWV Streaming © 2026</p></aside>'''

def dashboard(theme):
    light=theme=='light';f='club-dashboard-'+theme
    img=lambda n,alt='',css='':asset(f,n,alt,css)
    other='dark' if light else 'light'
    search_icon='imgIcon8.svg' if light else 'imgSearchLg.svg'
    notifications='imgIcon10.svg' if light else 'imgContainer.svg'
    profile='CA' if light else img('imgUser.svg')
    header=f'''<header class="dash-header"><p class="breadcrumb">Workspace <span>/</span> <strong>Club Dashboard</strong></p><div class="dash-header-controls"><label class="dash-search">{img(search_icon)}<span class="sr-only">Search dashboard records</span><input type="search" placeholder="{'Search anything...' if light else 'Search'}" data-dashboard-search></label><a href="../club-dashboard-{other}/index.html" class="dash-theme" aria-label="Switch to {other} theme">{img('imgIcon9.svg' if light else 'imgIcon.svg')}{theme.title()}<span class="theme-track" aria-hidden="true"></span></a>{unavailable('','Notification panel is not designed in Design Ready.','dash-icon',img(notifications)).replace('<button ','<button aria-label="Notifications unavailable" ',1)}{unavailable('','Profile menu is not supplied.','dash-icon profile',profile).replace('<button ','<button aria-label="Profile unavailable" ',1)}</div></header>'''
    hero_background='' if light else img('imgMagnificPreserveTheOriginalCompositionAndExactlyFive654021.png',css='dash-hero-photo')
    plus=img('imgIcon11.svg' if light else 'imgPlus.svg')
    hero=f'''<section class="dash-hero">{hero_background}<div><p class="dash-eyebrow"><span></span>YOUR JWV CLUB HUB</p><h1>Welcome back! Let's get streaming.</h1><p>Everything your club needs to manage broadcasts, follow live games, and<br> keep every great moment on record.</p><div class="dash-actions"><a class="button button-primary" href="../register-broadcaster-{theme}/index.html">{plus}Start broadcasting</a><a class="button" href="#live-streams">View live streams</a></div></div></section>'''
    data=[('Broadcasters','1','2.4% vs last 30 days','imgIcon12.svg','imgCast.svg'),('Broadcast requests' if light else 'Broadcast Request','0','No new requests','imgIcon13.svg','imgNoteAdd1.svg'),('Pending approvals' if light else 'Broadcast Request','0','All caught up' if light else 'No new request','imgIcon14.svg','imgUserGroup02.svg'),('Total streams' if light else 'Streams','12','2.4% vs last 30 days','imgIcon15.svg','imgPlayCircle.svg')]
    cards=[]
    for i,(label,value,note,li,di) in enumerate(data):
        icon=img(li if light else di)
        if light:cards.append(f'<article class="metric"><span class="metric-icon">{icon}</span><div><h3>{label}</h3><strong>{value}</strong><p class="metric-note {"positive" if i in [0,3] else ""}">{note}</p></div></article>')
        else:cards.append(f'<article class="metric"><h3>{label}</h3><div class="metric-body"><div><span class="metric-icon">{icon}</span><strong>{value}</strong></div><p class="metric-note">'+('<span class="positive">↑ 2.4%</span> from last 30 days' if i in [0,3] else note)+'</p></div></article>')
    overview='<section class="dash-overview"><header><h2>Club overview</h2>'+('<p>Here’s what’s happening with your club.</p>' if light else '')+'</header><div class="metric-grid">'+''.join(cards)+'</div></section>'
    range_control=unavailable('Last 30 days','Only the designed last-30-days data is supplied. Other ranges have no source data.','chart-range',img('imgArrowDown01.svg') if not light else '')
    chart_file='8436-7280.svg' if light else '8436-8252.svg'
    chart_intro='<p class="chart-total"><strong>12</strong> Total streams <span>↑ 2.4%</span></p>' if light else '<div class="chart-legend"><span>● Streams</span><p>Updated today</p></div>'
    chart=f'''<section class="dash-card activity"><header><div><h2>Streaming activity</h2><p>Live and completed streams from your club</p></div>{range_control}</header>{chart_intro}<figure class="stream-chart">{asset('dashboard-charts',chart_file,'Streaming activity across four weeks, peaking at approximately twelve streams.')}<figcaption class="sr-only">Sample data copied from Figma; not a live analytics feed.</figcaption></figure>{'<p class="chart-footer">● Streams &nbsp; Updated today</p>' if light else ''}</section>'''
    playback='Playback is blocked: no game-details screen or playable media is supplied. This local preview is not a live stream.'
    if light:
        live=''
        for name,sport,photo in [('EAGLES VS PHOENIX','Hockey','imgImageHockeyGame.png'),('BROWNS VS CLOTS','Volleyball','imgImageVolleyballGame.png')]:
            live+=f'<article class="live-row" data-dashboard-record="{name} {sport}"><div class="live-thumb">{img(photo,name)}<span class="live-label">● LIVE</span></div><div><span class="mini-live">● LIVE</span><h3>{name}</h3><p>{sport} · Club tournament</p><strong class="watching">● 1.2K watching</strong></div>{unavailable('⋮',playback,'live-more')}</article>'
        live_head='<div><h2>Live right now <span>● 2</span></h2><p>Catch the action as it happens</p></div>'
    else:
        live=f'''<article class="featured-live" data-dashboard-record="Eagles vs phoenix hockey">{img('imgMatchCard.png','Hockey match')}<span class="live-label">● LIVE NOW</span><span class="live-team-logos">{img('imgTeamLogo.png')}&nbsp;VS&nbsp;{img('imgTeamLogo1.png')}</span><span class="viewer-count">{img('imgView.svg')}9.8K</span><div><h3>Eagles vs phoenix</h3><p>Hockey · 1.2K Watching</p></div></article><article class="live-row secondary-live" data-dashboard-record="Browns vs clots volleyball"><div><span class="mini-live">● LIVE</span> <strong class="watching">● 1.2K watching</strong><h3>BROWNS VS CLOTS</h3><p>Volleyball · Club tournament</p></div>{unavailable('⋮',playback,'live-more')}</article>'''
        live_head='<h2>Live Streams</h2>'
    live=f'<section class="dash-card live-streams" id="live-streams"><header>{live_head}<a href="../home-signed-in-{theme}/index.html#live-streams">View all</a></header>{live}</section>'
    storage=f'''<section class="dash-card dash-storage"><h2>Storage usage</h2><p>Your club’s recorded streams and files</p><div class="storage-measure"><span class="metric-icon">{img('imgIcon16.svg' if light else 'imgCloudUpload1.svg')}</span><p><strong>320GB</strong> of 1 TB</p><span>32% used</span></div><meter min="0" max="100" value="32">32% used</meter><a class="button" href="../storage-services-{theme}/index.html">{img('imgSettings01.svg') if not light else ''}Manage storage</a></section>'''
    rows=[]
    for i,(name,team,status) in enumerate(zip(['John Carter']*3 if light else ['Koray Okumus','Zahir Mays','Joshua Wilson'],['Riverside FC','Lakeview United','Pinecrest'],['Approved','Pending','Rejected'])):
        avatar='<span class="initial-avatar">JC</span>' if light else img('imgAvatar'+(str(i) if i else '')+'.png','',css='request-avatar')
        rows.append(f'<tr data-dashboard-record="{name} {team} {status}"><td><span class="requester">{avatar}{name}</span></td><td><span class="team-star">✦</span> {team}</td><td>Wed 1:00 PM</td><td><span class="request-status {status.lower()}">{status}</span></td></tr>')
    requests=f'''<section class="dash-card dash-requests"><header><div><h2>Recent broadcast requests</h2><p>Review the latest requests from your club</p></div><a href="../broadcaster-requests-{theme}/index.html">View all</a></header><table><caption class="sr-only">Recent broadcast requests</caption><thead><tr><th>Requester</th><th>Team</th><th>Requested on</th><th>Status</th></tr></thead><tbody>{''.join(rows)}</tbody></table></section>'''
    footer='<footer class="dash-footer"><span>JWV Streaming · Club Dashboard</span><span>Concept redesign · Light / Dark theme</span></footer>'
    document(f,'Club Dashboard',f'<div class="dashboard-shell">{dashboard_sidebar(theme)}<main id="main" class="dashboard-main">{header}{hero}{overview}<div class="dashboard-upper">{chart}{live}</div><div class="dashboard-lower">{storage}{requests}</div>{footer}</main></div>',body_class='dashboard-page '+theme,node='8436:7027' if light else '8436:7470',extra_css='<link rel="stylesheet" href="../shared/dashboard.css">')

if __name__=='__main__':
    dashboard('dark')
    dashboard('light')
