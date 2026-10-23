from qwen_replay.canonicalize import sha256_value


def test_qv_002_argument_canonicalization():
    a = {"city": "北京", "unit": "c"}
    b = {"unit": "c", "city": "北京"}
    assert sha256_value(a) == sha256_value(b)
