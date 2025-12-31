import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
export default function Upload() {
    return (_jsxs("div", { className: "space-y-6 animate-in fade-in duration-300", children: [_jsx("h1", { className: "text-2xl font-bold", children: "Upload Assignment" }), _jsx(Input, { type: "file" }), _jsx(Button, { children: "Upload" })] }));
}
