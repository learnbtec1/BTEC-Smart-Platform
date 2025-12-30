import { createBrowserRouter } from "react-router-dom";
import AppLayout from "@/layout/AppLayout";

import Login from "@/pages/Login";
import Dashboard from "@/pages/Dashboard";
import Upload from "@/pages/Upload";
import Results from "@/pages/Results";
import Students from "@/pages/Students";
import Assignments from "@/pages/Assignments";

export const router = createBrowserRouter([
  { path: "/login", element: <Login /> },

  {
    path: "/",
    element: (
      <AppLayout>
        <Dashboard />
      </AppLayout>
    ),
  },

  {
    path: "/upload",
    element: (
      <AppLayout>
        <Upload />
      </AppLayout>
    ),
  },

  {
    path: "/results",
    element: (
      <AppLayout>
        <Results />
      </AppLayout>
    ),
  },

  {
    path: "/students",
    element: (
      <AppLayout>
        <Students />
      </AppLayout>
    ),
  },

  {
    path: "/assignments",
    element: (
      <AppLayout>
        <Assignments />
      </AppLayout>
    ),
  },
]);