// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IMigrationRelayerReputationOracle {
    function ingestFailClosed(bytes32 sourceWitnessHash, bytes32 rejectCode, address relayer) external returns (bytes32 penaltyId);
}

/// @title MigrationGuard
/// @notice Transport-only cross-chain migration guard. It preserves or explicitly degrades confidence; it never upgrades it.
contract MigrationGuard {
    bytes32 public constant REJECT_NONE = bytes32(0);
    bytes32 public constant REJECT_TARGET_CONFIDENCE_PROMOTION = keccak256("TARGET_CONFIDENCE_PROMOTION");
    bytes32 public constant REJECT_CONSTITUTIONAL_ROOT_MISMATCH = keccak256("CONSTITUTIONAL_ROOT_MISMATCH");
    bytes32 public constant REJECT_RECEIPT_INTEGRITY_MISMATCH = keccak256("RECEIPT_INTEGRITY_MISMATCH");
    bytes32 public constant REJECT_MISSING_DEGRADATION_LOG = keccak256("MISSING_DEGRADATION_LOG");
    bytes32 public constant REJECT_SEMANTICALLY_UNMAPPED_EXECUTION_BLOCKED = keccak256("SEMANTICALLY_UNMAPPED_EXECUTION_BLOCKED");

    uint8 public constant EXTERNAL_OBSERVER_PENDING = 1;
    bytes32 public constant ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;

    bytes32 public immutable constitutionalRootUID;
    address public immutable oracle;

    mapping(bytes32 => bool) public passiveWitnessRecords;
    mapping(bytes32 => bool) public failureLog;

    struct MigrationReceipt {
        bytes32 constitutionalRootUID;
        bytes32 sourceWitnessHash;
        uint8 sourceConfidenceLevel;
        uint8 targetConfidenceLevel;
        bytes32 degradationLogHash;
        string degradationLogURI;
        uint8 restraintFlags;
        bytes32 receiptIntegrity;
        bool executionRequested;
        address relayer;
    }

    event MigrationReceiptWritten(bytes32 indexed sourceWitnessHash, uint8 sourceConfidence, uint8 targetConfidence, bytes32 receiptIntegrity);
    event MigrationFailClosed(bytes32 indexed sourceWitnessHash, bytes32 rejectCode, address relayer, bytes32 computedIntegrity, bytes32 providedIntegrity);

    error ZeroConstitutionalRoot();
    error ZeroOracle();

    constructor(bytes32 constitutionalRootUID_, address oracle_) {
        if (constitutionalRootUID_ == bytes32(0)) revert ZeroConstitutionalRoot();
        if (oracle_ == address(0)) revert ZeroOracle();
        constitutionalRootUID = constitutionalRootUID_;
        oracle = oracle_;
    }

    function computeReceiptIntegrity(MigrationReceipt calldata receipt) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(
            receipt.sourceWitnessHash,
            receipt.sourceConfidenceLevel,
            receipt.targetConfidenceLevel,
            receipt.degradationLogHash,
            receipt.restraintFlags
        ));
    }

    function preStorageWriteGuard(MigrationReceipt calldata receipt) public view returns (bytes32 rejectCode, bytes32 computedIntegrity) {
        computedIntegrity = computeReceiptIntegrity(receipt);

        if (receipt.constitutionalRootUID != constitutionalRootUID) {
            return (REJECT_CONSTITUTIONAL_ROOT_MISMATCH, computedIntegrity);
        }

        if (receipt.targetConfidenceLevel > receipt.sourceConfidenceLevel) {
            return (REJECT_TARGET_CONFIDENCE_PROMOTION, computedIntegrity);
        }

        if (computedIntegrity != receipt.receiptIntegrity) {
            return (REJECT_RECEIPT_INTEGRITY_MISMATCH, computedIntegrity);
        }

        if (receipt.degradationLogHash == bytes32(0)) {
            return (REJECT_MISSING_DEGRADATION_LOG, computedIntegrity);
        }

        if (receipt.degradationLogHash == ZERO_HASH_FOR_EMPTY_DEGRADATION_LOG && bytes(receipt.degradationLogURI).length != 0) {
            return (REJECT_MISSING_DEGRADATION_LOG, computedIntegrity);
        }

        if (receipt.executionRequested && receipt.sourceConfidenceLevel == EXTERNAL_OBSERVER_PENDING) {
            return (REJECT_SEMANTICALLY_UNMAPPED_EXECUTION_BLOCKED, computedIntegrity);
        }

        return (REJECT_NONE, computedIntegrity);
    }

    function submitMigration(MigrationReceipt calldata receipt) external {
        (bytes32 rejectCode, bytes32 computedIntegrity) = preStorageWriteGuard(receipt);

        if (rejectCode == REJECT_NONE) {
            passiveWitnessRecords[receipt.sourceWitnessHash] = true;
            emit MigrationReceiptWritten(receipt.sourceWitnessHash, receipt.sourceConfidenceLevel, receipt.targetConfidenceLevel, receipt.receiptIntegrity);
            return;
        }

        failureLog[receipt.sourceWitnessHash] = true;
        (bool ok,) = oracle.call(abi.encodeWithSelector(
            IMigrationRelayerReputationOracle.ingestFailClosed.selector,
            receipt.sourceWitnessHash,
            rejectCode,
            receipt.relayer
        ));
        ok;

        emit MigrationFailClosed(receipt.sourceWitnessHash, rejectCode, receipt.relayer, computedIntegrity, receipt.receiptIntegrity);
    }
}
