class MockNoirVerifier:
    def __init__(self, always_valid=True):
        self.always_valid = always_valid

    def verify(self, proof_bytes, public_inputs):
        return self.always_valid
