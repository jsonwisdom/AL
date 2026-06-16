// receipts/generator.ts
// Minimal verifiable receipt generator for AL v1
// Stack: JCS (RFC8785) + SHA256 + secp256k1 signature
// Signature mode: ETH_PERSONAL_SIGN over actionHash string.
// Onchain verifier note: replicate EIP-191 message semantics, not raw digest recovery.
// No vibes. Deterministic only.

import { createHash } from 'crypto'
import canonicalize from 'canonicalize'
import { Wallet, verifyMessage } from 'ethers'

export interface AgentAction {
  version: '1.0.0'
  agent: string
  taskType: 'task-ingest-pdf'
  taskId: string
  timestamp: string
  input: {
    uri: string
    sha256: string
    bytes: number
  }
  output: {
    sha256: string
    bytes: number
    metadata?: Record<string, any>
  }
  policy: {
    allowNetwork: boolean
    maxBytes: number
  }
  previousReceipt?: string
}

export interface AgentReceipt {
  action: AgentAction
  jcs: string
  actionHash: string
  signature: string
  signer: string
}

export function sha256Hex(data: Buffer | string): string {
  return '0x' + createHash('sha256').update(data).digest('hex')
}

export function canonicalizeAction(action: AgentAction): string {
  const jcs = canonicalize(action)
  if (!jcs) throw new Error('JCS failed')
  return jcs
}

export async function generateReceipt(
  action: AgentAction,
  privateKey: string
): Promise<AgentReceipt> {
  if (!privateKey) throw new Error('AGENT_PRIVATE_KEY missing')
  const jcs = canonicalizeAction(action)
  const actionHash = sha256Hex(jcs)
  const wallet = new Wallet(privateKey)
  const signature = await wallet.signMessage(actionHash)
  return {
    action,
    jcs,
    actionHash,
    signature,
    signer: await wallet.getAddress()
  }
}

export function verifyReceiptLocal(receipt: AgentReceipt): boolean {
  if (!receipt.signature?.startsWith('0x')) return false
  if (!receipt.signer?.startsWith('0x')) return false
  const recomputedJcs = canonicalizeAction(receipt.action)
  if (recomputedJcs !== receipt.jcs) return false
  const recomputedHash = sha256Hex(recomputedJcs)
  if (recomputedHash !== receipt.actionHash) return false
  const recovered = verifyMessage(receipt.actionHash, receipt.signature)
  return recovered.toLowerCase() === receipt.signer.toLowerCase()
}
