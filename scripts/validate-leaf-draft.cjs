const fs = require("fs");
const cp = require("child_process");

const draftPath = process.argv[2] || "drafts/leaf-002/draft-manifest.json";

function fail(msg) {
  console.error("FAIL:", msg);
  process.exit(1);
}

const draft = JSON.parse(fs.readFileSync(draftPath, "utf8"));
const head = cp.execSync("git rev-parse --short HEAD").toString().trim();

if (!/^AL-[A-Z0-9-]+-\d{3}$/.test(draft.audit_id)) fail("audit_id format invalid");
if (draft.review_status !== "APPROVED") fail("review_status must be APPROVED");
if (draft.witness_status !== "DRAFT") fail("witness_status must be DRAFT before wallet witness");
if (!draft.source_url || !/^https?:\/\//.test(draft.source_url)) fail("source_url must be http(s)");
if (!Array.isArray(draft.claims)) fail("claims must be an array");
if (draft.git_commit && draft.git_commit !== head) fail(`git_commit mismatch: draft=${draft.git_commit} head=${head}`);

for (const claim of draft.claims) {
  if (!claim.id || !claim.statement) fail("each claim needs id and statement");
  if (!["FACTUAL", "PREDICTIVE", "INTEGRITY", "EXISTENCE"].includes(claim.type)) {
    fail(`claim ${claim.id} missing valid type`);
  }
}

console.log("PASS: leaf draft validated");
console.log(JSON.stringify({ draftPath, head }, null, 2));
