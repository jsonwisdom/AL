import assert from 'node:assert/strict';
import { assessQuad } from './apple_blossom_quad_gate_v1.mjs';
const base = () => ({action:'search_public',sources:['https://github.com/jsonwisdom/JOY/blob/main/README.md'],
 userInitiated:true,advisors:{leahPrime:{stance:'SUPPORT',advice:'ok'},maryDeeBot:{stance:'SUPPORT',advice:'ok'}},
 retention:'none',replayVerified:true,stopConditionsDefined:true,realPerson:false,minor:false,privateData:false,recordVoice:false,
 dissentNotes:[]});
let n=0;
function test(name,fn){fn();n++;}
test('eligible public draft',()=>assert.equal(assessQuad(base()).decision,'DRAFT_READ_ONLY'));
test('authority remains false',()=>assert.equal(assessQuad(base()).authority,false));
test('no actor promotion',()=>assert.equal(assessQuad(base()).human.approved_action,null));
test('real-person query gated',()=>{const v=base();v.realPerson=true;assert(assessQuad(v).problems.includes('REAL_PERSON_REVIEW_REQUIRED'));});
test('minor gated even with advisor support',()=>{const v=base();v.minor=true;assert.equal(assessQuad(v).result_state,'HOLD');});
test('private data gated',()=>{const v=base();v.privateData=true;assert.equal(assessQuad(v).decision,'HOLD');});
test('voice recording gated',()=>{const v=base();v.recordVoice=true;assert.equal(assessQuad(v).decision,'HOLD');});
test('uninitiated gated',()=>{const v=base();v.userInitiated=false;assert.equal(assessQuad(v).result_state,'HOLD');});
test('empty source gated',()=>{const v=base();v.sources=[];assert.equal(assessQuad(v).source.state,'HOLD');});
test('non HTTPS source gated',()=>{const v=base();v.sources=['file:///etc/passwd'];assert.equal(assessQuad(v).decision,'HOLD');});
test('advisor missing gated',()=>{const v=base();delete v.advisors;assert.equal(assessQuad(v).result_state,'HOLD');});
test('advisor stance retained',()=>{const v=base();v.advisors.leahPrime.stance='HOLD';assert.equal(assessQuad(v).advisors[0].stance,'HOLD');});
test('dissent preserved',()=>{const v=base();v.advisors.leahPrime.stance='DISSENT';v.dissentNotes=['Source interpretation contested'];const r=assessQuad(v);assert.deepEqual(r.dissent_notes,['Source interpretation contested']);assert.equal(r.result_state,'HOLD');});
test('unrecorded dissent gated',()=>{const v=base();v.advisors.leahPrime.stance='DISSENT';assert(assessQuad(v).problems.includes('DISSENT_UNPRESERVED'));});
test('retention gated',()=>{const v=base();v.retention='forever';assert.equal(assessQuad(v).result_state,'HOLD');});
test('replay required',()=>{const v=base();v.replayVerified=false;assert.equal(assessQuad(v).replay.state,'HOLD');});
test('stop conditions required',()=>{const v=base();v.stopConditionsDefined=false;assert(assessQuad(v).problems.includes('STOP_CONDITIONS_MISSING'));});
for(const act of ['deploy','merge','publish','send_message','spend','sign','record_voice','configure_cloudflare','read_secret'])test(`deny ${act}`,()=>{const v=base();v.action=act;assert.equal(assessQuad(v).decision,'DENY');});
test('non-object input fail-closed',()=>assert.equal(assessQuad(null).result_state,'HOLD'));
test('empty input fail-closed',()=>assert.equal(assessQuad({}).result_state,'HOLD'));
test('deterministic replay',()=>assert.deepEqual(assessQuad(base()),assessQuad(base())));
// 200 deterministic combinations of privacy, missing source, dissent, prohibited action.
let seed=20261123; const rand=()=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed/4294967296;};
for(let j=0;j<200;j++){const v=base();if(rand()<0.5)v.realPerson=true;if(rand()<0.5)v.minor=true;if(rand()<0.5)v.privateData=true;if(rand()<0.5)v.sources=[];if(rand()<0.5)v.advisors.leahPrime.stance='DISSENT';if(rand()<0.5)v.action='deploy';let r=assessQuad(v);assert.equal(r.authority,false);assert.equal(r.human.approved_action,null);assert.deepEqual(r,assessQuad(v));if(v.realPerson||v.minor||v.privateData||v.sources.length===0||v.advisors.leahPrime.stance==='DISSENT'||v.action==='deploy')assert.notEqual(r.result_state,'DRAFT_READY');n++;}
console.log(JSON.stringify({status:'PASS',assertions:n,explicit:n-200,fuzz:200,seed:20261123,authority:false,scope:'LOCAL_POLICY_SIMULATION'}));
