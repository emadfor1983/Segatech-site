# دليل نشر تطبيق Segatech

## 🚀 الخيارات المتاحة للنشر

### 1. GitHub Codespaces (للتطوير)

1. اذهب إلى المستودع: https://github.com/emadfor1983/Segatech-site
2. اضغط **Code** → **Codespaces** → **Create codespace**
3. في Terminal:
   ```bash
   cd sega
   pip install -r requirements.txt
   python3 run.py
   ```
4. افتح Port 5000 من تبويب Ports

---

### 2. Render (استضافة مجانية)

1. اذهب إلى: https://render.com
2. سجل دخول بحساب GitHub
3. اضغط **New** → **Blueprint**
4. اختر المستودع: `emadfor1983/Segatech-site`
5. اختر الفرع: `claude/business-analysis-experts-...`
6. Render سيقرأ ملف `render.yaml` تلقائياً
7. اضغط **Apply**

**المتغيرات المطلوبة:**
- `SECRET_KEY` - سيتم توليده تلقائياً
- `ADMIN_CODE` - كود دخول الإدارة (افتراضي: 1234)

---

### 3. Railway (استضافة مجانية)

1. اذهب إلى: https://railway.app
2. سجل دخول بحساب GitHub
3. اضغط **New Project**
4. اختر **Deploy from GitHub repo**
5. اختر: `emadfor1983/Segatech-site`
6. أضف المتغيرات:
   - `SECRET_KEY` = قيمة عشوائية
   - `ADMIN_CODE` = 1234
7. Railway سيستخدم `Procfile` تلقائياً

---

### 4. Heroku (استضافة مدفوعة)

```bash
# تثبيت Heroku CLI
heroku login
heroku create segatech-site

# إضافة المتغيرات
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set ADMIN_CODE=1234

# النشر
git push heroku claude/business-analysis-experts-...:main
```

---

## 🔧 ملاحظات مهمة

1. **قاعدة البيانات**: SQLite تعمل على Render/Railway، لكن البيانات قد تُحذف عند إعادة التشغيل
2. **للإنتاج الحقيقي**: استخدم PostgreSQL أو MySQL
3. **الأمان**: غيّر `SECRET_KEY` و `ADMIN_CODE` في الإنتاج

---

## 📝 الملفات المطلوبة للنشر

- ✅ `requirements.txt` - المكتبات المطلوبة
- ✅ `Procfile` - أوامر التشغيل (Heroku/Railway)
- ✅ `render.yaml` - إعدادات Render
- ✅ `runtime.txt` - إصدار Python
- ✅ `.gitignore` - الملفات المتجاهلة
