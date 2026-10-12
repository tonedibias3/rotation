// Copies the website files into www/, which is what the iOS app wraps.
const fs = require("fs"), path = require("path");
const root = path.join(__dirname, ".."), out = path.join(root, "www");
fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out);
for (const f of ["index.html", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png"]) fs.copyFileSync(path.join(root, f), path.join(out, f));
console.log("www/ ready");
