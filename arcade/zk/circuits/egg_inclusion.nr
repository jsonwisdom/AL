// egg_inclusion.nr
// Arcade ZK Rule Engine v0.2
// Proves an episode-scoped SnapBack egg is included in a root
// without exposing the player history.

global MERKLE_DEPTH = 10;
global MIN_REPLAY_REQUIRED = 1;
global EPISODE_001_ID = 1001;

fn main(
    player_id: Field,
    episode_id: Field,
    replay_count: Field,
    egg_id: Field,
    path_siblings: [Field; MERKLE_DEPTH],
    path_indices: [u8; MERKLE_DEPTH],

    root: pub Field,
    public_episode_id: pub Field,
    public_egg_id: pub Field
) {
    assert(episode_id == EPISODE_001_ID);
    assert(public_episode_id == episode_id);
    assert(public_egg_id == egg_id);
    assert(replay_count >= MIN_REPLAY_REQUIRED);

    // Leaf binds identity, episode, replay count, and egg together.
    // Replay count is not a floating private claim; it is committed into the leaf.
    let leaf = std::hash::pedersen([
        player_id,
        episode_id,
        replay_count,
        egg_id
    ]);

    let calculated_root = std::merkle::compute_merkle_root(
        leaf,
        path_siblings,
        path_indices
    );

    assert(calculated_root == root);
}
