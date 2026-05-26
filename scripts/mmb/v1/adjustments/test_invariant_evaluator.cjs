const { evaluate } = require("./invariant_evaluator.cjs");

function run(name, fn) {
  try {
    fn();
    console.log(`PASS: ${name}`);
  } catch (err) {
    console.error(`FAIL: ${name}`);
    console.error(err.message);
    process.exit(1);
  }
}

run("balanced same fund same epoch passes", () => {
  const result = evaluate({
    epoch_id: "fy2026_q1",
    fund_id: "general",
    override_flag: false,
    line_items: [
      { line_item_id: "ops", epoch_id: "fy2026_q1", fund_id: "general", amount_delta_cents: -10000 },
      { line_item_id: "infra", epoch_id: "fy2026_q1", fund_id: "general", amount_delta_cents: 10000 }
    ]
  });
  if (result.status !== "PASS") throw new Error("expected PASS");
});

run("unbalanced fails without override", () => {
  let failed = false;
  try {
    evaluate({
      epoch_id: "fy2026_q1",
      fund_id: "general",
      override_flag: false,
      line_items: [
        { line_item_id: "ops", epoch_id: "fy2026_q1", fund_id: "general", amount_delta_cents: -10000 }
      ]
    });
  } catch {
    failed = true;
  }
  if (!failed) throw new Error("expected failure");
});

run("unbalanced passes with override receipt", () => {
  const result = evaluate({
    epoch_id: "fy2026_q1",
    fund_id: "general",
    override_flag: true,
    override_receipt_sha256: "a".repeat(64),
    line_items: [
      { line_item_id: "ops", epoch_id: "fy2026_q1", fund_id: "general", amount_delta_cents: -10000 }
    ]
  });
  if (result.status !== "OVERRIDDEN") throw new Error("expected OVERRIDDEN");
});
