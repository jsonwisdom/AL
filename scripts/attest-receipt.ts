import { EAS, SchemaEncoder } from '@ethereum-attestation-service/eas-sdk';
import { ethers } from 'ethers';
import fs from 'fs';

const EAS_ADDR = '0x4200000000000000000000000000000000000021';
const SCHEMA = 'bytes32 actionHash,address signer,bytes signature,uint64 timestamp,string payloadRef';

async function main() {
  const receiptPath = process.argv[2];
  if (!receiptPath) throw new Error('Usage: npx ts-node scripts/attest-receipt.ts <receipt.json>');
  if (!process.env.BASE_SEPOLIA_RPC) throw new Error('BASE_SEPOLIA_RPC missing');
  if (!process.env.PRIVATE_KEY) throw new Error('PRIVATE_KEY missing');
  if (!process.env.EAS_SCHEMA_UID) throw new Error('EAS_SCHEMA_UID missing');

  const receipt = JSON.parse(fs.readFileSync(receiptPath, 'utf8'));
  if (!receipt.actionHash || !receipt.signer || !receipt.signature) {
    throw new Error('Receipt must contain actionHash, signer, and signature');
  }

  const provider = new ethers.JsonRpcProvider(process.env.BASE_SEPOLIA_RPC);
  const signer = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

  const eas = new EAS(EAS_ADDR);
  eas.connect(signer);

  const encoder = new SchemaEncoder(SCHEMA);
  const encodedData = encoder.encodeData([
    { name: 'actionHash', value: receipt.actionHash, type: 'bytes32' },
    { name: 'signer', value: receipt.signer, type: 'address' },
    { name: 'signature', value: receipt.signature, type: 'bytes' },
    { name: 'timestamp', value: receipt.timestamp ?? Math.floor(Date.now() / 1000), type: 'uint64' },
    { name: 'payloadRef', value: receipt.payloadRef ?? '', type: 'string' }
  ]);

  const tx = await eas.attest({
    schema: process.env.EAS_SCHEMA_UID,
    data: {
      recipient: receipt.signer,
      expirationTime: 0,
      revocable: true,
      refUID: ethers.ZeroHash,
      data: encodedData,
      value: 0n
    }
  });

  const attestationUID = await tx.wait();

  console.log(JSON.stringify({
    network: 'base-sepolia',
    eas: EAS_ADDR,
    schemaUID: process.env.EAS_SCHEMA_UID,
    actionHash: receipt.actionHash,
    signer: receipt.signer,
    attestationUID,
    txHash: tx.hash
  }, null, 2));
}

main().catch((err) => {
  console.error(JSON.stringify({
    state: 'ATTEST_RECEIPT_FAILED',
    error: err instanceof Error ? err.message : String(err)
  }, null, 2));
  process.exit(1);
});
