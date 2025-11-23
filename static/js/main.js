const root = document.documentElement;
const body = document.body;
const themeToggle = document.getElementById('themeToggle');
const langToggle = document.getElementById('langToggle');
const menuToggle = document.getElementById('menuToggle');
const nav = document.getElementById('primaryNav');

const translations = {
    en: {
        brandName: 'Evergreen International School',
        brandTagline: 'Learning for a brighter tomorrow',
        navHome: 'Home',
        navAbout: 'About',
        navDepartments: 'Departments',
        navTeachers: 'Teachers',
        navContact: 'Contact',
        langToggle: 'FA',
        footerAbout: 'Evergreen International School nurtures students to become confident, creative, and responsible global citizens.',
        footerLinks: 'Quick Links',
        footerContact: 'Get in Touch',
        footerPhone: 'Phone: +1 (555) 123-4567',
        footerEmail: 'Email: hello@evergreenschool.edu',
        footerRights: '© 2024 Evergreen International School. All rights reserved.',
        heroEyebrow: 'Welcome to our community',
        heroTitle: 'Inspiring excellence through curiosity, creativity, and character.',
        heroSubtitle: 'Evergreen International School blends rigorous academics with compassionate mentorship to help students thrive in a global society.',
        heroPrimary: 'Explore our story',
        heroSecondary: 'Latest news',
        heroCardTitle: 'Upcoming Open Day',
        heroCardCopy: 'Meet our teachers, tour classrooms, and discover how we personalize learning for every child.',
        heroCardDate: 'Saturday, November 16 · 10:00 AM',
        heroCardLocation: 'Evergreen Campus Atrium',
        heroCardCta: 'Book your visit',
        aboutEyebrow: 'Who we are',
        aboutTitle: 'A caring environment where every student is seen and challenged.',
        aboutCopy: 'From kindergarten to graduation, our educators design engaging lessons, lead clubs, and spark curiosity through arts, sciences, and service learning.',
        feature1Title: 'Modern Classrooms',
        feature1Copy: 'Light-filled labs, collaborative studios, and maker spaces equipped for STEM, media, and design.',
        feature2Title: 'Whole-Child Care',
        feature2Copy: 'Counseling, wellness programs, and inclusive activities that support every learner’s wellbeing.',
        feature3Title: 'Global Citizenship',
        feature3Copy: 'Bilingual curriculum, cultural exchanges, and community projects that broaden perspectives.',
        newsEyebrow: 'News & Events',
        newsTitle: 'Stay updated with campus life.',
        news1Tag: 'Academics',
        news1Title: 'Robotics team advances to regional finals',
        news1Copy: 'Our middle school robotics team earned top honors with their eco-friendly automation project.',
        news1Meta: 'October 28, 2024',
        news2Tag: 'Arts',
        news2Title: 'Winter concert celebrates student talent',
        news2Copy: 'Choirs, orchestras, and theater students present an evening of music from around the world.',
        news2Meta: 'November 2, 2024',
        news3Tag: 'Community',
        news3Title: 'Service day partners with local shelters',
        news3Copy: 'Students and families assembled care kits and raised funds for neighborhood shelters.',
        news3Meta: 'November 10, 2024',
        aboutHeroEyebrow: 'About Evergreen',
        aboutHeroTitle: 'Mission-driven learning rooted in empathy, courage, and innovation.',
        aboutHeroCopy: 'We empower students to ask bold questions, collaborate across cultures, and build solutions for a better world.',
        missionTitle: 'Our Mission',
        missionCopy: 'To nurture curious minds through research, arts, athletics, and service so every learner discovers their unique strengths.',
        visionTitle: 'Our Vision',
        visionCopy: 'A vibrant community where students graduate as multilingual, compassionate leaders ready to shape the future.',
        principalEyebrow: 'Leadership',
        principalTitle: 'A message from our principal',
        principalCopy: '“Evergreen’s heart is its people. Together, we celebrate diversity, honor student voice, and ensure every family feels welcome on campus.”',
        principalName: 'Dr. Laleh Rahimi, Principal',
        achievementsEyebrow: 'Milestones',
        achievementsTitle: 'Achievements we are proud of',
        achievement1Number: '98%',
        achievement1Label: 'College acceptance rate',
        achievement2Number: '40+',
        achievement2Label: 'Student-led clubs',
        achievement3Number: '25',
        achievement3Label: 'International partnerships',
        achievement4Number: '12',
        achievement4Label: 'Years of academic excellence',
        departmentsEyebrow: 'Academics',
        departmentsTitle: 'Dynamic departments that celebrate every field of study.',
        departmentsCopy: 'From advanced sciences to fine arts, our faculty design hands-on experiences that make learning memorable.',
        dept1Title: 'Science & Research',
        dept1Copy: 'Biology, chemistry, physics, and environmental science labs with inquiry-based projects.',
        dept2Title: 'Humanities & Languages',
        dept2Copy: 'Literature, history, philosophy, and bilingual courses that strengthen critical thinking.',
        dept3Title: 'Mathematics',
        dept3Copy: 'Applied mathematics, statistics, and problem-solving labs using real-world scenarios.',
        dept4Title: 'Arts & Design',
        dept4Copy: 'Visual arts, theater, music ensembles, and digital design studios that inspire imagination.',
        dept5Title: 'Technology & Innovation',
        dept5Copy: 'Coding, robotics, UX design, and cybersecurity fundamentals for future-ready skills.',
        dept6Title: 'Athletics & Wellness',
        dept6Copy: 'Team sports, fitness training, and mindfulness programs guided by certified coaches.',
        teachersEyebrow: 'Our Team',
        teachersTitle: 'Meet the educators guiding every learner’s journey.',
        teachersCopy: 'Our faculty blend subject expertise with compassion, creating classrooms where questions are celebrated and curiosity leads.',
        teacher1Name: 'Marjan Rahmani',
        teacher1Role: 'Mathematics Lead',
        teacher1Contact: 'm.rahmani@evergreenschool.edu',
        teacher2Name: 'Amir Etemadi',
        teacher2Role: 'Science Coordinator',
        teacher2Contact: 'a.etemadi@evergreenschool.edu',
        teacher3Name: 'Nasrin Safavi',
        teacher3Role: 'Literature & Bilingual Studies',
        teacher3Contact: 'n.safavi@evergreenschool.edu',
        teacher4Name: 'Daniel Thompson',
        teacher4Role: 'Arts & Media',
        teacher4Contact: 'd.thompson@evergreenschool.edu',
        teacher5Name: 'Sara Zand',
        teacher5Role: 'Counselor & Wellbeing',
        teacher5Contact: 's.zand@evergreenschool.edu',
        teacher6Name: 'Kourosh Farhadi',
        teacher6Role: 'Athletics Director',
        teacher6Contact: 'k.farhadi@evergreenschool.edu',
        contactEyebrow: 'Visit & Connect',
        contactTitle: 'We would love to hear from you.',
        contactCopy: 'Share your questions, schedule a tour, or ask about enrollment. Our team responds within one business day.',
        contactFormTitle: 'Send a Message',
        contactNameLabel: 'Full Name',
        contactEmailLabel: 'Email',
        contactSubjectLabel: 'Subject',
        contactMessageLabel: 'Message',
        contactSubmit: 'Send message',
        contactVisitTitle: 'Visit Campus',
        contactVisitCopy: 'Evergreen International School, 123 Learning Way, Tehran',
        contactMap: 'Interactive map coming soon'
    },
    fa: {
        brandName: 'مدرسه بین‌المللی اورگرین',
        brandTagline: 'یادگیری برای فردایی روشن‌تر',
        navHome: 'خانه',
        navAbout: 'درباره',
        navDepartments: 'دپارتمان‌ها',
        navTeachers: 'معلمان',
        navContact: 'تماس',
        langToggle: 'EN',
        footerAbout: 'مدرسه بین‌المللی اورگرین دانش‌آموزان را به شهروندانی خلاق، مسئول و بااعتمادبه‌نفس تبدیل می‌کند.',
        footerLinks: 'دسترسی سریع',
        footerContact: 'ارتباط با ما',
        footerPhone: 'تلفن: ۵۵۵ ۱۲۳ ۴۵۶۷+',
        footerEmail: 'ایمیل: hello@evergreenschool.edu',
        footerRights: '© ۲۰۲۴ مدرسه بین‌المللی اورگرین. تمامی حقوق محفوظ است.',
        heroEyebrow: 'به جامعه ما خوش آمدید',
        heroTitle: 'الهام‌بخش برتری از مسیر کنجکاوی، خلاقیت و شخصیت.',
        heroSubtitle: 'مدرسه اورگرین تلفیقی از آموزش دقیق و راهنمایی مهربانانه است تا دانش‌آموزان در جامعه جهانی بدرخشند.',
        heroPrimary: 'داستان ما را ببینید',
        heroSecondary: 'آخرین اخبار',
        heroCardTitle: 'روز بازدید پیش رو',
        heroCardCopy: 'با معلمان ما آشنا شوید، کلاس‌ها را ببینید و روش یادگیری شخصی‌سازی‌شده را کشف کنید.',
        heroCardDate: 'شنبه، ۱۶ آبان · ساعت ۱۰',
        heroCardLocation: 'سالن مرکزی اورگرین',
        heroCardCta: 'رزرو بازدید',
        aboutEyebrow: 'ما که هستیم',
        aboutTitle: 'محیطی صمیمی که هر دانش‌آموز را می‌بیند و به چالش می‌کشد.',
        aboutCopy: 'از مهدکودک تا فارغ‌التحصیلی، معلمان ما درس‌های جذاب، باشگاه‌ها و پروژه‌های هنری و علمی را طراحی می‌کنند.',
        feature1Title: 'کلاس‌های مدرن',
        feature1Copy: 'آزمایشگاه‌های روشن، استودیوهای تعاملی و کارگاه‌های سازنده برای STEM، رسانه و طراحی.',
        feature2Title: 'توجه به کل دانش‌آموز',
        feature2Copy: 'مشاوره، برنامه‌های سلامت و فعالیت‌های فراگیر که از رفاه هر دانش‌آموز حمایت می‌کند.',
        feature3Title: 'شهروندی جهانی',
        feature3Copy: 'برنامه درسی دو زبانه، تبادل فرهنگی و پروژه‌های اجتماعی که افق دید را گسترش می‌دهد.',
        newsEyebrow: 'اخبار و رویدادها',
        newsTitle: 'با زندگی پردیس همراه باشید.',
        news1Tag: 'آموزش',
        news1Title: 'تیم رباتیک به فینال منطقه‌ای راه یافت',
        news1Copy: 'تیم رباتیک مقطع متوسطه با پروژه اتوماسیون دوستدار محیط‌زیست مقام برتر را کسب کرد.',
        news1Meta: '۶ آبان ۱۴۰۳',
        news2Tag: 'هنر',
        news2Title: 'کنسرت زمستانی با درخشش استعدادها',
        news2Copy: 'کر، ارکستر و تئاتر دانش‌آموزی شبی از موسیقی ملل را اجرا می‌کنند.',
        news2Meta: '۱۱ آبان ۱۴۰۳',
        news3Tag: 'اجتماع',
        news3Title: 'روز خدمت با پناهگاه‌های محلی',
        news3Copy: 'دانش‌آموزان و خانواده‌ها بسته‌های حمایتی آماده و برای پناهگاه‌ها کمک مالی جمع‌آوری کردند.',
        news3Meta: '۱۹ آبان ۱۴۰۳',
        aboutHeroEyebrow: 'درباره اورگرین',
        aboutHeroTitle: 'آموزش مأموریت‌محور بر پایه همدلی، شجاعت و نوآوری.',
        aboutHeroCopy: 'ما دانش‌آموزان را تشویق می‌کنیم که پرسش‌های جسورانه بپرسند، بین فرهنگ‌ها همکاری کنند و راه‌حل بسازند.',
        missionTitle: 'ماموریت ما',
        missionCopy: 'پرورش ذهن‌های کنجکاو از طریق پژوهش، هنر، ورزش و خدمت تا هر یادگیرنده استعداد خود را کشف کند.',
        visionTitle: 'چشم‌انداز ما',
        visionCopy: 'جامعه‌ای پویا که دانش‌آموزان آن به عنوان رهبران دوزبانه و دلسوز آینده شناخته می‌شوند.',
        principalEyebrow: 'رهبری',
        principalTitle: 'پیام مدیر مدرسه',
        principalCopy: '«قلب اورگرین مردم آن است. با هم تنوع را جشن می‌گیریم، صدای دانش‌آموز را می‌شنویم و خانواده‌ها را در مدرسه خوشامد می‌گوییم.»',
        principalName: 'دکتر لاله رحیمی، مدیر',
        achievementsEyebrow: 'دستاوردها',
        achievementsTitle: 'افتخاراتی که به آن‌ها می‌بالیم',
        achievement1Number: '۹۸٪',
        achievement1Label: 'پذیرش دانشگاهی',
        achievement2Number: '۴۰+',
        achievement2Label: 'باشگاه‌های دانش‌آموزی',
        achievement3Number: '۲۵',
        achievement3Label: 'همکاری‌های بین‌المللی',
        achievement4Number: '۱۲',
        achievement4Label: 'سال‌های موفقیت آموزشی',
        departmentsEyebrow: 'آکادمیک',
        departmentsTitle: 'دپارتمان‌های پویایی که همه رشته‌ها را جشن می‌گیرند.',
        departmentsCopy: 'از علوم پیشرفته تا هنرهای زیبا، استادان ما تجربه‌های عملی و ماندگار می‌سازند.',
        dept1Title: 'علوم و پژوهش',
        dept1Copy: 'آزمایشگاه‌های زیست، شیمی، فیزیک و محیط‌زیست با پروژه‌های پژوهش‌محور.',
        dept2Title: 'علوم انسانی و زبان‌ها',
        dept2Copy: 'ادبیات، تاریخ، فلسفه و دوره‌های دوزبانه برای تقویت تفکر انتقادی.',
        dept3Title: 'ریاضیات',
        dept3Copy: 'ریاضی کاربردی، آمار و آزمایشگاه‌های حل مسئله با سناریوهای واقعی.',
        dept4Title: 'هنر و طراحی',
        dept4Copy: 'هنرهای تجسمی، تئاتر، گروه‌های موسیقی و استودیوهای طراحی دیجیتال.',
        dept5Title: 'فناوری و نوآوری',
        dept5Copy: 'کدنویسی، رباتیک، طراحی تجربه کاربر و امنیت سایبری برای مهارت‌های آینده.',
        dept6Title: 'ورزش و تندرستی',
        dept6Copy: 'تیم‌های ورزشی، تمرین‌های آمادگی جسمانی و برنامه‌های ذهن‌آگاهی با مربیان متخصص.',
        teachersEyebrow: 'تیم ما',
        teachersTitle: 'با معلمانی آشنا شوید که همراه هر یادگیرنده هستند.',
        teachersCopy: 'هیئت علمی ما تخصص موضوعی را با همدلی ترکیب می‌کند و کلاس را به فضایی پر از پرسش بدل می‌سازد.',
        teacher1Name: 'مرجان رحمانی',
        teacher1Role: 'سرگروه ریاضی',
        teacher1Contact: 'm.rahmani@evergreenschool.edu',
        teacher2Name: 'امیر اعتمادی',
        teacher2Role: 'هماهنگ‌کننده علوم',
        teacher2Contact: 'a.etemadi@evergreenschool.edu',
        teacher3Name: 'نسرین صفوی',
        teacher3Role: 'ادبیات و مطالعات دو زبانه',
        teacher3Contact: 'n.safavi@evergreenschool.edu',
        teacher4Name: 'دنیل تامپسون',
        teacher4Role: 'هنر و رسانه',
        teacher4Contact: 'd.thompson@evergreenschool.edu',
        teacher5Name: 'سارا زند',
        teacher5Role: 'مشاور و سلامت',
        teacher5Contact: 's.zand@evergreenschool.edu',
        teacher6Name: 'کوروش فرهادی',
        teacher6Role: 'مدیر تربیت‌بدنی',
        teacher6Contact: 'k.farhadi@evergreenschool.edu',
        contactEyebrow: 'بازدید و ارتباط',
        contactTitle: 'خوشحال می‌شویم از شما بشنویم.',
        contactCopy: 'سوالات خود را مطرح کنید، تور مدرسه رزرو کنید یا درباره ثبت‌نام بپرسید. تیم ما در یک روز کاری پاسخ می‌دهد.',
        contactFormTitle: 'ارسال پیام',
        contactNameLabel: 'نام و نام خانوادگی',
        contactEmailLabel: 'ایمیل',
        contactSubjectLabel: 'موضوع',
        contactMessageLabel: 'پیام',
        contactSubmit: 'ارسال پیام',
        contactVisitTitle: 'بازدید از پردیس',
        contactVisitCopy: 'مدرسه بین‌المللی اورگرین، خیابان یادگیری ۱۲۳، تهران',
        contactMap: 'نقشه تعاملی به زودی'
    }
};

function setTheme(theme) {
    const isDark = theme === 'dark';
    body.classList.toggle('dark', isDark);
    body.dataset.theme = theme;
    localStorage.setItem('theme', theme);
    themeToggle.querySelector('.icon-moon').textContent = isDark ? '☀️' : '🌙';
}

function applyLanguage(lang) {
    const dictionary = translations[lang] || translations.en;
    body.dir = lang === 'fa' ? 'rtl' : 'ltr';
    body.dataset.lang = lang;
    langToggle.textContent = lang === 'fa' ? 'EN' : 'FA';
    document.querySelectorAll('[data-i18n]').forEach((node) => {
        const key = node.dataset.i18n;
        if (dictionary[key]) {
            node.textContent = dictionary[key];
        }
    });
}

function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setTheme(savedTheme || (prefersDark ? 'dark' : 'light'));
}

function initLanguage() {
    const savedLang = localStorage.getItem('lang') || 'en';
    applyLanguage(savedLang);
}

function bindEvents() {
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const nextTheme = body.classList.contains('dark') ? 'light' : 'dark';
            setTheme(nextTheme);
        });
    }

    if (langToggle) {
        langToggle.addEventListener('click', () => {
            const nextLang = (body.dataset.lang || 'en') === 'en' ? 'fa' : 'en';
            localStorage.setItem('lang', nextLang);
            applyLanguage(nextLang);
        });
    }

    if (menuToggle && nav) {
        menuToggle.addEventListener('click', () => {
            nav.classList.toggle('open');
        });

        nav.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', () => nav.classList.remove('open'));
        });
    }

    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', (e) => {
            const targetId = anchor.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

initTheme();
initLanguage();
bindEvents();
