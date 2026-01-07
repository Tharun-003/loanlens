// Theme toggle: persists choice in localStorage and toggles `theme-light` class
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('theme-toggle');
    const root = document.documentElement || document.body;

    function applyTheme(theme) {
        if (theme === 'light') {
            root.classList.add('theme-light');
        } else {
            root.classList.remove('theme-light');
        }
    }

    const saved = localStorage.getItem('loanlens_theme') || 'light';
    applyTheme(saved);

    if (toggle) {
        toggle.addEventListener('click', function() {
            const current = root.classList.contains('theme-light') ? 'light' : 'dark';
            const next = current === 'light' ? 'dark' : 'light';
            applyTheme(next);
            localStorage.setItem('loanlens_theme', next);
            // update button text/icon
            toggle.innerText = next === 'light' ? '🌙 Dark' : '☀️ Light';
        });

        // set initial label
        toggle.innerText = (saved === 'light') ? '🌙 Dark' : '☀️ Light';
    }
});
