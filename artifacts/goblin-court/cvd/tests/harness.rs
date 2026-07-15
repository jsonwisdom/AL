use goblin_court_cvd::{
    DigestOracle, Event, EventKind, FailureCode, OracleState, DEBOUNCE_SECONDS,
};

#[test]
fn stale_attestation_debounces_then_enters_alarm() {
    let mut oracle = DigestOracle::new();

    let first = oracle.transition(Event {
        kind: EventKind::AttestationStale,
        observed_at_secs: 100,
    });
    assert!(!first.accepted);
    assert_eq!(oracle.state(), OracleState::Normal);

    let accepted = oracle.transition(Event {
        kind: EventKind::AttestationStale,
        observed_at_secs: 100 + DEBOUNCE_SECONDS,
    });
    assert!(accepted.accepted);
    assert_eq!(
        oracle.state(),
        OracleState::Alarm(FailureCode::F001AttestationStale)
    );
}

#[test]
fn unreachable_oracle_enters_degraded_not_global_shutdown() {
    let mut oracle = DigestOracle::new();
    oracle.transition(Event {
        kind: EventKind::OracleUnreachable,
        observed_at_secs: 10,
    });
    let cro = oracle.transition(Event {
        kind: EventKind::OracleUnreachable,
        observed_at_secs: 20,
    });

    assert!(cro.accepted);
    assert_eq!(oracle.state(), OracleState::Degraded);
}

#[test]
fn digest_mismatch_enters_critical_after_debounce() {
    let mut oracle = DigestOracle::new();
    oracle.transition(Event {
        kind: EventKind::DigestMismatch,
        observed_at_secs: 50,
    });
    let cro = oracle.transition(Event {
        kind: EventKind::DigestMismatch,
        observed_at_secs: 60,
    });

    assert!(cro.accepted);
    assert_eq!(oracle.state(), OracleState::Critical);
}

#[test]
fn equivocation_enters_critical_after_debounce() {
    let mut oracle = DigestOracle::new();
    oracle.transition(Event {
        kind: EventKind::OracleEquivocation,
        observed_at_secs: 70,
    });
    let cro = oracle.transition(Event {
        kind: EventKind::OracleEquivocation,
        observed_at_secs: 80,
    });

    assert!(cro.accepted);
    assert_eq!(oracle.state(), OracleState::Critical);
}

#[test]
fn rollback_replay_bypasses_debounce() {
    let mut oracle = DigestOracle::new();
    let cro = oracle.transition(Event {
        kind: EventKind::RollbackReplayDetected,
        observed_at_secs: 1,
    });

    assert!(cro.accepted);
    assert_eq!(oracle.state(), OracleState::Critical);
    assert!(cro.reason.contains("bypassed debounce"));
}

#[test]
fn changing_event_resets_debounce_candidate() {
    let mut oracle = DigestOracle::new();
    oracle.transition(Event {
        kind: EventKind::AttestationStale,
        observed_at_secs: 1,
    });
    oracle.transition(Event {
        kind: EventKind::OracleUnreachable,
        observed_at_secs: 5,
    });
    let cro = oracle.transition(Event {
        kind: EventKind::AttestationStale,
        observed_at_secs: 11,
    });

    assert!(!cro.accepted);
    assert_eq!(oracle.state(), OracleState::Normal);
    assert!(cro.reason.contains("debounce started"));
}

#[test]
fn healthy_event_can_recover_after_debounce() {
    let mut oracle = DigestOracle::new();
    oracle.transition(Event {
        kind: EventKind::OracleUnreachable,
        observed_at_secs: 10,
    });
    oracle.transition(Event {
        kind: EventKind::OracleUnreachable,
        observed_at_secs: 20,
    });
    assert_eq!(oracle.state(), OracleState::Degraded);

    oracle.transition(Event {
        kind: EventKind::Healthy,
        observed_at_secs: 30,
    });
    let cro = oracle.transition(Event {
        kind: EventKind::Healthy,
        observed_at_secs: 40,
    });

    assert!(cro.accepted);
    assert_eq!(oracle.state(), OracleState::Normal);
}
