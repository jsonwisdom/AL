import { jcsStringify } from "./jcs.ts";
import { CommitmentEnvelope } from "./types.ts";

export async function signEnvelope(
  envelope: CommitmentEnvelope,
  privateKeyHex: string
): Promise<string> {
  const canonical = jcsStringify(envelope);
  const privateKeyBytes = new Uint8Array(privateKeyHex.match(/.{1,2}/g)!.map(b => parseInt(b, 16)));
  
  const privateKey = await crypto.subtle.importKey(
    "pkcs8",
    privateKeyBytes,
    { name: "ECDSA", namedCurve: "P-256" },
    false,
    ["sign"]
  );
  
  const signature = await crypto.subtle.sign(
    { name: "ECDSA", hash: "SHA-256" },
    privateKey,
    new TextEncoder().encode(canonical)
  );
  
  return Array.from(new Uint8Array(signature)).map(b => b.toString(16).padStart(2, '0')).join('');
}

export async function verifyEnvelope(
  envelope: CommitmentEnvelope,
  signature: string,
  publicKeyHex: string
): Promise<boolean> {
  const canonical = jcsStringify(envelope);
  const sigBytes = new Uint8Array(signature.match(/.{1,2}/g)!.map(b => parseInt(b, 16)));
  const pubKeyBytes = new Uint8Array(publicKeyHex.match(/.{1,2}/g)!.map(b => parseInt(b, 16)));
  
  const publicKey = await crypto.subtle.importKey(
    "raw",
    pubKeyBytes,
    { name: "ECDSA", namedCurve: "P-256" },
    false,
    ["verify"]
  );
  
  return await crypto.subtle.verify(
    { name: "ECDSA", hash: "SHA-256" },
    publicKey,
    sigBytes,
    new TextEncoder().encode(canonical)
  );
}
