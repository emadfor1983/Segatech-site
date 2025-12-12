from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from dotenv import load_dotenv
import os
import json
from werkzeug.utils import secure_filename





app = Flask(__name__)
load_dotenv()


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['ADMIN_CODE'] = os.getenv('ADMIN_CODE')
# 🔹 إعداد مسار قاعدة البيانات بشكل آمن وواضح
BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # مجلد backend مثلاً
DB_DIR = os.path.join(BASE_DIR, '..', 'database')              # مجلد database فوق backend
os.makedirs(DB_DIR, exist_ok=True)                             # إنشاء المجلد لو مش موجود

# ✅ مجلد صور الشركاء
PARTNERS_UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'assets', 'images', 'partners')
os.makedirs(PARTNERS_UPLOAD_FOLDER, exist_ok=True)

# ✅ مجلد صور المشاريع
PROJECTS_UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'assets', 'images', 'projects')
os.makedirs(PROJECTS_UPLOAD_FOLDER, exist_ok=True)

# ✅ مجلد صور العملاء
CLIENTS_UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'assets', 'images', 'clients')
os.makedirs(CLIENTS_UPLOAD_FOLDER, exist_ok=True)

# ✅ مجلد صور خبراء تحليل الأعمال
EXPERTS_UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'assets', 'images', 'experts')
os.makedirs(EXPERTS_UPLOAD_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, 'segatech.db')                  # المسار الكامل للملف
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)
# نموذج الاستفسارات
class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    category = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'category': self.category,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# نموذج المشاريع
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    technologies = db.Column(db.Text)  # JSON string
    image_url = db.Column(db.String(300))
    client = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    status = db.Column(db.String(20), default='completed')
    year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# نموذج المستخدمين للإدارة
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200))                  # المسار الذي تمت زيارته
    ip_address = db.Column(db.String(50))             # IP
    user_agent = db.Column(db.String(300))            # نوع المتصفح
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(30))
    company = db.Column(db.String(150))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ حقول جديدة
    logo_url = db.Column(db.String(300))              # مسار/رابط شعار العميل
    is_active = db.Column(db.Boolean, default=True)   # يظهر في الموقع أو لا
    sort_order = db.Column(db.Integer, default=0)     # لترتيب عرض العملاء


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(300), nullable=False)
    type = db.Column(db.String(50), default='info')  # info, success, warning, error
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SiteStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # الإحصائيات الأساسية
    completed_projects = db.Column(db.Integer, default=0)   # مشروع مكتمل
    happy_clients = db.Column(db.Integer, default=0)        # عميل راضٍ
    years_experience = db.Column(db.Integer, default=0)     # سنوات خبرة
    support_hours = db.Column(db.Integer, default=0)        # ساعات دعم

    # الإحصائيات الإضافية
    team_members = db.Column(db.Integer, default=0)         # فريق متخصص
    countries = db.Column(db.Integer, default=0)            # دولة حول العالم
    finished_projects = db.Column(db.Integer, default=0)    # مشروع منجز

class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), default='Segatech')
    official_email = db.Column(db.String(200), default='ceo@segatech.site')
    admin_code = db.Column(db.String(100), default='1234')

    phone_number = db.Column(db.String(50), default='+963 968 000 580')
    whatsapp_number = db.Column(db.String(50), default='+963968000580')

    address = db.Column(db.String(200), default='سوريا - دمشق')

    facebook = db.Column(db.String(300))
    instagram = db.Column(db.String(300))
    linkedin = db.Column(db.String(300))
    github = db.Column(db.String(300))

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)         # الاسم
    job_title = db.Column(db.String(150), nullable=False)    # المسمّى الوظيفي
    bio = db.Column(db.Text)                                 # نبذة قصيرة
    image_url = db.Column(db.String(300))                    # رابط الصورة

    linkedin = db.Column(db.String(300))
    twitter = db.Column(db.String(300))
    github = db.Column(db.String(300))
    dribbble = db.Column(db.String(300))

    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)            # لترتيب الظهور
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)       # اسم الشريك
    logo_url = db.Column(db.String(300), nullable=False)   # مسار الشعار داخل static
    website = db.Column(db.String(300))                    # موقع الشريك (اختياري)
    is_active = db.Column(db.Boolean, default=True)        # يظهر في الموقع أو لا
    sort_order = db.Column(db.Integer, default=0)          # ترتيب العرض
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BusinessExpert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)       # اسم الخبير
    job_title = db.Column(db.String(150), nullable=False)  # المسمى الوظيفي
    specialization = db.Column(db.String(200))             # التخصص (مثل: تحليل الأعمال، إدارة المشاريع)
    bio = db.Column(db.Text)                               # نبذة عن الخبير
    expertise_areas = db.Column(db.Text)                   # مجالات الخبرة (JSON أو نص)
    image_url = db.Column(db.String(300))                  # صورة الخبير

    # معلومات الاتصال
    email = db.Column(db.String(100))
    phone = db.Column(db.String(30))

    # روابط التواصل الاجتماعي
    linkedin = db.Column(db.String(300))
    twitter = db.Column(db.String(300))
    github = db.Column(db.String(300))
    website = db.Column(db.String(300))

    # معلومات إضافية
    years_experience = db.Column(db.Integer, default=0)    # سنوات الخبرة
    certifications = db.Column(db.Text)                    # الشهادات (JSON أو نص)

    # حالة العرض
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def create_notification(title, message, type='info'):
    notif = Notification(
        title=title,
        message=message,
        type=type
    )
    db.session.add(notif)
    db.session.commit()

def get_site_settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings(
            company_name='Segatech',
            official_email='ceo@segatech.site',
            admin_code=app.config.get('ADMIN_CODE', '1234')
        )
        db.session.add(settings)
        db.session.commit()
    return settings

@app.route('/admin/partners')
def admin_partners():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    partners = Partner.query.order_by(Partner.sort_order.asc(),
                                      Partner.created_at.asc()).all()
    return render_template('admin_partners.html', partners=partners)

@app.route('/admin/partners/new', methods=['GET', 'POST'])
def admin_partner_new():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()

        # رفع ملف الشعار (اختياري)
        logo_path = None
        file = request.files.get('logo_file')

        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(PARTNERS_UPLOAD_FOLDER, filename)
            file.save(save_path)
            # مسار الشعار داخل static
            logo_path = f'assets/images/partners/{filename}'
        else:
            # أو كتابة المسار يدويًا
            logo_path = (request.form.get('logo_url') or '').strip()

        if not name or not logo_path:
            flash('اسم الشريك ورابط الشعار حقول إلزامية', 'danger')
            return render_template('admin_partner_form.html', partner=None)

        partner = Partner(
            name=name,
            logo_url=logo_path,
            website=request.form.get('website') or None,
            sort_order=int(request.form.get('sort_order') or 0),
            is_active=True if request.form.get('is_active') == 'on' else False
        )
        db.session.add(partner)
        db.session.commit()

        create_notification(
            title='شريك جديد',
            message=f'تم إضافة الشريك: {partner.name}',
            type='success'
        )

        flash('تم إضافة شريك جديد بنجاح', 'success')
        return redirect(url_for('admin_partners'))

    return render_template('admin_partner_form.html', partner=None)

@app.route('/admin/partners/<int:partner_id>/edit', methods=['GET', 'POST'])
def admin_partner_edit(partner_id):
    ...
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        website = (request.form.get('website') or '').strip()
        sort_order = int(request.form.get('sort_order') or 0)
        is_active = True if request.form.get('is_active') == 'on' else False

        # ملف جديد؟
        file = request.files.get('logo_file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(PARTNERS_UPLOAD_FOLDER, filename)
            file.save(save_path)
            partner.logo_url = f'assets/images/partners/{filename}'
        else:
            # أو تعديل المسار نصيًا
            logo_url = (request.form.get('logo_url') or '').strip()
            if logo_url:
                partner.logo_url = logo_url

        partner.name = name
        partner.website = website or None
        partner.sort_order = sort_order
        partner.is_active = is_active

        db.session.commit()
        ...

@app.route('/admin/partners/<int:partner_id>/delete', methods=['POST'])
def admin_partner_delete(partner_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    partner = Partner.query.get_or_404(partner_id)
    name = partner.name

    db.session.delete(partner)
    db.session.commit()

    create_notification(
        title='حذف شريك',
        message=f'تم حذف الشريك: {name}',
        type='warning'
    )

    flash('تم حذف الشريك بنجاح', 'warning')
    return redirect(url_for('admin_partners'))

def get_site_stats():
    stats = SiteStats.query.first()
    if not stats:
        stats = SiteStats(
            completed_projects=150,
            happy_clients=50,
            years_experience=5,
            support_hours=24,
            team_members=20,
            countries=15,
            finished_projects=500
        )
        db.session.add(stats)
        db.session.commit()
    return stats

@app.context_processor
def inject_settings():
    settings = get_site_settings()
    return dict(site_settings=settings)

# إنشاء الجداول
@app.before_request
def create_tables():
    db.create_all()


@app.before_request
def log_visit():
    # لا نسجل زيارات الـ static ولا صفحات الأدمن ولا الـ API
    if request.path.startswith('/static'):
        return
    if request.path.startswith('/admin'):
        return
    if request.path.startswith('/api'):
        return

    visit = Visit(
        path=request.path,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent', '')
    )
    db.session.add(visit)
    db.session.commit()

# الروابط الأساسية
@app.route('/')
def index():
    stats_public = get_site_stats()
    clients = Client.query.filter_by(is_active=True) \
                          .order_by(Client.sort_order.asc(),
                                    Client.created_at.asc()) \
                          .all()

    # ★ جلب 3 مشاريع فقط بالترتيب من الأحدث إلى الأقدم
    latest_projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()

    return render_template(
        'index.html',
        stats_public=stats_public,
        clients=clients,
        latest_projects=latest_projects   # ★ إرسال المشاريع للقالب
    )

@app.route('/about')
def about():
    stats_public = get_site_stats()

    team_members = TeamMember.query.filter_by(is_active=True) \
                                   .order_by(TeamMember.sort_order.asc(),
                                             TeamMember.created_at.asc()) \
                                   .all()
    return render_template('about.html',
                           stats_public=stats_public,
                           team_members=team_members)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/projects')
def projects():
    partners = Partner.query.filter_by(is_active=True) \
                            .order_by(Partner.sort_order.asc(),
                                      Partner.created_at.asc()) \
                            .all()

    # 🔍 Debug في الكونسول
    print("==== PARTNERS DEBUG ====")
    print("Partners count:", len(partners))
    for p in partners:
        print(p.id, p.name, p.logo_url, p.is_active)

    return render_template(
        'projects.html',
        partners=partners
    )

@app.route('/contact')
def contact():
    return render_template('contact.html')
    


# API للاستفسارات
@app.route('/api/inquiries', methods=['GET', 'POST'])
def handle_inquiries():
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            inquiry = Inquiry(
                name=data['name'],
                email=data['email'],
                phone=data.get('phone', ''),
                category=data['category'],
                subject=data['subject'],
                message=data['message']
            )
            
            db.session.add(inquiry)
            db.session.commit()
            create_notification(
    title='استفسار جديد',
    message=f'تم استلام استفسار جديد من {inquiry.name}',
    type='success'
)
            
            return jsonify({
                'success': True,
                'message': 'تم إرسال استفسارك بنجاح',
                'inquiry_id': inquiry.id
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'حدث خطأ: {str(e)}'
            }), 400
    
    else:  # GET request
        inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
        return jsonify([inquiry.to_dict() for inquiry in inquiries])

# API للمشاريع (تم تعريفه مرة واحدة فقط)
@app.route('/api/projects')
def get_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    projects_data = []
    
    for project in projects:
        projects_data.append({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'category': project.category,
            'technologies': project.technologies,
            'image_url': project.image_url,
            'client': project.client,
            'duration': project.duration,
            'status': project.status,
            'year': project.year
        })
    
    return jsonify(projects_data)

# API لمشروع واحد
@app.route('/api/projects/<int:project_id>')
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'category': project.category,
        'technologies': project.technologies,
        'image_url': project.image_url,
        'client': project.client,
        'duration': project.duration,
        'status': project.status,
        'year': project.year
    })


    # حماية لوحة التحكم
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # لو هو أصلاً مسجل دخول كأدمن، دخله مباشرة للوحة التحكم
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard_page'))

    error = None

    # قراءة الإعدادات من قاعدة البيانات
    settings = get_site_settings()
    expected_code = settings.admin_code or app.config.get('ADMIN_CODE')

    if request.method == 'POST':
        code = request.form.get('code')

        if code == expected_code:
            session['is_admin'] = True
            next_page = request.args.get('next') or url_for('admin_dashboard_page')
            return redirect(next_page)
        else:
            error = 'رمز الدخول غير صحيح، حاول مرة أخرى.'

    return render_template('admin_login.html', error=error)


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin/inquiries')
def admin_inquiries():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return render_template('admin_inquiries.html', inquiries=inquiries)


@app.route('/admin/projects')
def admin_projects():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin_projects.html', projects=projects)


@app.route('/admin/projects/new', methods=['GET', 'POST'])
def admin_project_new():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        raw_technologies = request.form.get('technologies', '').strip()
        image_file = request.files.get('image_file')  # الحصول على الصورة المرفوعة
        client = request.form.get('client')
        duration = request.form.get('duration')
        status = request.form.get('status') or 'completed'
        year = request.form.get('year') or None

        # 👇 تحويل التقنيات من نص مفصول بفواصل إلى JSON
        tech_list = [t.strip() for t in raw_technologies.split(',') if t.strip()]
        technologies_json = json.dumps(tech_list) if tech_list else None

        # معالجة الصورة
        image_url = None
        if image_file and image_file.filename:
            # تأكد من أن المجلد موجود
            os.makedirs(PROJECTS_UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(PROJECTS_UPLOAD_FOLDER, filename)
            image_file.save(save_path)
            image_url = f'assets/images/projects/{filename}'  # حفظ المسار داخل قاعدة البيانات

        project = Project(
            title=title,
            description=description,
            category=category,
            technologies=technologies_json,
            image_url=image_url,
            client=client,
            duration=duration,
            status=status,
            year=int(year) if year else None
        )

        db.session.add(project)
        db.session.commit()

        create_notification(
            title='مشروع جديد',
            message=f'تم إضافة مشروع: {project.title}',
            type='info'
        )

        flash('تم إضافة المشروع بنجاح', 'success')
        return redirect(url_for('admin_projects'))

    # عند GET
    return render_template('admin_project_form.html', project=None, technologies_text='')

@app.route('/admin/projects/<int:project_id>/edit', methods=['GET', 'POST'])
def admin_project_edit(project_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        # تحديث بيانات المشروع
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.category = request.form.get('category')

        raw_technologies = request.form.get('technologies', '').strip()
        tech_list = [t.strip() for t in raw_technologies.split(',') if t.strip()]
        project.technologies = json.dumps(tech_list) if tech_list else None

        # معالجة الصورة الجديدة إذا تم رفعها
        image_file = request.files.get('image_file')
        if image_file and image_file.filename:
            # تأكد من أن المجلد موجود
            os.makedirs(PROJECTS_UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(PROJECTS_UPLOAD_FOLDER, filename)
            image_file.save(save_path)
            project.image_url = f'assets/images/projects/{filename}'  # حفظ المسار الجديد داخل قاعدة البيانات

        # تحديث باقي الحقول
        project.client = request.form.get('client')
        project.duration = request.form.get('duration')
        project.status = request.form.get('status') or project.status
        year = request.form.get('year') or None
        project.year = int(year) if year else None

        # حفظ التعديلات في قاعدة البيانات
        db.session.commit()

        create_notification(
            title='تعديل مشروع',
            message=f'تم تعديل المشروع: {project.title}',
            type='info'
        )

        flash('تم تحديث المشروع بنجاح', 'success')
        return redirect(url_for('admin_projects'))

    # عند GET: تجهيز النص الظاهر في حقل التقنيات
    technologies_text = ''
    if project.technologies:
        try:
            tech_list = json.loads(project.technologies)
            technologies_text = ', '.join(tech_list)
        except Exception:
            technologies_text = project.technologies  # لو كان قديم أو غير JSON

    return render_template('admin_project_form.html', project=project, technologies_text=technologies_text)


@app.route('/admin/projects/<int:project_id>/delete', methods=['POST'])
def admin_project_delete(project_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    project = Project.query.get_or_404(project_id)

    db.session.delete(project)
    db.session.commit()

    create_notification(
        title='حذف مشروع',
        message=f'تم حذف المشروع: {project.title}',
        type='warning'
    )

    return redirect(url_for('admin_projects'))


@app.route('/admin/clients')
def admin_clients():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    clients = Client.query.order_by(Client.created_at.desc()).all()
    return render_template('admin_clients.html', clients=clients)


@app.route('/admin/clients/new', methods=['GET', 'POST'])
def admin_client_new():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()

        # ✅ استرجاع الحقول العادية
        email = (request.form.get('email') or '').strip()
        phone = (request.form.get('phone') or '').strip()
        company = (request.form.get('company') or '').strip()
        notes = request.form.get('notes')
        sort_order = int(request.form.get('sort_order') or 0)
        is_active = True if request.form.get('is_active') == 'on' else False

        # ✅ معالجة ملف الشعار
        logo_path = None
        file = request.files.get('logo_file')

        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(CLIENTS_UPLOAD_FOLDER, filename)
            file.save(save_path)
            # مسار النسبي داخل static
            logo_path = f'assets/images/clients/{filename}'

        client = Client(
            name=name,
            email=email or None,
            phone=phone or None,
            company=company or None,
            notes=notes,
            logo_url=logo_path,          # ✅ الآن من الملف المرفوع
            sort_order=sort_order,
            is_active=is_active
        )

        db.session.add(client)
        db.session.commit()

        create_notification(
            title='عميل جديد',
            message=f'تم إضافة العميل: {client.name}',
            type='success'
        )

        flash('تم إضافة عميل جديد بنجاح', 'success')
        return redirect(url_for('admin_clients'))

    return render_template('admin_client_form.html', client=None)

@app.route('/admin/clients/<int:client_id>/edit', methods=['GET', 'POST'])
def admin_client_edit(client_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    client = Client.query.get_or_404(client_id)

    if request.method == 'POST':
        client.name = request.form.get('name')
        client.email = request.form.get('email')
        client.phone = request.form.get('phone')
        client.company = request.form.get('company')
        client.notes = request.form.get('notes')
        client.sort_order = int(request.form.get('sort_order') or 0)
        client.is_active = True if request.form.get('is_active') == 'on' else False

        # ✅ لو تم رفع شعار جديد نستبدله
        file = request.files.get('logo_file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(CLIENTS_UPLOAD_FOLDER, filename)
            file.save(save_path)
            client.logo_url = f'assets/images/clients/{filename}'

        db.session.commit()

        create_notification(
            title='تعديل عميل',
            message=f'تم تعديل بيانات العميل: {client.name}',
            type='info'
        )

        flash('تم تحديث بيانات العميل بنجاح', 'success')
        return redirect(url_for('admin_clients'))

    return render_template('admin_client_form.html', client=client)

@app.route('/admin/clients/<int:client_id>/delete', methods=['POST'])
def admin_client_delete(client_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()

    create_notification(
        title='حذف عميل',
        message=f'تم حذف العميل: {client.name}',
        type='warning'
    )

    return redirect(url_for('admin_clients'))



@app.route('/admin/dashboard')
def admin_dashboard_page():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    today = date.today()
    start_today = datetime(today.year, today.month, today.day)

    total_visits = Visit.query.count()
    today_visits = Visit.query.filter(Visit.created_at >= start_today).count()

    total_inquiries = Inquiry.query.count()
    today_inquiries = Inquiry.query.filter(Inquiry.created_at >= start_today).count()
    total_projects = Project.query.count()

    recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(5).all()
    notifications = Notification.query.order_by(Notification.created_at.desc()).limit(5).all()

    stats = {
        'total_visits': total_visits,
        'today_visits': today_visits,
        'total_inquiries': total_inquiries,
        'today_inquiries': today_inquiries,
        'total_projects': total_projects,
    }

    return render_template(
        'dashboard.html',
        stats=stats,
        recent_inquiries=recent_inquiries,
        notifications=notifications
    )


@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    stats = get_site_stats()
    settings = get_site_settings()

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        # ✅ حفظ الإعدادات العامة (اسم الشركة + البريد + رمز الأدمن)
        if form_type == 'general':
            settings.company_name = request.form.get('company_name') or settings.company_name
            settings.official_email = request.form.get('official_email') or settings.official_email
            settings.admin_code = request.form.get('admin_code') or settings.admin_code

            db.session.commit()

            create_notification(
                title='تحديث الإعدادات العامة',
                message='تم تحديث اسم الشركة والبريد الرسمي ورمز الدخول',
                type='success'
            )

            flash('تم حفظ الإعدادات العامة بنجاح', 'success')
            return redirect(url_for('admin_settings'))

        # ✅ حفظ إعدادات الاتصال والروابط
        elif form_type == 'contact':
            settings.phone_number   = request.form.get('phone_number')   or settings.phone_number
            settings.whatsapp_number = request.form.get('whatsapp_number') or settings.whatsapp_number
            settings.address        = request.form.get('address')        or settings.address

            settings.facebook = request.form.get('facebook') or None
            settings.instagram = request.form.get('instagram') or None
            settings.linkedin = request.form.get('linkedin') or None
            settings.github = request.form.get('github') or None

            db.session.commit()

            create_notification(
                title='تحديث بيانات الاتصال',
                message='تم تحديث أرقام الاتصال وروابط التواصل الاجتماعي',
                type='success'
            )

            flash('تم حفظ إعدادات الاتصال والروابط بنجاح', 'success')
            return redirect(url_for('admin_settings'))

        # ✅ حفظ إعدادات الإحصائيات
        elif form_type == 'stats':
            stats.completed_projects = int(request.form.get('completed_projects') or 0)
            stats.happy_clients = int(request.form.get('happy_clients') or 0)
            stats.years_experience = int(request.form.get('years_experience') or 0)
            stats.support_hours = int(request.form.get('support_hours') or 0)

            stats.team_members = int(request.form.get('team_members') or 0)
            stats.countries = int(request.form.get('countries') or 0)
            stats.finished_projects = int(request.form.get('finished_projects') or 0)

            db.session.commit()

            create_notification(
                title='تحديث الإحصائيات',
                message='تم تحديث أرقام الإحصائيات في الصفحة الرئيسية',
                type='success'
            )

            flash('تم حفظ إعدادات الإحصائيات بنجاح', 'success')
            return redirect(url_for('admin_settings'))

    return render_template('admin_settings.html', stats=stats, settings=settings)

@app.route('/admin/team')
def admin_team():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    members = TeamMember.query.order_by(TeamMember.sort_order.asc(),
                                        TeamMember.created_at.asc()).all()
    return render_template('admin_team.html', members=members)


@app.route('/admin/team/new', methods=['GET', 'POST'])
def admin_team_new():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    if request.method == 'POST':
        member = TeamMember(
            name=request.form.get('name'),
            job_title=request.form.get('job_title'),
            bio=request.form.get('bio'),
            image_url=request.form.get('image_url'),
            linkedin=request.form.get('linkedin') or None,
            twitter=request.form.get('twitter') or None,
            github=request.form.get('github') or None,
            dribbble=request.form.get('dribbble') or None,
            sort_order=int(request.form.get('sort_order') or 0),
            is_active=True if request.form.get('is_active') == 'on' else False
        )
        db.session.add(member)
        db.session.commit()

        create_notification(
            title='عضو جديد في الفريق',
            message=f'تم إضافة {member.name} إلى فريق العمل',
            type='success'
        )

        flash('تم إضافة عضو جديد إلى الفريق', 'success')
        return redirect(url_for('admin_team'))

    return render_template('admin_team_form.html', member=None)


@app.route('/admin/team/<int:member_id>/edit', methods=['GET', 'POST'])
def admin_team_edit(member_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    member = TeamMember.query.get_or_404(member_id)

    if request.method == 'POST':
        member.name = request.form.get('name')
        member.job_title = request.form.get('job_title')
        member.bio = request.form.get('bio')
        
        # تعيين الصورة URL، إذا كانت فارغة ضع None
        member.image_url = request.form.get('image_url')
        
        # تحقق من الروابط الفارغة وتعيين None إذا كانت فارغة
        member.linkedin = request.form.get('linkedin') or None
        member.twitter = request.form.get('twitter') or None
        member.github = request.form.get('github') or None
        member.dribbble = request.form.get('dribbble') or None
        
        # تعيين ترتيب العرض
        member.sort_order = int(request.form.get('sort_order') or 0)
        
        # تحقق من الحالة إذا كانت مفعلة
        member.is_active = True if request.form.get('is_active') == 'on' else False

        # حفظ التغييرات في قاعدة البيانات
        db.session.commit()

        # إنشاء إشعار
        create_notification(
            title='تعديل عضو فريق',
            message=f'تم تعديل بيانات {member.name}',
            type='info'
        )

        flash('تم تحديث بيانات العضو بنجاح', 'success')
        return redirect(url_for('admin_team'))

    return render_template('admin_team_form.html', member=member)

@app.route('/admin/team/<int:member_id>/delete', methods=['POST'])
def admin_team_delete(member_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    member = TeamMember.query.get_or_404(member_id)
    name = member.name

    db.session.delete(member)
    db.session.commit()

    create_notification(
        title='حذف عضو فريق',
        message=f'تم حذف {name} من فريق العمل',
        type='warning'
    )

    flash('تم حذف العضو من الفريق', 'warning')
    return redirect(url_for('admin_team'))

# ============================================================
# Business Experts Admin Routes
# ============================================================

@app.route('/admin/business-experts')
def admin_business_experts():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    experts = BusinessExpert.query.order_by(BusinessExpert.sort_order.asc(),
                                            BusinessExpert.created_at.asc()).all()
    return render_template('admin_business_experts.html', experts=experts)


@app.route('/admin/business-experts/new', methods=['GET', 'POST'])
def admin_business_expert_new():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        job_title = (request.form.get('job_title') or '').strip()

        if not name or not job_title:
            flash('الاسم والمسمى الوظيفي حقول إلزامية', 'danger')
            return render_template('admin_business_expert_form.html', expert=None)

        # معالجة ملف الصورة
        image_path = None
        file = request.files.get('image_file')

        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(EXPERTS_UPLOAD_FOLDER, filename)
            file.save(save_path)
            image_path = f'assets/images/experts/{filename}'
        else:
            # أو استخدام رابط يدوي
            image_path = (request.form.get('image_url') or '').strip()

        # معالجة مجالات الخبرة
        raw_expertise = request.form.get('expertise_areas', '').strip()
        expertise_list = [e.strip() for e in raw_expertise.split(',') if e.strip()]
        expertise_json = json.dumps(expertise_list) if expertise_list else None

        # معالجة الشهادات
        raw_certifications = request.form.get('certifications', '').strip()
        cert_list = [c.strip() for c in raw_certifications.split(',') if c.strip()]
        certifications_json = json.dumps(cert_list) if cert_list else None

        expert = BusinessExpert(
            name=name,
            job_title=job_title,
            specialization=request.form.get('specialization') or None,
            bio=request.form.get('bio') or None,
            expertise_areas=expertise_json,
            image_url=image_path,
            email=request.form.get('email') or None,
            phone=request.form.get('phone') or None,
            linkedin=request.form.get('linkedin') or None,
            twitter=request.form.get('twitter') or None,
            github=request.form.get('github') or None,
            website=request.form.get('website') or None,
            years_experience=int(request.form.get('years_experience') or 0),
            certifications=certifications_json,
            sort_order=int(request.form.get('sort_order') or 0),
            is_active=True if request.form.get('is_active') == 'on' else False
        )

        db.session.add(expert)
        db.session.commit()

        create_notification(
            title='خبير جديد',
            message=f'تم إضافة الخبير: {expert.name}',
            type='success'
        )

        flash('تم إضافة خبير تحليل الأعمال بنجاح', 'success')
        return redirect(url_for('admin_business_experts'))

    return render_template('admin_business_expert_form.html', expert=None,
                         expertise_text='', certifications_text='')


@app.route('/admin/business-experts/<int:expert_id>/edit', methods=['GET', 'POST'])
def admin_business_expert_edit(expert_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    expert = BusinessExpert.query.get_or_404(expert_id)

    if request.method == 'POST':
        expert.name = request.form.get('name')
        expert.job_title = request.form.get('job_title')
        expert.specialization = request.form.get('specialization') or None
        expert.bio = request.form.get('bio') or None

        # معالجة الصورة الجديدة
        file = request.files.get('image_file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            save_path = os.path.join(EXPERTS_UPLOAD_FOLDER, filename)
            file.save(save_path)
            expert.image_url = f'assets/images/experts/{filename}'
        else:
            # تحديث الرابط اليدوي
            image_url = (request.form.get('image_url') or '').strip()
            if image_url:
                expert.image_url = image_url

        # معالجة مجالات الخبرة
        raw_expertise = request.form.get('expertise_areas', '').strip()
        expertise_list = [e.strip() for e in raw_expertise.split(',') if e.strip()]
        expert.expertise_areas = json.dumps(expertise_list) if expertise_list else None

        # معالجة الشهادات
        raw_certifications = request.form.get('certifications', '').strip()
        cert_list = [c.strip() for c in raw_certifications.split(',') if c.strip()]
        expert.certifications = json.dumps(cert_list) if cert_list else None

        expert.email = request.form.get('email') or None
        expert.phone = request.form.get('phone') or None
        expert.linkedin = request.form.get('linkedin') or None
        expert.twitter = request.form.get('twitter') or None
        expert.github = request.form.get('github') or None
        expert.website = request.form.get('website') or None
        expert.years_experience = int(request.form.get('years_experience') or 0)
        expert.sort_order = int(request.form.get('sort_order') or 0)
        expert.is_active = True if request.form.get('is_active') == 'on' else False

        db.session.commit()

        create_notification(
            title='تعديل خبير',
            message=f'تم تعديل بيانات الخبير: {expert.name}',
            type='info'
        )

        flash('تم تحديث بيانات الخبير بنجاح', 'success')
        return redirect(url_for('admin_business_experts'))

    # عند GET: تجهيز النصوص
    expertise_text = ''
    if expert.expertise_areas:
        try:
            expertise_list = json.loads(expert.expertise_areas)
            expertise_text = ', '.join(expertise_list)
        except Exception:
            expertise_text = expert.expertise_areas

    certifications_text = ''
    if expert.certifications:
        try:
            cert_list = json.loads(expert.certifications)
            certifications_text = ', '.join(cert_list)
        except Exception:
            certifications_text = expert.certifications

    return render_template('admin_business_expert_form.html', expert=expert,
                         expertise_text=expertise_text,
                         certifications_text=certifications_text)


@app.route('/admin/business-experts/<int:expert_id>/delete', methods=['POST'])
def admin_business_expert_delete(expert_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login', next=request.path))

    expert = BusinessExpert.query.get_or_404(expert_id)
    name = expert.name

    db.session.delete(expert)
    db.session.commit()

    create_notification(
        title='حذف خبير',
        message=f'تم حذف الخبير: {name}',
        type='warning'
    )

    flash('تم حذف الخبير بنجاح', 'warning')
    return redirect(url_for('admin_business_experts'))


# Public route for business experts
@app.route('/business-experts')
def business_experts():
    experts = BusinessExpert.query.filter_by(is_active=True) \
                                  .order_by(BusinessExpert.sort_order.asc(),
                                           BusinessExpert.created_at.asc()) \
                                  .all()
    return render_template('business_experts.html', experts=experts)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
