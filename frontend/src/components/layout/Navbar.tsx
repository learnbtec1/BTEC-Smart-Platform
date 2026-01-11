'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Menu, X, Cpu, LayoutDashboard, Terminal, User } from 'lucide-react'

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  const navItems = [
    { href: '/', label: 'الرئيسية', icon: <Cpu size={18} /> },
    { href: '/dashboard', label: 'لوحة التحكم', icon: <LayoutDashboard size={18} /> },
    { href: '/simulation', label: 'المحاكاة', icon: <Terminal size={18} /> },
    { href: '/profile', label: 'الملف الشخصي', icon: <User size={18} /> },
  ]

  return (
    <nav className="sticky top-0 z-50 bg-[#020617]/80 backdrop-blur-xl border-b border-white/10">
      <div className="container mx-auto px-6">
        <div className="flex justify-between items-center h-20">
          
          {/* الشعار المستقبلي */}
          <Link href="/" className="flex items-center gap-2 text-2xl font-black italic tracking-tighter text-white">
            <div className="w-8 h-8 bg-cyan-500 rounded-lg animate-pulse shadow-[0_0_15px_rgba(6,182,212,0.5)]" />
            NEURAL CORE
          </Link>

          {/* القائمة للأجهزة الكبيرة */}
          <div className="hidden md:flex items-center space-x-8 rtl:space-x-reverse">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center gap-2 text-sm font-medium text-slate-400 hover:text-cyan-400 transition-colors"
              >
                {item.label}
              </Link>
            ))}
            <button className="px-5 py-2 bg-white text-black text-xs font-bold rounded-full hover:bg-cyan-400 transition-all">
              تسجيل الدخول
            </button>
          </div>

          {/* زر الجوال */}
          <button onClick={() => setIsOpen(!isOpen)} className="md:hidden text-white">
            {isOpen ? <X size={28} /> : <Menu size={28} />}
          </button>
        </div>

        {/* قائمة الجوال */}
        {isOpen && (
          <div className="md:hidden py-6 space-y-4 border-t border-white/5 animate-in slide-in-from-top">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="block text-lg font-bold text-slate-300 hover:text-cyan-400"
                onClick={() => setIsOpen(false)}
              >
                {item.label}
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  )
}