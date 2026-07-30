const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export type PublicTenant = {
  id: number;
  name: string;
  slug: string;
  institution_type: string;
  tagline?: string | null;
  logo_path?: string | null;
  primary_color: string;
  accent_color: string;
};

export type PublicSite = {
  tenant: {
    id: number;
    name: string;
    slug: string;
    institution_type: string;
    tagline?: string | null;
    about?: string | null;
    logo_path?: string | null;
    primary_color: string;
    accent_color: string;
  };
  website?: {
    hero_title?: string | null;
    hero_subtitle?: string | null;
    hero_image_path?: string | null;
    hero_cta_text: string;
    hero_cta_link: string;
    about_heading?: string | null;
    about_body?: string | null;
    about_image_path?: string | null;
    gallery_heading: string;
    gallery_subtitle?: string | null;
  } | null;
  contact?: {
    address_line1?: string | null;
    address_line2?: string | null;
    city?: string | null;
    state?: string | null;
    pincode?: string | null;
    country?: string;
    phone_primary?: string | null;
    phone_secondary?: string | null;
    email?: string | null;
    email_admissions?: string | null;
    working_hours?: string | null;
    map_embed_url?: string | null;
    facebook_url?: string | null;
    instagram_url?: string | null;
    youtube_url?: string | null;
  } | null;
  gallery: Array<{
    id: number;
    title?: string | null;
    caption?: string | null;
    image_path: string;
  }>;
};

export function mediaUrl(path?: string | null) {
  if (!path) return null;
  if (path.startsWith("http")) return path;
  return `${API_BASE}${path.startsWith("/") ? "" : "/"}${path}`;
}

export async function fetchTenants(): Promise<PublicTenant[]> {
  const res = await fetch(`${API_BASE}/api/public/tenants`, { next: { revalidate: 30 } });
  if (!res.ok) throw new Error("Failed to load schools");
  return res.json();
}

export async function fetchSite(slug: string): Promise<PublicSite> {
  const res = await fetch(`${API_BASE}/api/public/site/${slug}`, { next: { revalidate: 15 } });
  if (!res.ok) throw new Error("School not found");
  return res.json();
}

export { API_BASE };
