const ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
const BASE = 58n;

class DidKeyError extends Error {
  constructor(message) {
    super(message);
    this.name = 'DidKeyError';
  }
}

function base58Decode(value) {
  if (typeof value !== 'string' || value.length === 0) {
    throw new DidKeyError('invalid base58btc payload');
  }

  let num = 0n;
  for (const char of value) {
    const index = ALPHABET.indexOf(char);
    if (index === -1) {
      throw new DidKeyError('invalid base58btc payload');
    }
    num = num * BASE + BigInt(index);
  }

  const bytes = [];
  while (num > 0n) {
    bytes.push(Number(num % 256n));
    num = num / 256n;
  }
  bytes.reverse();

  for (const char of value) {
    if (char === '1') {
      bytes.unshift(0);
    } else {
      break;
    }
  }

  return Buffer.from(bytes);
}

function decodeDidKey(did) {
  const prefix = 'did:key:z';

  if (typeof did !== 'string') {
    throw new DidKeyError('did must be a string');
  }

  if (!did.startsWith(prefix)) {
    throw new DidKeyError('invalid did:key prefix');
  }

  const payload = did.slice(prefix.length);
  if (!payload) {
    throw new DidKeyError('missing base58btc payload');
  }

  const data = base58Decode(payload);

  if (data.length !== 34) {
    throw new DidKeyError('invalid multicodec length');
  }

  if (data[0] !== 0xed || data[1] !== 0x01) {
    throw new DidKeyError('invalid multicodec prefix');
  }

  const raw32 = data.slice(2);
  if (raw32.length !== 32) {
    throw new DidKeyError('invalid key length');
  }

  return raw32;
}

module.exports = { decodeDidKey, DidKeyError, base58Decode };
