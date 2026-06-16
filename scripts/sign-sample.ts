// scripts/sign-sample.ts
import fs from 'fs'
import path from 'path'
import { generateReceipt, AgentReceipt } from '../receipts/generator'

const RECEIPT_PATH = path.join(process.cwd(), '_truth/receipts/sample_agent1_pdf_ingest.json')

async function main() {
  const privateKey = process.env.AGENT_PRIVATE_KEY
  if (!privateKey) throw new Error('AGENT_PRIVATE_KEY missing')

  const raw = fs.readFileSync(RECEIPT_PATH, 'utf8')
  const current = JSON.parse(raw) as AgentReceipt

  const signed = await generateReceipt(current.action, privateKey)

  fs.writeFileSync(RECEIPT_PATH, JSON.stringify(signed, null, 2) + '\n')

  console.log(JSON.stringify({
    state: 'SAMPLE_SIGNED',
    actionHash: signed.actionHash,
    signer: signed.signer
  }, null, 2))
}

main().catch(err => {
  console.error(err)
  process.exit(1)
})
