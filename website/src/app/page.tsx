import Link from "next/link";
import { fetchTenants, type PublicTenant } from "@/lib/api";
import { BackendDown } from "@/components/BackendDown";

export default async function HomePage() {
  let tenants: PublicTenant[] = [];
  let showBackendDown = false;

  try {
    tenants = await fetchTenants();
  } catch {
    showBackendDown = true;
  }

  return (
    <main className="home">
      <div className="container">
        <h1>EduNest Schools</h1>
        <p>
          Choose a school or college website. Public sites are powered by Next.js and the FastAPI
          backend.
        </p>

        {showBackendDown ? <BackendDown /> : null}

        <div className="school-list">
          {tenants.map((tenant) => (
            <Link key={tenant.id} href={`/site/${tenant.slug}`}>
              <strong>{tenant.name}</strong>
              <span className="muted">{tenant.tagline || tenant.institution_type}</span>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
