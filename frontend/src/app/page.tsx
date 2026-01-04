"use client";
import React, { useState } from "react";

export default function GlobalSystem() {
  const [auth, setAuth] = useState(null);
  const [error, setError] = useState("");

  const login = async (e) => {
    e.preventDefault();
    const u = e.target.username.value;
    const p = e.target.password.value;
    
    setError("جاري الاتصال بالنواة..."); // رسالة طمأنة للمستخدم

    try {
      // تم تصحيح العنوان هنا من 127.00.0.1 إلى 127.0.0.1
      const res = await fetch(`http://localhost:10000/api/v1/auth/login?u=${u}&p=${p}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (res.ok) {
        const data = await res.json();
        setAuth(data);
        setError("");
      } else {
        setError("فشل الدخول: تأكد من اسم المستخدم وكلمة المرور");
      }
    } catch (err) {
      console.error("Connection Error:", err);
      setError("النظام متصل ولكن السيرفر لا يستجيب.. تأكد من تشغيل Docker Backend");
    }
  };

  if (auth) return (
    <div className="bg-black min-h-screen text-cyan-400 p-20 font-mono flex flex-col items-center justify-center">
      <div className="border-2 border-cyan-500 p-10 rounded-[3rem] shadow-[0_0_50px_rgba(6,182,212,0.3)]">
        <h1 className="text-5xl font-black italic mb-4 animate-pulse">BTEC_NEXUS: ONLINE</h1>
        <p className="mt-4 text-xl border-b border-cyan-900 pb-4">مرحباً بالقائد: {auth.role}</p>
        <div className="grid grid-cols-3 gap-10 mt-10">
           <div className="p-10 border border-cyan-800 rounded-3xl text-center font-bold hover:bg-cyan-500 hover:text-black transition-all cursor-pointer">📊 إحصائيات 1000 طالب</div>
           <div className="p-10 border border-cyan-800 rounded-3xl text-center font-bold hover:bg-cyan-500 hover:text-black transition-all cursor-pointer">🤖 كاشف الانتحال</div>
           <div className="p-10 border border-cyan-800 rounded-3xl text-center font-bold hover:bg-cyan-500 hover:text-black transition-all cursor-pointer">🥽 بيئة الـ VR</div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="bg-[#000205] min-h-screen flex items-center justify-center font-mono">
      <form onSubmit={login} className="p-10 border border-cyan-500 rounded-[3rem] w-full max-w-md bg-black/50 backdrop-blur-xl shadow-2xl">
        <div className="flex justify-center mb-6">
            <div className="w-20 h-20 border-4 border-cyan-500 rounded-full flex items-center justify-center animate-spin-slow">
                <span className="text-cyan-500 font-bold">BTEC</span>
            </div>
        </div>
        <h2 className="text-cyan-400 text-center text-2xl font-black mb-8 italic tracking-widest">بوابة الدخول الموحدة</h2>
        <input name="username" placeholder="اسم المستخدم (Key)" className="w-full mb-4 p-4 bg-black border border-cyan-900 text-white rounded-2xl focus:border-cyan-500 outline-none transition-all" />
        <input name="password" type="password" placeholder="كلمة المرور" className="w-full mb-6 p-4 bg-black border border-cyan-900 text-white rounded-2xl focus:border-cyan-500 outline-none transition-all" />
        <button className="w-full p-4 bg-cyan-500 text-black font-black rounded-2xl uppercase hover:bg-white transition-colors shadow-[0_0_20px_rgba(6,182,212,0.5)]">تفعيل الدخول</button>
        {error && <p className="text-cyan-600 text-xs mt-4 text-center italic font-bold">{error}</p>}
      </form>
    </div>
  );
}