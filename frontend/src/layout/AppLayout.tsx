import { ReactNode, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Home, Upload, FileText, Users, BookOpen } from "lucide-react";

export default function AppLayout({ children }: { children: ReactNode }) {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    if (dark) document.documentElement.classList.add("dark");
    else document.documentElement.classList.remove("dark");
  }, [dark]);

  return (
    <div className="flex min-h-screen bg-background text-foreground">
      {/* Sidebar */}
      <aside className="w-64 border-r p-6">
        <h2 className="text-xl font-bold mb-6">BTEC Platform</h2>

        <nav className="flex flex-col gap-4">
          <Link to="/" className="flex items-center gap-2 hover:text-primary">
            <Home size={18} /> Dashboard
          </Link>

          <Link to="/upload" className="flex items-center gap-2 hover:text-primary">
            <Upload size={18} /> Upload
          </Link>

          <Link to="/results" className="flex items-center gap-2 hover:text-primary">
            <FileText size={18} /> Results
          </Link>

          <Link to="/students" className="flex items-center gap-2 hover:text-primary">
            <Users size={18} /> Students
          </Link>

          <Link to="/assignments" className="flex items-center gap-2 hover:text-primary">
            <BookOpen size={18} /> Assignments
          </Link>
        </nav>
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col">
        <header className="border-b p-4 flex justify-end">
          <Button variant="outline" onClick={() => setDark(!dark)}>
            {dark ? "Light Mode" : "Dark Mode"}
          </Button>
        </header>

        <main className="flex-1 p-10">{children}</main>
      </div>
    </div>
  );
}