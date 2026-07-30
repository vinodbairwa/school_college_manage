import Link from "next/link";
import { fetchTenants, type PublicTenant } from "@/lib/api";

export default async function HomePage() {
  let tenants: PublicTenant[] = [];
  let error = "";
  try {
    tenants = await fetchTenants();
  } catch {
    error = "backend_unreachable";
  }

  return (
    <main className="home">
      <div className="container">
        <h1>EduNest Schools</h1>
        <p>Choose a school or college website. Public sites are powered by Next.js and the FastAPI backend.</p>
        {error ? (
          <div className="error">
            <strong>Backend API is not reachable on port 8000.</strong>
            <p style={{ margin: "0.75rem 0 0" }}>
              Website alone is not enough — FastAPI backend must also be running.
            </p>
            <ol style={{ margin: "0.75rem 0 0", paddingLeft: "1.2rem", lineHeight: 1.6 }}>
                From project root run: <code>npm start</code> (starts backend + website + panel)
              </li>
              <li>
                Confirm backend: open <code>http://127.0.0.1:8000/health</code>
              </li>
              <li>Then refresh this page. Full help: <code>LOCAL_SETUP.md</code></li>
            </ol>
          </div>
        ) : null}
        <div className="school-list">
          {tenants.map((t) => (
            <Link key={t.id} href={`/site/${t.slug}`}>
              <strong>{t.name}</strong>
              <span className="muted">{t.tagline || t.institution_type}</span>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
