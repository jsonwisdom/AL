import { create } from "ipfs-http-client";
import fs from "fs";

const client = create({ url: "https://ipfs.infura.io:5001/api/v0" });

const file = process.argv[2];
const content = fs.readFileSync(file);

const result = await client.add(content);
console.log("CID:", result.cid.toString());
