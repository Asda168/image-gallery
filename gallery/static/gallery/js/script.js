// Subtle header shadow on scroll
const header = document.querySelector('.site-header');
if (header) {
  window.addEventListener('scroll', () => {
    header.style.boxShadow = window.scrollY > 8 ? '0 8px 24px -12px rgba(0,0,0,0.5)' : 'none';
  });
}

// Full-screen lightbox
(function () {
  const triggers = Array.from(document.querySelectorAll('.lightbox-trigger'));
  const lightbox = document.getElementById('lightbox');
  if (!triggers.length || !lightbox) return;

  const imgEl = document.getElementById('lightboxImg');
  const titleEl = document.getElementById('lightboxTitle');
  const categoryEl = document.getElementById('lightboxCategory');
  const detailLink = document.getElementById('lightboxDetailLink');
  const closeBtn = document.getElementById('lightboxClose');
  const prevBtn = document.getElementById('lightboxPrev');
  const nextBtn = document.getElementById('lightboxNext');

  let currentIndex = 0;
  let lastFocused = null;

  function openAt(index) {
    currentIndex = (index + triggers.length) % triggers.length;
    const d = triggers[currentIndex].dataset;

    imgEl.src = d.full;
    imgEl.alt = d.title || '';
    titleEl.textContent = d.title || '';

    if (d.category) {
      categoryEl.textContent = d.category;
      categoryEl.hidden = false;
    } else {
      categoryEl.hidden = true;
    }

    detailLink.href = d.detail || '#';

    const multiple = triggers.length > 1;
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
})();
