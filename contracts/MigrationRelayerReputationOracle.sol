// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title MigrationRelayerReputationOracle
/// @notice Receipt-bound relayer reputation oracle following REPUTATION_CORRECTION_DOCTRINE_V1.
/// @dev No permanent identity score. No hidden ban. Violations are role/context scoped.
contract MigrationRelayerReputationOracle {
    bytes32 public constant REJECT_TARGET_CONFIDENCE_PROMOTION =
        keccak256("TARGET_CONFIDENCE_PROMOTION");
    bytes32 public constant REJECT_RESTRAINT_FLAG_STRIPPED =
        keccak256("RESTRAINT_FLAG_STRIPPED");
    bytes32 public constant REJECT_RECEIPT_INTEGRITY_MISMATCH =
        keccak256("RECEIPT_INTEGRITY_MISMATCH");
    bytes32 public constant REJECT_CONCEALMENT_ESCALATION =
        keccak256("CONCEALMENT_ESCALATION");

    address public immutable auditCommittee;

    struct RelayerRecord {
        uint256 promotionAttempts;
        uint256 integrityViolations;
        uint256 concealedViolations;
        uint256 lastViolationBlock;
        bool isActive;
        bool repairVerified;
        bytes32 repairProofHash;
    }

    mapping(address => RelayerRecord) public relayers;

    event SlashableFault(
        address indexed relayer,
        bytes32 indexed rejectCode,
        bytes32 indexed sourceWitnessHash,
        uint256 promotionCount,
        uint256 integrityCount
    );

    event RepairSubmitted(address indexed relayer, bytes32 indexed proofHash);
    event RepairVerified(address indexed relayer, bytes32 indexed proofHash);
    event RelayerSuspended(address indexed relayer, bytes32 indexed reason);
    event ConcealmentReported(address indexed relayer, uint256 concealedCount);

    error Unauthorized();
    error ZeroAuditCommittee();
    error RepairAlreadyVerified();
    error ProofMismatch();

    modifier onlyAuditCommittee() {
        if (msg.sender != auditCommittee) revert Unauthorized();
        _;
    }

    constructor(address auditCommittee_) {
        if (auditCommittee_ == address(0)) revert ZeroAuditCommittee();
        auditCommittee = auditCommittee_;
    }

    /// @notice Neutral start: unknown relayers are treated as active until receipt evidence says otherwise.
    function _ensureInitialized(RelayerRecord storage r) internal {
        if (!r.isActive && r.lastViolationBlock == 0) {
            r.isActive = true;
        }
    }

    /// @notice Ingests fail-closed evidence from the migration guard.
    /// @dev Promotion remains immediate suspension. Integrity faults allow verified repair path.
    function ingestFailClosed(
        bytes32 sourceWitnessHash,
        bytes32 rejectCode,
        address relayer
    ) external {
        RelayerRecord storage r = relayers[relayer];
        _ensureInitialized(r);

        r.lastViolationBlock = block.number;

        if (rejectCode == REJECT_TARGET_CONFIDENCE_PROMOTION) {
            r.promotionAttempts++;
            emit SlashableFault(
                relayer,
                rejectCode,
                sourceWitnessHash,
                r.promotionAttempts,
                r.integrityViolations
            );

            r.isActive = false;
            emit RelayerSuspended(relayer, rejectCode);
            return;
        }

        if (
            rejectCode == REJECT_RESTRAINT_FLAG_STRIPPED ||
            rejectCode == REJECT_RECEIPT_INTEGRITY_MISMATCH
        ) {
            r.integrityViolations++;
            emit SlashableFault(
                relayer,
                rejectCode,
                sourceWitnessHash,
                r.promotionAttempts,
                r.integrityViolations
            );

            if (r.integrityViolations >= 2 && !r.repairVerified) {
                r.isActive = false;
                emit RelayerSuspended(relayer, rejectCode);
            }
        }
    }

    /// @notice Relayer submits off-chain remediation evidence hash.
    function submitRepair(bytes32 proofHash) external {
        RelayerRecord storage r = relayers[msg.sender];
        _ensureInitialized(r);

        if (r.repairVerified) revert RepairAlreadyVerified();

        r.repairProofHash = proofHash;
        emit RepairSubmitted(msg.sender, proofHash);
    }

    /// @notice Audit committee verifies repair evidence.
    function verifyRepair(address relayer, bytes32 proofHash) external onlyAuditCommittee {
        RelayerRecord storage r = relayers[relayer];
        _ensureInitialized(r);

        if (r.repairProofHash != proofHash) revert ProofMismatch();
        if (r.repairVerified) revert RepairAlreadyVerified();

        r.repairVerified = true;

        if (!r.isActive && r.concealedViolations == 0) {
            r.isActive = true;
        }

        emit RepairVerified(relayer, proofHash);
    }

    /// @notice Concealment is escalation: hiding failures is worse than correction.
    function reportConcealment(address relayer, uint256 concealedCount) external onlyAuditCommittee {
        RelayerRecord storage r = relayers[relayer];
        _ensureInitialized(r);

        r.concealedViolations += concealedCount;
        emit ConcealmentReported(relayer, concealedCount);

        if (r.concealedViolations >= 1) {
            r.isActive = false;
            emit RelayerSuspended(relayer, REJECT_CONCEALMENT_ESCALATION);
        }
    }

    function canRelay(address relayer) external view returns (bool) {
        RelayerRecord memory r = relayers[relayer];
        if (r.lastViolationBlock == 0 && !r.isActive) return true;
        return r.isActive;
    }
}
