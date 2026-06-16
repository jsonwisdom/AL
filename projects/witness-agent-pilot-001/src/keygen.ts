// Generate EC key pair (P-256 / secp256r1)
const keyPair = await crypto.subtle.generateKey(
  { name: "ECDSA", namedCurve: "P-256" },
  true,
  ["sign", "verify"]
);

const pubRaw = await crypto.subtle.exportKey("raw", keyPair.publicKey);
const publicKeyHex = Array.from(new Uint8Array(pubRaw)).map(b => b.toString(16).padStart(2, '0')).join('');

const privRaw = await crypto.subtle.exportKey("pkcs8", keyPair.privateKey);
const privateKeyHex = Array.from(new Uint8Array(privRaw)).map(b => b.toString(16).padStart(2, '0')).join('');

await Deno.writeTextFile("./keys/public_key.hex", publicKeyHex);
await Deno.writeTextFile("./keys/private_key.pkcs8.hex", privateKeyHex);

console.log("✅ Keys generated:");
console.log("   Public:", publicKeyHex.slice(0, 32) + "...");
console.log("   Private saved to keys/private_key.pkcs8.hex (KEEP SECRET)");
