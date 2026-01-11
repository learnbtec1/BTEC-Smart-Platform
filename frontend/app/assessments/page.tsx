'use client';
import { useState } from 'react';

export default function AssessmentPage() {
  const [formData, setFormData] = useState({ question: '', major: '', level: '' });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/v1/assessments/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert('حدث خطأ في الاتصال بالسيرفر');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='min-h-screen bg-gray-50 p-8' dir='rtl'>
      <div className='max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-6'>
        <h1 className='text-2xl font-bold text-blue-800 mb-6'>أداة تقييم أسئلة BTEC</h1>
        
        <div className='space-y-4'>
          <div>
            <label className='block text-gray-700 mb-2'>نص السؤال</label>
            <textarea
              className='w-full border p-3 rounded-lg'
              rows={3}
              onChange={(e) => setFormData({...formData, question: e.target.value})}
            />
          </div>
          <div className='grid grid-cols-2 gap-4'>
            <input 
              placeholder='التخصص (مثلاً: إدارة أعمال)' 
              className='border p-3 rounded-lg'
              onChange={(e) => setFormData({...formData, major: e.target.value})}
            />
            <input 
              placeholder='المستوى (Pass/Merit/Distinction)' 
              className='border p-3 rounded-lg'
              onChange={(e) => setFormData({...formData, level: e.target.value})}
            />
          </div>
          
          <button 
            onClick={handleSubmit}
            disabled={loading}
            className='w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400'
          >
            {loading ? 'جاري التحليل...' : 'تحليل السؤال'}
          </button>
        </div>

        {result && (
          <div className='mt-8 p-6 bg-blue-50 rounded-xl border border-blue-100'>
            <div className='flex items-center gap-4 mb-4'>
              <div className='text-4xl font-bold text-blue-600'>{result.difficulty_score}/10</div>
              <div className='text-gray-600'>مستوى الصعوبة المقدر</div>
            </div>
            <p className='text-gray-800 leading-relaxed'>{result.advice}</p>
          </div>
        )}
      </div>
    </div>
  );
}
