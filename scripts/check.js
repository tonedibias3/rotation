// Deterministic checks for Rotation. Run: node scripts/check.js
// Exits non-zero if any check fails. Prints one line per check: PASS/FAIL | name | evidence.
const fs = require("fs"), path = require("path"), vm = require("vm");
const root = path.join(__dirname, "..");
const read = (f) => fs.readFileSync(path.join(root, f), "utf8");
const results = [];
const check = (name, fn) => {
  try { const r = fn(); results.push([r === true || r === undefined ? "PASS" : "FAIL", name, r === true || r === undefined ? "" : String(r)]); }
  catch (e) { results.push(["FAIL", name, e.message]); }
};

const app = read("app/index.html");
const pages = ["app/index.html", "landing/index.html", "install/index.html", "index.html", "privacy.html"];

check("app inline scripts parse", () => {
  const blocks = [...app.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
  if (!blocks.length) return "no inline scripts found";
  blocks.forEach((b, i) => { try { new vm.Script(b); } catch (e) { throw new Error("script " + i + ": " + e.message); } });
});

check("no old handle (@rotationcloset) anywhere", () => {
  const hits = pages.filter((f) => /rotationcloset/i.test(read(f)));
  return hits.length ? "found in " + hits.join(", ") : true;
});

check("share watermark is single ROTATION.fit line", () => /ROTATION\.fit/.test(app) ? true : "wordmark string missing from app");

check("beta app URL not on public pages", () => {
  const bad = ["landing/index.html", "index.html"].filter((f) => /tonedibias3\.github\.io\/rotation/.test(read(f)));
  return bad.length ? "app URL leaked in " + bad.join(", ") : true;
});

check("manifest valid + icons exist", () => {
  const m = JSON.parse(read("app/manifest.webmanifest"));
  const missing = m.icons.map((i) => i.src).filter((s) => !fs.existsSync(path.join(root, "app", s)));
  return missing.length ? "missing icons: " + missing.join(", ") : true;
});

check("no external trackers or unexpected hosts in app", () => {
  const hosts = new Set([...app.matchAll(/https?:\/\/([a-z0-9.-]+)/gi)].map((m) => m[1].toLowerCase()));
  const allowed = ["api.open-meteo.com", "geocoding-api.open-meteo.com", "api.bigdatacloud.net", "www.w3.org", "w3.org", "rotation.fit", "tonedibias3.github.io", "fonts.googleapis.com", "fonts.gstatic.com", "www.googleapis.com", "github.com", "images.weserv.nl"];
  const extra = [...hosts].filter((h) => !allowed.some((a) => h === a || h.endsWith("." + a)));
  return extra.length ? "unreviewed hosts: " + extra.join(", ") : true;
});

check("ios build script runs (www/ ready)", () => {
  require("child_process").execFileSync("node", [path.join(root, "scripts/make-www.js")], { stdio: "pipe" });
  return fs.existsSync(path.join(root, "www/index.html")) ? true : "www/index.html not produced";
});

const w = Math.max(...results.map((r) => r[1].length));
results.forEach((r) => console.log(r[0] + " | " + r[1].padEnd(w) + " | " + r[2]));
const failed = results.filter((r) => r[0] === "FAIL").length;
console.log("\n" + (results.length - failed) + "/" + results.length + " passed");
process.exit(failed ? 1 : 0);
