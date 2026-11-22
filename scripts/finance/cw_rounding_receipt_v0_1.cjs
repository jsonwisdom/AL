#!/usr/bin/env node
// CW rounding receipt v0.1: exact micro-unit accounting, deterministic read-only test.
// Unit = 1/100000 USD. Settlement at 1000 units per cent.
// This utility is synthetic/testing only: never posts financial entries or authorizes payment.
'use strict';
const assert = require('node:assert/strict');
const assertUnits = x => {
  if (typeof x !== 'bigint') throw new TypeError('unit amounts must be bigint');
};
function settleTruncateTowardZero(entries, increment = 1000n) {
  if (!Array.isArray(entries) || !entries.length) throw new Error('entries required');
  assertUnits(increment);
  if (increment <= 0n) throw new Error('increment must be positive');
  for (const x of entries) assertUnits(x);
  const rawUnits = entries.reduce((s, x) => s + x, 0n);
  const settledUnits = (rawUnits / increment) * increment;
  const remainderUnits = rawUnits - settledUnits;
  assert.equal(rawUnits, settledUnits + remainderUnits);
  if (remainderUnits >= increment || remainderUnits <= -increment) throw new Error('remainder outside bounds');
  return {rawUnits, settledUnits, remainderUnits};
}
function microUsd(units) {
  assertUnits(units);
  const abs = units < 0n ? -units : units;
  return (units < 0n ? '-$' : '$') + (abs / 100000n).toString() + '.' + (abs % 100000n).toString().padStart(5, '0');
}
if (require.main === module) {
  const examples = [
    {name:'zero',entries:[0n],want:[0n,0n,0n]},
    {name:'single fractional cent',entries:[1n],want:[1n,0n,1n]},
    {name:'1,000 verified synthetic increments',entries:Array(1000).fill(1n),want:[1000n,1000n,0n]},
    {name:'carry forward 234',entries:[1234n],want:[1234n,1000n,234n]},
    {name:'negative refund',entries:[-1234n],want:[-1234n,-1000n,-234n]},
    {name:'positive and negative cancel',entries:[1350n,-1350n],want:[0n,0n,0n]},
    {name:'large exact integer',entries:[9007199254740993n],want:[9007199254740993n,9007199254740000n,993n]}
  ];
  for (const x of examples) {
    const r=settleTruncateTowardZero(x.entries);
    assert.deepEqual([r.rawUnits,r.settledUnits,r.remainderUnits],x.want,x.name);
    console.log('PASS '+x.name+' '+microUsd(r.rawUnits)+' = '+microUsd(r.settledUnits)+' + '+microUsd(r.remainderUnits));
  }
  const perAction = Array(1000).fill(1n);
  const wrong = perAction.reduce((s,x)=>s+(x/1000n)*1000n,0n);
  const correct = settleTruncateTowardZero(perAction).settledUnits;
  assert.equal(wrong,0n); assert.equal(correct,1000n);
  assert.throws(()=>settleTruncateTowardZero([0.1]),/bigint/);
  assert.throws(()=>settleTruncateTowardZero([]),/entries required/);
  assert.throws(()=>settleTruncateTowardZero([1n],0n),/positive/);
  console.log('PASS premature-rounding counterexample and invalid-input guards');
}
module.exports={settleTruncateTowardZero,microUsd};
