# Base Mesh Targets

Goal: expand Nitro Observer pattern into a multi-contract mesh.

Rules:
- No guessed addresses.
- Official deployment source first.
- Missing getter = YELLOW, not GREEN.
- Real mutation = RED.
- Verified clean live read = GREEN.

Priority targets:
1. SystemConfig proxy
2. OptimismPortal
3. L1StandardBridge
4. L1CrossDomainMessenger
5. L2StandardBridge
6. SequencerFeeVault
7. L2CrossDomainMessenger
8. ProxyAdmin / governance / timelock surfaces

Known L2 predeploys:
- L2StandardBridge = 0x4200000000000000000000000000000000000010
- SequencerFeeVault = 0x4200000000000000000000000000000000000011
- L2CrossDomainMessenger = 0x4200000000000000000000000000000000000007
