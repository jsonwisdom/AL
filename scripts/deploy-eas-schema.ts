import { ethers } from 'ethers';
import fs from 'fs';

const EAS_SCHEMA_REGISTRY = '0x4200000000000000000000000000000000000020';

async function main() {
  const provider = new ethers.JsonRpcProvider(process.env.BASE_SEPOLIA_RPC);
  const wallet = new ethers.Wallet(process.env.PRIVATE_KEY!, provider);

  const abi = [
    'function register(string schema, address resolver, bool revocable) public returns (bytes32)'
  ];

  const registry = new ethers.Contract(EAS_SCHEMA_REGISTRY, abi, wallet);

  const schema = 'bytes32 actionHash,address signer,bytes signature,uint64 timestamp,string payloadRef';

  const tx = await registry.register(schema, ethers.ZeroAddress, true);
  const receipt = await tx.wait();

  console.log('Schema registered tx:', receipt.hash);
}

main();