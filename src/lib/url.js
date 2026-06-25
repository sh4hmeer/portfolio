// Prefix a site-relative path with Astro's configured base so links keep working
// whether the site is served from a user repo (base '/') or a project repo
// (base '/portfolio/'). Pass paths WITHOUT a leading slash, e.g. 'clinic/x.html'.
const BASE = import.meta.env.BASE_URL || '/';
export function withBase(path) {
  const b = BASE.endsWith('/') ? BASE : BASE + '/';
  return b + String(path).replace(/^\/+/, '');
}
