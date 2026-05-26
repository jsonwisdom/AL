function attest(receipt) {
  const witnesses = receipt.time_witnesses || [];
  if (witnesses.length < 3) return "UNVERIFIABLE";
  return "ATTESTED";
}
module.exports = { attest };
