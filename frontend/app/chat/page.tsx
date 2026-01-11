'use client';
import { useState, useRef, useEffect } from 'react';

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { role: 'ai', content: 'أهلاً بك! أنا معلمك المساعد لنظام BTEC. اسألني عن أي معيار (Pass, Merit, Distinction) وسأشرح لك المطلوب.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/v1/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage.content }),
      });

      if (res.ok) {
        const data = await res.json();
        setMessages((prev) => [...prev, { role: 'ai', content: data.response }]);
      } else {
        setMessages((prev) => [...prev, { role: 'ai', content: 'عذراً، حدث خطأ في الاتصال بالمعلم.' }]);
      }
    } catch (error) {
      setMessages((prev) => [...prev, { role: 'ai', content: 'عذراً، الخادم لا يستجيب حالياً.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='min-h-screen bg-gray-50 flex flex-col items-center p-4' dir='rtl'>
      <div className='w-full max-w-2xl bg-white rounded-2xl shadow-xl overflow-hidden flex flex-col h-[80vh]'>
        
        {/* Header */}
        <div className='bg-blue-600 p-4 text-white flex items-center gap-3'>
          <div className='w-10 h-10 bg-white rounded-full flex items-center justify-center text-blue-600 font-bold'>
            AI
          </div>
          <div>
            <h1 className='font-bold text-lg'>المعلم الذكي (BTEC Tutor)</h1>
            <p className='text-xs text-blue-100 opacity-80'>متاح للمساعدة الفورية</p>
          </div>
        </div>

        {/* Chat Area */}
        <div className='flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50'>
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-2xl text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-br-none'
                    : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none shadow-sm'
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className='flex justify-start'>
              <div className='bg-gray-200 text-gray-500 p-3 rounded-2xl rounded-bl-none text-xs animate-pulse'>
                جاري الكتابة...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className='p-4 bg-white border-t border-gray-100 flex gap-2'>
          <input
            type='text'
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder='اكتب سؤالك للمعلم هنا...'
            className='flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all'
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className='bg-blue-600 hover:bg-blue-700 text-white w-10 h-10 rounded-full flex items-center justify-center transition-colors disabled:opacity-50'
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}
