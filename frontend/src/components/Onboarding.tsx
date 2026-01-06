import React, { useState, useEffect } from "react";

export default function Onboarding() {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const seen = typeof window !== "undefined" && localStorage.getItem("btec_onboard_seen");
    if (!seen) setShow(true);
  }, []);
  if (!show) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="w-full max-w-2xl p-6 bg-white dark:bg-neutral-900 rounded-lg shadow-lg">
        <h2 className="text-xl font-semibold mb-3">Welcome to the platform</h2>
        <p className="mb-4">Quick tour: search, chat with the helper, and upload files easily.</p>
        <div className="flex justify-end">
          <button className="px-4 py-2 rounded bg-primary text-white" onClick={() => { localStorage.setItem("btec_onboard_seen","1"); window.location.reload(); }}>
            Get started
          </button>
        </div>
      </div>
    </div>
  );
}
