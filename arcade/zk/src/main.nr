// egg_inclusion_compile_pass_v0
// Minimal Noir compile target for Arcade ZK.
// This proves circuit wiring compiles; it does NOT prove Merkle inclusion yet.

global MIN_REPLAY_REQUIRED: u32 = 1;
global EPISODE_001_ID: Field = 1001;

fn main(
    episode_id: Field,
    replay_count: u32,
    root: pub Field,
    egg_id: pub Field
) {
    assert(episode_id == EPISODE_001_ID);
    assert(replay_count >= MIN_REPLAY_REQUIRED);
    assert(root != 0);
    assert(egg_id != 0);
}
