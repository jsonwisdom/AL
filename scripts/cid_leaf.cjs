const fs = require("fs");
const Hash = require("ipfs-only-hash");

(async () => {
  const file = process.argv[2];
  if (!file) {
    console.error("usage: node scripts/cid_leaf.cjs <file>");
    process.exit(1);
  }

  const data = fs.readFileSync(file);
  const cid = await Hash.of(data, { cidVersion: 1, rawLeaves: false });
  console.log(cid);
})();
