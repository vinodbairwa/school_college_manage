import Link from "next/link";
import { fetchSite, mediaUrl, type PublicSite } from "@/lib/api";
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
          <p><Link href="/">Back to directory</Link></p>
        </div>
      </main>
    );
  }

  const { tenant, website, contact, gallery } = site;
  const panelUrl = process.env.NEXT_PUBLIC_PANEL_URL || "http://127.0.0.1:5173";
  const heroImage = mediaUrl(website?.hero_image_path);
  const aboutImage = mediaUrl(website?.about_image_path);

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
            <a href="#campus">Campus</a>
            <a href="#admissions">Admissions</a>
            <a href="#gallery">Gallery</a>
            <a href="#contact">Contact</a>
            <a className={styles.btnNav} href={panelUrl}>Portal login</a>
          </nav>
        </div>
      </header>

      <section
        className={styles.hero}
        style={heroImage ? { backgroundImage: `linear-gradient(180deg, rgba(8,28,32,.28), rgba(8,28,32,.78)), url(${heroImage})` } : undefined}
      >
        <div className={`container ${styles.heroCopy}`}>
          <p className={styles.heroBrand}>{tenant.name}</p>
          <h1>{website?.hero_title || tenant.tagline || "Learning that shapes character and future"}</h1>
          <p className={styles.heroSub}>
            {website?.hero_subtitle ||
              "A caring campus for strong academics, values, and all-round growth — built for every student and family."}
          </p>
          <div className={styles.actions}>
            <a className={styles.btn} href={website?.hero_cta_link || "#admissions"}>
              {website?.hero_cta_text || "Apply for admission"}
            </a>
            <a className={styles.btnGhost} href="#about">Explore campus</a>
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
                `${tenant.name} is committed to academic excellence, character formation, and a safe, welcoming campus for every learner.`}
            </p>
            <ul className={styles.plainList}>
              <li>Safe, disciplined, and inclusive learning environment</li>
              <li>Experienced teachers and personal attention</li>
              <li>Balanced focus on academics, arts, sports, and values</li>
            </ul>
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
          <h2>A complete education for every learner</h2>
          <p className={styles.lead}>
            Clear curriculum, skilled teachers, and steady progress checks that keep students confident and future-ready.
          </p>
          <div className={styles.features}>
            <article><h3>Strong curriculum</h3><p>Age-appropriate syllabus with clear learning goals and regular assessments.</p></article>
            <article><h3>Dedicated teachers</h3><p>Qualified educators who mentor students and partner with families.</p></article>
            <article><h3>Skills &amp; values</h3><p>Communication, teamwork, digital literacy, and ethics in daily learning.</p></article>
            <article><h3>Holistic growth</h3><p>Sports, arts, clubs, and community service beyond textbooks.</p></article>
          </div>
        </div>
      </section>

      <section className={styles.block} id="campus">
        <div className="container">
          <p className={styles.kicker}>Campus life</p>
          <h2>A place students are proud to belong</h2>
          <p className={styles.lead}>
            From morning assembly to evening practice, campus life at {tenant.name} builds friendship, discipline, and joy in learning.
          </p>
          <div className={styles.split}>
            <div>
              <h3>What students experience</h3>
              <ul>
                <li>Well-kept classrooms and learning spaces</li>
                <li>Library / reading corner and digital resources</li>
                <li>Playground and indoor activity areas</li>
                <li>Clean campus with focus on student safety</li>
              </ul>
            </div>
            <div>
              <h3>Co-curricular highlights</h3>
              <ul>
                <li>Sports day, annual day, and cultural events</li>
                <li>Debates, quizzes, and exhibitions</li>
                <li>Art, music, and drama opportunities</li>
                <li>Leadership roles and value education</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section className={`${styles.block} ${styles.deep}`} id="admissions">
        <div className="container">
          <p className={styles.kickerLight}>Admissions</p>
          <h2>Start your journey with us</h2>
          <p className={styles.leadLight}>Enquiry → campus visit → application → confirmation. Simple steps for every family.</p>
          <ol className={styles.steps}>
            <li><strong>Enquiry</strong><span>Call, email, or visit the campus desk.</span></li>
            <li><strong>Campus visit</strong><span>Tour classrooms and meet our team.</span></li>
            <li><strong>Application</strong><span>Submit form with required documents.</span></li>
            <li><strong>Confirmation</strong><span>Complete interaction if needed, then join.</span></li>
          </ol>
          <div className={styles.actions}>
            <a className={styles.btn} href="#contact">Talk to admissions</a>
            <a className={styles.btnGhost} href={panelUrl}>Parent / student portal</a>
          </div>
        </div>
      </section>

      <section className={styles.block} id="gallery">
        <div className="container">
          <p className={styles.kicker}>Gallery</p>
          <h2>{website?.gallery_heading || "Moments from campus"}</h2>
          <p className={styles.lead}>{website?.gallery_subtitle || "A glimpse of classrooms, celebrations, sports, and everyday learning."}</p>
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
            <p className={styles.lead}>Gallery images uploaded from the admin panel will appear here.</p>
          )}
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
                  {contact?.city ? <><br />{contact.city}{contact.state ? `, ${contact.state}` : ""}</> : null}
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
                <strong>Hours</strong>
                <span>{contact?.working_hours || "Mon–Sat · 8:30 AM – 3:30 PM"}</span>
              </li>
            </ul>
          </div>
          <div className={styles.visit}>
            <h3>Front office</h3>
            <p>Walk-ins are welcome during office hours.</p>
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
            <p>{tenant.tagline || "A trusted place for learning, values, and growth."}</p>
          </div>
          <div>
            <h3>Explore</h3>
            <a href="#about">About</a>
            <a href="#academics">Academics</a>
            <a href="#admissions">Admissions</a>
          </div>
          <div>
            <h3>Families</h3>
            <a href="#contact">Contact</a>
            <a href={panelUrl}>Portal login</a>
          </div>
        </div>
        <div className={`container ${styles.footerBottom}`}>
          <span>© {tenant.name}</span>
          <span>Powered by EduNest · Next.js website</span>
        </div>
      </footer>
    </div>
  );
}
