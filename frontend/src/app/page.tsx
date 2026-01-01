"use client";
import React, { useState, useEffect } from "react";

export default function BTECNexusEnterprise() {
  const [stats, setStats] = useState({ active_now: 0, total_students: 1000 });

  return (
    <div className="min-h-screen bg-[#00050a] text-cyan-400 p-8 font-mono">
      {/* هيدر القيادة */}
      <header className="border-b border-cyan-500/30 pb-6 mb-12 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-black text-white italic">BTEC_NEXUS_v2200</h1>
          <p className="text-[10px] text-cyan-700 uppercase tracking-[0.5em]">نظام إدارة الموارد الشامل</p>
        </div>
        <div className="bg-cyan-500 text-black px-6 py-2 rounded-full font-bold text-xs">
          ADMIN_HAMZA: ROOT_ACCESS
        </div>
      </header>

      {/* لوحة التحكم الكبرى (الأتمتة) */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
        <div className="p-6 bg-slate-900/40 border border-cyan-500/20 rounded-2xl">
          <p className="text-xs text-slate-500 mb-2">إجمالي الطلاب</p>
          <p className="text-4xl font-black text-white">1,000</p>
        </div>
        <div className="p-6 bg-slate-900/40 border border-cyan-500/20 rounded-2xl">
          <p className="text-xs text-slate-500 mb-2">المعلمين</p>
          <p className="text-4xl font-black text-white">50</p>
        </div>
        <div className="p-6 bg-slate-900/40 border border-cyan-500/20 rounded-2xl">
          <p className="text-xs text-slate-500 mb-2">رؤساء الأقسام</p>
          <p className="text-4xl font-black text-white">10</p>
        </div>
        <div className="p-6 bg-cyan-500/10 border border-cyan-500/50 rounded-2xl">
          <p className="text-xs text-cyan-500 mb-2">الحالة العامة</p>
          <p className="text-4xl font-black text-green-400 animate-pulse">ACTIVE</p>
        </div>
      </div>

      {/* منطقة إدارة الكوادر */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <section className="p-8 border border-white/5 bg-slate-900/20 rounded-[3rem]">
           <h3 className="text-xl font-bold mb-6 italic text-white underline">إدارة المعلمين (50 معلم)</h3>
           <div className="space-y-4">
              {[1, 2, 3].map(i => (
                <div key={i} className="p-4 bg-white/5 rounded-xl border-l-2 border-cyan-500 flex justify-between items-center">
                  <span>TEACHER_PRO_00{i}</span>
                  <button className="text-[10px] bg-cyan-900/30 px-3 py-1 rounded">إدارة الصلاحيات</button>
                </div>
              ))}
              <p className="text-center text-xs text-slate-600">... تم تحميل 50 سجلاً من قاعدة البيانات ...</p>
           </div>
        </section>

        <section className="p-8 border border-white/5 bg-slate-900/20 rounded-[3rem]">
           <h3 className="text-xl font-bold mb-6 italic text-white underline">إدارة رؤساء الأقسام (10 قادة)</h3>
           <div className="space-y-4">
              {[1, 2].map(i => (
                <div key={i} className="p-4 bg-white/5 rounded-xl border-l-2 border-purple-500 flex justify-between items-center">
                  <span>DEPT_HEAD_0{i}</span>
                  <span className="text-[10px] text-purple-400">IT & ENGINEERING</span>
                </div>
              ))}
           </div>
        </section>
      </div>
    </div>
  );
}