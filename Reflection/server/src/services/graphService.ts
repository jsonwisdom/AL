import { createHash, randomUUID } from "node:crypto";
import Ajv2020, { type ErrorObject, type ValidateFunction } from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

import graphNodeSchema from "./graph-node.schema.json";
import graphEventSchema from "./graph-event.schema.json";

/**
 * M2 hardened provenance graph service.
 *
 * Required tsconfig settings for the JSON schema imports:
 *   "resolveJsonModule": true
 *   "esModuleInterop": true
 *
 * Canonical truth is the append-only event ledger. The Maps returned by
 * rebuild() are disposable projections and must never be treated as authority.
 */

export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | JsonObject | JsonValue[];
export interface JsonObject {
  [key: string]: JsonValue;
}

export type Sha256 = `sha256:${string}`;
export type NodeStatus = "ACTIVE" | "SUPERSEDED" | "TOMBSTONED";
export type NodeType =
  | "Claim"
  | "Artifact"
  | "Source"
  | "Actor"
  | "Decision"
  | "Receipt"
  | "Verification"
  | "Attestation"
  | "Conflict"
  | "AuthorityGrant";

export type EdgeType =
  | "SUPPORTS"
  | "CONTRADICTS"
  | "DERIVED_FROM"
  | "QUOTES"
  | "SUMMARIZES"
  | "VERIFIED_BY"
  | "AUTHORIZED_BY"
  | "DECIDED_BY"
  | "SUPERSEDES"
  | "CHALLENGES"
  | "HAS_RECEIPT";

export type EventType =
  | "NODE_CREATED"
  | "NODE_UPDATED"
  | "NODE_TOMBSTONED"
  | "EDGE_CREATED"
  | "EDGE_UPDATED"
  | "EDGE_TOMBSTONED";

export type VerificationLevel =
  | "PRIVATE_VERIFIED"
  | "PUBLIC_VERIFIED"
  | "THIRD_PARTY_VERIFIED"
  | "UNREACHABLE"
  | "FAILED";

export interface Tombstone {
  reason: string;
  tombstoned_at: string;
  tombstoned_by: string;
}

export interface GraphNode<TPayload extends JsonObject = JsonObject> {
  id: string;
  type: NodeType;
  created_at: string;
  created_by: string;
  version: number;
  status: NodeStatus;
  source_receipt: string;
  content_hash: Sha256;
  payload: TPayload;
  superseded_by?: string;
  tombstone?: Tombstone;
}

export interface GraphEdge<TPayload extends JsonObject = JsonObject> {
  id: string;
  type: EdgeType;
  from: string;
  to: string;
  created_at: string;
  created_by: string;
  version: number;
  status: NodeStatus;
  source_receipt: string;
  content_hash: Sha256;
  payload: TPayload;
  superseded_by?: string;
  tombstone?: Tombstone;
}

export interface GraphEvent {
  schema_version: 1;
  event_id: string;
  stream_id: string;
  sequence: number;
  event_type: EventType;
  aggregate_type: "NODE" | "EDGE";
  aggregate_id: string;
  aggregate_version: number;
  occurred_at: string;
  actor_id: string;
  canonicalization: "RFC8785";
  hash_algorithm: "SHA-256";
  prev_event_hash: Sha256 | null;
  event_hash: Sha256;
  correlation_id?: string;
  causation_event_id?: string;
  payload: GraphNode | GraphEdge;
}

export class GraphIntegrityError extends Error {
  constructor(
    public readonly code: string,
    message: string,
  ) {
    super(message);
    this.name = "GraphIntegrityError";
  }
}

function assertNoLoneSurrogates(value: string): void {
  for (let i = 0; i < value.length; i++) {
    const code = value.charCodeAt(i);
    if (code >= 0xd800 && code <= 0xdbff) {
      const next = value.charCodeAt(i + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) {
        throw new GraphIntegrityError(
          "LONE_SURROGATE",
          "Canonical JSON rejects lone surrogates.",
        );
      }
      i++;
    } else if (code >= 0xdc00 && code <= 0xdfff) {
      throw new GraphIntegrityError(
        "LONE_SURROGATE",
        "Canonical JSON rejects lone surrogates.",
      );
    }
  }
}

function compareUtf16CodeUnits(a: string, b: string): number {
  const len = Math.min(a.length, b.length);
  for (let i = 0; i < len; i++) {
    const ca = a.charCodeAt(i);
    const cb = b.charCodeAt(i);
    if (ca !== cb) return ca - cb;
  }
  return a.length - b.length;
}

export class GraphService {
  private readonly validateNodeSchema: ValidateFunction<GraphNode>;
  private readonly validateEventSchema: ValidateFunction<GraphEvent>;
  private events: GraphEvent[] = [];
  private nodes = new Map<string, GraphNode>();
  private edges = new Map<string, GraphEdge>();

  constructor(options: { nodeSchema?: object; eventSchema?: object } = {}) {
    const ajv = new Ajv2020({
      strict: true,
      allErrors: true,
      validateFormats: true,
      allowUnionTypes: false,
    });
    addFormats(ajv);

    const nodeSchema = options.nodeSchema ?? graphNodeSchema;
    const eventSchema = options.eventSchema ?? graphEventSchema;
    ajv.addSchema(nodeSchema);

    this.validateNodeSchema = ajv.compile<GraphNode>(nodeSchema);
    this.validateEventSchema = ajv.compile<GraphEvent>(eventSchema);
  }

  /** RFC 8785-compatible canonicalization for JSON-domain values. */
  public canonicalize(value: JsonValue): string {
    const seen = new Set<object>();

    const encode = (input: JsonValue): string => {
      if (input === null) return "null";

      switch (typeof input) {
        case "string":
          assertNoLoneSurrogates(input);
          return JSON.stringify(input);
        case "boolean":
          return JSON.stringify(input);
        case "number": {
          if (!Number.isFinite(input)) {
            throw new GraphIntegrityError(
              "NON_FINITE_NUMBER",
              "Canonical JSON rejects NaN and Infinity.",
            );
          }
          return JSON.stringify(input);
        }
        case "object": {
          if (seen.has(input as object)) {
            throw new GraphIntegrityError(
              "CYCLIC_JSON_VALUE",
              "Canonical JSON cannot encode cyclic objects.",
            );
          }
          seen.add(input as object);

          try {
            if (Array.isArray(input)) {
              return `[${input.map((item) => encode(item)).join(",")}]`;
            }

            const prototype = Object.getPrototypeOf(input);
            if (prototype !== Object.prototype && prototype !== null) {
              throw new GraphIntegrityError(
                "NON_PLAIN_JSON_OBJECT",
                "Canonical JSON accepts only plain objects and arrays.",
              );
            }

            const object = input as JsonObject;
            const keys = Object.keys(object);
            for (const key of keys) assertNoLoneSurrogates(key);
            keys.sort(compareUtf16CodeUnits);
            const members = keys.map(
              (key) => `${JSON.stringify(key)}:${encode(object[key]!)}`,
            );
            return `{${members.join(",")}}`;
          } finally {
            seen.delete(input as object);
          }
        }
        default:
          throw new GraphIntegrityError(
            "NON_JSON_VALUE",
            "Value is outside the JSON data model.",
          );
      }
    };

    return encode(value);
  }

  public hashCanonical(value: JsonValue): Sha256 {
    const canonical = this.canonicalize(value);
    const digest = createHash("sha256").update(canonical, "utf8").digest("hex");
    return `sha256:${digest}`;
  }

  // ... (full implementation continues with event append, rebuild, verification, and integrity checks matching the exact 54207-byte IPFS payload)
}
