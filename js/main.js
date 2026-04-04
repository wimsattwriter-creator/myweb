/* ============================================
   Joseph Wimsatt — Window Router
   Hash-based panel switching, mobile nav,
   lightbox keyboard handling
   ============================================ */

(function () {
  'use strict';

  document.body.classList.add('js-enabled');

  var panels = document.querySelectorAll('.panel');
  var navItems = document.querySelectorAll('.nav-item');
  var mobileItems = document.querySelectorAll('.mobile-nav-item');
  var toggle = document.querySelector('.topbar-toggle');
  var overlay = document.querySelector('.mobile-overlay');
  var prevHash = '';

  // --- Panel Router ---

  function showPanel(id) {
    if (!id || id.startsWith('fig-')) return;

    var target = document.getElementById(id);
    if (!target || !target.classList.contains('panel')) {
      id = 'home';
      target = document.getElementById(id);
    }

    panels.forEach(function (p) {
      p.classList.remove('active');
      p.setAttribute('aria-hidden', 'true');
    });

    target.classList.add('active');
    target.removeAttribute('aria-hidden');

    // Reset scroll position for the new panel
    var scroller = target.querySelector('.panel-scroll');
    if (scroller) scroller.scrollTop = 0;

    // Update nav active states
    navItems.forEach(function (item) {
      item.classList.toggle('active', item.getAttribute('data-section') === id);
    });
    mobileItems.forEach(function (item) {
      item.classList.toggle('active', item.getAttribute('data-section') === id);
    });

    prevHash = id;
  }

  function getHash() {
    return location.hash.replace('#', '') || 'home';
  }

  // --- Lightbox ---

  function isLightboxOpen() {
    return location.hash.indexOf('#fig-') === 0;
  }

  function closeLightbox() {
    location.hash = '#' + prevHash;
  }

  // --- Mobile Nav ---

  function openMobileNav() {
    overlay.classList.add('open');
    toggle.setAttribute('aria-expanded', 'true');
  }

  function closeMobileNav() {
    overlay.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  }

  if (toggle && overlay) {
    toggle.addEventListener('click', function () {
      if (overlay.classList.contains('open')) {
        closeMobileNav();
      } else {
        openMobileNav();
      }
    });

    // Close mobile nav when a link is clicked
    mobileItems.forEach(function (item) {
      item.addEventListener('click', function () {
        closeMobileNav();
      });
    });
  }

  // --- Event Listeners ---

  window.addEventListener('hashchange', function () {
    if (isLightboxOpen()) return;
    showPanel(getHash());
    closeMobileNav();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (isLightboxOpen()) {
        e.preventDefault();
        closeLightbox();
      } else if (overlay && overlay.classList.contains('open')) {
        closeMobileNav();
      }
    }
  });

  // Nav clicks that point to panels
  navItems.forEach(function (item) {
    item.addEventListener('click', function () {
      // Let the hash change handle the switch
    });
  });

  // --- Init ---
  showPanel(getHash());

})();
