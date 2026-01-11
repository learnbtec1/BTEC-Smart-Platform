"use client";

import React, { useState } from "react";
import { HelpCircle, BookOpen, BarChart2, Send, AlertCircle, CheckCircle2 } from "lucide-react";
import LottieHero from "../../components/LottieHero";

type Result = {
  difficulty_score?: number | null;
  advice?: string | null;
};

export default function AssessmentPage() {
  const [question, setQuestion] = useState("");
  const [major, setMajor] = useState("");
  const [level, setLevel] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<Result | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setResult(null);

    if (!question.trim() || !major.trim() || !level.trim()) {
      setError("الرجاء تعبئة جميع الحقول المطلوبة.");
      return;
    }

    setLoading(true);
    try {
      const apiBase =
        (process.env.NEXT_PUBLIC_API_URL as string) ??
        (typeof window !== "undefined" &&
        window.location.hostname.includes("localhost")
          ? "http://127.0.0.1:8000"
          : "");
      
      // إصلاح التكرار المحتمل في المسار
      const target = `${apiBase}/api/v1/assessments/`.replace("//api", "/api");

      const res = await fetch(target, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, major, level }),
      });

      if (!res.ok) {
        const json = await res.json().catch(() => null);
        const message =
          json?.detail ||
          json?.message ||
          (await res.text()) ||
          `Request failed: ${res.status}`;
        throw new Error(message);
      }

      const data = await res.json();
      setResult({
        difficulty_score: data.difficulty_score,
        advice: data.advice,
      });
    } catch (err: any) {
      setError(err?.message || "حدث خطأ غير متوقع.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen py-12 bg-background text-foreground">
      <div className="max-w-3xl mx-auto px-4">
        <div className="glass-panel rounded-lg overflow-hidden border border-border bg-card shadow-sm">
          <div className="px-6 py-8">
            
            {/* Header Section */}
            <div className="mb-4 text-center sm:text-right">
              <LottieHero speed={1.25} loop={true} height="14rem" />
              <h1 className="text-2xl font-semibold text-card-foreground mt-4">
                تقييم السؤال
              </h1>
              <p className="mt-2 text-sm text-muted-foreground">
                أدخل نص السؤال والمعلومات ثم اضغط إرسال للحصول على مستوى الصعوبة والنصيحة.
              </p>
            </div>

            {/* Form Section */}
            <form onSubmit={handleSubmit} className="mt-6 space-y-6">
              {/* Question Input */}
              <div>
                <label className="block text-sm font-medium text-card-foreground mb-2">
                  نص السؤال
                </label>
                <div className="flex items-start gap-3">
                  <HelpCircle className="mt-3 w-6 h-6 flex-shrink-0 text-muted-foreground" />
                  <textarea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    rows={6}
                    className="flex-1 rounded-lg border border-input bg-transparent p-3 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-ring"
                    placeholder="ألصق نص السؤال هنا..."
                  />
                </div>
              </div>

              {/* Major & Level Inputs */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-card-foreground mb-2">
                    المادة / التخصص
                  </label>
                  <div className="flex items-center gap-2">
                    <BookOpen className="w-5 h-5 flex-shrink-0 text-muted-foreground" />
                    <input
                      value={major}
                      onChange={(e) => setMajor(e.target.value)}
                      className="flex-1 rounded-md border border-input bg-transparent p-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-ring"
                      placeholder="مثال: إدارة الأعمال"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-card-foreground mb-2">
                    المستوى المستهدف
                  </label>
                  <div className="flex items-center gap-2">
                    <BarChart2 className="w-5 h-5 flex-shrink-0 text-muted-foreground" />
                    <input
                      value={level}
                      onChange={(e) => setLevel(e.target.value)}
                      className="flex-1 rounded-md border border-input bg-transparent p-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-ring"
                      placeholder="سهل | متوسط | صعب"
                    />
                  </div>
                </div>
              </div>

              {/* Submit Button (Fixed) */}
              <div className="flex items-center gap-3 pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="inline-flex items-center gap-2 px-6 py-2.5 bg-primary text-primary-foreground rounded-md hover:brightness-90 disabled:opacity-60 transition-all"
                >
                  {loading ? (
                    <svg
                      className="animate-spin h-5 w-5 mr-2 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                  ) : (
                    <Send className="w-5 h-5" />
                  )}
                  <span>{loading ? "جاري التحليل..." : "تحليل السؤال"}</span>
                </button>
              </div>
            </form>

            {/* Error Message */}
            {error && (
              <div className="mt-6 p-4 rounded-md bg-destructive/10 text-destructive flex items-start gap-3">
                <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <p className="text-sm">{error}</p>
              </div>
            )}

            {/* Results Display Section (Added) */}
            {result && (
              <div className="mt-8 pt-6 border-t border-border animate-in fade-in slide-in-from-bottom-4 duration-500">
                <h3 className="text-lg font-semibold text-card-foreground flex items-center gap-2 mb-4">
                  <CheckCircle2 className="w-5 h-5 text-green-500" />
                  نتائج التقييم
                </h3>
                
                <div className="grid gap-4 bg-muted/50 p-4 rounded-lg">
                  {result.difficulty_score !== null && (
                    <div className="flex justify-between items-center border-b border-border/50 pb-2">
                      <span className="text-sm font-medium text-muted-foreground">مستوى الصعوبة المقدر:</span>
                      <span className="text-lg font-bold text-primary">
                        {result.difficulty_score} / 10
                      </span>
                    </div>
                  )}
                  
                  {result.advice && (
                    <div className="mt-2">
                      <span className="block text-sm font-medium text-muted-foreground mb-1">التحليل والنصيحة:</span>
                      <p className="text-sm leading-relaxed text-card-foreground whitespace-pre-line">
                        {result.advice}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}

          </div>
        </div>
      </div>
    </main>
  );
}