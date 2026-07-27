/* ============================================================
   FertilEus – Main JavaScript
   ============================================================ */

/* ---- Mobile Nav Toggle ---- */
const hamburger = document.getElementById('hamburger');
const mobNav = document.getElementById('mobNav');
const mobNavClose = document.getElementById('mobNavClose');

function closeMobNav() {
  mobNav.classList.remove('open');
  const spans = hamburger.querySelectorAll('span');
  spans[0].style.transform = '';
  spans[1].style.opacity   = '';
  spans[2].style.transform = '';
  document.body.style.overflow = '';
}

hamburger.addEventListener('click', () => {
  mobNav.classList.toggle('open');
  const isOpen = mobNav.classList.contains('open');
  // Animate hamburger to X
  const spans = hamburger.querySelectorAll('span');
  if (isOpen) {
    spans[0].style.transform = 'translateY(7px) rotate(45deg)';
    spans[1].style.opacity   = '0';
    spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
    document.body.style.overflow = 'hidden'; // Prevent body scroll
  } else {
    closeMobNav();
  }
});

// Close nav when cancel button is clicked
if (mobNavClose) {
  mobNavClose.addEventListener('click', closeMobNav);
}

// Close nav when a link is clicked
const mobNavLinks = document.querySelectorAll('.mob-nav-links a');
mobNavLinks.forEach(link => {
  link.addEventListener('click', closeMobNav);
});

// Close nav on outside click
document.addEventListener('click', (e) => {
  if (!hamburger.contains(e.target) && !mobNav.contains(e.target)) {
    closeMobNav();
  }
});


/* ---- Scroll Reveal ---- */
const revealEls = document.querySelectorAll(
  '.hero-left, .hero-right, .about-left, .about-right, ' +
  '.service-card, .options-left, .options-right, ' +
  '.journal-card, .cta-container, .ed-stage-card'
);

revealEls.forEach((el, i) => {
  el.classList.add('reveal');
  // stagger cards
  if (el.classList.contains('service-card') || el.classList.contains('journal-card')) {
    const siblings = [...el.parentElement.children];
    const idx = siblings.indexOf(el);
    if (idx === 1) el.classList.add('reveal-delay-1');
    if (idx === 2) el.classList.add('reveal-delay-2');
    if (idx === 3) el.classList.add('reveal-delay-3');
  }
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

revealEls.forEach(el => revealObserver.observe(el));


/* ---- Sticky Navbar Shadow on Scroll ---- */
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 10) {
    navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,.10)';
  } else {
    navbar.style.boxShadow = '0 1px 12px rgba(0,0,0,.05)';
  }
});


/* ---- Newsletter Form ---- */
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
  newsletterForm.addEventListener('submit', (e) => {
    e.preventDefault();
  });

  const btn = newsletterForm.querySelector('button');
  const input = newsletterForm.querySelector('input');

  btn.addEventListener('click', () => {
    const email = input.value.trim();
    if (!email || !/\S+@\S+\.\S+/.test(email)) {
      input.style.borderColor = '#e05252';
      input.placeholder = 'Enter a valid email';
      setTimeout(() => {
        input.style.borderColor = '';
        input.placeholder = 'Your email address';
      }, 2000);
      return;
    }
    btn.textContent = '✓';
    btn.style.background = '#52b788';
    input.value = '';
    input.placeholder = 'Thank you!';
    setTimeout(() => {
      btn.textContent = 'Go';
      btn.style.background = '';
      input.placeholder = 'Your email address';
    }, 3000);
  });
}


/* ---- Stat Counter Animation ---- */
function animateCounter(el, target, suffix = '') {
  const duration = 1800;
  const step = 16;
  const increment = target / (duration / step);
  let current = 0;

  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    el.textContent = Math.floor(current).toLocaleString() + suffix;
  }, step);
}

const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const statNumbers = document.querySelectorAll('.stat-number');
      const data = [
        { el: statNumbers[0], target: 10000, suffix: '+' },
        { el: statNumbers[1], target: 50,    suffix: '+' },
        { el: statNumbers[2], target: 12,    suffix: '+' },
      ];
      data.forEach(d => {
        if (d.el) animateCounter(d.el, d.target, d.suffix);
      });
      statsObserver.disconnect();
    }
  });
}, { threshold: 0.5 });

const statsSection = document.querySelector('.hero-stats');
if (statsSection) statsObserver.observe(statsSection);


/* ---- Active Nav Link on Scroll ---- */
const sections = document.querySelectorAll('section[id]');
const navItems = document.querySelectorAll('.nav-links li a');

if (sections.length && navItems.length) {
  const activeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        navItems.forEach(a => a.classList.remove('active'));
        const active = document.querySelector(`.nav-links a[href="#${entry.target.id}"]`);
        if (active) active.classList.add('active');
      }
    });
  }, { rootMargin: '-40% 0px -55% 0px' });

  sections.forEach(s => activeObserver.observe(s));
}
