import json, hashlib
from pathlib import Path

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))

def sha3_obj(obj):
    return "sha3-256:" + hashlib.sha3_256(canonical(obj).encode()).hexdigest()

class AppendOnlyOverrideLog:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
    def append(self, record):
        record = dict(record)
        record["runtime_delta_hash"] = sha3_obj(record.get("policy_delta", {}))
        self.path.write_text(self.path.read_text() + canonical(record) + "\n")
        return record
    def all(self):
        return [json.loads(line) for line in self.path.read_text().splitlines() if line.strip()]
