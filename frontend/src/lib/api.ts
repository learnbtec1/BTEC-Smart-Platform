const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:10000";

async function request(path: string, opts: RequestInit = {}) {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const headers: any = Object.assign({ "Content-Type": "application/json" }, opts.headers || {});
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(`${BASE}${path}`, { ...opts, headers });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json().catch(() => null);
}

export const api = {
  get: (p: string) => request(p, { method: "GET" }),
  post: (p: string, body?: any) => request(p, { method: "POST", body: JSON.stringify(body) }),
  put: (p: string, body?: any) => request(p, { method: "PUT", body: JSON.stringify(body) }),
  del: (p: string) => request(p, { method: "DELETE" }),
};
