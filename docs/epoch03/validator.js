export const VALIDATOR_VERSION = "0.1.0";

export function canonicalJson(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(",")}}`;
}

export async function sha256Hex(value) {
  const input = typeof value === "string" ? value : canonicalJson(value);
  const bytes = new TextEncoder().encode(input);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export function findTransition(fsm, step) {
  return fsm.transitions.find((transition) =>
    transition.from === step.from &&
    transition.to === step.to &&
    transition.trigger === step.trigger &&
    transition.guard === step.guard
  ) || null;
}

export function validateStep(step, fsm, doctrine) {
  const transition = findTransition(fsm, step);
  if (!transition) {
    return {
      verdict: "REJECT",
      code: "E_TRANSITION_NOT_ALLOWED",
      message: "Transition does not exist in canonical FSM."
    };
  }

  const clause = doctrine.clauses.find((item) => item.code === step.guard);
  if (!clause) {
    return {
      verdict: "REJECT",
      code: "E_GUARD_NOT_FOUND",
      message: "Guard code does not exist in doctrine."
    };
  }

  if (step.result !== "ACCEPT" && step.result !== "REJECT") {
    return {
      verdict: "REJECT",
      code: "E_RESULT_INVALID",
      message: "Recorded result must be ACCEPT or REJECT."
    };
  }

  return {
    verdict: step.result,
    code: step.result === "ACCEPT" ? "OK" : step.guard,
    message: step.result === "ACCEPT" ? "Transition accepted by canonical FSM." : clause.error_message
  };
}

export function validateTranscript(transcript, fsm, doctrine) {
  if (!transcript || !Array.isArray(transcript.steps)) {
    return {
      verdict: "REJECT",
      code: "E_TRANSCRIPT_INVALID",
      message: "Transcript must include finite steps array.",
      steps: []
    };
  }

  let previous = transcript.initial_state;
  const stepResults = [];

  for (const step of transcript.steps) {
    if (step.from !== previous) {
      return {
        verdict: "REJECT",
        code: "E_SEQUENCE_BROKEN",
        message: `Step ${step.seq} does not begin at previous state ${previous}.`,
        steps: stepResults
      };
    }

    const result = validateStep(step, fsm, doctrine);
    stepResults.push({ seq: step.seq, ...result });

    if (result.verdict !== step.result) {
      return {
        verdict: "REJECT",
        code: "E_REPLAY_MISMATCH",
        message: `Step ${step.seq} recorded ${step.result} but validator returned ${result.verdict}.`,
        steps: stepResults
      };
    }

    previous = step.to;
  }

  if (previous !== transcript.final_state) {
    return {
      verdict: "REJECT",
      code: "E_FINAL_STATE_MISMATCH",
      message: `Final state ${transcript.final_state} does not match replay state ${previous}.`,
      steps: stepResults
    };
  }

  return {
    verdict: "ACCEPT",
    code: "OK",
    message: "Transcript replay consistent with canonical FSM and doctrine.",
    steps: stepResults
  };
}

export async function hashDoctrine(doctrine) {
  return sha256Hex(doctrine);
}

export async function hashFsm(fsm) {
  return sha256Hex(fsm);
}

export async function hashTranscript(transcript) {
  return sha256Hex(transcript);
}
