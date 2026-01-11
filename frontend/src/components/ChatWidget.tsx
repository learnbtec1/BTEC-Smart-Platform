import React, { useState } from "react";
import { api } from "../lib/api";

type Msg = { role: string; text: string; sources?: string[] };

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [level, setLevel] = useState("L2");
  const [major, setMajor] = useState("Business");

  async function send() {
    if (!input) return;
    const userMsg: Msg = { role: "user", text: input };
    setMessages((m) => [...m, userMsg]);
    setInput("");

    try {
      const body = { question: input, level, major };
      const resp = await api.post("/api/v1/assistant", body);
      const answer = resp?.answer || resp?.data?.answer || "Sorry, no answer.";
      const sources = resp?.sources || resp?.data?.sources || [];
      setMessages((m) => [...m, { role: "assistant", text: answer, sources }]);
    } catch (e) {
      setMessages((m) => [...m, { role: "assistant", text: "Error occurred, try again later." }]);
    }
  }

  function downloadTemplate() {
    const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:10000";
    const url = `${base}/api/v1/assistant/download-template/${level}/1`;
    window.open(url, "_blank");
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {open ? (
        <div className="w-96 bg-white dark:bg-neutral-800 rounded-lg shadow-lg p-3">
          {/* Toolbar */}
          <div className="flex items-center gap-2 mb-2">
            <label className="text-sm">المستوى:</label>
            <select value={level} onChange={(e) => setLevel(e.target.value)} className="px-2 py-1 border rounded">
              <option value="L2">L2</option>
              <option value="L3">L3</option>
            </select>

            <label className="text-sm ml-2">التخصص:</label>
            <select value={major} onChange={(e) => setMajor(e.target.value)} className="px-2 py-1 border rounded">
              <option value="Business">Business</option>
              <option value="IT">IT</option>
            </select>

            <button onClick={downloadTemplate} className="ml-auto px-2 py-1 bg-gray-100 dark:bg-neutral-700 rounded text-sm">
              تحميل النموذج
            </button>
          </div>

          <div className="h-56 overflow-auto mb-2 space-y-2">
            {messages.map((m, i) => (
              <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
                <div className={m.role === "user" ? "inline-block bg-blue-100 text-right p-2 rounded" : "inline-block bg-gray-100 dark:bg-neutral-700 p-2 rounded"}>
                  {m.text}
                </div>
                {m.sources && m.sources.length > 0 ? (
                  <div className="mt-1 text-xs text-gray-600 dark:text-gray-300">
                    <div className="font-semibold">مصادر:</div>
                    <ul className="list-none pl-0">
                      {m.sources.map((s, idx) => (
                        <li key={idx} className="flex items-center gap-2 mt-1">
                          <span className="text-yellow-600">📚</span>
                          <span className="truncate max-w-xs">{s}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : null}
              </div>
            ))}
          </div>

          <div className="flex gap-2">
            <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="اكتب سؤالك هنا..." className="flex-1 p-2 rounded border" />
            <button onClick={send} className="px-4 py-2 bg-primary text-white rounded">Send</button>
          </div>
        </div>
      ) : null}
      <button onClick={() => setOpen((s) => !s)} aria-label="Toggle chat" className="w-12 h-12 rounded-full bg-primary text-white shadow-lg">💬</button>
    </div>
  );
}
