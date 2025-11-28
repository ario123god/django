function toggleMenu() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
}

window.addEventListener('scroll', () => {
    const header = document.querySelector('.topbar');
    if (window.scrollY > 10) {
        header.style.boxShadow = '0 12px 30px rgba(0,0,0,0.08)';
    } else {
        header.style.boxShadow = '';
    }
});
