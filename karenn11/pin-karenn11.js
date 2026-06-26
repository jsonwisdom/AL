import fs from "fs";
import FormData from "form-data";
import axios from "axios";

const JWT = process.env.PINATA_JWT;
if (!JWT) throw new Error("Missing PINATA_JWT");

function sleep(ms){ return new Promise(r => setTimeout(r, ms)); }

async function retry(fn, label, max = 3) {
  for (let i = 1; i <= max; i++) {
    try { return await fn(); }
    catch (err) {
      console.error(`${label} attempt ${i} failed:`, err.response?.data || err.message);
      if (i === max) throw err;
      await sleep(1000 * i);
    }
  }
}

async function pinFile(path, name) {
  if (!fs.existsSync(path)) throw new Error(`Missing file: ${path}`);
  return retry(async () => {
    const data = new FormData();
    data.append("file", fs.createReadStream(path), name);
    const res = await axios.post("https://api.pinata.cloud/pinning/pinFileToIPFS", data, {
      maxBodyLength: Infinity,
      headers: { Authorization: `Bearer ${JWT}`, ...data.getHeaders() }
    });
    return res.data.IpfsHash;
  }, `pinFile ${name}`);
}

async function pinJSON(json) {
  return retry(async () => {
    const res = await axios.post("https://api.pinata.cloud/pinning/pinJSONToIPFS",
      { pinataContent: json },
      { headers: { Authorization: `Bearer ${JWT}`, "Content-Type": "application/json" } }
    );
    return res.data.IpfsHash;
  }, "pinJSON");
}

const metadata = JSON.parse(fs.readFileSync("./karenn11/karenn11-weather-goblin-metadata.json", "utf8"));
const imageCID = await pinFile("./karenn11/front.jpeg", "karenn11-front.jpeg");
const gifCID = await pinFile("./karenn11/goblin-meltdown.gif", "goblin-meltdown.gif");

metadata.image = `ipfs://${imageCID}`;
metadata.animation_url = `ipfs://${gifCID}`;
metadata.properties.files[0].uri = `ipfs://${imageCID}`;

fs.writeFileSync("./karenn11/final-metadata.json", JSON.stringify(metadata, null, 2));

const metadataCID = await pinJSON(metadata);

console.log("IMAGE:", `ipfs://${imageCID}`);
console.log("GIF:", `ipfs://${gifCID}`);
console.log("TOKEN_URI:", `ipfs://${metadataCID}`);
