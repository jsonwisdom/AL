import { EAS, SchemaEncoder } from '@ethereum-attestation-service/eas-sdk';
import { ethers } from 'ethers';
import fs from 'fs';

const EAS_ADDR = '0x4200000000000000000000000000000000000021';
const SCHEMA = 'bytes32 actionHash,address signer,bytes signature,uint64 timestamp,string payloadRef';

async function main() {
  const receipt = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

  const provider = new ethers.JsonRpcProvider(process.env.BASE_SEPOLIA_RPC);
  const signer = new ethers.Wallet(process.env.PRIVATE_KEY!, provider);

  const eas = new EAS(EAS_ADDR);
  eas.connect(signer);

  const encoder = new SchemaEncoder(SCHEMA);
  const data = encoder.encodeData([
    { name: 'actionHash', value: receipt.actionHash, type: 'bytes32' },
    { name: 'signer', value: receipt.signer, type: 'address' },
    { name: 'signature', value: receipt.signature, type: 'bytes' },
    { name: 'timestamp', value: receipt.timestamp ?? Math.floor(Date.now()/1000), type: 'uint64' },
    { name: 'payloadRef', value: receipt.payloadRef ?? '', type: 'string' }
  ]);

  const tx = await eas.attest({
    schema: process.env.EAS_SCHEMA_UID!,
    data: { recipient: receipt.signer, expirationTime: 0, revocable: true, refUID: ethers.ZeroHash, data, value: 0n }
  });

  const uid = await tx.wait();
  console.log(JSON.stringify({ attestationUID: uid, txHash: tx.hash }, null, 2));
}

main();
