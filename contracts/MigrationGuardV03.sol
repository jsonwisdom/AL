// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IEAS {
    struct Attestation {
        bytes32 uid;
        bytes32 schema;
        uint64 time;
        uint64 expirationTime;
        uint64 revocationTime;
        bytes32 refUID;
        address recipient;
        address attester;
        bool revocable;
        bytes data;
    }
    function getAttestation(bytes32 uid) external view returns (Attestation memory);
}

interface ISchemaRegistry {
    struct SchemaRecord {
        bytes32 uid;
        address resolver;
        bool revocable;
        string schema;
    }
    function getSchema(bytes32 uid) external view returns (SchemaRecord memory);
}

contract MigrationGuardV03 {
    error InvalidSchema(bytes32 actual, bytes32 expected);
    error RevocableSchema(bytes32 schemaUID);
    error ResolverForbidden(bytes32 schemaUID, address resolver);
    error RevokedAttestation(bytes32 attestationUID);
    error RevocableAttestation(bytes32 attestationUID);
    error EmptyAttestation(bytes32 attestationUID);

    IEAS public immutable eas;
    ISchemaRegistry public immutable schemaRegistry;
    bytes32 public immutable CONSTITUTIONAL_ROOT_SCHEMA_UID;
    bytes32 public immutable MIGRATION_RECEIPT_SCHEMA_UID;
    bytes32 public immutable AGENT_OUTPUT_RECEIPT_SCHEMA_UID;

    struct ConstitutionalRoot {
        bytes32 instrumentHash;
        bytes32 articlesHash;
        uint64 effectiveFrom;
        string version;
    }

    struct MigrationReceipt {
        bytes32 constitutionalRootUID;
        bytes32 sourceHash;
        bytes32 targetHash;
        bytes32 canonicalHash;
        bytes32 translationLossHash;
        uint8 sourceContext;
        uint8 targetContext;
        uint8 sourceConfidence;
        uint8 targetConfidence;
        uint64 timestamp;
    }

    struct AgentOutputReceipt {
        bytes32 constitutionalRootUID;
        bytes32 canonicalHash;
        bytes32 promptHash;
        bytes32 outputHash;
        bytes32 degradationHash;
        uint8 confidenceLevel;
        uint8 rejectionCode;
        bool isValid;
        uint64 timestamp;
    }

    constructor(
        address eas_,
        address schemaRegistry_,
        bytes32 constitutionalRootSchemaUID_,
        bytes32 migrationReceiptSchemaUID_,
        bytes32 agentOutputReceiptSchemaUID_
    ) {
        eas = IEAS(eas_);
        schemaRegistry = ISchemaRegistry(schemaRegistry_);
        CONSTITUTIONAL_ROOT_SCHEMA_UID = constitutionalRootSchemaUID_;
        MIGRATION_RECEIPT_SCHEMA_UID = migrationReceiptSchemaUID_;
        AGENT_OUTPUT_RECEIPT_SCHEMA_UID = agentOutputReceiptSchemaUID_;
    }

    function verifyConstitutionalRoot(bytes32 attestationUID)
        external
        view
        returns (ConstitutionalRoot memory)
    {
        IEAS.Attestation memory attestation =
            _validatedAttestation(attestationUID, CONSTITUTIONAL_ROOT_SCHEMA_UID);
        return abi.decode(attestation.data, (ConstitutionalRoot));
    }

    function verifyMigrationReceipt(bytes32 attestationUID)
        public
        view
        returns (MigrationReceipt memory)
    {
        IEAS.Attestation memory attestation =
            _validatedAttestation(attestationUID, MIGRATION_RECEIPT_SCHEMA_UID);
        return abi.decode(attestation.data, (MigrationReceipt));
    }

    function verifyAgentOutputReceipt(bytes32 attestationUID)
        external
        view
        returns (AgentOutputReceipt memory)
    {
        IEAS.Attestation memory attestation =
            _validatedAttestation(attestationUID, AGENT_OUTPUT_RECEIPT_SCHEMA_UID);
        return abi.decode(attestation.data, (AgentOutputReceipt));
    }

    function _validatedAttestation(bytes32 attestationUID, bytes32 expectedSchemaUID)
        internal
        view
        returns (IEAS.Attestation memory attestation)
    {
        attestation = eas.getAttestation(attestationUID);
        if (attestation.uid == bytes32(0)) {
            revert EmptyAttestation(attestationUID);
        }
        if (attestation.schema != expectedSchemaUID) {
            revert InvalidSchema(attestation.schema, expectedSchemaUID);
        }
        if (attestation.revocationTime != 0) {
            revert RevokedAttestation(attestationUID);
        }
        if (attestation.revocable) {
            revert RevocableAttestation(attestationUID);
        }
        _validateSchema(expectedSchemaUID);
    }

    function _validateSchema(bytes32 schemaUID) internal view {
        ISchemaRegistry.SchemaRecord memory record =
            schemaRegistry.getSchema(schemaUID);
        if (record.revocable) {
            revert RevocableSchema(schemaUID);
        }
        if (record.resolver != address(0)) {
            revert ResolverForbidden(schemaUID, record.resolver);
        }
    }
}
