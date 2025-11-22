// تهيئة صفحة المشاريع
document.addEventListener('DOMContentLoaded', function () {
    loadProjects();
    initFilterButtons();
    initSorting();
    initLoadMore();
    updateProjectsCount();
});

// تحميل وعرض المشاريع من الـ API
async function loadProjects(filter = 'all', sort = 'newest', limit = 6) {
    try {
        const response = await fetch('/api/projects');
        const projectsData = await response.json();

        const container = document.getElementById('projectsContainer');
        container.innerHTML = '';

        let filteredProjects = filter === 'all'
            ? projectsData
            : projectsData.filter(project => project.category === filter);

        // تطبيق الترتيب
        filteredProjects = sortProjects(filteredProjects, sort);

        // تطبيق الحد
        const displayedProjects = filteredProjects.slice(0, limit);

        if (displayedProjects.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="bi bi-inbox display-1 text-muted mb-3"></i>
                    <h4 class="text-muted">لا توجد مشاريع</h4>
                    <p class="text-muted">لم نعثر على مشاريع تطابق معايير البحث</p>
                </div>
            `;
            return;
        }

        displayedProjects.forEach(project => {
            const projectCard = createProjectCard(project);
            container.appendChild(projectCard);
        });

        updateProjectsCount(displayedProjects.length);
    } catch (error) {
        console.error("خطأ في تحميل المشاريع:", error);
        document.getElementById('projectsContainer').innerHTML = `
            <div class="col-12 text-center py-5">
                <h4 class="text-danger">حدث خطأ أثناء تحميل المشاريع</h4>
            </div>
        `;
    }
}

// إنشاء بطاقة مشروع محسنة
function createProjectCard(project) {
    const col = document.createElement('div');
    col.className = 'col-md-6 col-lg-4 mb-4 stagger-item';

    const statusClass = getStatusClass(project.status);
    const statusText = getStatusText(project.status);

    // التأكد من أن مسار الصورة يبدأ بـ `/static/`
    const imageUrl = project.image_url.startsWith('/static/') ? project.image_url : `/static/${project.image_url}`;

    col.innerHTML = `
        <div class="card project-card h-100 hover-lift" data-category="${project.category}">
            <div class="project-image-container">
                <img src="${imageUrl}" class="card-img-top" alt="${project.title}">
                <div class="project-overlay">
                    <div class="project-links">
                        <button class="btn btn-light btn-sm me-2" onclick="showProjectDetails(${project.id})" title="عرض التفاصيل">
                            <i class="bi bi-eye"></i>
                        </button>
                        ${project.demo ? `<a href="${project.demo}" class="btn btn-primary btn-sm" target="_blank" title="عرض التجربة">
                            <i class="bi bi-play-circle"></i>
                        </a>` : ''}
                    </div>
                </div>
                <span class="project-category">${getCategoryName(project.category)}</span>
                <span class="project-status ${statusClass}">${statusText}</span>
            </div>
            <div class="project-content">
                <h5 class="project-title">${project.title}</h5>
                <p class="project-description">${project.description}</p>
                
                <div class="project-tech mb-3">
                    ${project.technologies ? JSON.parse(project.technologies).slice(0, 3).map(tech =>
        `<span class="tech-badge">${tech}</span>`
    ).join('') : ''}
                    ${project.technologies && JSON.parse(project.technologies).length > 3 ?
            `<span class="tech-badge">+${JSON.parse(project.technologies).length - 3}</span>` : ''
        }
                </div>
                
                <div class="project-meta">
                    <div class="project-client">
                        <i class="bi bi-building me-1"></i>
                        ${project.client || 'N/A'}
                    </div>
                    <div class="project-duration">
                        <i class="bi bi-calendar me-1"></i>
                        ${project.duration || 'N/A'}
                    </div>
                </div>
                
                <div class="project-actions">
                    <button class="btn btn-outline-primary btn-sm flex-fill" onclick="showProjectDetails(${project.id})">
                        <i class="bi bi-info-circle me-1"></i>تفاصيل
                    </button>
                    ${project.link ? `<a href="${project.link}" class="btn btn-primary btn-sm" target="_blank">
                        <i class="bi bi-link me-1"></i>زيارة
                    </a>` : ''}
                </div>
            </div>
        </div>
    `;

    return col;
}

// تهيئة أزرار التصفية
function initFilterButtons() {
    const filterButtons = document.querySelectorAll('.btn-filter');

    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            // إزالة النشاط من جميع الأزرار
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // إضافة النشاط للزر المختار
            this.classList.add('active');
            // تصفية المشاريع
            const filter = this.getAttribute('data-filter');
            const sort = document.getElementById('sortProjects').value;
            loadProjects(filter, sort);
        });
    });
}

// تهيئة الترتيب
function initSorting() {
    const sortSelect = document.getElementById('sortProjects');
    sortSelect.addEventListener('change', function () {
        const filter = document.querySelector('.btn-filter.active').getAttribute('data-filter');
        loadProjects(filter, this.value);
    });
}

// تهيئة تحميل المزيد
function initLoadMore() {
    const loadMoreBtn = document.getElementById('loadMoreProjects');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function () {
            // في التطبيق الحقيقي، سيتم جلب المزيد من البيانات من الخادم
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> جاري التحميل...';
            this.disabled = true;

            setTimeout(() => {
                // محاكاة جلب المزيد من البيانات
                const currentFilter = document.querySelector('.btn-filter.active').getAttribute('data-filter');
                const currentSort = document.getElementById('sortProjects').value;
                loadProjects(currentFilter, currentSort, 12); // زيادة الحد

                this.style.display = 'none'; // إخفاء الزر بعد تحميل كل شيء
            }, 1500);
        });
    }
}

// تحديث عدد المشاريع المعروضة
function updateProjectsCount(count) {
    const countElement = document.getElementById('projectsCount');
    if (countElement) {
        countElement.textContent = count;
    }
}

// ترتيب المشاريع
function sortProjects(projects, sortBy) {
    switch (sortBy) {
        case 'newest':
            return projects.sort((a, b) => b.year - a.year);
        case 'oldest':
            return projects.sort((a, b) => a.year - b.year);
        case 'name':
            return projects.sort((a, b) => a.title.localeCompare(b.title, 'ar'));
        default:
            return projects;
    }
}

// الحصول على اسم الفئة بالعربية
function getCategoryName(category) {
    const categories = {
        digital: 'التسويق الرقمي',
        business: 'إدارة الأعمال',
        technology: 'الحلول التقنية',
        project: 'إدارة المشاريع'
    };
    return categories[category] || category;
}

// الحصول على كلاس الحالة
function getStatusClass(status) {
    switch (status) {
        case 'completed': return 'status-completed';
        case 'in-progress': return 'status-in-progress';
        case 'planning': return 'status-planning';
        default: return '';
    }
}

// الحصول على نص الحالة
function getStatusText(status) {
    switch (status) {
        case 'completed': return 'مكتمل';
        case 'in-progress': return 'قيد التنفيذ';
        case 'planning': return 'قيد التخطيط';
        default: return status;
    }
}

// عرض تفاصيل المشروع المحسن
function showProjectDetails(projectId) {
    // نحتاج إلى جلب تفاصيل المشروع من API
    fetch(`/api/projects/${projectId}`)
        .then(response => response.json())
        .then(project => {
            const modalTitle = document.getElementById('projectModalTitle');
            const modalBody = document.getElementById('projectModalBody');

            modalTitle.textContent = project.title;

            const imageUrl = project.image_url.startsWith('/static/') ? project.image_url : `/static/${project.image_url}`;

            modalBody.innerHTML = `
                <div class="project-modal-content">
                    <div class="project-modal-header">
                        <h2 class="project-modal-title">${project.title}</h2>
                        <p class="project-modal-subtitle">${project.description}</p>
                        <div class="d-flex flex-wrap gap-2 mt-3">
                            <span class="badge bg-primary">${getCategoryName(project.category)}</span>
                            <span class="badge ${getStatusClass(project.status)}">${getStatusText(project.status)}</span>
                            <span class="badge bg-secondary">${project.year}</span>
                        </div>
                    </div>
                    
                    <img src="${imageUrl}" class="project-modal-image" alt="${project.title}">
                    
                    <div class="project-modal-details">
                        <div class="detail-item">
                            <span class="detail-label">العميل</span>
                            <span class="detail-value">${project.client || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">مدة التنفيذ</span>
                            <span class="detail-value">${project.duration || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">سنة الإنجاز</span>
                            <span class="detail-value">${project.year || 'N/A'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">الحالة</span>
                            <span class="detail-value">${getStatusText(project.status)}</span>
                        </div>
                    </div>
                    
                    <div class="project-modal-description">
                        <h4 class="mb-3">عن المشروع</h4>
                        <p class="text-muted">${project.description} تم تنفيذ هذا المشروع باستخدام أحدث التقنيات والمعايير لضمان الجودة والأداء المتميز.</p>
                    </div>
                    
                    <div class="project-modal-tech">
                        <h4 class="mb-3">التقنيات المستخدمة</h4>
                        <div class="d-flex flex-wrap gap-2">
                            ${project.technologies ? JSON.parse(project.technologies).map(tech => `
                                <span class="badge bg-light text-dark">${tech}</span>
                            `).join('') : 'N/A'}
                        </div>
                    </div>
                    
                    <div class="project-modal-actions mt-4">
                        ${project.link ? `<a href="${project.link}" class="btn btn-primary me-2" target="_blank">
                            <i class="bi bi-link me-1"></i>زيارة المشروع
                        </a>` : ''}
                        ${project.demo ? `<a href="${project.demo}" class="btn btn-outline-primary me-2" target="_blank">
                            <i class="bi bi-play-circle me-1"></i>عرض التجربة
                        </a>` : ''}
                        <a href="/contact" class="btn btn-success">
                            <i class="bi bi-chat-dots me-1"></i>اطلب مشروع مماثل
                        </a>
                    </div>
                </div>
            `;

            // عرض النموذج
            const projectModal = new bootstrap.Modal(document.getElementById('projectModal'));
            projectModal.show();
        })
        .catch(error => console.error("خطأ في جلب تفاصيل المشروع:", error));
}