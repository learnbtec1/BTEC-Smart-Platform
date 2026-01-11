import os
from pypdf import PdfReader
from docx import Document

# مسار قاعدة المعرفة
BASE_DIR = r"D:\BTEC-backend\backend\app\knowledge_base"

def extract_text_snippet(file_path, file_type):
    """تحاول قراءة أول 200 حرف من الملف للتأكد من أنه قابل للقراءة"""
    text = ""
    try:
        if file_type == 'pdf':
            reader = PdfReader(file_path)
            if len(reader.pages) > 0:
                text = reader.pages[0].extract_text()
        elif file_type == 'docx':
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
                if len(text) > 200: break
        
        return text[:200].replace('\n', ' ') + "..." # إرجاع مقتطف بسيط
    except Exception as e:
        return f"Error reading file: {e}"

def scan_knowledge_base():
    if not os.path.exists(BASE_DIR):
        print(f"❌ Error: Directory not found: {BASE_DIR}")
        return

    print(f"📂 Scanning Knowledge Base at: {BASE_DIR}\n")
    print(f"{'Folder':<20} | {'Type':<5} | {'File Name'}")
    print("-" * 60)
    
    total_files = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        folder_name = os.path.basename(root)
        
        for file in files:
            file_path = os.path.join(root, file)
            ext = file.split('.')[-1].lower()
            
            if ext in ['pdf', 'docx', 'txt']:
                total_files += 1
                snippet = extract_text_snippet(file_path, ext)
                print(f"{folder_name:<20} | {ext.upper():<5} | {file}")
                # print(f"   Sample: {snippet}\n") # تفعيل هذا السطر إذا أردت رؤية النص

    print("-" * 60)
    print(f"\n✅ Found {total_files} valid documents.")

if __name__ == "__main__":
    scan_knowledge_base()
