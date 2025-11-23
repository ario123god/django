const USER_KEY = 'schoolAuthUser';
const SESSION_KEY = 'schoolAuthSession';

const emailRegex = /^[\w-.]+@([\w-]+\.)+[\w-]{2,}$/i;

const getStoredUser = () => {
    const raw = localStorage.getItem(USER_KEY);
    if (!raw) return null;
    try {
        return JSON.parse(raw);
    } catch (e) {
        return null;
    }
};

const saveUser = (user) => {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
};

const setActiveSession = (username, remember) => {
    if (remember) {
        localStorage.setItem(SESSION_KEY, username);
        sessionStorage.removeItem(SESSION_KEY);
    } else {
        sessionStorage.setItem(SESSION_KEY, username);
        localStorage.removeItem(SESSION_KEY);
    }
};

const getActiveSession = () => {
    return localStorage.getItem(SESSION_KEY) || sessionStorage.getItem(SESSION_KEY);
};

const clearSession = () => {
    localStorage.removeItem(SESSION_KEY);
    sessionStorage.removeItem(SESSION_KEY);
};

const setMessage = (el, text, type = 'error') => {
    if (!el) return;
    el.textContent = text;
    el.style.color = type === 'success' ? 'var(--accent)' : '#ef4444';
    el.style.fontWeight = '600';
};

const initLoginPage = () => {
    const form = document.getElementById('login-form');
    const message = document.getElementById('login-message');
    const rememberBox = document.getElementById('remember-me');

    const active = getActiveSession();
    if (active) {
        window.location.href = 'dashboard.html';
        return;
    }

    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = (document.getElementById('login-email')?.value || '').trim();
        const password = (document.getElementById('login-password')?.value || '').trim();

        if (!email || !password) {
            setMessage(message, 'Please fill in both email and password.');
            return;
        }

        if (!emailRegex.test(email)) {
            setMessage(message, 'Please use a valid email address.');
            return;
        }

        const stored = getStoredUser();
        if (!stored || stored.email.toLowerCase() !== email.toLowerCase() || stored.password !== password) {
            setMessage(message, 'Incorrect email or password.');
            return;
        }

        setActiveSession(stored.username || stored.email, rememberBox?.checked);
        setMessage(message, 'Login successful. Redirecting...', 'success');
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 600);
    });
};

const initRegisterPage = () => {
    const form = document.getElementById('register-form');
    const message = document.getElementById('register-message');

    if (getActiveSession()) {
        window.location.href = 'dashboard.html';
        return;
    }

    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const username = (document.getElementById('register-username')?.value || '').trim();
        const email = (document.getElementById('register-email')?.value || '').trim();
        const password = (document.getElementById('register-password')?.value || '').trim();
        const confirm = (document.getElementById('register-confirm')?.value || '').trim();

        if (!username || !email || !password || !confirm) {
            setMessage(message, 'Please complete all fields.');
            return;
        }

        if (!emailRegex.test(email)) {
            setMessage(message, 'Please enter a valid email address.');
            return;
        }

        if (password.length < 6) {
            setMessage(message, 'Password should be at least 6 characters.');
            return;
        }

        if (password !== confirm) {
            setMessage(message, 'Passwords do not match.');
            return;
        }

        saveUser({ username, email, password });
        setMessage(message, 'Account created. Redirecting to login...', 'success');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 650);
    });
};

const initDashboardPage = () => {
    const greeting = document.getElementById('dashboard-greeting');
    const username = getActiveSession();

    if (!username) {
        window.location.href = 'login.html';
        return;
    }

    if (greeting) {
        greeting.textContent = `Welcome, ${username}`;
    }
};

const attachLogout = () => {
    const logoutButtons = [
        document.getElementById('logout-btn'),
        document.getElementById('logout-btn-secondary'),
    ].filter(Boolean);

    logoutButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
            clearSession();
            window.location.href = 'login.html';
        });
    });
};

document.addEventListener('DOMContentLoaded', () => {
    const page = (window.location.pathname.split('/').pop() || '').toLowerCase();

    if (page === 'login.html') {
        initLoginPage();
    } else if (page === 'register.html') {
        initRegisterPage();
    } else if (page === 'dashboard.html') {
        initDashboardPage();
    }

    attachLogout();
});
