(function () {
  'use strict';

  var MOBILE_MAX = 1240;
  var bound = false;

  function isMobile() {
    return window.innerWidth < MOBILE_MAX;
  }

  function getToggle() {
    return document.querySelector('#Top_bar .responsive-menu-toggle');
  }

  function getMenu() {
    return document.querySelector('#Top_bar #menu');
  }

  function getOverlay() {
    return document.getElementById('wafa-mobile-menu-overlay');
  }

  function ensureOverlay() {
    var overlay = getOverlay();
    if (overlay) return overlay;

    overlay = document.createElement('div');
    overlay.id = 'wafa-mobile-menu-overlay';
    overlay.hidden = true;
    overlay.addEventListener('click', closeMenu);
    document.body.appendChild(overlay);
    return overlay;
  }

  function isOpen() {
    return document.body.classList.contains('wafa-mobile-menu-open');
  }

  function getToggleIcon() {
    var toggle = getToggle();
    return toggle ? toggle.querySelector('i') : null;
  }

  function setToggleIcon(open) {
    var toggle = getToggle();
    var icon = getToggleIcon();
    if (!toggle || !icon) return;

    icon.classList.remove('icon-menu-fine', 'icon-cancel-fine');
    icon.classList.add(open ? 'icon-cancel-fine' : 'icon-menu-fine');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }

  function setOpen(open) {
    var toggle = getToggle();
    var menu = getMenu();
    var overlay = ensureOverlay();
    if (!toggle || !menu) return;

    document.body.classList.toggle('wafa-mobile-menu-open', open);
    toggle.classList.toggle('active', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    menu.setAttribute('aria-expanded', open ? 'true' : 'false');
    setToggleIcon(open);

    if (open) {
      menu.removeAttribute('hidden');
      menu.style.removeProperty('display');
    } else {
      menu.setAttribute('hidden', '');
      menu.style.setProperty('display', 'none', 'important');
    }

    overlay.hidden = !open;
  }

  function openMenu() {
    setOpen(true);
  }

  function closeMenu() {
    setOpen(false);
  }

  function toggleMenu(event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
      event.stopImmediatePropagation();
    }
    if (!isMobile()) return;
    if (isOpen()) {
      closeMenu();
    } else {
      openMenu();
    }
  }

  function neutralizeThemeMenu() {
    if (!window.jQuery) return;
    window.jQuery('.responsive-menu-toggle').off('click');
    window.jQuery('#Top_bar #menu').stop(true, true);
  }

  function bindMenu() {
    if (bound) {
      neutralizeThemeMenu();
      return;
    }

    var toggle = getToggle();
    var menu = getMenu();
    if (!toggle || !menu) return;

    bound = true;
    ensureOverlay();
    neutralizeThemeMenu();
    setOpen(false);

    toggle.addEventListener('click', toggleMenu, true);

    menu.addEventListener('click', function (event) {
      if (event.target.closest('a:not(.menu-toggle)')) {
        closeMenu();
      }
    });

    window.addEventListener('resize', function () {
      if (!isMobile()) closeMenu();
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') closeMenu();
    });
  }

  function init() {
    bindMenu();
    if (window.jQuery) {
      window.jQuery(bindMenu);
    }
    window.setTimeout(bindMenu, 300);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
