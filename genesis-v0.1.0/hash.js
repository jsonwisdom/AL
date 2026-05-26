const crypto = require("crypto");
const { canonicalize } = require("./canonicalize");
function sha256Hex(bytes) {
  return crypto.createHash("sha256").update(bytes).digest("hex");
}
function hash_event(obj) {
  return sha256Hex(Buffer.from(canonicalize(obj), "utf8"));
}
module.exports = { sha256Hex, hash_event };
