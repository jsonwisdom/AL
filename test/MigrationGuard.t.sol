// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "../contracts/MigrationGuard.sol";

contract MockOracle is IMigrationRelayerReputationOracle {
    bytes32 public lastSourceWitnessHash;
    bytes32 public lastRejectCode;
    address public lastRelayer;

    function ingestFailClosed(bytes32 sourceWitnessHash, bytes32 rejectCode, address relayer)
        external
        override
        returns (bytes32 penaltyId)
    {
        lastSourceWitnessHash = sourceWitnessHash;
        lastRejectCode = rejectCode;
        lastRelayer = relayer;
        return keccak256(abi.encodePacked(sourceWitnessHash, rejectCode, relayer));
    }
}

contract MigrationGuardTest is Test {
    bytes32 constant ROOT = keccak256("JAYS_INSTRUMENT_ROOT");

    MockOracle oracle;
    MigrationGuard guard;

    function setUp() public {
        oracle = new MockOracle();
        guard = new MigrationGuard(ROOT, address(oracle));
    }

    function _buildReceipt(
        bytes32 sourceHash,
        uint8 sourceConfidence,
        uint8 targetConfidence,
        bytes32 degradationHash,
        string memory degradationURI,
        uint8 restraintFlags,
        bool executionRequested
    ) internal view returns (MigrationGuard.MigrationReceipt memory r) {
        bytes32 integrity = keccak256(abi.encodePacked(
            sourceHash,
            sourceConfidence,
            targetConfidence,
            degradationHash,
            restraintFlags
        ));

        r = MigrationGuard.MigrationReceipt({
            constitutionalRootUID: ROOT,
            sourceWitnessHash: sourceHash,
            sourceConfidenceLevel: sourceConfidence,
            targetConfidenceLevel: targetConfidence,
            degradationLogHash: degradationHash,
            degradationLogURI: degradationURI,
            restraintFlags: restraintFlags,
            receiptIntegrity: integrity,
            executionRequested: executionRequested,
            relayer: address(0xBEEF)
        });
    }

    function test_HonestTransport() public {
        MigrationGuard.MigrationReceipt memory r = _buildReceipt(
            keccak256("honest"),
            1,
            1,
            guard.ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG(),
            "",
            0x01,
            false
        );

        guard.submitMigration(r);
        assertTrue(guard.passiveWitnessRecords(r.sourceWitnessHash));
        assertFalse(guard.failureLog(r.sourceWitnessHash));
    }

    function test_PromotionAttempt() public {
        MigrationGuard.MigrationReceipt memory r = _buildReceipt(
            keccak256("promotion"),
            1,
            2,
            guard.ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG(),
            "",
            0x01,
            false
        );

        guard.submitMigration(r);

        assertFalse(guard.passiveWitnessRecords(r.sourceWitnessHash));
        assertTrue(guard.failureLog(r.sourceWitnessHash));
        assertEq(oracle.lastRejectCode(), guard.REJECT_TARGET_CONFIDENCE_PROMOTION());
    }

    function test_FlagStripIntegrityMismatch() public {
        MigrationGuard.MigrationReceipt memory r = _buildReceipt(
            keccak256("flagstrip"),
            1,
            1,
            guard.ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG(),
            "",
            0x01,
            false
        );

        r.restraintFlags = 0x00;

        guard.submitMigration(r);

        assertTrue(guard.failureLog(r.sourceWitnessHash));
        assertEq(oracle.lastRejectCode(), guard.REJECT_RECEIPT_INTEGRITY_MISMATCH());
    }

    function test_IntegrityMismatch() public {
        MigrationGuard.MigrationReceipt memory r = _buildReceipt(
            keccak256("integrity"),
            1,
            1,
            guard.ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG(),
            "",
            0x01,
            false
        );

        r.receiptIntegrity = keccak256("tampered");

        guard.submitMigration(r);

        assertTrue(guard.failureLog(r.sourceWitnessHash));
        assertEq(oracle.lastRejectCode(), guard.REJECT_RECEIPT_INTEGRITY_MISMATCH());
    }

    function test_MissingDegradationLog() public {
        MigrationGuard.MigrationReceipt memory r = _buildReceipt(
            keccak256("missingdeg"),
            1,
            1,
            bytes32(0),
            "",
            0x01,
            false
        );

        guard.submitMigration(r);

        assertTrue(guard.failureLog(r.sourceWitnessHash));
        assertEq(oracle.lastRejectCode(), guard.REJECT_MISSING_DEGRADATION_LOG());
    }

    function test_ConstitutionalRootMismatch() public {
        MigrationGuard.MigrationReceipt memory r = _buildReceipt(
            keccak256("rootmismatch"),
            1,
            1,
            guard.ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG(),
            "",
            0x01,
            false
        );

        r.constitutionalRootUID = keccak256("fake_root");

        guard.submitMigration(r);

        assertTrue(guard.failureLog(r.sourceWitnessHash));
        assertEq(oracle.lastRejectCode(), guard.REJECT_CONSTITUTIONAL_ROOT_MISMATCH());
    }

    function test_UnmappedExecutionBlocked() public {
        MigrationGuard.MigrationReceipt memory r = _buildReceipt(
            keccak256("unmapped"),
            guard.EXTERNAL_OBSERVER_PENDING(),
            guard.EXTERNAL_OBSERVER_PENDING(),
            guard.ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG(),
            "",
            0x01,
            true
        );

        guard.submitMigration(r);

        assertTrue(guard.failureLog(r.sourceWitnessHash));
        assertEq(oracle.lastRejectCode(), guard.REJECT_SEMANTICALLY_UNMAPPED_EXECUTION_BLOCKED());
    }

    function test_EmptyDegradationLogAllowed() public {
        MigrationGuard.MigrationReceipt memory r = _buildReceipt(
            keccak256("emptyallowed"),
            1,
            1,
            guard.ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG(),
            "",
            0x05,
            false
        );

        guard.submitMigration(r);

        assertTrue(guard.passiveWitnessRecords(r.sourceWitnessHash));
        assertFalse(guard.failureLog(r.sourceWitnessHash));
    }
}
