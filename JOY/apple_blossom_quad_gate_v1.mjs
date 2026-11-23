/** AppleBlossomAwesome: pure read-only policy evaluator. No API, IO, or identity side effects. */
export const VERSION = '1.1.0';
const READ_ONLY = new Set(['search_public', 'summarize_public', 'draft_receipt', 'replay_public']);
const STANCES = new Set(['SUPPORT', 'DISSENT', 'HOLD', 'UNOBSERVED']);
const safeText = x => typeof x === 'string' ? x : '';
const state = good => good ? 'READY' : 'HOLD';
export function assessQuad(input = {}) {
  // All claims, approvals, and sources in input are untrusted assertions, not verified facts.
  const i = input && typeof input === 'object' && !Array.isArray(input) ? input : {};
  const problems = [];
  const act = safeText(i.action);
  const allowed = READ_ONLY.has(act);
  if (!allowed) problems.push('ACTION_NOT_READ_ONLY');
  const publicSource = Array.isArray(i.sources) && i.sources.length > 0 &&
    i.sources.every(s => typeof s === 'string' && /^https:\/\/[a-z0-9.-]+\//i.test(s) && !s.includes('@'));
  if (!publicSource) problems.push('SOURCE_NOT_BOUND');
  if (i.realPerson === true) problems.push('REAL_PERSON_REVIEW_REQUIRED');
  if (i.minor === true) problems.push('MINOR_GUARDIAN_AND_HUMAN_GATE');
  if (i.privateData === true) problems.push('PRIVATE_DATA_DENIED');
  if (i.recordVoice === true) problems.push('VOICE_CAPTURE_DENIED');
  if (i.userInitiated !== true) problems.push('NOT_USER_INITIATED');
  const advisors = ['leahPrime', 'maryDeeBot'].map(k => {
    const a = i.advisors?.[k] || {};
    const stance = STANCES.has(a.stance) ? a.stance : 'UNOBSERVED';
    if (stance !== 'SUPPORT') problems.push(`${k.toUpperCase()}_${stance}`);
    return { seat: k, stance, advice: safeText(a.advice).slice(0, 500) };
  });
  const dissent = Array.isArray(i.dissentNotes) ? i.dissentNotes.filter(x => typeof x === 'string').slice(0, 12) : [];
  if (advisors.some(a => a.stance === 'DISSENT') && dissent.length === 0) problems.push('DISSENT_UNPRESERVED');
  if (i.retention !== 'none') problems.push('RETENTION_NOT_NONE');
  if (i.replayVerified !== true) problems.push('REPLAY_NOT_VERIFIED');
  if (i.stopConditionsDefined !== true) problems.push('STOP_CONDITIONS_MISSING');
  const output = {
    schema_version: VERSION, receipt_type: 'apple_blossom_quad_onion',
    authority: false, runtime: 'LOCAL_POLICY_SIMULATION',
    advisors, dissent_notes: dissent,
    source: { state: state(publicSource), pointers: publicSource ? [...i.sources] : [] },
    safety: { state: state(!problems.some(x => /PERSON|MINOR|PRIVATE|VOICE|RETENTION|INITIATED|DISSENT/.test(x))),
      consent: 'NOT_INFERRED', stop_on: [...problems] },
    replay: { state: state(i.replayVerified === true), hashes: [] },
    human: { state: problems.length ? 'REVIEW_OR_REFUSAL' : 'NOT_REQUIRED_FOR_DRAFT', approved_action: null },
    result_state: problems.length === 0 ? 'DRAFT_READY' : 'HOLD',
    decision: !allowed ? 'DENY' : problems.length ? 'HOLD' : 'DRAFT_READ_ONLY',
    problems: [...new Set(problems)].sort()
  };
  return output;
}
