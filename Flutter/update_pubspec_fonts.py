
import os
import yaml

# المسار الحالي لمشروع Flutter
flutter_path = os.getcwd()
pubspec_file = os.path.join(flutter_path, "pubspec.yaml")
fonts_dir = os.path.join(flutter_path, "assets/fonts")

def update_pubspec():
    if not os.path.isfile(pubspec_file):
        print("❌ لم يتم العثور على ملف pubspec.yaml.")
        return

    if not os.path.isdir(fonts_dir):
        print("❌ لم يتم العثور على مجلد الخطوط: assets/fonts/")
        return

    # قراءة ملفات الخطوط الموجودة
    font_files = [f for f in os.listdir(fonts_dir) if f.lower().endswith(('.ttf', '.otf'))]
    if not font_files:
        print("⚠️ لا توجد ملفات خطوط في assets/fonts/")
        return

    # تحميل pubspec.yaml
    with open(pubspec_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # تعديل قسم fonts
    data['flutter']['fonts'] = [
        {
            'family': 'Inter',
            'fonts': [{'asset': f'assets/fonts/{font}'} for font in font_files]
        }
    ]

    # حفظ التعديلات
    with open(pubspec_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

    print("✅ تم تحديث ملف pubspec.yaml بنجاح!")
    print("📌 الخطوط المضافة:")
    for font in font_files:
        print(f" - {font}")

if __name__ == "__main__":
    update_pubspec()
