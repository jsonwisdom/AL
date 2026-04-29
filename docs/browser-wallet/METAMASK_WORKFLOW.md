# MetaMask Workflow for ALMS

Purpose:
No private key enters terminal.

Canonical browser flow:
1. Connect wallet
2. Switch to Base
3. Send transaction
4. Capture tx hash
5. Verify receipt
6. Anchor result to ENS

Required RPC methods:
- eth_requestAccounts
- wallet_switchEthereumChain
- eth_sendTransaction

Human rule:
Jason approves every live transaction in wallet UI.

Terminal role:
Prepare calldata and verify receipts only.
