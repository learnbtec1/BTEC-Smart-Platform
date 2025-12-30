
import os
import subprocess
import yaml
import json

flutter_path = os.getcwd()
pubspec_file = os.path.join(flutter_path, "pubspec.yaml")
fonts_dir = os.path.join(flutter_path, "assets/fonts")
frontend_path = os.path.join(flutter_path, "frontend")

assets_dirs = ["assets/images", "assets/animations", "assets/icons", "assets/fonts"]

# الحقول الأساسية لـ pubspec.yaml
default_pubspec = {
    "name": "btec_smart_platform",
    "description": "BTEC AI Assessment Platform",
    "version": "1.0.0+1",
    "publish_to": "none",
    "environment": {"sdk": ">=3.0.0 <4.0.0"},
    "dependencies": {
        "flutter": {"sdk": "flutter"},
        "http": "^1.1.0",
        "google_fonts": "^6.1.0",
        "iconsax": "^0.0.8",
        "shimmer": "^3.0.0",
        "lottie": "^3.3.2",
        "percent_indicator": "^4.2.3",
        "animate_do": "^4.2.0",
        "fl_chart": "^1.1.1"
    },
    "dev_dependencies": {
        "flutter_test": {"sdk": "flutter"},
        "flutter_lints": "^6.0.0"
    },
    "flutter": {
        "uses-material-design": True,
        "assets": [
            "assets/images/",
            "assets/animations/",
            "assets/icons/",
            "assets/fonts/"
        ]
    }
}

def ensure_assets():
    print("🔍 التحقق من المجلدات...")
    for d in assets_dirs:
        path = os.path.join(flutter_path, d)
        if not os.path.exists(path):
            print(f"📂 إنشاء المجلد: {path}")
            os.makedirs(path)

def update_pubspec():
    if not os.path.isfile(pubspec_file):
        print("⚠️ ملف pubspec.yaml غير موجود، سيتم إنشاؤه...")
        data = default_pubspec
    else:
        with open(pubspec_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

    # إضافة الحقول الأساسية إذا كانت ناقصة
    for key, value in default_pubspec.items():
        if key not in data:
            data[key] = value

    # تحديث قسم الخطوط بناءً على الملفات الموجودة
    if os.path.isdir(fonts_dir):
        font_files = [f for f in os.listdir(fonts_dir) if f.lower().endswith(('.ttf', '.otf'))]
        if font_files:
            data['flutter']['fonts'] = [{
                'family': 'Inter',
                'fonts': [{'asset': f'assets/fonts/{font}'} for font in font_files]
            }]

    # حفظ التعديلات
    with open(pubspec_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

    print("✅ تم تحديث ملف pubspec.yaml بنجاح!")

def flutter_commands():
    print("\n🧹 تنظيف المشروع...")
    subprocess.run(["flutter", "clean"], cwd=flutter_path, shell=True)
    print("📦 جلب الحزم...")
    subprocess.run(["flutter", "pub", "get"], cwd=flutter_path, shell=True)
    print("🏗️ بناء المشروع لـ Windows...")
    subprocess.run(["flutter", "build", "windows"], cwd=flutter_path, shell=True)
    print("🚀 تشغيل التطبيق...")
    subprocess.run(["flutter", "run", "-d", "windows"], cwd=flutter_path, shell=True)

def setup_frontend():
    if os.path.isdir(frontend_path):
        package_json_path = os.path.join(frontend_path, "package.json")
        if not os.path.isfile(package_json_path):
            print("📄 إنشاء package.json للـ frontend...")
            package_data = {
                "name": "frontend-app",
                "version": "1.0.0",
                "scripts": {
                    "start": "react-scripts start",
                    "build": "react-scripts build",
                    "test": "react-scripts test",
                    "eject": "react-scripts eject"
                },
                "dependencies": {
                    "react": "^18.2.0",
                    "react-dom": "^18.2.0",
                    "react-scripts": "5.0.1"
                }
            }
            with open(package_json_path, "w") as f:
                json.dump(package_data, f, indent=2)

        print("📦 تثبيت مكتبات React...")
        subprocess.run(["npm", "install"], cwd=frontend_path, shell=True)
        print("🚀 تشغيل تطبيق React...")
        subprocess.run(["npm", "start"], cwd=frontend_path, shell=True)

if __name__ == "__main__":
    ensure_assets()
    update_pubspec()
    flutter_commands()
    setup_frontend()
