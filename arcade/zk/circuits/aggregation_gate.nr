// aggregation_gate.nr
// Episode 002: Constellation Alignment
// Design target: prove composite progression before Nebula Egg unlock.

global EPISODE_002_ID: Field = 1002;
global NEBULA_EGG_ID: Field = 2002;
global MIN_TOTAL_REPLAYS: u32 = 5;

fn main(
    episode_id: Field,
    egg_id: Field,
    total_replay_count: u32,

    fragment_a: Field,
    fragment_b: Field,
    fragment_c: Field,

    completion_hash: pub Field
) {
    assert(episode_id == EPISODE_002_ID);
    assert(egg_id == NEBULA_EGG_ID);
    assert(total_replay_count >= MIN_TOTAL_REPLAYS);

    assert(fragment_a != 0);
    assert(fragment_b != 0);
    assert(fragment_c != 0);

    assert(completion_hash != 0);
}
