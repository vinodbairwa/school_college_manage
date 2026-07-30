import { Link, useNavigate } from "react-router-dom";

const titles: Record<string, string> = {
  "/admin": "School Admin Panel",
  "/super-admin": "Super Admin Panel",
  "/teacher": "Teacher Panel",
  "/student": "Student Panel",
  "/parent": "Parent Panel",
};

export default function PanelHome({ path }: { path: string }) {
  const navigate = useNavigate();
  const role = localStorage.getItem("edunest_role") || "user";
  const websiteUrl = import.meta.env.VITE_WEBSITE_URL || "http://127.0.0.1:3000";

  function logout() {
    localStorage.removeItem("edunest_token");
    localStorage.removeItem("edunest_role");
    navigate("/login");
  }

  return (
    <div className="panel-shell">
      <aside>
        <h2>EduNest</h2>
        <nav>
          <Link to={path}>Dashboard</Link>
          <a href={`${websiteUrl}/site/greenfield`} target="_blank" rel="noreferrer">
            View public site
          </a>
          <button type="button" onClick={logout}>
            Logout
          </button>
        </nav>
      </aside>
      <main>
        <h1>{titles[path] || "Panel"}</h1>
        <p>
          Role: <strong>{role}</strong>. This React panel talks to the FastAPI backend. Website content editing
          screens will move here next; legacy Jinja admin remains on the API host for now.
        </p>
      </main>
    </div>
  );
}
