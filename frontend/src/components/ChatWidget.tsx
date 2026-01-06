import React, { useState } from "react";
import { api } from "../lib/api";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<{role:string,text:string}[]>([]);
  const [input, setInput] = useState("");

  async function send() {
    if (!input) return;
    const userMsg = { role: "user", text: input };
    setMessages(m => [...m, userMsg]);
    setInput("");
    try {
      const resp = await api.post("/chat", { q: input });
      setMessages(m => [...m, { role: "assistant", text: resp.answer || "Sorry, no answer." }]);
    } catch (e) {
      setMessages(m => [...m, { role: "assistant", text: "Error occurred, try again later." }]);
    }
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {open ? (
        <div className="w-80 bg-white dark:bg-neutral-800 rounded-lg shadow-lg p-3">
          <div className="h-48 overflow-auto mb-2">
            {messages.map((m,i) => <div key={i} className={m.role==="user"?"text-right":"text-left"}>{m.text}</div>)}
          </div>
          <div className="flex gap-2">
            <input value={input} onChange={e=>setInput(e.target.value)} className="flex-1 p-2 rounded border" />
            <button onClick={send} className="px-3 py-1 bg-primary text-white rounded">Send</button>
          </div>
        </div>
      ) : null}
      <button onClick={()=>setOpen(s=>!s)} className="w-12 h-12 rounded-full bg-primary text-white shadow-lg">ðŸ’¬</button>
    </div>
  );
}
