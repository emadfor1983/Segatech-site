// إدارة لوحة التحكم
class AdvancedAdminDashboard {
    constructor() {
        this.inquiries = JSON.parse(localStorage.getItem('segatech_inquiries') || '[]');
        this.settings = this.loadSettings();
        this.init();
    }

    init() {
        this.loadDashboardStats();
        this.loadRecentInquiries();
        this.loadNotifications();
        this.setupEventListeners();
        this.initAdvancedFeatures();
        this.initRealTimeUpdates();
    }

    // تحميل الإعدادات
    loadSettings() {
        const defaultSettings = {
            autoRefresh: true,
            notifications: true,
            itemsPerPage: 10,
            theme: 'light'
        };

        return JSON.parse(localStorage.getItem('admin_settings') || JSON.stringify(defaultSettings));
    }

    // حفظ الإعدادات
    saveSettings() {
        localStorage.setItem('admin_settings', JSON.stringify(this.settings));
    }

    // تهيئة الميزات المتقدمة
    initAdvancedFeatures() {
        this.initSearchAndFilter();
        this.initDataExport();
        this.initBulkActions();
        this.initCharts();
    }

    // البحث والتصفية المتقدم
    initSearchAndFilter() {
        const searchOptions = {
            searchFields: ['name', 'email', 'subject', 'message'],
            filterFields: [
                { value: 'technical', label: 'دعم فني' },
                { value: 'sales', label: 'استفسار مبيعات' },
                { value: 'partnership', label: 'شراكة' },
                { value: 'general', label: 'استفسار عام' },
                { value: 'complaint', label: 'شكوى' }
            ]
        };

        this.searchSystem = new AdvancedSearch('recentInquiriesTable', searchOptions);
    }
    // تصدير البيانات
    initDataExport() {
        const exportBtn = document.getElementById('exportData');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportData());
        }
    }

    exportData(format = 'json') {
        const data = {
            inquiries: this.inquiries,
            exportDate: new Date().toISOString(),
            totalRecords: this.inquiries.length
        };

        let content, mimeType, filename;

        switch (format) {
            case 'json':
                content = JSON.stringify(data, null, 2);
                mimeType = 'application/json';
                filename = `inquiries-${new Date().toISOString().split('T')[0]}.json`;
                break;
            case 'csv':
                content = this.convertToCSV(data.inquiries);
                mimeType = 'text/csv';
                filename = `inquiries-${new Date().toISOString().split('T')[0]}.csv`;
                break;
        }

        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);

        window.notifications.success('تم تصدير البيانات بنجاح');
    }

    convertToCSV(data) {
        const headers = ['الاسم', 'البريد الإلكتروني', 'النوع', 'الحالة', 'التاريخ'];
        const rows = data.map(item => [
            item.name,
            item.email,
            this.getCategoryName(item.category),
            this.getStatusText(item.status),
            new Date(item.createdAt).toLocaleDateString('ar-SA')
        ]);

        return [headers, ...rows].map(row =>
            row.map(field => `"${field}"`).join(',')
        ).join('\n');
    }

    // الإجراءات المجمعة
    initBulkActions() {
        const bulkActions = document.getElementById('bulkActions');
        if (bulkActions) {
            bulkActions.addEventListener('change', (e) => {
                const action = e.target.value;
                if (action) {
                    this.performBulkAction(action);
                    e.target.value = '';
                }
            });
        }
    }


    performBulkAction(action) {
        const selectedItems = this.getSelectedItems();

        if (selectedItems.length === 0) {
            window.notifications.warning('يرجى اختيار عناصر لأداء الإجراء');
            return;
        }

        switch (action) {
            case 'mark_completed':
                this.bulkUpdateStatus(selectedItems, 'completed');
                break;
            case 'mark_in_progress':
                this.bulkUpdateStatus(selectedItems, 'in_progress');
                break;
            case 'delete':
                this.bulkDelete(selectedItems);
                break;
        }
    }

    getSelectedItems() {
        return this.inquiries.filter(inq =>
            document.getElementById(`select_${inq.id}`)?.checked
        );
    }

    bulkUpdateStatus(items, status) {
        items.forEach(item => {
            this.updateStatus(item.id, status, false);
        });

        this.refreshData();
        window.notifications.success(`تم تحديث حالة ${items.length} عنصر`);
    }

    bulkDelete(items) {
        if (confirm(`هل أنت متأكد من حذف ${items.length} عنصر؟`)) {
            const idsToDelete = items.map(item => item.id);
            this.inquiries = this.inquiries.filter(inq => !idsToDelete.includes(inq.id));

            localStorage.setItem('segatech_inquiries', JSON.stringify(this.inquiries));
            this.refreshData();
            window.notifications.success('تم الحذف بنجاح');
        }
    }

    // الرسوم البيانية
    initCharts() {
        this.renderInquiriesChart();
        this.renderStatusChart();
    }

    renderInquiriesChart() {
        const ctx = document.getElementById('inquiriesChart');
        if (!ctx) return;

        const monthlyData = this.getMonthlyInquiriesData();

        // استخدام Chart.js إذا كان متوفراً
        if (window.Chart) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: monthlyData.labels,
                    datasets: [{
                        label: 'الاستفسارات الشهرية',
                        data: monthlyData.data,
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        }
    }

    renderStatusChart() {
        const ctx = document.getElementById('statusChart');
        if (!ctx) return;

        const statusData = this.getStatusDistribution();

        if (window.Chart) {
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: statusData.labels,
                    datasets: [{
                        data: statusData.data,
                        backgroundColor: [
                            '#3498db',
                            '#f39c12',
                            '#27ae60'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
    }

    getMonthlyInquiriesData() {
        const last6Months = [];
        for (let i = 5; i >= 0; i--) {
            const date = new Date();
            date.setMonth(date.getMonth() - i);
            last6Months.push(date);
        }

        const labels = last6Months.map(date =>
            date.toLocaleDateString('ar-SA', { month: 'short', year: 'numeric' })
        );

        const data = last6Months.map(date => {
            return this.inquiries.filter(inq => {
                const inquiryDate = new Date(inq.createdAt);
                return inquiryDate.getMonth() === date.getMonth() &&
                    inquiryDate.getFullYear() === date.getFullYear();
            }).length;
        });

        return { labels, data };
    }

    getStatusDistribution() {
        const statusCount = {
            new: this.inquiries.filter(inq => inq.status === 'new').length,
            in_progress: this.inquiries.filter(inq => inq.status === 'in_progress').length,
            completed: this.inquiries.filter(inq => inq.status === 'completed').length
        };

        return {
            labels: ['جديد', 'قيد المعالجة', 'مكتمل'],
            data: [statusCount.new, statusCount.in_progress, statusCount.completed]
        };
    }

    // التحديث في الوقت الحقيقي
    initRealTimeUpdates() {
        if (this.settings.autoRefresh) {
            this.startAutoRefresh();
        }
    }

    startAutoRefresh() {
        setInterval(() => {
            this.checkForNewData();
        }, 30000); // كل 30 ثانية
    }

    checkForNewData() {
        const oldCount = this.inquiries.length;
        const currentInquiries = JSON.parse(localStorage.getItem('segatech_inquiries') || '[]');

        if (currentInquiries.length > oldCount) {
            this.inquiries = currentInquiries;
            this.refreshData();
            window.notifications.info('تم تحديث البيانات ببيانات جديدة');
        }
    }

    refreshData() {
        this.loadDashboardStats();
        this.loadRecentInquiries();
        this.loadNotifications();

        if (this.searchSystem) {
            this.searchSystem.performSearch();
        }
    }

























    // تحميل إحصائيات لوحة التحكم
    loadDashboardStats() {
        const totalInquiries = this.inquiries.length;
        const newInquiries = this.inquiries.filter(inq => inq.status === 'new').length;

        document.getElementById('totalInquiries').textContent = totalInquiries;
        document.getElementById('newInquiries').textContent = newInquiries;
        document.getElementById('inquiriesBadge').textContent = newInquiries;

        // هذه البيانات مؤقتة - سيتم استبدالها ببيانات حقيقية لاحقاً
        document.getElementById('openTickets').textContent = '12';
        document.getElementById('completedProjects').textContent = '45';
        document.getElementById('ticketsBadge').textContent = '12';
    }

    // تحميل الاستفسارات الحديثة
    loadRecentInquiries() {
        const tableBody = document.getElementById('recentInquiriesTable');
        const recentInquiries = this.inquiries
            .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
            .slice(0, 5);

        tableBody.innerHTML = '';

        if (recentInquiries.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted">لا توجد استفسارات</td>
                </tr>
            `;
            return;
        }

        recentInquiries.forEach(inquiry => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${inquiry.name}</td>
                <td>${inquiry.email}</td>
                <td>${this.getCategoryName(inquiry.category)}</td>
                <td>
                    <span class="badge ${this.getStatusBadgeClass(inquiry.status)}">
                        ${this.getStatusText(inquiry.status)}
                    </span>
                </td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="adminDashboard.viewInquiry('${inquiry.id}')">
                        <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-success" onclick="adminDashboard.updateStatus('${inquiry.id}', 'completed')">
                        <i class="bi bi-check"></i>
                    </button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }

    // تحميل الإشعارات
    loadNotifications() {
        const notificationsList = document.getElementById('notificationsList');
        const newInquiriesCount = this.inquiries.filter(inq => inq.status === 'new').length;

        notificationsList.innerHTML = '';

        if (newInquiriesCount > 0) {
            const notificationItem = document.createElement('a');
            notificationItem.href = 'inquiries.html';
            notificationItem.className = 'list-group-item list-group-item-action';
            notificationItem.innerHTML = `
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">استفسارات جديدة</h6>
                    <small>الآن</small>
                </div>
                <p class="mb-1">يوجد ${newInquiriesCount} استفسار جديد يحتاج للرد</p>
            `;
            notificationsList.appendChild(notificationItem);
        }

        // إشعارات افتراضية
        const defaultNotifications = [
            {
                title: 'تحديث النظام',
                time: 'منذ ساعتين',
                message: 'تم تحديث النظام إلى الإصدار 2.1.0'
            },
            {
                title: 'نسخ احتياطي',
                time: 'منذ يوم',
                message: 'تم إنشاء نسخة احتياطية جديدة للبيانات'
            }
        ];

        defaultNotifications.forEach(notif => {
            const notificationItem = document.createElement('a');
            notificationItem.href = '#';
            notificationItem.className = 'list-group-item list-group-item-action';
            notificationItem.innerHTML = `
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">${notif.title}</h6>
                    <small>${notif.time}</small>
                </div>
                <p class="mb-1">${notif.message}</p>
            `;
            notificationsList.appendChild(notificationItem);
        });
    }

    // عرض تفاصيل الاستفسار
    viewInquiry(inquiryId) {
        const inquiry = this.inquiries.find(inq => inq.id === inquiryId);
        if (!inquiry) return;

        // هنا يمكن فتح نافذة عرض التفاصيل
        alert(`تفاصيل الاستفسار:\n\nالاسم: ${inquiry.name}\nالبريد: ${inquiry.email}\nالنوع: ${this.getCategoryName(inquiry.category)}\nالموضوع: ${inquiry.subject}\nالرسالة: ${inquiry.message}`);
    }

    updateStatus(inquiryId, newStatus, showNotification = true) {
        const inquiryIndex = this.inquiries.findIndex(inq => inq.id === inquiryId);
        if (inquiryIndex === -1) return;

        this.inquiries[inquiryIndex].status = newStatus;
        this.inquiries[inquiryIndex].updatedAt = new Date().toISOString();

        localStorage.setItem('segatech_inquiries', JSON.stringify(this.inquiries));

        this.refreshData();

        if (showNotification) {
            window.notifications.success('تم تحديث حالة الاستفسار بنجاح');
        }
    }

    // الحصول على اسم الفئة
    getCategoryName(category) {
        const categories = {
            'technical': 'دعم فني',
            'sales': 'استفسار مبيعات',
            'partnership': 'شراكة',
            'general': 'استفسار عام',
            'complaint': 'شكوى'
        };
        return categories[category] || category;
    }

    // الحصول على كلاس حالة الاستفسار
    getStatusBadgeClass(status) {
        switch (status) {
            case 'new': return 'bg-primary';
            case 'in_progress': return 'bg-warning';
            case 'completed': return 'bg-success';
            default: return 'bg-secondary';
        }
    }

    // الحصول على نص حالة الاستفسار
    getStatusText(status) {
        switch (status) {
            case 'new': return 'جديد';
            case 'in_progress': return 'قيد المعالجة';
            case 'completed': return 'مكتمل';
            default: return status;
        }
    }

    // إعداد مستمعي الأحداث
    setupEventListeners() {
        // يمكن إضافة مستمعي الأحداث الإضافية هنا
    }
}

// تهيئة لوحة التحكم عند تحميل الصفحة
let adminDashboard;
document.addEventListener('DOMContentLoaded', function() {
    adminDashboard = new AdvancedAdminDashboard();
});