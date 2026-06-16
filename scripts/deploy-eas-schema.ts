import { EAS, SchemaRegistry } from '@ethereum-attestation-service/eas-sdk';
import { ethers } from 'ethers';

const SCHEMA = 'bytes32 actionHash,address signer,bytes signature,uint64 timestamp,string payloadRef';

async function main() {
  const provider = new ethers.JsonRpcProvider(process.env.BASE_SEPOLIA_RPC);
  const signer = new ethers.Wallet(process.env.PRIVATE_KEY!, provider);

  const registry = new SchemaRegistry('0x4200000000000000000000000000000000000020');
  registry.connect(signer);

  const tx = await registry.register({ schema: SCHEMA, resolverAddress: ethers.ZeroAddress, revocable: true });
  const schemaUID = await tx.wait();

  console.log(JSON.stringify({ schemaUID }, null, 2));
}

main();
