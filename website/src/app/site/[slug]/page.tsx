import Link from "next/link";
import {
  fetchSite,
  mediaUrl,
  parseJson,
  type PublicSite,
  type SubjectsMap,
  type Topper,
} from "@/lib/api";
import styles from "./school.module.css";

type Props = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Props) {
  const { slug } = await params;
  try {
    const site = await fetchSite(slug);
    return { title: site.tenant.name };
  } catch {
    return { title: "School not found" };
  }
}

function SubjectGroup({ title, items }: { title: string; items?: string[] }) {
  if (!items?.length) return null;
  return (
    <div className={styles.subjectGroup}>
      <h3>{title}</h3>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default async function SchoolSitePage({ params }: Props) {
  const { slug } = await params;
  let site: PublicSite;
  try {
    site = await fetchSite(slug);
  } catch {
    return (
      <main className={styles.wrap}>
        <div className="container">
          <h1>School not found</h1>
          <p>
            <Link href="/">Back to directory</Link>
          </p>
        </div>
      </main>
    );
  }

  const { tenant, website, contact, gallery } = site;
  const panelUrl = process.env.NEXT_PUBLIC_PANEL_URL || "http://127.0.0.1:5173";
  const heroImage = mediaUrl(website?.hero_image_path);
  const aboutImage = mediaUrl(website?.about_image_path);
  const subjects = parseJson<SubjectsMap>(website?.subjects_json, {});
  const toppers = parseJson<Topper[]>(website?.toppers_json, []) || [];
  const legacyAdmin = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  return (
    <div
      className={styles.wrap}
      style={
        {
          "--deep": tenant.primary_color || "#0b3d44",
          "--accent": tenant.accent_color || "#d4a017",
        } as React.CSSProperties
      }
    >
      <header className={styles.topbar}>
        <div className={`container ${styles.topbarInner}`}>
          <Link className={styles.brand} href={`/site/${tenant.slug}`}>
            {tenant.logo_path ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={mediaUrl(tenant.logo_path) || ""} alt="" />
            ) : null}
            <span>{tenant.name}</span>
          </Link>
          <nav className={styles.menu}>
            <a href="#about">About</a>
            <a href="#academics">Academics</a>
            <a href="#toppers">Toppers</a>
            <a href="#method">Method</a>
            <a href="#gallery">Gallery</a>
            <a href="#contact">Contact</a>
            <a className={styles.btnNav} href={panelUrl}>
              Portal login
            </a>
          </nav>
        </div>
      </header>

      <section
        className={styles.hero}
        style={
          heroImage
            ? {
                backgroundImage: `linear-gradient(180deg, rgba(8,28,32,.28), rgba(8,28,32,.78)), url(${heroImage})`,
              }
            : undefined
        }
      >
        <div className={`container ${styles.heroCopy}`}>
          <p className={styles.heroBrand}>{tenant.name}</p>
          <h1>{website?.hero_title || tenant.tagline || "Learning that shapes character and future"}</h1>
          <p className={styles.heroSub}>
            {website?.hero_subtitle ||
              "A caring campus for strong academics, values, and all-round growth."}
          </p>
          <div className={styles.actions}>
            <a className={styles.btn} href={website?.hero_cta_link || "#admissions"}>
              {website?.hero_cta_text || "Apply for admission"}
            </a>
            <a className={styles.btnGhost} href="#academics">
              View academics
            </a>
          </div>
        </div>
      </section>

      <section className={styles.infoStrip} aria-label="School snapshot">
        <div className={`container ${styles.infoGrid}`}>
          <div>
            <span>Board</span>
            <strong>{website?.board_name || "CBSE"}</strong>
          </div>
          <div>
            <span>Classes</span>
            <strong>{website?.classes_offered || "Nursery to Class 12"}</strong>
          </div>
          <div>
            <span>School timing</span>
            <strong>{website?.school_timings || contact?.working_hours || "Mon–Sat · 8:00 AM – 2:30 PM"}</strong>
          </div>
          <div>
            <span>Assembly</span>
            <strong>{website?.assembly_time || "7:50 AM"}</strong>
          </div>
          <div>
            <span>Streams (11–12)</span>
            <strong>{website?.streams_offered || "Science, Commerce, Arts"}</strong>
          </div>
        </div>
      </section>

      <section className={styles.block} id="about">
        <div className={`container ${styles.aboutGrid}`}>
          <div>
            <p className={styles.kicker}>About us</p>
            <h2>{website?.about_heading || `Welcome to ${tenant.name}`}</h2>
            <p className={styles.body}>
              {website?.about_body ||
                tenant.about ||
                `${tenant.name} is committed to academic excellence and a safe campus for every learner.`}
            </p>
          </div>
          <div
            className={styles.aboutVisual}
            style={aboutImage ? { backgroundImage: `url(${aboutImage})` } : undefined}
            aria-hidden
          />
        </div>
      </section>

      <section className={`${styles.block} ${styles.tint}`} id="academics">
        <div className="container">
          <p className={styles.kicker}>Academics</p>
          <h2>Classes, subjects &amp; streams</h2>
          <p className={styles.lead}>
            {tenant.name} follows <strong>{website?.board_name || "CBSE"}</strong> curriculum from{" "}
            <strong>{website?.classes_offered || "Nursery to Class 12"}</strong>. Senior secondary offers{" "}
            <strong>{website?.streams_offered || "Science, Commerce and Arts"}</strong>.
          </p>

          <div className={styles.subjectGrid}>
            <SubjectGroup title="Primary (I–V)" items={subjects?.primary} />
            <SubjectGroup title="Middle (VI–VIII)" items={subjects?.middle} />
            <SubjectGroup title="Secondary (IX–X)" items={subjects?.secondary} />
          </div>

          <h3 className={styles.subheading}>Class 11 &amp; 12 streams</h3>
          <div className={styles.subjectGrid}>
            <SubjectGroup title="Science" items={subjects?.senior?.science} />
            <SubjectGroup title="Commerce" items={subjects?.senior?.commerce} />
            <SubjectGroup title="Arts" items={subjects?.senior?.arts} />
          </div>
        </div>
      </section>

      <section className={styles.block} id="toppers">
        <div className="container">
          <p className={styles.kicker}>Results</p>
          <h2>Our board toppers</h2>
          <p className={styles.lead}>
            Class 10 and Class 12 achievers from Science, Commerce, and Arts — updated from the school website panel.
          </p>
          {toppers.length ? (
            <div className={styles.topperGrid}>
              {toppers.map((t) => (
                <article key={`${t.name}-${t.class_name}-${t.stream}`}>
                  <div
                    className={styles.topperPhoto}
                    style={
                      t.photo_path
                        ? { backgroundImage: `url(${mediaUrl(t.photo_path)})` }
                        : undefined
                    }
                  />
                  <h3>{t.name}</h3>
                  <p>
                    {t.class_name}
                    {t.stream ? ` · ${t.stream}` : ""}
                  </p>
                  <strong>
                    {t.percentage}
                    {t.year ? ` · ${t.year}` : ""}
                  </strong>
                </article>
              ))}
            </div>
          ) : (
            <p className={styles.lead}>Toppers added from the admin Website panel will appear here.</p>
          )}
        </div>
      </section>

      <section className={`${styles.block} ${styles.tint}`} id="method">
        <div className="container">
          <p className={styles.kicker}>Teaching method</p>
          <h2>How we teach</h2>
          <p className={styles.body}>{website?.methodology || "Student-centred CBSE teaching with continuous assessment, labs, and mentorship."}</p>
        </div>
      </section>

      <section className={styles.block} id="gallery">
        <div className="container">
          <p className={styles.kicker}>Gallery</p>
          <h2>{website?.gallery_heading || "Moments from campus"}</h2>
          <p className={styles.lead}>{website?.gallery_subtitle || "Campus photos from the school gallery."}</p>
          {gallery.length ? (
            <div className={styles.gallery}>
              {gallery.map((item) => (
                <figure key={item.id}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={mediaUrl(item.image_path) || ""} alt={item.title || "Campus gallery"} />
                  {item.title || item.caption ? <figcaption>{item.title || item.caption}</figcaption> : null}
                </figure>
              ))}
            </div>
          ) : (
            <p className={styles.lead}>Upload gallery images from the admin Gallery panel.</p>
          )}
        </div>
      </section>

      <section className={`${styles.block} ${styles.deep}`} id="admissions">
        <div className="container">
          <p className={styles.kickerLight}>Admissions</p>
          <h2>Join Greenfield</h2>
          <p className={styles.leadLight}>
            Seats open for Nursery to Class 12. Bring previous marksheet for Class 10/12 lateral entry.
          </p>
          <ol className={styles.steps}>
            <li>
              <strong>Enquiry</strong>
              <span>Call admissions or visit the campus desk.</span>
            </li>
            <li>
              <strong>Campus visit</strong>
              <span>Tour classrooms, labs, and meet teachers.</span>
            </li>
            <li>
              <strong>Application</strong>
              <span>Submit form with documents and photos.</span>
            </li>
            <li>
              <strong>Confirmation</strong>
              <span>Interaction / assessment if needed, then fee confirmation.</span>
            </li>
          </ol>
          <div className={styles.actions}>
            <a className={styles.btn} href="#contact">
              Talk to admissions
            </a>
            <a className={styles.btnGhost} href={`${legacyAdmin}/admin/website`}>
              Edit website (admin panel)
            </a>
          </div>
        </div>
      </section>

      <section className={`${styles.block} ${styles.tint}`} id="contact">
        <div className={`container ${styles.contact}`}>
          <div>
            <p className={styles.kicker}>Contact</p>
            <h2>We are happy to help</h2>
            <ul className={styles.contactList}>
              <li>
                <strong>Address</strong>
                <span>
                  {contact?.address_line1 || "Campus address"}
                  {contact?.city ? (
                    <>
                      <br />
                      {contact.city}
                      {contact.state ? `, ${contact.state}` : ""}
                    </>
                  ) : null}
                </span>
              </li>
              <li>
                <strong>Phone</strong>
                <span>{contact?.phone_primary || "—"}</span>
              </li>
              <li>
                <strong>Email</strong>
                <span>{contact?.email || "—"}</span>
              </li>
              <li>
                <strong>School hours</strong>
                <span>{website?.school_timings || contact?.working_hours || "Mon–Sat · 8:00 AM – 2:30 PM"}</span>
              </li>
            </ul>
          </div>
          <div className={styles.visit}>
            <h3>Front office</h3>
            <p>Walk-ins welcome during school hours. Parent ID may be required at the gate.</p>
            {contact?.map_embed_url ? (
              <iframe src={contact.map_embed_url} title="Map" loading="lazy" />
            ) : (
              <p className={styles.lead}>Map can be added from the admin Contact panel.</p>
            )}
          </div>
        </div>
      </section>

      <footer className={styles.footer}>
        <div className={`container ${styles.footerGrid}`}>
          <div>
            <strong>{tenant.name}</strong>
            <p>{tenant.tagline || "CBSE school · Nursery to Class 12"}</p>
          </div>
          <div>
            <h3>Explore</h3>
            <a href="#academics">Academics</a>
            <a href="#toppers">Toppers</a>
            <a href="#gallery">Gallery</a>
          </div>
          <div>
            <h3>Families</h3>
            <a href="#contact">Contact</a>
            <a href={panelUrl}>Portal login</a>
            <a href={`${legacyAdmin}/login`}>Website panel login</a>
          </div>
        </div>
        <div className={`container ${styles.footerBottom}`}>
          <span>© {tenant.name}</span>
          <span>Board: {website?.board_name || "CBSE"}</span>
        </div>
      </footer>
    </div>
  );
}
