/* AvtoBilet.kg main JS — theme, helpers, seat selection */
(function () {
  'use strict';

  // ===== Theme handling =====
  const THEME_KEY = 'av_theme';
  const root = document.documentElement;
  const saved = localStorage.getItem(THEME_KEY);
  if (saved) root.setAttribute('data-theme', saved);

  window.toggleTheme = function () {
    const current = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem(THEME_KEY, next);
    // refresh icons
    document.querySelectorAll('[data-theme-icon]').forEach(el => {
      el.textContent = next === 'dark' ? '☀️' : '🌙';
    });
  };

  document.addEventListener('DOMContentLoaded', () => {
    const isDark = root.getAttribute('data-theme') === 'dark';
    document.querySelectorAll('[data-theme-icon]').forEach(el => {
      el.textContent = isDark ? '☀️' : '🌙';
    });
  });

  // ===== Auto-hide flash messages =====
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.alert').forEach(el => {
      setTimeout(() => { el.style.transition = 'opacity .5s'; el.style.opacity = '0'; }, 5000);
      setTimeout(() => el.remove(), 5600);
    });
  });

  // ===== HTMX CSRF integration =====
  document.body.addEventListener('htmx:configRequest', (event) => {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    if (token) event.detail.headers['X-CSRFToken'] = token.value;
  });

  // ===== Seat picker (Alpine.js component) =====
  window.seatPicker = function (totalSeats, takenSeats, maxSeats, basePrice) {
    return {
      selected: [],
      taken: new Set(takenSeats),
      total: totalSeats,
      max: maxSeats || 4,
      basePrice: basePrice,
      toggle(n) {
        if (this.taken.has(n)) return;
        const idx = this.selected.indexOf(n);
        if (idx >= 0) {
          this.selected.splice(idx, 1);
        } else {
          if (this.selected.length >= this.max) {
            alert(`Можно выбрать не более ${this.max} мест за один раз`);
            return;
          }
          this.selected.push(n);
          this.selected.sort((a, b) => a - b);
        }
      },
      isSelected(n) { return this.selected.includes(n); },
      isTaken(n) { return this.taken.has(n); },
      get totalPrice() { return (this.basePrice * this.selected.length).toFixed(2); },
      get count() { return this.selected.length; },
      get seatsValue() { return this.selected.join(','); }
    };
  };

  // ===== Swap origin/destination =====
  window.swapCities = function () {
    const origin = document.querySelector('[name=origin]');
    const dest = document.querySelector('[name=destination]');
    if (origin && dest) {
      const tmp = origin.value;
      origin.value = dest.value;
      dest.value = tmp;
    }
  };

  // ===== Print =====
  window.printPage = function () { window.print(); };

  // ===== Countdown for booking expiration =====
  window.countdownComponent = function (deadline) {
    return {
      timeLeft: '',
      init() {
        this.update();
        this._t = setInterval(() => this.update(), 1000);
      },
      destroy() { clearInterval(this._t); },
      update() {
        const diff = new Date(deadline) - new Date();
        if (diff <= 0) {
          this.timeLeft = 'Истекло';
          clearInterval(this._t);
          return;
        }
        const m = Math.floor(diff / 60000);
        const s = Math.floor((diff % 60000) / 1000);
        this.timeLeft = `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
      }
    };
  };

  // ===== Scroll Reveal Animation Engine =====
  document.addEventListener('DOMContentLoaded', () => {
    const reveals = document.querySelectorAll('.scroll-reveal');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('reveal-active');
        }
      });
    }, { threshold: 0.08 });
    reveals.forEach(el => observer.observe(el));
  });
})();

