(() => {
  const STORAGE_KEY = 'ai-director-language';

  function applyLanguage(language) {
    document.querySelectorAll('[data-language-panel]').forEach((panel) => {
      const matches = panel.getAttribute('data-language-panel') === language;
      panel.hidden = !matches;
    });

    document.querySelectorAll('[data-language-target]').forEach((button) => {
      button.classList.toggle('is-active', button.getAttribute('data-language-target') === language);
      button.setAttribute('aria-pressed', String(button.getAttribute('data-language-target') === language));
    });

    document.documentElement.lang = language === 'ar' ? 'ar' : 'en';
  }

  function preferredLanguage() {
    const saved = window.localStorage.getItem(STORAGE_KEY);
    return saved === 'ar' ? 'ar' : 'en';
  }

  document.addEventListener('click', (event) => {
    const button = event.target.closest('[data-language-target]');
    if (!button) {
      return;
    }

    const language = button.getAttribute('data-language-target');
    if (!language) {
      return;
    }

    window.localStorage.setItem(STORAGE_KEY, language);
    applyLanguage(language);
  });

  document.addEventListener('DOMContentLoaded', () => {
    applyLanguage(preferredLanguage());
  });
})();
