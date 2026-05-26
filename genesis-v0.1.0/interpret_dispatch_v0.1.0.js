function interpret(receipt, fn) {
  if (receipt.attestation_status !== "ATTESTED") {
    throw new Error("NO_INTERPRETATION_WITHOUT_ATTESTATION");
  }
  return fn(receipt);
}
module.exports = { interpret };
