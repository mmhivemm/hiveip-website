/* Hive IP — main.js
   Minimal progressive enhancement:
   - mobile nav drawer toggle
   - close on link click / ESC / outside click
   - mark current nav link with aria-current
*/
(function () {
  'use strict';

  const toggle  = document.querySelector('[data-nav-toggle]');
  const drawer  = document.querySelector('[data-nav-drawer]');
  const body    = document.body;

  if (toggle && drawer) {
    const openLabel  = 'Open menu';
    const closeLabel = 'Close menu';

    function setOpen(open) {
      drawer.dataset.open = open ? 'true' : 'false';
      drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? closeLabel : openLabel);
      body.classList.toggle('no-scroll', open);
    }

    setOpen(false);

    toggle.addEventListener('click', function () {
      const isOpen = drawer.dataset.open === 'true';
      setOpen(!isOpen);
    });

    drawer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setOpen(false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.dataset.open === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });

    document.addEventListener('click', function (e) {
      if (drawer.dataset.open !== 'true') return;
      if (drawer.contains(e.target) || toggle.contains(e.target)) return;
      setOpen(false);
    });

    // Close drawer when resizing up to desktop
    let lastIsDesktop = window.innerWidth >= 1024;
    window.addEventListener('resize', function () {
      const isDesktop = window.innerWidth >= 1024;
      if (isDesktop && !lastIsDesktop) setOpen(false);
      lastIsDesktop = isDesktop;
    });
  }

  // Mark current nav link
  const path = location.pathname.replace(/\/+$/, '') || '/';
  document.querySelectorAll('[data-nav] a').forEach(function (a) {
    const href = a.getAttribute('href');
    if (!href) return;
    const normalised = href.replace(/\/+$/, '') || '/';
    if (normalised === path) a.setAttribute('aria-current', 'page');
  });

  const success = document.querySelector('[data-form-success]');
  if (success && new URLSearchParams(window.location.search).get('sent') === '1') {
    success.hidden = false;
    success.setAttribute('tabindex', '-1');
    success.focus({ preventScroll: true });
  }
})();
