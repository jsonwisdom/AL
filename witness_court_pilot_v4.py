import hashlib
import json
import time
import sqlite3
import os
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
import uvicorn
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

DATA_DIR = os.getenv("DATA_DIR", "/tmp/witness-data")
KEY_PATH = f"{DATA_DIR}/witness_key.pem"
DB_PATH = f"{DATA_DIR}/court_witness.db"

class WitnessKeyManager:
    def __init__(self, name: str):
        self.name = name
        self.priv_key = None
        self.pub_key = None
        self._load_or_create_key()

    def _load_or_create_key(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if os.path.exists(KEY_PATH):
            with open(KEY_PATH, "rb") as f:
                pem = f.read()
            self.priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(pem)
        else:
            self.priv_key = ed25519.Ed25519PrivateKey.generate()
            pem = self.priv_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open(KEY_PATH, "wb") as f:
                f.write(pem)
        self.pub_key = self.priv_key.public_key()

    def sign(self, data: Dict) -> str:
        msg = json.dumps(data, sort_keys=True, default=str).encode()
        sig = self.priv_key.sign(msg)
        pub_bytes = self.pub_key.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
        return f"{sig.hex()}:{pub_bytes.hex()}:{int(time.time())}"

class MerkleTree:
    def __init__(self, leaves: List[bytes]):
        self.leaves = leaves
        self.tree = self._build(leaves)
        self.root = self.tree[-1][0] if self.tree and self.tree[-1] else b''

    def _build(self, leaves: List[bytes]) -> List[List[bytes]]:
        if not leaves: return []
        tree = [leaves[:]]
        while len(tree[-1]) > 1:
            level = tree[-1]
            new_level = []
            for i in range(0, len(level), 2):
                left = level[i]
                right = level[i+1] if i+1 < len(level) else left
                new_level.append(hashlib.sha256(left + right).digest())
            tree.append(new_level)
        return tree

    def get_proof(self, index: int) -> List[bytes]:
        if index < 0 or index >= len(self.leaves): raise IndexError("Invalid index")
        proof = []
        pos = index
        for level in self.tree[:-1]:
            sibling_pos = pos ^ 1
            sibling = level[sibling_pos] if sibling_pos < len(level) else level[pos]
            proof.append(sibling)
            pos //= 2
        return proof

    @staticmethod
    def verify_proof(leaf: bytes, proof: List[bytes], root: bytes, index: int) -> bool:
        current = leaf
        pos = index
        for sibling in proof:
            if pos % 2 == 0:
                current = hashlib.sha256(current + sibling).digest()
            else:
                current = hashlib.sha256(sibling + current).digest()
            pos //= 2
        return current == root

class WitnessLog:
    def __init__(self, name: str = "court-2026-001"):
        self.name = name
        self.log: List[Dict] = []
        self.key_manager = WitnessKeyManager(name)
        self._init_db()
        self._load_log()
        if not self.log:
            self._create_genesis()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''CREATE TABLE IF NOT EXISTS events (
            index_id INTEGER PRIMARY KEY, type TEXT, timestamp REAL,
            payload TEXT, metadata TEXT, prev_hash TEXT, hash TEXT UNIQUE)''')
        conn.commit()
        conn.close()

    def _load_log(self):
        conn = sqlite3.connect(DB_PATH)
        for row in conn.execute("SELECT * FROM events ORDER BY index_id"):
            self.log.append({
                "index": row[0], "type": row[1], "timestamp": row[2],
                "payload": json.loads(row[3]), "metadata": json.loads(row[4]),
                "prev_hash": row[5], "hash": row[6]
            })
        conn.close()

    def _save_event(self, event: Dict):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?)", (
            event["index"], event["type"], event["timestamp"],
            json.dumps(event["payload"], default=str),
            json.dumps(event["metadata"], default=str),
            event["prev_hash"], event["hash"]
        ))
        conn.commit()
        conn.close()

    def _create_genesis(self):
        genesis = {"index": 0, "type": "genesis", "timestamp": time.time(),
                   "payload": {"name": self.name, "version": "0.4"}, "metadata": {},
                   "prev_hash": "0"*64, "hash": hashlib.sha256(b"genesis").hexdigest()}
        self.log.append(genesis)
        self._save_event(genesis)

    def append(self, event_type: str, payload: Dict, metadata: Dict = None) -> Dict:
        prev_hash = self.log[-1]["hash"] if self.log else "0"*64
        event = {
            "index": len(self.log), "type": event_type, "timestamp": time.time(),
            "payload": payload, "metadata": metadata or {}, "prev_hash": prev_hash
        }
        event_str = json.dumps(event, sort_keys=True, default=str)
        event["hash"] = hashlib.sha256(event_str.encode()).hexdigest()
        self.log.append(event)
        self._save_event(event)
        return event

    def get_merkle_tree(self) -> MerkleTree:
        leaves = [bytes.fromhex(e["hash"]) for e in self.log]
        return MerkleTree(leaves)

    def get_inclusion_proof(self, index: int) -> Dict:
        event = self.log[index]
        mt = self.get_merkle_tree()
        proof = mt.get_proof(index)
        return {
            "log_name": self.name, "index": index, "event_hash": event["hash"],
            "merkle_root": mt.root.hex(), "proof": [p.hex() for p in proof]
        }

    def propose_signed_fork(self, parent_index: int, new_events: List[Dict], justification: str, proposer: str) -> Dict:
        if parent_index >= len(self.log):
            raise HTTPException(400, "Invalid parent index")
        fork_id = f"fork-{os.urandom(4).hex()}"
        fork_data = {"fork_id": fork_id, "parent_index": parent_index, "justification": justification, "proposer": proposer}
        signature = self.key_manager.sign(fork_data)
        return {"status": "proposed", "fork_id": fork_id, "signature": signature}

app = FastAPI(title="Witness v0.4 — Court Pilot", version="0.4")
court = WitnessLog()

if len(court.log) <= 1:
    court.append("case_filing", {"case_id": "2026-CR-001", "defendant": "John Doe"})
    court.append("evidence_intake", {"source": "bodycam-47-ferguson", "hash": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"})
    court.append("rule_application", {"rule": "Miranda", "outcome": "valid"})

@app.get("/summarize")
async def summarize():
    mt = court.get_merkle_tree()
    return {"name": court.name, "events": len(court.log), "merkle_root": mt.root.hex()}

@app.get("/replay")
async def replay():
    return court.log

@app.get("/proof/{index}")
async def proof(index: int):
    return court.get_inclusion_proof(index)

@app.post("/governance/fork")
async def fork(req: Dict):
    return court.propose_signed_fork(req["parent_index"], req.get("new_events", []), req["justification"], req.get("proposer", "clerk"))

@app.get("/convergence-receipt")
async def convergence_receipt():
    mt = court.get_merkle_tree()
    return {
        "log_name": court.name,
        "event_count": len(court.log),
        "merkle_root": mt.root.hex(),
        "timestamp": time.time(),
        "verification_instruction": "Any observer can recompute Merkle root from /replay and must match"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
