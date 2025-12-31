import { jsx as _jsx } from "react/jsx-runtime";
import { createBrowserRouter } from "react-router-dom";
import AppLayout from "@/layout/AppLayout";
import Login from "@/pages/Login";
import Dashboard from "@/pages/Dashboard";
import Upload from "@/pages/Upload";
import Results from "@/pages/Results";
import Students from "@/pages/Students";
import Assignments from "@/pages/Assignments";
export const router = createBrowserRouter([
    { path: "/login", element: _jsx(Login, {}) },
    {
        path: "/",
        element: (_jsx(AppLayout, { children: _jsx(Dashboard, {}) })),
    },
    {
        path: "/upload",
        element: (_jsx(AppLayout, { children: _jsx(Upload, {}) })),
    },
    {
        path: "/results",
        element: (_jsx(AppLayout, { children: _jsx(Results, {}) })),
    },
    {
        path: "/students",
        element: (_jsx(AppLayout, { children: _jsx(Students, {}) })),
    },
    {
        path: "/assignments",
        element: (_jsx(AppLayout, { children: _jsx(Assignments, {}) })),
    },
]);
