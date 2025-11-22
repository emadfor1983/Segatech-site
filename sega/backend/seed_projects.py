from app import app, db, Project
import json

def seed_projects():
    with app.app_context():
        # إنشاء الجداول لو لسه ما اتعملتش
        db.create_all()

        # لو في مشاريع مسبقًا، لا نضيف مرة ثانية
        if Project.query.count() > 0:
            print("يوجد مشاريع بالفعل في قاعدة البيانات، لن يتم التكرار.")
            return

        sample_projects = [
            # 💻 حلول تقنية (technology)
            Project(
                title="منصة تعليمية متكاملة",
                description="منصة تعليمية شاملة تقدم تجربة تعلم تفاعلية مع إدارة محتوى متقدمة.",
                category="technology",
                technologies=json.dumps(["React", "Node.js", "MongoDB"]),
                image_url="assets/images/projects/project6.jpg",
                client="شركة التعليم الحديث",
                duration="3 أشهر",
                status="completed",
                year=2023
            ),

            # 📣 مشروع تسويق رقمي (digital)
            Project(
                title="حملة تسويق رقمي لمتجر إلكتروني",
                description="إدارة حملة تسويق رقمي شاملة عبر محركات البحث ووسائل التواصل الاجتماعي.",
                category="digital",
                technologies=json.dumps(["SEO", "Google Ads", "Meta Ads"]),
                image_url="assets/images/projects/project3.png",
                client="متجر الأناقة",
                duration="4 أشهر",
                status="completed",
                year=2022
            ),

            # 📱 إدارة مشاريع تطبيق جوال (project)
            Project(
                title="إدارة مشروع تطبيق توصيل طلبات",
                description="إدارة دورة حياة مشروع تطبيق توصيل من التحليل وحتى الإطلاق.",
                category="project",
                technologies=json.dumps(["Agile", "Jira", "Flutter", "Firebase"]),
                image_url="assets/images/projects/project2.jpg",
                client="شركة النقل السريع",
                duration="5 أشهر",
                status="completed",
                year=2023
            ),

            # 💻 نظام حلول تقنية للشركات (technology)
            Project(
                title="نظام إدارة شركات تقنية",
                description="نظام لإدارة العمليات الداخلية لشركات التقنية (عملاء، مشاريع، مهام، فواتير).",
                category="technology",
                technologies=json.dumps(["Laravel", "MySQL", "Bootstrap"]),
                image_url="assets/images/projects/project5.jpg",
                client="Segatech",
                duration="6 أشهر",
                status="in-progress",
                year=2024
            ),

            # 📣 هوية وتسويق لشركة ناشئة (digital)
            Project(
                title="هوية بصرية وحملة إطلاق رقمية",
                description="تصميم هوية بصرية كاملة مع حملة إطلاق رقمية لشركة ناشئة في مجال التقنية.",
                category="digital",
                technologies=json.dumps(["Branding", "Illustrator", "Photoshop"]),
                image_url="assets/images/projects/project7.jpg",
                client="شركة ستارت أب",
                duration="1 شهر",
                status="completed",
                year=2022
            ),

            # 🧾 نظام إدارة أعمال (business)
            Project(
                title="نظام إدارة أعمال لمركز طبي",
                description="منصة لإدارة المواعيد، العملاء، التقارير المالية، والموارد البشرية.",
                category="business",
                technologies=json.dumps(["Vue.js", "Node.js", "MySQL"]),
                image_url="assets/images/projects/project9.jpg",
                client="مركز الخدمات الطبية",
                duration="3 أشهر",
                status="completed",
                year=2023
            ),

            # 📊 منصة إدارة مهام كجزء من إدارة المشاريع (project)
            Project(
                title="منصة إدارة مهام فرق العمل",
                description="منصة لإدارة مهام الفرق، الجداول الزمنية، وتتبع التقدم كجزء من إدارة المشاريع.",
                category="project",
                technologies=json.dumps(["React Native", "REST API"]),
                image_url="assets/images/projects/project10.png",
                client="شركة استشارات",
                duration="2 أشهر",
                status="planning",
                year=2024
            ),
        ]

        db.session.add_all(sample_projects)
        db.session.commit()
        print("✅ تم إضافة المشاريع التجريبية بنجاح.")

if __name__ == "__main__":
    seed_projects()
