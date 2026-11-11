"""Author static admin variants from their inspected Design Ready frames."""
from pathlib import Path
import json
from build_pages import ROOT, asset, brand, document, unavailable, NAV

FRAMES = json.loads((ROOT/'docs/source/admin-frame-map.json').read_text())

def sidebar(slug):
    theme=slug.rsplit('-',1)[1]
    active=slug.replace('-empty','')
    links=[]
    for label,dest,icon in NAV:
        if dest.endswith('-dark'):dest=dest[:-4]+theme
        if dest=='teams-list' and theme=='light':dest='teams-list-light'
        if dest=='broadcasters-wallets' and theme=='light':dest='broadcasters-wallets-light'
        if icon=='imgUserGroup02.svg' and (slug=='club-dashboard-dark' or not (ROOT/'shared/assets'/slug/icon).exists()):icon='imgUserGroup.svg'
        if icon=='imgCancelCircle.svg' and not (ROOT/'shared/assets'/slug/icon).exists():icon='imgCircleX.svg'
        if icon=='imgReceiptText.svg' and not (ROOT/'shared/assets'/slug/icon).exists():icon='imgInvoice01.svg'
        contents=asset(slug,icon)+label
        if (ROOT/dest/'index.html').exists() or dest in FRAMES.values():
            current=' aria-current="page"' if active==dest else ''
            links.append(f'<a class="nav-link" href="../{dest}/index.html"{current}>{contents}</a>')
        else:links.append(unavailable(label,label+': source reconciliation and implementation pending.','nav-link',asset(slug,icon)))
    other=slug[:-4]+'light' if theme=='dark' else slug[:-5]+'dark'
    if slug=='teams-list-light':other='teams-list'
    if slug=='broadcasters-wallets-light':other='broadcasters-wallets'
    theme_control=f'<a class="theme-link admin-theme" href="../{other}/index.html" aria-label="Switch theme"><span class="theme-track" aria-hidden="true"></span>Dark Mode</a>'
    if slug=='broadcasters-wallets-light' and not (ROOT/other/'index.html').exists():
        theme_control=unavailable('Dark Mode','Dark wallet redesign is waiting for WIP approval clarification.','theme-link admin-theme','<span class="theme-track" aria-hidden="true"></span>')
    return f'''<aside class="sidebar"><div class="sidebar-header">{brand(slug)}<button type="button" class="button mobile-navigation" data-navigation-toggle aria-controls="workspace-nav" aria-expanded="false">Menu</button></div><nav class="side-nav" id="workspace-nav" aria-label="Workspace">{''.join(links)}</nav>{theme_control}</aside>'''

def empty_art(slug):
    return '<div class="empty-art" aria-hidden="true">'+''.join(asset(slug,'imgVector'+(str(i) if i else '')+'.svg',css='empty-vector v'+str(i)) for i in range(5))+asset(slug,'imgGroup.svg',css='empty-symbol')+'</div>'

def table_page(slug):
    transaction=slug.startswith('transaction');rejected=slug.startswith('rejected');empty='-empty-' in slug or transaction
    title='Transaction History' if transaction else ('Rejected Broadcasters' if rejected else 'Broadcaster Requests')
    desc="View and track your club’s streaming time purchases, credit transfers, and wallet transactions." if transaction else 'Review and manage broadcaster requests to join your club.'
    if rejected:desc='View and track broadcaster requests that were declined.'
    status='Rejected' if rejected else 'Pending'
    badge=('0' if empty else '2')+(' Transactions' if transaction else (' Rejected' if rejected else ' Pending Requests'))
    headers=['Date','Cart ID','Amount','Status','Receipt'] if transaction else ['ID','Channel Name','Username','Email Id']+(['Requested on'] if not empty or rejected and slug.endswith('light') else [])+['Status']
    content='<div class="admin-table-box"><table class="admin-table '+('transaction-table' if transaction else 'requests-table')+'"><caption class="sr-only">'+title+'</caption><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in headers)+'</tr></thead><tbody>'
    if not empty:
        for name,user,email in [('Riverside Hawks Live','hawks10u_live','hawks10u@example.com'),('Lakeview Titans TV','titans12u_tv','titans12u@example.com')]:
            values=['15189',name,user,email,'Wed 1:00pm',f'<span class="status-badge {status.lower()}">{status}</span>']
            content+='<tr>'+''.join(f'<td data-label="{h}">{v}</td>' for h,v in zip(headers,values))+'</tr>'
    content+='</tbody></table>'
    if empty:
        empty_title='No Transactions Yet' if transaction else ('No Rejected Broadcasters' if rejected else 'No Pending Requests')
        empty_desc="Your club's transactions will appear here once you make a purchase or transfer credits." if transaction else ('New Rejected Broadcasters will appear here when submitted.' if rejected else 'New broadcaster requests will appear here when submitted.')
        content+=f'<div class="empty-state">{empty_art(slug)}<div><h2>{empty_title}</h2><p>{empty_desc}</p></div></div>'
    else:
        content+=f'''<div class="admin-pagination"><label class="density-control"><input type="checkbox" data-density><span aria-hidden="true"></span>Dense</label><div class="pagination"><label>Rows per page <select aria-label="Rows per page"><option>10</option><option>20</option><option>50</option></select></label><span class="page-number" aria-current="page">1</span><span class="pagination-placeholder">...</span><span class="pagination-placeholder" title="Only two rows are supplied; page 3 has no data.">3</span>{unavailable('','Only two rows are supplied. There is no next page of data.','icon-button',asset(slug,'imgChevronRight.svg')).replace('<button ','<button aria-label="Next page unavailable" ',1)}</div></div>'''
    return title,desc,badge,content+'</div>'

def youtube(slug):
    summary='Your YouTube channel is verified and ready to receive stream recordings automatically.'
    stats=''.join(f'<div class="connection-stat"><span>{asset(slug,icon) if icon else ""}{label}</span><strong>{asset(slug,"imgCheckmarkCircle3.svg") if label!="Last Sync" else ""}{value}</strong></div>' for label,value,icon in [('Status','Verified',''),('Autosave','Enabled','imgDownload04.svg'),('Last Sync','Today','imgHistory.svg')])
    reason='Local source-state preview only. No YouTube account is connected. The authorization and channel-management flow is not supplied.'
    controls=unavailable('Manage Channel',reason,'button button-primary')+unavailable('Unlink Channel',reason,'button',asset(slug,'imgUnlink04.svg'))
    content=f'''<section class="youtube-card" aria-label="Designed YouTube connection state"><div class="youtube-emblem"><span class="featured-icon">{asset(slug,'imgCheckmarkCircle02.svg')}</span><div class="youtube-logo">{asset(slug,'imgG7433.svg')}{asset(slug,'imgG7449.svg')}</div></div><div class="youtube-copy"><h2>YouTube connected successfully</h2><p>{summary}</p></div><div class="connection-stats">{stats}</div><hr class="connection-divider"><div class="connected-channel"><p>{asset(slug,'imgYoutube1.svg')}Connected Channel: <strong>JVW Straming</strong></p><div class="connection-actions">{controls}</div></div><p class="connection-note">{asset(slug,'imgInfo.svg')}New broadcast can be saved to Youtuber automatically after streaming</p></section><p class="preview-boundary">Sample connection state from Figma. No account is connected in this local preview.</p>'''
    return 'Authorize YouTube Channel','Connect your club’s YouTube channel to enable automatic saving and publishing for your streams.','',content

def storage(slug):
    reason='Local source-state preview only. No storage account is connected and no files are uploaded. The account authorization flow is not supplied.'
    content=f'''<section class="storage-summary">{asset(slug,'imgCheckmarkCircle02.svg')}<div><h2>1 of 3 services connected</h2><p>Completed broadcasts will be uploaded to your linked storage accounts.</p></div></section><div class="storage-grid">'''
    for i,(name,icon) in enumerate([('Google Drive','imgFi2504719.svg'),('OneDrive','imgFrame.svg'),('Dropbox','imgX346Dropbox.svg')]):
        content+=f'''<section class="storage-card"><header><div class="storage-logo">{asset(slug,icon)}</div><div><h2>{name}</h2><p>Upload completed broadcasts to {name}.</p></div></header><p class="storage-state {'linked' if i==0 else ''}">{asset(slug,'imgLink04.svg') if i==0 else ''}{'Linked' if i==0 else 'Not linked'}</p>'''
        if i==0:
            content+=f'''<div class="storage-body"><div class="account-info"><div class="account-person">{asset(slug,'imgUser.svg')}<div><strong>JWV Development</strong><p>jwvplayconsole@gmail.com</p></div>{asset(slug,'imgShare04.svg')}</div><p class="linked-date">{asset(slug,'imgCalendar04.svg')}Linked on Oct 22, 2026, 12:32 AM</p></div></div><div class="storage-actions">{unavailable('Change Account',reason,'button button-blue')}{unavailable('Unlink',reason,'button',asset(slug,'imgUnlink04.svg'))}</div>'''
        else:
            content+=f'''<div class="storage-body storage-empty">{asset(slug,'imgCloudUpload1.svg')}<h3>Connect your {name}</h3><p>Link your account to automatically store completed broadcasts.</p></div><div class="storage-actions">{unavailable('Link Account',reason,'button button-primary')}</div>'''
        content+='</section>'
    content+='</div><p class="preview-boundary">Sample connection states from Figma. No storage accounts are connected in this local preview.</p>'
    return 'Storage Services','Link the club accounts that should receive completed broadcasts.<br>Broadcasters in this club use these connections.','',content

def build():
    for node,slug in FRAMES.items():
        title,desc,badge,content=youtube(slug) if slug.startswith('youtube') else storage(slug) if slug.startswith('storage') else table_page(slug)
        heading=f'<header class="admin-heading"><div><h1>{title}</h1><p>{desc}</p></div>'+ (f'<span class="admin-count">{badge}</span>' if badge else '')+'</header>'
        document(slug,title,f'<div class="admin-shell">{sidebar(slug)}<main id="main" class="admin-panel">{heading}{content}</main></div>',body_class='admin-page '+slug.rsplit('-',1)[1],node=node,extra_css='<link rel="stylesheet" href="../shared/admin.css">')

def build_light_variants():
    for slug,node in [('teams-list-light','8427:691'),('broadcasters-wallets-light','8427:846')]:
        teams=slug.startswith('teams');title='Team List' if teams else 'Broadcasters & Wallets'
        desc="Manage your club's teams and access their details." if teams else "Manage your club's broadcasters, streaming time, and wallet balances in one place."
        add=unavailable('Add Teams','The add-team form is not designed. No team has been created.','button button-primary',asset(slug,'imgPlus.svg')) if teams else ''
        heading=f'<header class="admin-heading"><div><h1>{title}</h1><p>{desc}</p></div>{add}</header>'
        content=''
        if not teams:
            content=f'''<section class="wallet-summary"><div><span class="wallet-cast">{asset(slug,'imgCast.svg')}</span><div><p>Streaming time</p><h2>0 minutes</h2><p class="wallet-rate"><strong>$0.00</strong> available to transfer&nbsp; · &nbsp;<b>$4.80</b> per hour</p></div></div>{unavailable('Add streaming time','Payment and streaming-time purchase designs are not supplied. No payment has been made.','button button-primary',asset(slug,'imgPlus.svg'))}</section>'''
        heads=['Teams ID','Team Name',''] if teams else ['Id','Channel Name','Email Id','Wallet Balance','Status','Action','Transfer Credits','']
        content+='<div class="admin-table-box"><table class="admin-table legacy-table '+('legacy-teams' if teams else 'legacy-wallet')+'"><caption class="sr-only">'+title+'</caption><thead><tr>'+''.join('<th scope="col">'+(h or '<span class="sr-only">Actions</span>')+'</th>' for h in heads)+'</tr></thead><tbody>'
        if teams:
            for name in ['Eastwood Falcons 10U','Westbrook Eagles 12U','Northfield Wolves 14U','Southridge Titans 16U']:
                actions=''.join(unavailable('',label+' team has no supplied interaction or confirmation design. No team has changed.','legacy-icon',asset(slug,icon)).replace('<button ','<button aria-label="'+label+' '+name+' unavailable" ',1) for label,icon in [('Delete','imgTrash01.svg'),('Edit','imgEdit01.svg')])
                content+=f'<tr><td data-label="Teams ID">15189</td><td data-label="Team Name">{name}</td><td data-label="Actions"><div class="legacy-actions">{actions}</div></td></tr>'
        else:
            action=unavailable('Approve','Broadcaster status options and confirmation are not supplied. No permission has changed.','legacy-select',asset(slug,'imgChevronDown.svg'))
            transfer=unavailable('Transfer','Transfer credits dialog and payment integration are not supplied. No credits have moved.','legacy-transfer',asset(slug,'imgDot1.svg'))
            edit=unavailable('','Broadcaster edit form is not supplied. No account has changed.','legacy-icon',asset(slug,'imgEdit01.svg')).replace('<button ','<button aria-label="Edit broadcaster unavailable" ',1)
            values=['15189','Test Club Broadcaster','testclubbroadcast@jwvstreaming.com','$4.50','<span class="wallet-allowed">'+asset(slug,'imgDot.svg')+'Allowed</span>',action,transfer,edit]
            content+='<tr>'+''.join(f'<td data-label="{h}">{v}</td>' for h,v in zip(heads,values))+'</tr>'
        content+=f'''</tbody></table><div class="admin-pagination"><label class="density-control"><input type="checkbox" data-density><span aria-hidden="true"></span>Dense</label><div class="pagination"><label>Rows per page <select aria-label="Rows per page"><option>10</option><option>20</option><option>50</option></select></label><span class="page-number" aria-current="page">1</span><span class="pagination-placeholder">...</span><span class="pagination-placeholder" title="Additional page data is not supplied">3</span>{unavailable('','No additional rows are supplied.','icon-button',asset(slug,'imgChevronRight.svg')).replace('<button ','<button aria-label="Next page unavailable" ',1)}</div></div></div>'''
        document(slug,title,f'<div class="admin-shell">{sidebar(slug)}<main id="main" class="admin-panel">{heading}{content}</main></div>',body_class='admin-page light',node=node,extra_css='<link rel="stylesheet" href="../shared/admin.css">')

if __name__=='__main__':
    build_light_variants()
    build()
