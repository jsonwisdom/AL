import * as jsValidator from "./validator.js";

export const ENGINE_CONTRACT_VERSION = "0.1.0";

let engine = {
  mode: "js",
  contract: ENGINE_CONTRACT_VERSION,
  validator_version: jsValidator.VALIDATOR_VERSION,
  validateStep: async (step, fsm, doctrine) => jsValidator.validateStep(step, fsm, doctrine),
  validateTranscript: async (transcript, fsm, doctrine) => jsValidator.validateTranscript(transcript, fsm, doctrine),
  hashDoctrine: async (doctrine) => jsValidator.hashDoctrine(doctrine),
  hashFsm: async (fsm) => jsValidator.hashFsm(fsm),
  hashTranscript: async (transcript) => jsValidator.hashTranscript(transcript),
  sha256Hex: async (value) => jsValidator.sha256Hex(value)
};

function readWasmString(exports, ptr) {
  const len = exports.get_last_result_len();
  const bytes = new Uint8Array(exports.memory.buffer, ptr, len);
  return new TextDecoder().decode(bytes);
}

function writeWasmString(exports, value) {
  const bytes = new TextEncoder().encode(value);
  const ptr = exports.alloc(bytes.length);
  const mem = new Uint8Array(exports.memory.buffer, ptr, bytes.length);
  mem.set(bytes);
  return { ptr, len: bytes.length };
}

function callHashCanonical(exports, json) {
  const input = writeWasmString(exports, json);
  const outPtr = exports.hash_canonical(input.ptr, input.len);
  return readWasmString(exports, outPtr);
}

export async function initEpoch03Engine() {
  try {
    const wasm = await WebAssembly.instantiateStreaming(fetch("./epoch03_validator.wasm"), {});
    const exports = wasm.instance.exports;

    const required = ["memory", "alloc", "get_last_result_len", "validate_wasm", "hash_canonical"];
    for (const name of required) {
      if (!exports[name]) throw new Error(`missing WASM export: ${name}`);
    }

    engine = {
      mode: "wasm",
      contract: ENGINE_CONTRACT_VERSION,
      validator_version: jsValidator.VALIDATOR_VERSION,
      async validateTranscript(transcript, fsm, doctrine) {
        const fsmInput = writeWasmString(exports, JSON.stringify(fsm));
        const transcriptInput = writeWasmString(exports, JSON.stringify(transcript));
        const outPtr = exports.validate_wasm(fsmInput.ptr, fsmInput.len, transcriptInput.ptr, transcriptInput.len);
        return JSON.parse(readWasmString(exports, outPtr));
      },
      async validateStep(step, fsm, doctrine) {
        const tx = {
          meta: {
            id: "single-step",
            epoch: "epoch03",
            doctrine_id: doctrine.doctrine_id,
            doctrine_version: doctrine.version,
            fsm_id: fsm.meta.id,
            fsm_version: fsm.meta.version
          },
          initial_state: step.from,
          steps: [step],
          final_state: step.to
        };
        const verdict = await this.validateTranscript(tx, fsm, doctrine);
        const stepVerdict = verdict.steps && verdict.steps[0] ? verdict.steps[0] : null;
        return stepVerdict || verdict;
      },
      async hashDoctrine(doctrine) {
        return callHashCanonical(exports, JSON.stringify(doctrine));
      },
      async hashFsm(fsm) {
        return callHashCanonical(exports, JSON.stringify(fsm));
      },
      async hashTranscript(transcript) {
        return callHashCanonical(exports, JSON.stringify(transcript));
      },
      async sha256Hex(value) {
        return callHashCanonical(exports, typeof value === "string" ? value : JSON.stringify(value));
      }
    };
  } catch (error) {
    console.warn("[epoch03] WASM unavailable; using JS validator fallback", error);
  }

  window.epoch03Engine = engine;
  return engine;
}

export function getEpoch03Engine() {
  return engine;
}
