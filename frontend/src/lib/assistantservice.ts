import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1/assistant';

// دالة إرسال السؤال مع التخصص والمستوى
export const askAssistant = async (question, level, major) => {
  try {
    const response = await axios.post(`${API_URL}/`, {
      question: question,
      level: level,
      major: major
    }, {
      headers: { 'Content-Type': 'application/json' }
    });
    return response.data;
  } catch (error) {
    console.error("Error asking assistant:", error);
    throw error;
  }
};

// دالة تحميل النموذج (مهم جداً: responseType: blob)
export const downloadTemplate = async (level, unit = "1") => {
  try {
    const response = await axios.get(`${API_URL}/download-template/${level}/${unit}`, {
      responseType: 'blob', // ضروري جداً لملفات الورد
    });
    
    // إنشاء رابط تحميل وهمي في المتصفح
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `BTEC_${level}_Unit${unit}_Template.docx`);
    document.body.appendChild(link);
    link.click();
    
    // تنظيف الذاكرة
    link.parentNode.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Error downloading template:", error);
    throw error;
  }
};