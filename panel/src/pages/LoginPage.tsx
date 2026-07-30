import { useEffect, useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { fetchTenants, loginJson, roleHome, type TenantOption } from "../lib/api";

export default function LoginPage() {
  const navigate = useNavigate();
  const [tenants, setTenants] = useState<TenantOption[]>([]);
  const [tenantSlug, setTenantSlug] = useState("");
  const [email, setEmail] = useState("admin@greenfield.edu");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTenants()
      .then((list) => {
        setTenants(list);
        if (list[0]) setTenantSlug(list[0].slug);
      })
      .catch(() => setError("Backend API not reachable on port 8000"));
  }, []);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const result = await loginJson(email, password, tenantSlug || undefined);
      localStorage.setItem("edunest_token", result.access_token);
      localStorage.setItem("edunest_role", result.role);
      navigate(roleHome(result.role));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-page">
      <form className="auth-card" onSubmit={onSubmit}>
        <h1>EduNest Panel</h1>
        <p>Sign in to your school admin / staff portal (React)</p>
        {error ? <div className="alert">{error}</div> : null}
        <label>
          School / Institution
          <select value={tenantSlug} onChange={(e) => setTenantSlug(e.target.value)}>
            <option value="">Platform Super Admin</option>
            {tenants.map((t) => (
              <option key={t.id} value={t.slug}>
                {t.name} ({t.slug})
              </option>
            ))}
          </select>
        </label>
        <label>
          Email
          <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
        </label>
        <label>
          Password
          <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Signing in…" : "Sign in"}
        </button>
        <p className="hint">Demo: admin@greenfield.edu / admin123</p>
      </form>
    </main>
  );
}
