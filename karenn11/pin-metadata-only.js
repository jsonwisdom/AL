import fs from "fs";
import axios from "axios";

const JWT = process.env.PINATA_JWT;
if (!JWT) throw new Error("Missing PINATA_JWT");

const metadata = JSON.parse(
  fs.readFileSync("./karenn11/karenn11-weather-goblin-metadata.json", "utf8")
);

const res = await axios.post(
  "https://api.pinata.cloud/pinning/pinJSONToIPFS",
  {
    pinataMetadata: { name: "KARENN11 Weather Goblin Exclusive Metadata" },
    pinataContent: metadata
  },
  {
    headers: {
      Authorization: `Bearer ${JWT}`,
      "Content-Type": "application/json"
    }
  }
);

console.log("METADATA_CID:", res.data.IpfsHash);
console.log("TOKEN_URI:", `ipfs://${res.data.IpfsHash}`);
console.log("GATEWAY:", `https://gateway.pinata.cloud/ipfs/${res.data.IpfsHash}`);
