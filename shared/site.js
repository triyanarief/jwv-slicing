'use strict';

// The source library uses literal placeholder copy; no help instructions are invented.
const tooltipTriggers = [...document.querySelectorAll('[data-tooltip]')];
if (tooltipTriggers.length) {
  const tooltip = document.createElement('span');
  tooltip.id = 'source-tooltip';
  tooltip.className = 'source-tooltip';
  tooltip.role = 'tooltip';
  tooltip.hidden = true;
  document.body.append(tooltip);
  let owner = null;
  let originalIcon = null;
  let hideTimer;
  const hide = () => {
    clearTimeout(hideTimer);
    tooltip.hidden = true;
    if (originalIcon && owner) owner.querySelector('img').src = originalIcon;
    originalIcon = null;
    owner?.removeAttribute('aria-describedby');
    owner = null;
  };
  const show = trigger => {
    hide();
    owner = trigger;
    if (trigger.classList.contains('help-tooltip')) {
      originalIcon = trigger.querySelector('img').getAttribute('src');
      trigger.querySelector('img').src = '../shared/assets/component-states/help-hover.svg';
    }
    tooltip.textContent = trigger.dataset.tooltip;
    tooltip.hidden = false;
    trigger.setAttribute('aria-describedby', tooltip.id);
    const rect = trigger.getBoundingClientRect();
    const left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 - .5;
    tooltip.style.left = Math.max(8, Math.min(left, innerWidth - tooltip.offsetWidth - 8)) + 'px';
    tooltip.style.top = Math.max(8, rect.top - tooltip.offsetHeight - 4) + 'px';
  };
  const scheduleHide = () => { hideTimer = setTimeout(hide, 100); };
  tooltipTriggers.forEach(trigger => {
    trigger.addEventListener('pointerenter', () => show(trigger));
    trigger.addEventListener('pointerleave', scheduleHide);
    trigger.addEventListener('focus', () => show(trigger));
    trigger.addEventListener('blur', hide);
  });
  tooltip.addEventListener('pointerenter', () => clearTimeout(hideTimer));
  tooltip.addEventListener('pointerleave', scheduleHide);
  document.addEventListener('keydown', event => { if (event.key === 'Escape') hide(); });
  window.addEventListener('resize', hide);
  window.addEventListener('scroll', hide, true);
}

document.querySelector('[data-preview-fullscreen]')?.addEventListener('click', async () => {
  const preview = document.querySelector('.broadcast-showcase');
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await preview.requestFullscreen();
  } catch {
    window.alert('This browser cannot expand the static preview. No stream has started.');
  }
});

document.querySelector('[data-dashboard-search]')?.addEventListener('input', event => {
  const query = event.target.value.trim().toLowerCase();
  document.querySelectorAll('[data-dashboard-record]').forEach(item => {
    item.hidden = !item.dataset.dashboardRecord.toLowerCase().includes(query);
  });
});

const homeMenu = document.querySelector('[data-home-menu]');
homeMenu?.addEventListener('click', () => {
  const open = document.querySelector('.home-header').toggleAttribute('data-open');
  homeMenu.setAttribute('aria-expanded', String(open));
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && homeMenu) {
    const header = document.querySelector('.home-header');
    const wasOpen = header.hasAttribute('data-open');
    header.removeAttribute('data-open');
    homeMenu.setAttribute('aria-expanded', 'false');
    if (wasOpen) homeMenu.focus();
  }
});
const carouselUpdates = [];
document.querySelectorAll('[data-scroll]').forEach(button => {
  const track = document.getElementById(button.dataset.track);
  const update = () => {
    const atStart = track.scrollLeft <= 1;
    const atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 1;
    button.disabled = Number(button.dataset.scroll) < 0 ? atStart : atEnd;
  };
  button.addEventListener('click', () => track.scrollBy({left: Number(button.dataset.scroll) * track.clientWidth * .8, behavior: 'smooth'}));
  track.addEventListener('scroll', update, {passive:true});
  window.addEventListener('resize', update);
  carouselUpdates.push(update);
  update();
});
document.querySelector('[data-home-search]')?.addEventListener('input', event => {
  const query = event.target.value.trim().toLowerCase();
  const items = [...document.querySelectorAll('[data-home-item]')];
  items.forEach(item => { item.hidden = !item.dataset.homeItem.toLowerCase().includes(query); });
  document.querySelectorAll('[data-home-empty]').forEach(node => { node.hidden = items.some(item => !item.hidden); });
  // Filtering changes scrollable width even when the scroll position stays still.
  requestAnimationFrame(() => carouselUpdates.forEach(update => update()));
});

document.querySelector('[data-density]')?.addEventListener('change', event => {
  document.querySelector('.admin-table-box').toggleAttribute('data-dense', event.target.checked);
});

// Every backend-dependent action stays local and states its boundary explicitly.
document.querySelectorAll('[data-unavailable]').forEach(button => {
  button.addEventListener('click', event => {
    event.preventDefault();
    window.alert(button.dataset.unavailable);
  });
});

const navigationButton = document.querySelector('[data-navigation-toggle]');
navigationButton?.addEventListener('click', () => {
  const sidebar = document.querySelector('.sidebar');
  const open = sidebar.toggleAttribute('data-open');
  navigationButton.setAttribute('aria-expanded', String(open));
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && document.querySelector('.sidebar[data-open]')) {
    document.querySelector('.sidebar').removeAttribute('data-open');
    navigationButton.setAttribute('aria-expanded', 'false');
    navigationButton.focus();
  }
});

const search = document.querySelector('[data-team-search]');
const age = document.querySelector('[data-age-filter]');
const rows = [...document.querySelectorAll('[data-team]')];
function filterTeams() {
  const query = search.value.trim().toLocaleLowerCase();
  let visible = 0;
  rows.forEach(row => {
    const match = row.dataset.team.toLocaleLowerCase().includes(query)
      && (!age.value || row.dataset.age === age.value);
    row.hidden = !match;
    if (match) visible++;
  });
  document.querySelectorAll('[data-result-count]').forEach(node => {
    node.textContent = `${visible} ${visible === 1 ? 'team' : 'teams'}`;
  });
  const footer = document.querySelector('[data-table-count]');
  if (footer) footer.textContent = `Showing ${visible} of ${rows.length} teams`;
  document.querySelector('[data-no-results]').hidden = visible !== 0;
  document.querySelectorAll('[data-view-link]').forEach(link => {
    const url = new URL(link.href);
    if (query) url.searchParams.set('search', search.value); else url.searchParams.delete('search');
    if (age.value) url.searchParams.set('age', age.value); else url.searchParams.delete('age');
    link.href = `${url.pathname}${url.search}`;
  });
}
if (search && age) {
  const params = new URLSearchParams(location.search);
  search.value = params.get('search') || '';
  age.value = params.get('age') || '';
  search.addEventListener('input', filterTeams);
  age.addEventListener('change', filterTeams);
  filterTeams();
}

document.querySelectorAll('[data-password-toggle]').forEach(button => {
  button.addEventListener('click', () => {
    const input = document.getElementById(button.dataset.passwordToggle);
    const visible = input.type === 'password';
    input.type = visible ? 'text' : 'password';
    button.setAttribute('aria-pressed', String(visible));
    const label = document.querySelector(`label[for="${input.id}"]`).textContent.toLowerCase();
    button.setAttribute('aria-label', `${visible ? 'Hide' : 'Show'} ${label}`);
  });
});
const authForm = document.querySelector('[data-local-auth]');
if (authForm) {
  const confirm = authForm.elements.namedItem('confirm-password');
  const password = authForm.elements.namedItem('password');
  function validateConfirmation() {
    if (confirm) confirm.setCustomValidity(confirm.value !== password.value ? 'Passwords must match.' : '');
  }
  password.addEventListener('input', validateConfirmation);
  confirm?.addEventListener('input', validateConfirmation);
  authForm.addEventListener('submit', event => {
    event.preventDefault();
    validateConfirmation();
    if (!authForm.reportValidity()) return;
    const status = document.querySelector('[data-auth-status]');
    status.hidden = false;
    status.textContent = 'Local preview only. No account was created or signed in, and no information was sent or stored.';
    password.value = '';
    if (confirm) confirm.value = '';
  });
}
// Search the single source-provided broadcaster without inventing account data.
document.querySelector('[data-wallet-search]')?.addEventListener('input', event => {
  const query = event.target.value.trim().toLowerCase();
  const row = document.querySelector('[data-wallet-record]');
  const visible = row.dataset.walletRecord.toLowerCase().includes(query);
  row.hidden = !visible;
  document.querySelector('[data-wallet-empty]').hidden = visible;
  document.querySelector('[data-wallet-count]').textContent = visible ? '1 broadcaster' : '0 broadcasters';
  document.querySelector('[data-wallet-summary]').textContent = `Showing ${visible ? 1 : 0} of 1 broadcasters`;
});
