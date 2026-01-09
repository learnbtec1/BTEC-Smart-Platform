"use client"

import React, { useState } from "react";

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
      setError("Please fill all fields.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/v1/assessments/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, major, level }),
      });

      if (!res.ok) {
        const json = await res.json().catch(() => null);
        const message = json?.detail || json?.message || (await res.text()) || `Request failed: ${res.status}`;
        throw new Error(message);
      }

      const data = await res.json();
      setResult({ difficulty_score: data.difficulty_score, advice: data.advice });
    } catch (err: any) {
      setError(err?.message || "An unknown error occurred");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-3xl mx-auto px-4">
        <div className="bg-white shadow-md rounded-lg overflow-hidden">
          <div className="px-6 py-8">
            <h1 className="text-2xl font-semibold text-gray-800">Assess Question</h1>
            <p className="mt-2 text-sm text-gray-500">Enter a question and metadata to receive difficulty and advice.</p>

            <form onSubmit={handleSubmit} className="mt-6 space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Question</label>
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  rows={6}
                  className="block w-full rounded-lg border border-gray-200 p-3 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                  placeholder="Paste the question text here"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Major</label>
                  <input
                    value={major}
                    onChange={(e) => setMajor(e.target.value)}
                    className="block w-full rounded-md border border-gray-200 p-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                    placeholder="e.g., Mathematics"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Level</label>
                  <input
                    value={level}
                    onChange={(e) => setLevel(e.target.value)}
                    className="block w-full rounded-md border border-gray-200 p-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                    placeholder="e.g., easy | medium | hard"
                  />
                </div>
              </div>

              <div className="flex items-center gap-3">
                <button
                  type="submit"
                  disabled={loading}
                  className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-60"
                >
                  {loading ? (
                    <svg className="animate-spin h-5 w-5 mr-2 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
                    </svg>
                  ) : null}
                  {loading ? "Submitting..." : "Submit"}
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setQuestion("");
                    setMajor("");
                    setLevel("");
                    setResult(null);
                    setError(null);
                  }}
                  className="px-3 py-2 border rounded-md text-sm"
                >
                  Reset
                </button>
              </div>
            </form>
          </div>

          <div className="border-t bg-gray-50 px-6 py-6">
            {error && (
              <div className="p-4 bg-red-50 text-red-700 rounded-md" role="alert" aria-live="assertive">
                {error}
              </div>
            )}

            {result ? (
              <div className="bg-white rounded-lg shadow-sm p-4">
                <h2 className="text-lg font-medium text-gray-800">Assessment Result</h2>
                <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
                  <div className="p-3 bg-gray-50 rounded">
                    <div className="text-sm text-gray-500">Difficulty score</div>
                    <div className="text-2xl font-semibold text-indigo-600">{result.difficulty_score ?? '—'}</div>
                  </div>

                  <div className="p-3 bg-gray-50 rounded sm:col-span-1">
                    <div className="text-sm text-gray-500">Advice</div>
                    <div className="mt-2 text-sm text-gray-700 whitespace-pre-wrap">{result.advice ?? 'No advice provided.'}</div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-sm text-gray-500">No result yet. Submit a question to get an assessment.</div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
