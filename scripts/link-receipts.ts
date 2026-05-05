import { EAS, SchemaEncoder } from '@ethereum-attestation-service/eas-sdk';
import { ethers } from 'ethers';
import fs from 'fs';

const EAS_ADDR = '0x4200000000000000000000000000000000000021';
const SCHEMA = 'bytes32 parentUID,bytes32 childUID,bytes32 parentActionHash,bytes32 childActionHash,address parentSigner,address childSigner,string relation,uint64 timestamp,string payloadRef';

async function main() {
  const [parentPath, childPath, relation] = process.argv.slice(2);
  if (!parentPath || !childPath || !relation) throw new Error('Usage: link parent.json child.json relation');

  const parent = JSON.parse(fs.readFileSync(parentPath, 'utf8'));
  const child = JSON.parse(fs.readFileSync(childPath, 'utf8'));

  const provider = new ethers.JsonRpcProvider(process.env.BASE_SEPOLIA_RPC);
  const signer = new ethers.Wallet(process.env.PRIVATE_KEY!, provider);

  const eas = new EAS(EAS_ADDR);
  eas.connect(signer);

  const encoder = new SchemaEncoder(SCHEMA);
  const data = encoder.encodeData([
    { name: 'parentUID', value: parent.attestationUID, type: 'bytes32' },
    { name: 'childUID', value: child.attestationUID, type: 'bytes32' },
    { name: 'parentActionHash', value: parent.actionHash, type: 'bytes32' },
    { name: 'childActionHash', value: child.actionHash, type: 'bytes32' },
    { name: 'parentSigner', value: parent.signer, type: 'address' },
    { name: 'childSigner', value: child.signer, type: 'address' },
    { name: 'relation', value: relation, type: 'string' },
    { name: 'timestamp', value: Math.floor(Date.now()/1000), type: 'uint64' },
    { name: 'payloadRef', value: '', type: 'string' }
  ]);

  const tx = await eas.attest({
    schema: process.env.LINK_SCHEMA_UID!,
    data: { recipient: child.signer, expirationTime: 0, revocable: true, refUID: ethers.ZeroHash, data, value: 0n }
  });

  const uid = await tx.wait();
  console.log(JSON.stringify({ linkUID: uid, txHash: tx.hash }, null, 2));
}

main();
