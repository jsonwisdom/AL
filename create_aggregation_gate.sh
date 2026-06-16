#!/usr/bin/env bash
set -euo pipefail

mkdir -p arcade/zk/src

cat > arcade/zk/src/aggregation_gate.nr <<'NR'
// aggregation_gate.nr v1.0
// Three constitutional leaves -> one completion hash

use dep::std::hash::poseidon::bn254::hash_5;

fn compute_leaf_commitment(
    player_id: Field,
    episode_id: Field,
    fragment_id: Field,
    replay_count: Field,
    egg_id: Field,
) -> Field {
    hash_5([player_id, episode_id, fragment_id, replay_count, egg_id])
}

fn main(
    root: pub Field,
    episode_id: pub Field,
    completion_hash: pub Field,

    threshold: Field,

    player_id_a: Field,
    fragment_id_a: Field,
    replay_count_a: Field,
    egg_id_a: Field,

    player_id_b: Field,
    fragment_id_b: Field,
    replay_count_b: Field,
    egg_id_b: Field,

    player_id_c: Field,
    fragment_id_c: Field,
    replay_count_c: Field,
    egg_id_c: Field,
) {
    let leaf_a = compute_leaf_commitment(player_id_a, episode_id, fragment_id_a, replay_count_a, egg_id_a);
    let leaf_b = compute_leaf_commitment(player_id_b, episode_id, fragment_id_b, replay_count_b, egg_id_b);
    let leaf_c = compute_leaf_commitment(player_id_c, episode_id, fragment_id_c, replay_count_c, egg_id_c);

    assert(replay_count_a >= threshold);
    assert(replay_count_b >= threshold);
    assert(replay_count_c >= threshold);

    let computed_completion = hash_5([leaf_a, leaf_b, leaf_c, threshold, root]);

    assert(computed_completion == completion_hash);
}
NR

echo "created arcade/zk/src/aggregation_gate.nr"
sha256sum arcade/zk/src/aggregation_gate.nr
