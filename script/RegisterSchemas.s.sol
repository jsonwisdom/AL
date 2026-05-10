// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";

interface ISchemaRegistry {
    function register(string calldata schema, address resolver, bool revocable) external returns (bytes32);
}

contract RegisterSchemas is Script {
    address constant SCHEMA_REGISTRY = 0x4200000000000000000000000000000000000020;
    address constant NO_RESOLVER = address(0);
    bool constant REVOCABLE_FALSE = false;

    string constant CONSTITUTIONAL_ROOT =
        "bytes32 instrumentHash,bytes32 articlesHash,uint64 effectiveFrom,string version";

    string constant MIGRATION_RECEIPT =
        "bytes32 constitutionalRootUID,bytes32 sourceHash,bytes32 targetHash,bytes32 canonicalHash,bytes32 translationLossHash,uint8 sourceContext,uint8 targetContext,uint8 sourceConfidence,uint8 targetConfidence,uint64 timestamp";

    string constant AGENT_OUTPUT_RECEIPT =
        "bytes32 constitutionalRootUID,bytes32 canonicalHash,bytes32 promptHash,bytes32 outputHash,bytes32 degradationHash,uint8 confidenceLevel,uint8 rejectionCode,bool isValid,uint64 timestamp";

    function run() external {
        uint256 deployerKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerKey);

        ISchemaRegistry registry = ISchemaRegistry(SCHEMA_REGISTRY);

        bytes32 constitutionalRootUID = registry.register(CONSTITUTIONAL_ROOT, NO_RESOLVER, REVOCABLE_FALSE);
        bytes32 migrationReceiptUID = registry.register(MIGRATION_RECEIPT, NO_RESOLVER, REVOCABLE_FALSE);
        bytes32 agentOutputReceiptUID = registry.register(AGENT_OUTPUT_RECEIPT, NO_RESOLVER, REVOCABLE_FALSE);

        vm.stopBroadcast();

        console2.log("CONSTITUTIONAL_ROOT_SCHEMA_UID:");
        console2.logBytes32(constitutionalRootUID);
        console2.log("MIGRATION_RECEIPT_SCHEMA_UID:");
        console2.logBytes32(migrationReceiptUID);
        console2.log("AGENT_OUTPUT_RECEIPT_SCHEMA_UID:");
        console2.logBytes32(agentOutputReceiptUID);
    }
}
