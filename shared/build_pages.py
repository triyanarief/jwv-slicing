"""Generate semantic static pages from shared markup; no runtime dependencies."""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

def asset(folder, name, alt='', css=''):
    path = ROOT / 'shared/assets' / folder / name
    assert path.is_file(), path
    dimensions = ''
    if path.suffix == '.svg':
        root = re.search(r'<svg[^>]+>', path.read_text()).group()
        dimensions = ' '.join(f'{key}="{value}"' for key, value in re.findall(r'\b(width|height)="([^\"]+)"', root))
    return f'<img src="../shared/assets/{folder}/{name}" alt="{escape(alt)}" class="{css}" {dimensions}>'

def unavailable(label, reason, css='button', icon=''):
    hint = 'data-tooltip="Tooltip"' if css == 'legacy-icon' else f'title="{escape(reason, quote=True)}"'
    return f'<button type="button" class="{css}" aria-disabled="true" data-unavailable="{escape(reason, quote=True)}" {hint}>{icon}{escape(label)}</button>'

def brand(folder):
    return f'''<a class="brand" href="../index.html" aria-label="JWV Streaming — page directory">
      <span class="brand-mark">{asset(folder,'imgCurvedHighlight.svg')}JWV</span>
      <span class="brand-copy"><span class="brand-title">STREAMING{asset(folder,'imgPlayEmblem.svg')}</span><small>POWERED BY JWV DEV</small></span>
    </a>'''

NAV = [
    ('Dashboard','club-dashboard-dark','imgMenuSquare.svg'),
    ('Teams List','teams-list','imgUserGroup02.svg'),
    ('Broadcasters & Wallet','broadcasters-wallets','imgWallet01.svg'),
    ('Broadcaster Request','broadcaster-requests-dark','imgNoteAdd.svg'),
    ('Rejected Broadcasters','rejected-broadcasters-dark','imgCancelCircle.svg'),
    ('Authorize YouTube Channel','youtube-channel-dark','imgYoutube.svg'),
    ('Storage Services','storage-services-dark','imgCloudUpload.svg'),
    ('Transaction History','transaction-history-dark','imgReceiptText.svg'),
]

def sidebar(folder, active):
    sections=[]
    for heading, items in [('WORKSPACE',NAV[:5]),('STREAMING TOOLS',NAV[5:])]:
        links=[]
        for label, slug, icon in items:
            current=' aria-current="page"' if slug == active else ''
            # Pending destinations are labelled honestly until their pages exist.
            if (ROOT/slug/'index.html').exists() or slug==active:
                links.append(f'<a class="nav-link" href="../{slug}/index.html"{current}>{asset(folder,icon)}{escape(label)}</a>')
            else:
                links.append(unavailable(label,f'{label}: source reconciliation and implementation are pending. No destination is available yet.','nav-link',asset(folder,icon)))
        sections.append(f'<div class="nav-group"><p class="nav-heading">{heading}</p>'+''.join(links)+'</div>')
    return f'''<aside class="sidebar"><div class="sidebar-header">{brand(folder)}<button class="button mobile-navigation" type="button" data-navigation-toggle aria-controls="workspace-nav" aria-expanded="false">Menu</button></div>
    <nav id="workspace-nav" class="side-nav" aria-label="Workspace">{''.join(sections)}</nav></aside>'''

def document(slug, title, content, body_class='', node='', extra_css=''):
    folder=ROOT/slug;folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="dark light"><link rel="icon" href="data:,"><title>{escape(title)} — JWV Streaming</title><link rel="stylesheet" href="../shared/site.css">{extra_css}<script defer src="../shared/site.js"></script></head>
<body class="{body_class}" data-figma-node="{node}"><a class="skip-link" href="#main">Skip to content</a>{content}</body></html>\n''')

TEAMS=[('Eastwood Falcons','10U','imgContainer.png','imgIcon4.svg'),('Westbrook Eagles','12U','imgContainer1.png','imgIcon6.svg'),('Northfield Wolves','14U','imgContainer2.png','imgIcon7.svg'),('Southridge Titans','16U','imgContainer3.png','imgIcon8.svg')]

def teams(grid):
    slug='teams-grid' if grid else 'teams-list'; f=slug
    crests=''.join('<span>'+asset(f,'imgIcon'+(str(i) if i else '')+'.svg')+'</span>' for i in range(4))
    heading=f'''<header class="page-heading"><div><p class="eyebrow">CLUB MANAGEMENT / TEAMS</p><h1>Team List</h1><p class="description">Manage your club's teams and access their details.</p></div>{unavailable('Add Team','Add Team is blocked: no add-team screen or form is designed in Design Ready.','button button-primary',asset(f,'imgPlus.svg'))}</header>
    <section class="directory-banner" aria-label="Team directory"><div><p class="eyebrow">JWV / TEAM DIRECTORY</p><h2>Every team. One home.</h2><p class="description">Your club lineup, organized and ready for game day.</p></div><div class="directory-summary"><div class="crest-stack" aria-hidden="true">{crests}</div><p class="team-total"><strong>04</strong>Club teams</p></div></section>'''
    views=''.join(f'<a href="../{s}/index.html" aria-label="{label}" data-view-link'+(' aria-current="page"' if s==slug else '')+'>'+asset(f,icon)+'</a>' for s,label,icon in [('teams-list','List view','imgList.svg'),('teams-grid','Grid view','imgMenuSquare1.svg')])
    toolbar=f'''<div class="toolbar"><p class="toolbar-title">Your teams <span class="pill" data-result-count aria-live="polite">4 teams</span></p><div class="toolbar-controls"><label class="search-field">{asset(f,'imgSearchLg.svg')}<span class="sr-only">Search teams or ID</span><input type="search" placeholder="Search teams or ID..." data-team-search></label><label class="select-wrap"><span class="sr-only">Age group</span><select data-age-filter><option value="">All age groups</option>{''.join(f'<option>{age}</option>' for _,age,_,_ in TEAMS)}</select>{asset(f,'imgArrowDown01.svg')}</label><nav class="view-switch" aria-label="Team display">{views}</nav></div></div>'''
    items=[]
    for i,(name,age,photo,crest) in enumerate(TEAMS):
        attrs=f'data-team="{name} #15189" data-age="{age}"'
        management=unavailable('Manage team',f'{name}: a manage-team screen is not present in the supplied design. No team data has changed.','button button-primary button-small')
        more=unavailable('',f'{name}: the team actions menu has no supplied design.','icon-button',asset(f,'imgIcon5.svg')).replace('<button ','<button aria-label="More actions for '+name+'" ',1)
        if grid:
            items.append(f'''<article class="team-card" {attrs}><div class="team-photo">{asset(f,photo,name+' team photo')}<span class="team-crest">{asset(f,crest)}</span></div><div class="team-card-body"><h3>{name}</h3><div class="team-meta"><span>Team ID #15189</span><span class="pill age-pill">{age}</span></div><div class="team-actions">{management}{more}</div></div></article>''')
        else:
            # The list source uses the corresponding crest at 41.222 x 42.778.
            items.append(f'''<tr class="team-row" {attrs}><td><div class="team-cell"><span class="team-crest">{asset(f,crest)}</span><div><h3>{name}</h3><p>Youth division</p></div></div></td><td>#15189</td><td><span class="pill age-pill">{age}</span></td><td><div class="team-actions">{management}{more}</div></td></tr>''')
    if grid: content='<section class="team-grid" aria-label="Club teams">'+''.join(items)+'</section>'
    else:
        content='''<div class="data-table-wrap"><table class="data-table"><caption class="sr-only">Club teams</caption><thead><tr><th scope="col">TEAM</th><th scope="col">TEAM ID</th><th scope="col">AGE GROUP</th><th scope="col">ACTION</th></tr></thead><tbody>'''+''.join(items)+f'''</tbody></table><div class="table-footer"><span data-table-count>Showing 4 of 4 teams</span><div class="pagination"><label>Rows per page <select aria-label="Rows per page"><option>10</option><option>20</option><option>50</option></select></label><span class="page-number" aria-current="page">1</span><span class="pagination-placeholder">...</span><span class="unavailable-page pagination-placeholder" title="Only four teams are supplied; page 3 has no data.">3</span>{unavailable('','Only four teams are supplied. There is no next page of team data.','icon-button',asset(f,'imgChevronRight.svg')).replace('<button ','<button aria-label="Next page unavailable" ',1)}</div></div></div>'''
    content+='<p class="no-results" data-no-results hidden role="status">No teams match your search.</p>'
    document(slug,'Team List',f'<div class="app-shell">{sidebar(f,"teams-list")}<main id="main" class="workspace"><div class="page-panel">{heading}{toolbar}{content}</div></main></div>',node='8439:10585' if grid else '8438:9957')

AUTH_FRAMES={('login','dark'):'8350:8841',('register-user','dark'):'8354:27846',('register-broadcaster','dark'):'8354:28283',('login','light'):'8433:5384',('register-user','light'):'8433:5555',('register-broadcaster','light'):'8433:5766'}

def auth(kind, theme):
    slug=f'{kind}-{theme}'; registering=kind!='login'; broadcaster=kind=='register-broadcaster'
    other='light' if theme=='dark' else 'dark'
    theme_link=f'<a class="theme-link" href="../{kind}-{other}/index.html" aria-label="Switch to {other} theme"><span class="theme-track" aria-hidden="true"></span>Dark</a>'
    background='imgLogIn.png' if theme=='light' or kind=='login' else ('imgRegisterAsBroadcaster.png' if broadcaster else 'imgRegisterAsUser.png')
    home=f'<a class="back-home" href="../home-{theme}/index.html">'+asset(slug,'imgArrowLeft02.svg')+'Back to home</a>'
    header=f'<header class="auth-header">{brand(slug)}<div class="auth-header-actions">{theme_link}{home}</div></header>'
    def field(label, name, placeholder, input_type='text', autocomplete='off'):
        suffix=''
        if input_type=='password':suffix=f'<button type="button" class="password-toggle" data-password-toggle="{name}" data-tooltip="This is a tooltip" aria-label="Show {label.lower()}" aria-pressed="false">{asset(slug,"imgHelpIcon.svg")}</button>'
        return f'<div class="field"><label for="{name}">{label}</label><div class="input-control"><input id="{name}" name="{name}" type="{input_type}" placeholder="{placeholder}" autocomplete="{autocomplete}" required>{suffix}</div></div>'
    fields=[]
    if registering:
        first=('Channel Name','channel','Enter channel name') if broadcaster else ('First Name','first-name','Enter your first name')
        last=('Username','username','Enter username') if broadcaster else ('Last Name','last-name','Enter your last name')
        fields.append('<div class="field-pair">'+field(*first)+field(*last)+'</div>')
        if broadcaster:
            fields.append(f'<div class="field"><label for="club">Club Association</label><div class="input-control"><select id="club" name="club" class="auth-select" aria-describedby="club-note"><option>Individual Broadcaster (No Club)</option></select>{asset(slug,"imgChevronDown.svg")}</div><span class="sr-only" id="club-note">Only the designed individual broadcaster option is available. Club membership data is not connected.</span></div>')
    fields.append(field('Email Address','email','Enter your email address','email','email'))
    if registering:
        fields.append(f'<div class="field"><label for="phone">Phone number</label><div class="input-control"><span class="phone-prefix">US {asset(slug,"imgChevronDown1.svg" if broadcaster else "imgChevronDown.svg")}</span><input type="tel" id="phone" name="phone" placeholder="+1 (555) 000-0000" autocomplete="tel" required><button type="button" class="help-tooltip" data-tooltip="This is a tooltip" aria-label="Phone number help">{asset(slug,"imgOpenFalseSupportingTextFalseTooltipTopNoArrow.svg")}</button></div></div>')
    fields.append(field('Create Password' if registering else 'Password','password','Enter password','password','new-password' if registering else 'current-password'))
    if registering:fields.append(field('Confirm Password','confirm-password','Enter password','password','new-password'))
    tabs=''
    if registering:
        tabs='<nav class="auth-tabs" aria-label="Registration type">'+''.join(f'<a href="../{role}-{theme}/index.html"'+(' aria-current="page"' if role==kind else '')+'>'+label+'</a>' for role,label in [('register-user','Register as User'),('register-broadcaster','Register as Broadcaster')])+'</nav>'
    title='Join JWV Streaming' if registering else 'Sign in to JWV Streaming'
    intro='Create an account to start watching and streaming.' if registering else 'Welcome back! Please enter your details below.'
    footer=f'Already have an account? <a href="../login-{theme}/index.html">Log in</a>' if registering else f'Don’t have an account? <a href="../register-user-{theme}/index.html">Sign up</a>'
    forgot=unavailable('Forgot password','Password recovery is blocked: no recovery screen or backend is supplied. No email has been sent.','text-button')
    card=f'''<section class="auth-card" aria-labelledby="auth-title"><h1 id="auth-title">{title}</h1><p class="auth-intro">{intro}</p>{tabs}
    <form data-local-auth autocomplete="off"><div class="auth-fields">{''.join(fields)}</div><div class="auth-options"><label class="remember"><input type="checkbox" name="remember">Remember for 30 days</label>{forgot}</div><button class="auth-submit" type="submit">Sign in</button><p class="auth-status" role="status" data-auth-status hidden></p></form><p class="auth-footer">{footer}</p></section>'''
    bottom=f'<div class="auth-bottom-theme">{theme_link}</div>' if kind=='login' and theme=='dark' else ''
    document(slug,title,f'<div class="auth-backdrop" aria-hidden="true">{asset(slug,background)}</div>{header}<main class="auth-main" id="main">{card}</main>{bottom}',body_class='auth-page '+theme+(' register-page' if registering else '')+(' broadcaster' if broadcaster else ''),node=AUTH_FRAMES[(kind,theme)],extra_css='<link rel="stylesheet" href="../shared/auth.css">')

def directory():
    entries=[]
    for page in sorted(ROOT.glob('*/index.html')):
        if page.parent.name.startswith('.'):continue
        markup=page.read_text()
        node=re.search(r'data-figma-node="([^"]+)"',markup)
        if node:entries.append((page.parent.name,page.parent.name.replace('-', ' ').title(),node.group(1)))
    links=''.join(f'<li><a href="{slug}/index.html">{title}<small>Figma {node} · implemented · QA reviewed · source blockers remain</small></a></li>' for slug,title,node in entries)
    (ROOT/'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"><title>JWV — local page directory</title><link rel="stylesheet" href="shared/site.css"></head><body><main class="directory-index"><h1>JWV Streaming</h1><p>Local implementation review. Screens below are drafts, not accepted delivery. Backend services are not connected.</p><ul>{links}</ul><p>Full coverage, design blockers and QA results: <a href="docs/status/tracker.md">coverage tracker</a>.</p></main></body></html>\n''')

if __name__=='__main__':
    teams(False)
    teams(True)
    teams(False)
    for kind,theme in AUTH_FRAMES:
        auth(kind,theme)
    directory()
