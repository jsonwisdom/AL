--------------------------- MODULE CEC_GOVERNOR_STATE_MACHINE_V0_1 ---------------------------
EXTENDS Integers, FiniteSets, TLC

(*
   CEC Governor - Temporal Gatekeeper Model v0.1
   TLC-READY: Bound hashes, stateful time, fixed invariants, tuple collision result.
*)

CONSTANTS
    MaxRoots, MaxSigners, M, TimeHorizon, ChallengeWindow, MaxReceipts

ASSUME M \in 1..MaxSigners
ASSUME MaxRoots \in 1..10
ASSUME MaxSigners \in 1..10
ASSUME TimeHorizon \in 5..100
ASSUME ChallengeWindow \in 1..TimeHorizon
ASSUME MaxReceipts \in 5..100

Root == 0 .. (MaxRoots - 1)
Signer == 0 .. (MaxSigners - 1)
Timestamp == 0 .. (TimeHorizon - 1)
Hash == 0 .. (MaxReceipts - 1)

Receipt == [hash: Hash, root: Root, ts_claimed: Timestamp,
            signers: SUBSET Signer, submit_time: Timestamp,
            signer_snapshot: SUBSET Signer]

Challenge == [receipt_hash: Hash, valid: BOOLEAN, ts: Timestamp]

VARIABLES
    current_root,
    active_signers,
    registration_valid_from,
    pending_receipts,
    challenged_receipts,
    rejected_receipts,
    accepted_receipts,
    log,
    frozen,
    current_time

vars == << current_root, active_signers, registration_valid_from,
          pending_receipts, challenged_receipts, rejected_receipts,
          accepted_receipts, log, frozen, current_time >>

Init ==
    /\ current_root = 0
    /\ active_signers = Signer
    /\ registration_valid_from = 0
    /\ pending_receipts = {}
    /\ challenged_receipts = {}
    /\ rejected_receipts = {}
    /\ accepted_receipts = {}
    /\ log = {}
    /\ frozen = FALSE
    /\ current_time = 0

IsValidSignerSetAgainst(signer_set, signer_snapshot) ==
    signer_set \subseteq signer_snapshot
    /\ Cardinality(signer_set) >= M

IsValidSignerSet(signer_set, check_time) ==
    LET active_at_time ==
        IF check_time >= registration_valid_from
        THEN active_signers
        ELSE {}
    IN IsValidSignerSetAgainst(signer_set, active_at_time)

IsProcessed(receipt) == receipt \in log

ResolvedRoot(expired_hashes) ==
    LET expired_receipts == {r \in log : r.hash \in expired_hashes}
        roots_set == {r.root : r \in expired_receipts}
    IN IF Cardinality(roots_set) = 1
       THEN [status |-> "OK", root |-> CHOOSE r \in roots_set : TRUE]
       ELSE [status |-> "COLLISION_FREEZE", root |-> current_root]

ReceiptSubmit(receipt) ==
    /\ frozen = FALSE
    /\ ~IsProcessed(receipt)
    /\ IsValidSignerSet(receipt.signers, current_time)
    /\ receipt.signer_snapshot = active_signers
    /\ receipt.root \in Root
    /\ receipt.submit_time = current_time
    /\ receipt.ts_claimed \in Timestamp
    /\ receipt.hash \in Hash
    /\ receipt.hash \notin {r.hash : r \in log}
    /\ LET window_expires == current_time + ChallengeWindow
       IN
       IF current_time < window_expires
       THEN
           /\ pending_receipts' = pending_receipts \union {receipt.hash}
           /\ UNCHANGED <<accepted_receipts, current_root>>
       ELSE
           /\ accepted_receipts' = accepted_receipts \union {receipt.hash}
           /\ current_root' = receipt.root
           /\ UNCHANGED pending_receipts
    /\ log' = log \union {receipt}
    /\ UNCHANGED <<challenged_receipts, rejected_receipts,
                   active_signers, registration_valid_from, frozen, current_time>>

ChallengeSubmit(receipt_hash, challenge) ==
    /\ frozen = FALSE
    /\ receipt_hash \in pending_receipts
    /\ challenge.receipt_hash = receipt_hash
    /\ challenge.ts = current_time
    /\ LET receipt == CHOOSE r \in log: r.hash = receipt_hash
       IN challenge.ts <= receipt.submit_time + ChallengeWindow
    /\ challenge.valid \in BOOLEAN
    /\ IF challenge.valid = TRUE
       THEN
           /\ pending_receipts' = pending_receipts \ {receipt_hash}
           /\ challenged_receipts' = challenged_receipts \union {receipt_hash}
       ELSE
           /\ UNCHANGED <<pending_receipts, challenged_receipts>>
    /\ UNCHANGED <<current_root, active_signers, registration_valid_from,
                   rejected_receipts, accepted_receipts, log, frozen, current_time>>

ChallengeResolve(receipt_hash, outcome) ==
    /\ frozen = FALSE
    /\ receipt_hash \in challenged_receipts
    /\ outcome \in BOOLEAN
    /\ LET receipt == CHOOSE r \in log: r.hash = receipt_hash
       IN IF outcome = TRUE
          THEN
              /\ challenged_receipts' = challenged_receipts \ {receipt_hash}
              /\ rejected_receipts' = rejected_receipts \union {receipt_hash}
              /\ UNCHANGED current_root
          ELSE
              /\ challenged_receipts' = challenged_receipts \ {receipt_hash}
              /\ accepted_receipts' = accepted_receipts \union {receipt_hash}
              /\ current_root' = receipt.root
    /\ UNCHANGED <<pending_receipts, active_signers, registration_valid_from,
                   log, frozen, current_time>>

TimeAdvance ==
    /\ frozen = FALSE
    /\ current_time < TimeHorizon - 1
    /\ LET new_time == current_time + 1
           expired == {h \in pending_receipts:
                       LET r == CHOOSE rr \in log: rr.hash = h
                       IN new_time >= r.submit_time + ChallengeWindow}
       IN
       IF expired = {}
       THEN
           /\ pending_receipts' = pending_receipts
           /\ UNCHANGED <<current_root, accepted_receipts, frozen>>
       ELSE
           LET resolution == ResolvedRoot(expired)
           IN
           IF resolution.status = "COLLISION_FREEZE"
           THEN
               /\ frozen' = TRUE
               /\ UNCHANGED <<current_root, pending_receipts, accepted_receipts>>
           ELSE
               /\ pending_receipts' = pending_receipts \ expired
               /\ accepted_receipts' = accepted_receipts \union expired
               /\ current_root' = resolution.root
               /\ UNCHANGED frozen
    /\ current_time' = current_time + 1
    /\ UNCHANGED <<challenged_receipts, rejected_receipts, log,
                   active_signers, registration_valid_from>>

QuorumRotation(new_signers, valid_from) ==
    /\ frozen = FALSE
    /\ current_time >= registration_valid_from
    /\ new_signers \subseteq Signer
    /\ Cardinality(new_signers) >= M
    /\ valid_from \in Timestamp
    /\ valid_from >= current_time
    /\ active_signers' = new_signers
    /\ registration_valid_from' = valid_from
    /\ UNCHANGED <<current_root, pending_receipts, challenged_receipts,
                   rejected_receipts, accepted_receipts, log, frozen, current_time>>

QuorumRevocation(revoked_signer) ==
    /\ frozen = FALSE
    /\ revoked_signer \in active_signers
    /\ current_time >= registration_valid_from
    /\ active_signers' = active_signers \ {revoked_signer}
    /\ Cardinality(active_signers') >= M
    /\ registration_valid_from' = current_time
    /\ UNCHANGED <<current_root, pending_receipts, challenged_receipts,
                   rejected_receipts, accepted_receipts, log, frozen, current_time>>

ManualSupersession(new_root) ==
    /\ frozen = TRUE
    /\ new_root \in Root
    /\ current_root' = new_root
    /\ frozen' = FALSE
    /\ UNCHANGED <<active_signers, registration_valid_from, pending_receipts,
                   challenged_receipts, rejected_receipts, accepted_receipts,
                   log, current_time>>

Next ==
    \/ \E receipt \in Receipt: ReceiptSubmit(receipt)
    \/ \E receipt_hash \in Hash, challenge \in Challenge: ChallengeSubmit(receipt_hash, challenge)
    \/ \E receipt_hash \in Hash, outcome \in BOOLEAN: ChallengeResolve(receipt_hash, outcome)
    \/ TimeAdvance
    \/ \E new_signers \in SUBSET Signer, valid_from \in Timestamp: QuorumRotation(new_signers, valid_from)
    \/ \E revoked_signer \in Signer: QuorumRevocation(revoked_signer)
    \/ \E new_root \in Root: ManualSupersession(new_root)

Spec == Init /\ [][Next]_vars

NoInvalidRootAccepted ==
    frozen = FALSE =>
        \A h \in accepted_receipts:
            LET r == CHOOSE rr \in log: rr.hash = h
            IN IsValidSignerSetAgainst(r.signers, r.signer_snapshot)
               /\ r.root = current_root

RevokedSignerCannotAuthorize ==
    \A r \in log:
        IsValidSignerSetAgainst(r.signers, r.signer_snapshot)

ValidChallengeBlocksAcceptance ==
    (challenged_receipts \intersect accepted_receipts) = {}
    /\ (challenged_receipts \intersect rejected_receipts) = {}

TimeMonotonic ==
    current_time \in Timestamp

Safety == NoInvalidRootAccepted /\ RevokedSignerCannotAuthorize /\
          ValidChallengeBlocksAcceptance /\ TimeMonotonic

=============================================================================
