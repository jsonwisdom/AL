// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import { SchemaResolver } from "@ethereum-attestation-service/eas-contracts/contracts/resolver/SchemaResolver.sol";
import { IEAS } from "@ethereum-attestation-service/eas-contracts/contracts/IEAS.sol";
import { Attestation } from "@ethereum-attestation-service/eas-contracts/contracts/Common.sol";

contract MigrationGuardResolver is SchemaResolver {
    address public immutable ALLOWED_ATTESTER;
    bytes32 public immutable EXPECTED_DEPLOY_HASH;

    error UnauthorizedAttester();
    error HashMismatch();

    constructor(
        IEAS eas,
        address allowedAttester,
        bytes32 expectedDeployHash
    ) SchemaResolver(eas) {
        ALLOWED_ATTESTER = allowedAttester;
        EXPECTED_DEPLOY_HASH = expectedDeployHash;
    }

    function onAttest(
        Attestation calldata attestation,
        uint256 /* value */
    ) internal view override returns (bool) {
        if (attestation.attester != ALLOWED_ATTESTER) {
            revert UnauthorizedAttester();
        }

        // Decode schema: bytes32 deployHash, bytes32 verifyHash, bytes32 mirrorHash, string metadata, uint256 timestamp
        (bytes32 deployHash, bytes32 verifyHash, bytes32 mirrorHash, , ) =
            abi.decode(attestation.data, (bytes32, bytes32, bytes32, string, uint256));

        if (deployHash != EXPECTED_DEPLOY_HASH) {
            revert HashMismatch();
        }

        // Future-proof: additional hash checks can be enabled here.
        verifyHash;
        mirrorHash;
        return true;
    }

    function onRevoke(
        Attestation calldata /* attestation */,
        uint256 /* value */
    ) internal pure override returns (bool) {
        return true;
    }
}
