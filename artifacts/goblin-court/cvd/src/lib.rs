use serde::{Deserialize, Serialize};

pub const DEBOUNCE_SECONDS: u64 = 10;
pub const MIN_TRANSITION_INTERVAL_SECONDS: u64 = 1;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum FailureCode {
    F001AttestationStale,
    F002OracleUnreachable,
    F003DigestMismatch,
    F004OracleEquivocation,
    F005RollbackReplay,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum OracleState {
    Normal,
    Alarm(FailureCode),
    Degraded,
    Critical,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EventKind {
    Healthy,
    AttestationStale,
    OracleUnreachable,
    DigestMismatch,
    OracleEquivocation,
    RollbackReplayDetected,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Event {
    pub kind: EventKind,
    pub observed_at_secs: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Cro {
    pub previous_state: OracleState,
    pub resulting_state: OracleState,
    pub event: String,
    pub accepted: bool,
    pub reason: String,
    pub observed_at_secs: u64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct PendingTransition {
    event_kind: EventKind,
    first_seen_at_secs: u64,
}

#[derive(Debug)]
pub struct DigestOracle {
    state: OracleState,
    last_transition_at_secs: Option<u64>,
    pending: Option<PendingTransition>,
}

impl Default for DigestOracle {
    fn default() -> Self {
        Self::new()
    }
}

impl DigestOracle {
    pub fn new() -> Self {
        Self {
            state: OracleState::Normal,
            last_transition_at_secs: None,
            pending: None,
        }
    }

    pub fn state(&self) -> OracleState {
        self.state
    }

    pub fn transition(&mut self, event: Event) -> Cro {
        let previous_state = self.state;

        if event.kind == EventKind::RollbackReplayDetected {
            self.pending = None;
            return self.apply_transition(
                previous_state,
                OracleState::Critical,
                event,
                "F005 bypassed debounce and failed closed immediately",
            );
        }

        let target = target_state(event.kind);
        if target == previous_state {
            self.pending = None;
            return Cro {
                previous_state,
                resulting_state: previous_state,
                event: event_name(event.kind).to_string(),
                accepted: false,
                reason: "event maps to current state; no transition required".to_string(),
                observed_at_secs: event.observed_at_secs,
            };
        }

        if let Some(last) = self.last_transition_at_secs {
            if event.observed_at_secs.saturating_sub(last) < MIN_TRANSITION_INTERVAL_SECONDS {
                return Cro {
                    previous_state,
                    resulting_state: previous_state,
                    event: event_name(event.kind).to_string(),
                    accepted: false,
                    reason: "hysteresis guard blocked transition inside minimum interval"
                        .to_string(),
                    observed_at_secs: event.observed_at_secs,
                };
            }
        }

        match self.pending {
            Some(pending) if pending.event_kind == event.kind => {
                let held_for = event
                    .observed_at_secs
                    .saturating_sub(pending.first_seen_at_secs);
                if held_for < DEBOUNCE_SECONDS {
                    return Cro {
                        previous_state,
                        resulting_state: previous_state,
                        event: event_name(event.kind).to_string(),
                        accepted: false,
                        reason: format!(
                            "debounce pending: held for {held_for}s, requires {DEBOUNCE_SECONDS}s"
                        ),
                        observed_at_secs: event.observed_at_secs,
                    };
                }

                self.pending = None;
                self.apply_transition(
                    previous_state,
                    target,
                    event,
                    "debounce satisfied; transition accepted",
                )
            }
            _ => {
                self.pending = Some(PendingTransition {
                    event_kind: event.kind,
                    first_seen_at_secs: event.observed_at_secs,
                });
                Cro {
                    previous_state,
                    resulting_state: previous_state,
                    event: event_name(event.kind).to_string(),
                    accepted: false,
                    reason: format!(
                        "debounce started; repeat same event after {DEBOUNCE_SECONDS}s"
                    ),
                    observed_at_secs: event.observed_at_secs,
                }
            }
        }
    }

    fn apply_transition(
        &mut self,
        previous_state: OracleState,
        target: OracleState,
        event: Event,
        reason: &str,
    ) -> Cro {
        self.state = target;
        self.last_transition_at_secs = Some(event.observed_at_secs);
        Cro {
            previous_state,
            resulting_state: target,
            event: event_name(event.kind).to_string(),
            accepted: true,
            reason: reason.to_string(),
            observed_at_secs: event.observed_at_secs,
        }
    }
}

fn target_state(kind: EventKind) -> OracleState {
    match kind {
        EventKind::Healthy => OracleState::Normal,
        EventKind::AttestationStale => OracleState::Alarm(FailureCode::F001AttestationStale),
        EventKind::OracleUnreachable => OracleState::Degraded,
        EventKind::DigestMismatch => OracleState::Critical,
        EventKind::OracleEquivocation => OracleState::Critical,
        EventKind::RollbackReplayDetected => OracleState::Critical,
    }
}

fn event_name(kind: EventKind) -> &'static str {
    match kind {
        EventKind::Healthy => "HEALTHY",
        EventKind::AttestationStale => "F001_ATTESTATION_STALE",
        EventKind::OracleUnreachable => "F002_ORACLE_UNREACHABLE",
        EventKind::DigestMismatch => "F003_DIGEST_MISMATCH",
        EventKind::OracleEquivocation => "F004_ORACLE_EQUIVOCATION",
        EventKind::RollbackReplayDetected => "F005_ROLLBACK_REPLAY_DETECTED",
    }
}
