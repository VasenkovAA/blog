document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const recommendedSidebar = document.getElementById('recommendedSidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarToggleMobile = document.getElementById('sidebarToggleMobile');
    const sidebarToggleDesktop = document.getElementById('sidebarToggleDesktop');
    const recommendedToggle = document.getElementById('recommendedToggle');
    const themeToggle = document.getElementById('themeToggle');

    initTheme();
    initSidebar();
    initRecommendedSidebar();

    if (sidebarToggleMobile) {
        sidebarToggleMobile.addEventListener('click', toggleMobileSidebar);
    }

    if (sidebarToggleDesktop) {
        sidebarToggleDesktop.addEventListener('click', toggleDesktopSidebar);
    }

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }

    if (recommendedToggle) {
        recommendedToggle.addEventListener('click', toggleRecommendedSidebar);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    document.addEventListener('click', function(event) {
        const isMobile = window.innerWidth < 992;
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnMobileToggle = sidebarToggleMobile?.contains(event.target);

        if (isMobile && !isClickInsideSidebar && !isClickOnMobileToggle) {
            sidebar.classList.remove('show');
        }
    });

    window.addEventListener('resize', handleResize);

    function initTheme() {
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        let theme = 'light';
        if (savedTheme) {
            theme = savedTheme;
        } else if (systemPrefersDark) {
            theme = 'dark';
        }

        document.documentElement.setAttribute('data-bs-theme', theme);
        updateThemeButton(theme);
    }

    function toggleTheme() {
        const html = document.documentElement;
        const currentTheme = html.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        html.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeButton(newTheme);
    }

    function updateThemeButton(theme) {
        if (!themeToggle) return;

        const icon = theme === 'dark' ? 'bi-sun' : 'bi-moon';
        const text = theme === 'dark' ? 'Светлая тема' : 'Тёмная тема';

        themeToggle.innerHTML = `<i class="bi ${icon} me-2"></i>${text}`;
    }

    function initSidebar() {
        const sidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        const isMobile = window.innerWidth < 992;

        if (isMobile) {
            sidebar.classList.remove('collapsed');
            sidebar.classList.remove('show');
        } else {
            if (sidebarCollapsed) {
                collapseSidebar();
            } else {
                expandSidebar();
            }
        }
    }

    function toggleSidebar() {
        const isMobile = window.innerWidth < 992;

        if (isMobile) {
            sidebar.classList.remove('show');
        } else {
            const isCollapsed = sidebar.classList.contains('collapsed');
            if (isCollapsed) {
                expandSidebar();
            } else {
                collapseSidebar();
            }
        }
    }

    function toggleMobileSidebar() {
        sidebar.classList.toggle('show');
    }

    function toggleDesktopSidebar() {
        const isCollapsed = sidebar.classList.contains('collapsed');
        if (isCollapsed) {
            expandSidebar();
        } else {
            collapseSidebar();
        }
    }

    function collapseSidebar() {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('expanded');

        if (sidebarToggle) {
            const icon = sidebarToggle.querySelector('i');
            icon.className = 'bi bi-chevron-right';
        }

        localStorage.setItem('sidebarCollapsed', 'true');
    }

    function expandSidebar() {
        sidebar.classList.remove('collapsed');
        mainContent.classList.remove('expanded');

        if (sidebarToggle) {
            const icon = sidebarToggle.querySelector('i');
            icon.className = 'bi bi-chevron-left';
        }

        localStorage.setItem('sidebarCollapsed', 'false');
    }

    function initRecommendedSidebar() {
        const recommendedHidden = localStorage.getItem('recommendedHidden') === 'true';

        if (recommendedHidden && recommendedSidebar) {
            recommendedSidebar.style.display = 'none';
            updateRecommendedToggleButton(true);
        }
    }

    function toggleRecommendedSidebar() {
        if (!recommendedSidebar || !recommendedToggle) return;

        const isHidden = recommendedSidebar.style.display === 'none';

        if (isHidden) {
            recommendedSidebar.style.display = 'block';
            localStorage.setItem('recommendedHidden', 'false');
        } else {
            recommendedSidebar.style.display = 'none';
            localStorage.setItem('recommendedHidden', 'true');
        }

        updateRecommendedToggleButton(!isHidden);
    }

    function updateRecommendedToggleButton(isHidden) {
        if (!recommendedToggle) return;

        const icon = isHidden ? 'bi-chevron-down' : 'bi-chevron-up';
        const text = isHidden ? 'Показать рекомендации' : 'Скрыть рекомендации';

        recommendedToggle.innerHTML = `<i class="bi ${icon}"></i> ${text}`;
    }

    function handleResize() {
        if (window.innerWidth >= 992) {
            sidebar.classList.remove('show');

            const recommendedHidden = localStorage.getItem('recommendedHidden');
            if (recommendedSidebar && recommendedHidden === 'true') {
                recommendedSidebar.style.display = 'block';
            }

            const isCollapsed = sidebar.classList.contains('collapsed');
            if (sidebarToggle) {
                const icon = sidebarToggle.querySelector('i');
                icon.className = isCollapsed ? 'bi bi-chevron-right' : 'bi bi-chevron-left';
            }
        } else {
            sidebar.classList.remove('collapsed');
            mainContent.classList.remove('expanded');

            if (sidebarToggle) {
                const icon = sidebarToggle.querySelector('i');
                icon.className = 'bi bi-x-lg';
            }
        }
    }

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            const newTheme = e.matches ? 'dark' : 'light';
            document.documentElement.setAttribute('data-bs-theme', newTheme);
            updateThemeButton(newTheme);
        }
    });

    handleResize();
});
