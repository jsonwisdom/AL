// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import { IEAS, AttestationRequest, AttestationRequestData } from "eas-contracts/IEAS.sol";

/// @title GenesisAttestation
/// @notice Anchors the Constitutional Root to Base Sepolia
contract GenesisAttestation is Script {
    address constant EAS = 0x4200000000000000000000000000000000000021;

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        bytes32 schemaUID = vm.envBytes32("CONSTITUTIONAL_ROOT_SCHEMA_UID");
        bytes32 instrumentHash = vm.envBytes32("INSTRUMENT_HASH");
        bytes32 articlesHash = vm.envBytes32("ARTICLES_HASH");

        vm.startBroadcast(deployerPrivateKey);

        IEAS eas = IEAS(EAS);

        bytes memory data = abi.encode(
            instrumentHash,
            articlesHash,
            uint64(block.timestamp),
            "v0.1",
            vm.addr(deployerPrivateKey)
        );

        AttestationRequestData memory requestData = AttestationRequestData({
            recipient: address(0),
            expirationTime: 0,
            revocable: false,
            refUID: bytes32(0),
            data: data,
            value: 0
        });

        AttestationRequest memory request = AttestationRequest({
            schema: schemaUID,
            data: requestData
        });

        bytes32 attestationUID = eas.attest(request);

        vm.stopBroadcast();

        console.log("CONSTITUTIONAL_ROOT_UID:");
        console.logBytes32(attestationUID);
        console.log("Instrument Hash:");
        console.logBytes32(instrumentHash);
        console.log("Articles Hash:");
        console.logBytes32(articlesHash);
    }
}
