import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
export default function Students() {
    const students = [
        { name: "John Doe", id: "STU-001" },
        { name: "Sarah Smith", id: "STU-002" },
        { name: "Michael Brown", id: "STU-003" },
    ];
    return (_jsxs("div", { className: "space-y-6 animate-in fade-in duration-300", children: [_jsx("h1", { className: "text-2xl font-bold", children: "Students" }), _jsx("div", { className: "border rounded-lg p-4", children: _jsxs("table", { className: "w-full", children: [_jsx("thead", { children: _jsxs("tr", { className: "text-left border-b", children: [_jsx("th", { className: "py-2", children: "Name" }), _jsx("th", { className: "py-2", children: "ID" })] }) }), _jsx("tbody", { children: students.map((s) => (_jsxs("tr", { className: "border-b", children: [_jsx("td", { className: "py-2", children: s.name }), _jsx("td", { className: "py-2", children: s.id })] }, s.id))) })] }) })] }));
}
