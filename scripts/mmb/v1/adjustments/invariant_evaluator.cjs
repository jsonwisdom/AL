function fail(message) {
  throw new Error(message);
}

function validSha256(value) {
  return typeof value === "string" && /^[a-fA-F0-9]{64}$/.test(value);
}

function evaluate(manifest) {
  const {
    epoch_id,
    fund_id,
    line_items,
    override_flag,
    override_receipt_sha256
  } = manifest;

  if (!epoch_id) fail("missing epoch_id");
  if (!fund_id) fail("missing fund_id");
  if (!Array.isArray(line_items) || line_items.length === 0) fail("line_items required");

  const net = line_items.reduce((sum, item) => {
    if (!item.line_item_id) fail("line_item_id required");
    if (item.epoch_id !== epoch_id) fail(`epoch mismatch: ${item.line_item_id}`);
    if (item.fund_id !== fund_id) fail(`fund mismatch: ${item.line_item_id}`);
    if (!Number.isInteger(item.amount_delta_cents)) fail(`amount_delta_cents must be integer: ${item.line_item_id}`);
    return sum + item.amount_delta_cents;
  }, 0);

  if (net !== 0) {
    if (override_flag === true && validSha256(override_receipt_sha256)) {
      return { status: "OVERRIDDEN", net_delta_cents: net, override_receipt_sha256 };
    }
    fail(`NO_UNBALANCED_NEGATIVE_REALLOCATION: net_delta_cents=${net}`);
  }

  return { status: "PASS", net_delta_cents: net };
}

module.exports = { evaluate };
