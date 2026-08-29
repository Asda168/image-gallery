// Subtle header shadow on scroll
const header = document.querySelector('.site-header');
if (header) {
  window.addEventListener('scroll', () => {
    header.style.boxShadow = window.scrollY > 8 ? '0 8px 24px -12px rgba(0,0,0,0.5)' : 'none';
  });
}

// Mobile search overlay + ⌘K shortcut
(function () {
  const trigger = document.getElementById('searchTrigger');
  const overlay = document.getElementById('searchOverlay');
  const overlayInput = document.getElementById('searchOverlayInput');
  const overlayClose = document.getElementById('searchOverlayClose');
  const searchInput = document.getElementById('searchInput');
  if (!overlay) return;

  function openOverlay() {
    overlay.classList.add('open');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.classList.add('lightbox-locked');
    overlayInput?.focus();
  }
  function closeOverlay() {
    overlay.classList.remove('open');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('lightbox-locked');
  }

  trigger?.addEventListener('click', openOverlay);
  overlayClose?.addEventListener('click', closeOverlay);
  overlay.addEventListener('click', (e) => { if (e.target === overlay) closeOverlay(); });

  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (window.matchMedia('(max-width: 760px)').matches) {
        openOverlay();
      } else {
        searchInput?.focus();
      }
    }
    if (e.key === 'Escape' && overlay.classList.contains('open')) closeOverlay();
  });
})();

// Full-screen lightbox
(function () {
  const triggers = Array.from(document.querySelectorAll('.lightbox-trigger'));
  const lightbox = document.getElementById('lightbox');
  if (!triggers.length || !lightbox) return;

  const imgEl = document.getElementById('lightboxImg');
  const titleEl = document.getElementById('lightboxTitle');
  const categoryEl = document.getElementById('lightboxCategory');
  const counterEl = document.getElementById('lightboxCounter');
  const detailLink = document.getElementById('lightboxDetailLink');
  const closeBtn = document.getElementById('lightboxClose');
  const prevBtn = document.getElementById('lightboxPrev');
  const nextBtn = document.getElementById('lightboxNext');
  const stage = document.querySelector('.lightbox-stage');

  let currentIndex = 0;
  let lastFocused = null;

  function pad(n, len) {
    return String(n).padStart(len, '0');
  }

  function openAt(index) {
    currentIndex = (index + triggers.length) % triggers.length;
    const d = triggers[currentIndex].dataset;

    imgEl.src = d.full;
    imgEl.alt = d.title || '';
    titleEl.textContent = d.title || '';

    const parts = [d.category, d.date].filter(Boolean);
    if (parts.length) {
      categoryEl.textContent = parts.join(' · ');
      categoryEl.hidden = false;
    } else {
      categoryEl.hidden = true;
    }

    const total = triggers.length;
    counterEl.textContent = `${pad(currentIndex + 1, 2)} / ${pad(total, 2)}`;
    counterEl.hidden = total <= 1;

    detailLink.href = d.detail || '#';

    const multiple = total > 1;
    prevBtn.hidden = !multiple;
    nextBtn.hidden = !multiple;

    lastFocused = document.activeElement;
    lightbox.classList.add('open');
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.classList.add('lightbox-locked');
    closeBtn.focus();
  }

  function close() {
    lightbox.classList.remove('open');
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('lightbox-locked');
    if (lastFocused) lastFocused.focus();
  }

  triggers.forEach((trigger, index) => {
    trigger.addEventListener('click', () => openAt(index));
    trigger.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openAt(index);
      }
    });
  });

  closeBtn.addEventListener('click', close);
  prevBtn.addEventListener('click', () => openAt(currentIndex - 1));
  nextBtn.addEventListener('click', () => openAt(currentIndex + 1));

  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) close();
  });

  document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') openAt(currentIndex - 1);
    if (e.key === 'ArrowRight') openAt(currentIndex + 1);
  });

  // Swipe navigation on touch devices
  let touchStartX = 0;
  stage?.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].clientX;
  }, { passive: true });
  stage?.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) < 40) return;
    if (dx < 0) openAt(currentIndex + 1);
    else openAt(currentIndex - 1);
  }, { passive: true });
})();
