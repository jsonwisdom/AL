// scripts/sign-sample.ts
// One-shot local gate signer for AL v1.
// Reads _truth/receipts/sample_agent1_pdf_ingest.json, signs actionHash with AGENT_PRIVATE_KEY,
// writes signature + signer back into the receipt.
// No Base. No EAS. No payment.

import fs from 'fs'
import path from 'path'
import { generateReceipt, AgentReceipt } from '../receipts/generator'

const RECEIPT_PATH = path.join(process.cwd(), '_truth/receipts/sample_agent1_pdf_ingest.json')

async function main() {
  const privateKey = process.env.AGENT_PRIVATE_KEY
  if (!privateKey) throw new Error('AGENT_PRIVATE_KEY missing')

  const raw = fs.readFileSync(RECEIPT_PATH, 'utf8')
  const current = JSON.parse(raw) as AgentReceipt

  if (!current.action) throw new Error('receipt.action missing')

  const signed = await generateReceipt(current.action, privateKey)

  fs.writeFileSync(RECEIPT_PATH, JSON.stringify(signed, null, 2) + '\n')

  console.log(JSON.stringify({
    state: 'SAMPLE_SIGNED',
    path: RECEIPT_PATH,
    actionHash: signed.actionHash,
    signer: signed.signer,
    signaturePrefix: signed.signature.slice(0, 10)
  }, null, 2))
}

main().catch((err) => {
  console.error(JSON.stringify({
    state: 'SAMPLE_SIGN_FAILED',
    error: err instanceof Error ? err.message : String(err)
  }, null, 2))
  process.exit(1)
})
