import { SchemaRegistry } from '@ethereum-attestation-service/eas-sdk';
import { ethers } from 'ethers';

const SCHEMA = 'bytes32 parentUID,bytes32 childUID,bytes32 parentActionHash,bytes32 childActionHash,address parentSigner,address childSigner,string relation,uint64 timestamp,string payloadRef';

async function main() {
  const provider = new ethers.JsonRpcProvider(process.env.BASE_SEPOLIA_RPC);
  const signer = new ethers.Wallet(process.env.PRIVATE_KEY!, provider);

  const registry = new SchemaRegistry('0x4200000000000000000000000000000000000020');
  registry.connect(signer);

  const tx = await registry.register({ schema: SCHEMA, resolverAddress: ethers.ZeroAddress, revocable: true });
  const uid = await tx.wait();

  console.log(JSON.stringify({ linkSchemaUID: uid }, null, 2));
}

main();
