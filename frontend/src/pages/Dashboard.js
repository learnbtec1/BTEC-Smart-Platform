import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from "@/components/ui/card";
export default function Dashboard() {
    return (_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-6 animate-in fade-in duration-300", children: [_jsxs(Card, { className: "p-6", children: [_jsx("h3", { className: "text-lg font-semibold", children: "Total Students" }), _jsx("p", { className: "text-3xl font-bold mt-2", children: "128" })] }), _jsxs(Card, { className: "p-6", children: [_jsx("h3", { className: "text-lg font-semibold", children: "AI Assessments" }), _jsx("p", { className: "text-3xl font-bold mt-2", children: "342" })] }), _jsxs(Card, { className: "p-6", children: [_jsx("h3", { className: "text-lg font-semibold", children: "Pending Reviews" }), _jsx("p", { className: "text-3xl font-bold mt-2", children: "17" })] })] }));
}
