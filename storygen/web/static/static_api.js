// Static-site data layer: answers api() calls from the JSON files exported by scripts/build_static.py (/info, /spec,
// /samples). Stories themselves are generated in the browser, so only the live Python check (/story/<seed>) is missing.
const files = new Map();
export async function staticApi(path) {
  const rel = path.replace(/^\/+/, '').split('?')[0];
  if (!files.has(rel)) files.set(rel, fetch('api/' + rel + '.json').then(r => { if (!r.ok) throw new Error(`${r.status} ${rel}`); return r.json(); }));
  return files.get(rel);
}
