// تحسينات تجربة المستخدم المتقدمة
class UXEnhancements {
    constructor() {
        this.init();
    }

    init() {
        this.initSmoothScrolling();
        this.initScrollEffects();
        this.initLoadingStates();
        this.initFormEnhancements();
        this.initInteractiveElements();
        this.initPerformanceOptimizations();
    }

    // التنقل السلس المحسن
    initSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"], .smooth-scroll');

        links.forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');

                if (href === '#' || href === '') return;

                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();

                    const offsetTop = target.offsetTop - 80;

                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });

                    // إضافة فئة نشطة للرابط
                    if (link.hash) {
                        this.updateActiveNavLink(link.hash);
                    }
                }
            });
        });
    }

    // تحديث رابط التنقل النشط
    updateActiveNavLink(hash) {
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            link.classList.remove('active');
        });

        const activeLink = document.querySelector(`.navbar-nav .nav-link[href="${hash}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }

    // تأثيرات التمرير المحسنة
    initScrollEffects() {
        // تأثير الشريط العلوي عند التمرير
        window.addEventListener('scroll', () => {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        // Intersection Observer للعناصر
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');

                    // تأثيرات متتالية للعناصر
                    if (entry.target.classList.contains('stagger-children')) {
                        this.staggerAnimation(entry.target);
                    }
                }
            });
        }, observerOptions);

        // مراقبة العناصر
        document.querySelectorAll('.fade-in-up, .fade-in-left, .fade-in-right, .stagger-children').forEach(el => {
            observer.observe(el);
        });
    }

    // تأثيرات متتالية
    staggerAnimation(parent) {
        const children = parent.querySelectorAll('.stagger-item');
        children.forEach((child, index) => {
            child.style.transitionDelay = `${index * 0.1}s`;
            child.classList.add('fade-in-up');
        });
    }

    // حالات التحميل
    initLoadingStates() {
        // إضافة مؤشر تحميل للأزرار
        document.addEventListener('submit', (e) => {
            const form = e.target;
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');

            if (submitBtn) {
                this.showButtonLoading(submitBtn);
            }
        });
    }

    // عرض حالة التحميل للزر
    showButtonLoading(button) {
        const originalText = button.innerHTML;
        button.innerHTML = `
            <span class="loading-spinner me-2"></span>
            جاري المعالجة...
        `;
        button.disabled = true;

        // استعادة الحالة الأصلية بعد 5 ثوان (للأمان)
        setTimeout(() => {
            if (button.disabled) {
                button.innerHTML = originalText;
                button.disabled = false;
            }
        }, 5000);
    }

    // استعادة حالة الزر
    resetButtonLoading(button, originalText) {
        button.innerHTML = originalText;
        button.disabled = false;
    }

    // تحسينات النماذج
    initFormEnhancements() {
        // التحقق في الوقت الحقيقي
        document.querySelectorAll('input, textarea, select').forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldValidation(input));
        });

        // إضافة تأثيرات للعناصر التفاعلية
        this.initInputEffects();
    }

    // تأثيرات الحقول
    initInputEffects() {
        document.querySelectorAll('.form-control').forEach(input => {
            input.addEventListener('focus', () => {
                input.parentElement.classList.add('focused');
            });

            input.addEventListener('blur', () => {
                if (!input.value) {
                    input.parentElement.classList.remove('focused');
                }
            });
        });
    }

    // التحقق من الحقل
    validateField(field) {
        const value = field.value.trim();
        const isRequired = field.hasAttribute('required');

        field.classList.remove('is-valid', 'is-invalid');

        if (isRequired && !value) {
            field.classList.add('is-invalid');
            this.showFieldError(field, 'هذا الحقل مطلوب');
            return false;
        }

        // تحقق إضافي حسب نوع الحقل
        if (field.type === 'email' && value && !this.isValidEmail(value)) {
            field.classList.add('is-invalid');
            this.showFieldError(field, 'يرجى إدخال بريد إلكتروني صحيح');
            return false;
        }

        if (field.type === 'tel' && value && !this.isValidPhone(value)) {
            field.classList.add('is-invalid');
            this.showFieldError(field, 'يرجى إدخال رقم هاتف صحيح');
            return false;
        }

        if (value) {
            field.classList.add('is-valid');
            this.clearFieldError(field);
        }

        return true;
    }

    // عرض خطأ الحقل
    showFieldError(field, message) {
        this.clearFieldError(field);

        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback d-block';
        errorDiv.textContent = message;

        field.parentElement.appendChild(errorDiv);
    }

    // مسح خطأ الحقل
    clearFieldError(field) {
        const existingError = field.parentElement.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
    }

    // مسح التحقق
    clearFieldValidation(field) {
        field.classList.remove('is-valid', 'is-invalid');
        this.clearFieldError(field);
    }

    // العناصر التفاعلية
    initInteractiveElements() {
        // إضافة تأثيرات Hover للبطاقات
        this.initCardInteractions();

        // تحسينات التنقل
        this.initNavigationEnhancements();

        // تحميل الصور الكسول
        this.initLazyLoading();
    }

    // تفاعلات البطاقات
    initCardInteractions() {
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-8px)';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
            });
        });
    }

    // تحسينات التنقل
    initNavigationEnhancements() {
        // إغلاق القائمة المتنقلة عند النقر على رابط
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            link.addEventListener('click', () => {
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse.classList.contains('show')) {
                    bootstrap.Collapse.getInstance(navbarCollapse).hide();
                }
            });
        });
    }

    // التحميل الكسول للصور
    initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    // تحسينات الأداء
    initPerformanceOptimizations() {
        // منع السلوك الافتراضي للروابط الفارغة
        document.querySelectorAll('a[href="#"]').forEach(link => {
            link.addEventListener('click', (e) => e.preventDefault());
        });
    }

    // التحقق من البريد الإلكتروني
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // التحقق من رقم الهاتف
    isValidPhone(phone) {
        const phoneRegex = /^[\+]?[0-9]{10,15}$/;
        return phoneRegex.test(phone.replace(/\s/g, ''));
    }
}

// نظام الإشعارات المحسن
class NotificationSystem {
    constructor() {
        this.container = this.createContainer();
        this.init();
    }

    createContainer() {
        let container = document.getElementById('notification-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notification-container';
            container.style.cssText = `
                position: fixed;
                top: 100px;
                right: 20px;
                z-index: 1060;
                min-width: 300px;
            `;
            document.body.appendChild(container);
        }
        return container;
    }

    init() {
        // يمكن إضافة تهيئة إضافية هنا
    }

    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show`;
        notification.style.cssText = 'margin-bottom: 10px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        this.container.appendChild(notification);

        // إضافة تأثير ظهور
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // إزالة تلقائية
        if (duration > 0) {
            setTimeout(() => {
                this.remove(notification);
            }, duration);
        }

        return notification;
    }

    remove(notification) {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }

    success(message, duration = 5000) {
        return this.show(message, 'success', duration);
    }

    error(message, duration = 5000) {
        return this.show(message, 'danger', duration);
    }

    warning(message, duration = 5000) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration = 5000) {
        return this.show(message, 'info', duration);
    }
}

// نظام البحث والتصفية المتقدم
class AdvancedSearch {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            searchFields: [],
            filterFields: [],
            ...options
        };
        this.init();
    }

    init() {
        this.createSearchInterface();
        this.bindEvents();
    }

    createSearchInterface() {
        const searchHTML = `
            <div class="search-filter-container mb-4">
                <div class="row g-3">
                    <div class="col-md-6">
                        <div class="search-box">
                            <input type="text" class="form-control" placeholder="البحث..." id="searchInput">
                            <i class="bi bi-search search-icon"></i>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <select class="form-select" id="categoryFilter">
                            <option value="">جميع الفئات</option>
                            ${this.options.filterFields.map(field =>
            `<option value="${field.value}">${field.label}</option>`
        ).join('')}
                        </select>
                    </div>
                    <div class="col-md-3">
                        <select class="form-select" id="statusFilter">
                            <option value="">جميع الحالات</option>
                            <option value="new">جديد</option>
                            <option value="in_progress">قيد المعالجة</option>
                            <option value="completed">مكتمل</option>
                        </select>
                    </div>
                </div>
            </div>
        `;

        this.container.insertAdjacentHTML('beforebegin', searchHTML);
    }

    bindEvents() {
        const searchInput = document.getElementById('searchInput');
        const categoryFilter = document.getElementById('categoryFilter');
        const statusFilter = document.getElementById('statusFilter');

        let timeout;

        searchInput.addEventListener('input', (e) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                this.performSearch();
            }, 300);
        });

        categoryFilter.addEventListener('change', () => this.performSearch());
        statusFilter.addEventListener('change', () => this.performSearch());
    }

    performSearch() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const category = document.getElementById('categoryFilter').value;
        const status = document.getElementById('statusFilter').value;

        const items = this.container.querySelectorAll('.searchable-item');

        items.forEach(item => {
            const itemText = item.textContent.toLowerCase();
            const itemCategory = item.dataset.category || '';
            const itemStatus = item.dataset.status || '';

            const matchesSearch = !searchTerm || itemText.includes(searchTerm);
            const matchesCategory = !category || itemCategory === category;
            const matchesStatus = !status || itemStatus === status;

            if (matchesSearch && matchesCategory && matchesStatus) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    }
}



// تهيئة كل شيء عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function () {
    // تعيين السنة الحالية
    document.getElementById('currentYear').textContent = new Date().getFullYear();

    // تهيئة تحسينات تجربة المستخدم
    window.uxEnhancements = new UXEnhancements();

    // تهيئة نظام الإشعارات
    window.notifications = new NotificationSystem();

    // تهيئة العدادات
    initCounters();

    // إضافة تأثيرات إضافية
    initAdditionalEffects();
});

// وظائف مساعدة إضافية
function initAdditionalEffects() {
    // إضافة تأثيرات للصور
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('load', function () {
            this.style.opacity = '1';
        });

        img.style.opacity = '0';
        img.style.transition = 'opacity 0.3s ease';
    });
}
// وظيفة عداد الأرقام
function initCounters() {
    const counters = document.querySelectorAll('[data-count]');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-count'));
                const duration = 2000; // مدة العد بالمللي ثانية
                const step = target / (duration / 16); // 60 إطار في الثانية
                let current = 0;

                const timer = setInterval(() => {
                    current += step;
                    if (current >= target) {
                        current = target;
                        clearInterval(timer);
                    }
                    counter.textContent = Math.floor(current);
                }, 16);

                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => {
        observer.observe(counter);
    });
}

// وظيفة تأثيرات الظهور عند التمرير
function initScrollEffects() {
    const fadeElements = document.querySelectorAll('.fade-in');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    fadeElements.forEach(element => {
        observer.observe(element);
    });
}

// وظيفة التنقل السلس
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // تعويض شريط التنقل

                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// وظيفة لإظهار رسائل التنبيه
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertContainer.style.cssText = 'top: 100px; right: 20px; z-index: 1050; min-width: 300px;';
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(alertContainer);

    // إزالة التنبيه تلقائياً بعد 5 ثوان
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.parentNode.removeChild(alertContainer);
        }
    }, 5000);
}

// وظيفة للتحقق من صحة البريد الإلكتروني
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// وظيفة للتحقق من صحة رقم الهاتف (نسخة مبسطة)
function isValidPhone(phone) {
    const phoneRegex = /^[\+]?[0-9]{10,15}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
}