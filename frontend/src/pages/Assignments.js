import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
export default function Assignments() {
    const assignments = [
        { title: "Unit 1 – Business Environment", due: "2025-01-10" },
        { title: "Unit 2 – Marketing Essentials", due: "2025-01-15" },
        { title: "Unit 3 – Finance for Business", due: "2025-01-20" },
    ];
    return (_jsxs("div", { className: "space-y-6 animate-in fade-in duration-300", children: [_jsx("h1", { className: "text-2xl font-bold", children: "Assignments" }), _jsx("div", { className: "border rounded-lg p-4", children: _jsxs("table", { className: "w-full", children: [_jsx("thead", { children: _jsxs("tr", { className: "text-left border-b", children: [_jsx("th", { className: "py-2", children: "Assignment" }), _jsx("th", { className: "py-2", children: "Due Date" })] }) }), _jsx("tbody", { children: assignments.map((a) => (_jsxs("tr", { className: "border-b", children: [_jsx("td", { className: "py-2", children: a.title }), _jsx("td", { className: "py-2", children: a.due })] }, a.title))) })] }) })] }));
}
