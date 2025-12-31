import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from "@/components/ui/card";
export default function Results() {
    return (_jsxs("div", { className: "space-y-6 animate-in fade-in duration-300", children: [_jsx("h1", { className: "text-2xl font-bold", children: "AI Assessment Results" }), _jsxs(Card, { className: "p-6", children: [_jsx("h3", { className: "text-lg font-semibold", children: "Student: John Doe" }), _jsx("p", { className: "mt-2", children: "Score: 87%" }), _jsx("p", { className: "text-muted-foreground mt-1", children: "Feedback: Good structure, minor issues." })] })] }));
}
