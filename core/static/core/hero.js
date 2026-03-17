document.addEventListener('DOMContentLoaded', function () {
  const section = document.querySelector('.hc-hero-section');
  if (!section) return;

  const slides = Array.from(section.querySelectorAll('.hc-hero-slide'));
  const prev = section.querySelector('.hc-hero-prev');
  const next = section.querySelector('.hc-hero-next');
  let idx = slides.findIndex(s => s.classList.contains('hc-active'));
  if (idx === -1) idx = 0;
  let interval = null;
  const delay = 5000;

  function show(i){
    slides.forEach((s, j) => {
      const active = j === i;
      s.classList.toggle('hc-active', active);
      s.setAttribute('aria-hidden', active ? 'false' : 'true');
    });
    idx = i;
  }

  function nextSlide(){ show((idx+1) % slides.length); }
  function prevSlide(){ show((idx-1+slides.length) % slides.length); }

  function start(){ if (slides.length <= 1) return; stop(); interval = setInterval(nextSlide, delay); }
  function stop(){ if (interval) { clearInterval(interval); interval = null; } }

  next && next.addEventListener('click', () => { nextSlide(); start(); });
  prev && prev.addEventListener('click', () => { prevSlide(); start(); });

  section.addEventListener('mouseenter', stop);
  section.addEventListener('mouseleave', start);

  // keyboard support
  section.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { nextSlide(); start(); }
    if (e.key === 'ArrowLeft') { prevSlide(); start(); }
  });

  // init - ensure initial state is correct and start autoplay if applicable
  show(idx);
  section.setAttribute('tabindex', '0');
  start();
});
