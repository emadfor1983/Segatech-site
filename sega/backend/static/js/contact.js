document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contactForm');
    if (!form) {
        console.warn('contactForm not found');
        return;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        console.log('🚀 submit event fired');

        // لو عندك دالة validateForm في main.js، استخدمها
        let isValid = true;
        if (typeof validateForm === 'function') {
            isValid = validateForm(form);
        }

        if (!isValid) {
            console.warn('❗ form not valid');
            return;
        }

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> جاري الإرسال...';
        submitBtn.disabled = true;

        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            category: document.getElementById('category').value,
            subject: document.getElementById('subject').value,
            message: document.getElementById('message').value
        };

        console.log('📦 sending data:', formData);

        try {
            const response = await fetch('/api/inquiries', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            console.log('📥 response status:', response.status);
            const result = await response.json();
            console.log('📥 response body:', result);

            if (result.success) {
                alert('✅ تم إرسال رسالتك بنجاح');
                form.reset();
            } else {
                throw new Error(result.message || 'حدث خطأ غير متوقع');
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            alert('❌ حدث خطأ أثناء إرسال الرسالة:\n' + error.message);
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    });
});
