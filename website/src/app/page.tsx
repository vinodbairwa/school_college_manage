import Link from "next/link";
import { fetchTenants, type PublicTenant } from "@/lib/api";

export default async function HomePage() {
  let tenants: PublicTenant[] = [];
  let error = "";
  try {
    tenants = await fetchTenants();
  } catch {
    error = "Backend API is not reachable. Start FastAPI on port 8000.";
  }

  return (
    <main className="home">
      <div className="container">
        <h1>EduNest Schools</h1>
        <p>Choose a school or college website. Public sites are powered by Next.js and the FastAPI backend.</p>
        {error ? <p className="error">{error}</p> : null}
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
