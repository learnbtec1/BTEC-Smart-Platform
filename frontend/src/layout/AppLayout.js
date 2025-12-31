import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Home, Upload, FileText, Users, BookOpen } from "lucide-react";
export default function AppLayout({ children }) {
    const [dark, setDark] = useState(false);
    useEffect(() => {
        if (dark)
            document.documentElement.classList.add("dark");
        else
            document.documentElement.classList.remove("dark");
    }, [dark]);
    return (_jsxs("div", { className: "flex min-h-screen bg-background text-foreground", children: [_jsxs("aside", { className: "w-64 border-r p-6", children: [_jsx("h2", { className: "text-xl font-bold mb-6", children: "BTEC Platform" }), _jsxs("nav", { className: "flex flex-col gap-4", children: [_jsxs(Link, { to: "/", className: "flex items-center gap-2 hover:text-primary", children: [_jsx(Home, { size: 18 }), " Dashboard"] }), _jsxs(Link, { to: "/upload", className: "flex items-center gap-2 hover:text-primary", children: [_jsx(Upload, { size: 18 }), " Upload"] }), _jsxs(Link, { to: "/results", className: "flex items-center gap-2 hover:text-primary", children: [_jsx(FileText, { size: 18 }), " Results"] }), _jsxs(Link, { to: "/students", className: "flex items-center gap-2 hover:text-primary", children: [_jsx(Users, { size: 18 }), " Students"] }), _jsxs(Link, { to: "/assignments", className: "flex items-center gap-2 hover:text-primary", children: [_jsx(BookOpen, { size: 18 }), " Assignments"] })] })] }), _jsxs("div", { className: "flex-1 flex flex-col", children: [_jsx("header", { className: "border-b p-4 flex justify-end", children: _jsx(Button, { variant: "outline", onClick: () => setDark(!dark), children: dark ? "Light Mode" : "Dark Mode" }) }), _jsx("main", { className: "flex-1 p-10", children: children })] })] }));
}
