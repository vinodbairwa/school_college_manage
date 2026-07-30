const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export type LoginResponse = {
  access_token: string;
  token_type: string;
  role: string;
  redirect_to: string;
};

export type TenantOption = {
  id: number;
  name: string;
  slug: string;
  institution_type: string;
};

export async function fetchTenants(): Promise<TenantOption[]> {
  const res = await fetch(`${API_BASE}/api/public/tenants`);
  if (!res.ok) throw new Error("Failed to load tenants");
  return res.json();
}

export async function loginJson(email: string, password: string, tenant_slug?: string) {
  const res = await fetch(`${API_BASE}/api/auth/login-json`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ email, password, tenant_slug: tenant_slug || null }),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    const detail = data.detail;
    const message = Array.isArray(detail)
      ? detail.map((d: { msg?: string }) => d.msg).filter(Boolean).join(", ")
      : detail || "Invalid login";
    throw new Error(message);
  }
  return (await res.json()) as LoginResponse;
}

export function roleHome(role: string) {
  switch (role) {
    case "super_admin":
      return "/super-admin";
    case "admin":
      return "/admin";
    case "teacher":
      return "/teacher";
    case "student":
      return "/student";
    case "parent":
      return "/parent";
    default:
      return "/";
  }
}

export { API_BASE };
