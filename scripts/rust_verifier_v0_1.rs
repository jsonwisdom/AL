// ALMS Cross-Verifier Independent Rust Gate v0.1
//
// Purpose:
//   Hash the committed ALMS replay preimage disclosure candidate bytes directly
//   and report whether those bytes satisfy the Branch 2 replay-hash gate.
//
// Important audit rule:
//   This verifier does not import the expected replay hash as a Rust constant.
//   It reads the expected digest declared in the committed preimage metadata and
//   compares it to SHA256(file bytes). If the committed file is metadata rather
//   than the exact replay preimage bytes, the gate must fail honestly.
//
// Usage:
//   rustc scripts/rust_verifier_v0_1.rs -o /tmp/rust_gate_v0_1
//   /tmp/rust_gate_v0_1 vectors/alms_replay_preimage_v0_1.json

use std::env;
use std::fs;
use std::io::Write;
use std::process::{Command, Stdio, exit};

fn json_get_string(src: &str, key: &str) -> String {
    let marker = format!("\"{}\"", key);
    let start = src.find(&marker).unwrap_or_else(|| panic!("missing key {}", key));
    let after_key = &src[start + marker.len()..];
    let colon = after_key.find(':').unwrap();
    let after_colon = after_key[colon + 1..].trim_start();
    assert!(after_colon.starts_with('"'), "key {} is not a JSON string", key);

    let mut out = String::new();
    let mut escaped = false;
    for ch in after_colon[1..].chars() {
        if escaped {
            out.push(ch);
            escaped = false;
        } else if ch == '\\' {
            escaped = true;
        } else if ch == '"' {
            break;
        } else {
            out.push(ch);
        }
    }
    out
}

fn sha256_bytes_with_system(bytes: &[u8]) -> String {
    let mut child = Command::new("sha256sum")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .expect("failed to execute sha256sum");

    child.stdin.as_mut().unwrap().write_all(bytes).unwrap();

    let out = child.wait_with_output().unwrap();
    let text = String::from_utf8(out.stdout).unwrap();
    format!("0x{}", text.split_whitespace().next().unwrap())
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let path = args.get(1).map(|s| s.as_str()).unwrap_or("vectors/alms_replay_preimage_v0_1.json");

    let bytes = fs::read(path).expect("failed to read preimage candidate file bytes");
    let text = String::from_utf8(bytes.clone()).expect("preimage candidate must be UTF-8 JSON");

    let expected_replay_hash = json_get_string(&text, "expected_sha256_replay_hash");
    let declared_candidate_file_sha256 = json_get_string(&text, "candidate_file_sha256");
    let ipfs_cid = json_get_string(&text, "ipfs_cid");
    let computed_file_sha256 = sha256_bytes_with_system(&bytes);

    let file_bytes_match_declared_candidate = computed_file_sha256 == declared_candidate_file_sha256;
    let replay_gate_pass = computed_file_sha256 == expected_replay_hash;

    println!("{{");
    println!("  \"implementation_name\": \"rust_preimage_byte_gate\",");
    println!("  \"implementation_version\": \"0.1\",");
    println!("  \"language\": \"rust\",");
    println!("  \"source_preimage_file\": \"{}\",", path);
    println!("  \"ipfs_cid\": \"{}\",", ipfs_cid);
    println!("  \"expected_replay_hash_from_committed_metadata\": \"{}\",", expected_replay_hash);
    println!("  \"declared_candidate_file_sha256\": \"{}\",", declared_candidate_file_sha256);
    println!("  \"computed_file_sha256\": \"{}\",", computed_file_sha256);
    println!("  \"file_bytes_match_declared_candidate\": {},", if file_bytes_match_declared_candidate { "true" } else { "false" });
    println!("  \"replay_gate_pass\": {},", if replay_gate_pass { "true" } else { "false" });
    println!("  \"full_replay_hash_recomputation_proven\": {},", if replay_gate_pass { "true" } else { "false" });
    println!("  \"audit_note\": \"If replay_gate_pass is false, the committed file is not the exact replay preimage bytes for the expected replay digest.\"");
    println!("}}");

    if replay_gate_pass { exit(0); } else { exit(1); }
}
