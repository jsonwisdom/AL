// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import "forge-std/Script.sol";
import { MigrationGuardResolver } from "../contracts/MigrationGuardResolver.sol";
import { IEAS } from "eas-contracts/IEAS.sol";

contract DeployMigrationGuardResolver is Script {
    address internal constant BASE_SEPOLIA_EAS = 0x4200000000000000000000000000000000000021;

    address internal constant ALLOWED_ATTESTER =
        0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8;

    bytes32 internal constant EXPECTED_DEPLOY_HASH =
        0x0e87c73f857682709447da6958018cdc6752b7468024336c7fe0316c09df83e4;

    function run() external {
        vm.startBroadcast();

        IEAS eas = IEAS(BASE_SEPOLIA_EAS);

        MigrationGuardResolver resolver = new MigrationGuardResolver(
            eas,
            ALLOWED_ATTESTER,
            EXPECTED_DEPLOY_HASH
        );

        vm.stopBroadcast();

        console2.log("MigrationGuardResolver deployed at:", address(resolver));
        console2.log("Allowed attester:", ALLOWED_ATTESTER);
        console2.logBytes32(EXPECTED_DEPLOY_HASH);
    }
}
