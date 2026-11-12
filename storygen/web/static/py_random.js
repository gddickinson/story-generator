// CPython's random.Random (MT19937, seeded from an int via init_by_array) ported to JS: random() and choice() with
// CPython's exact algorithms, so a seed picks the same templates, places and moods as the Python generator.
// Adapted from the evolutionart-art-system web port; checked by story_engine.test.mjs.

const N = 624;
const mul = (a, b) => Math.imul(a, b) >>> 0;

class MT19937 {
  constructor() { this.mt = new Uint32Array(N); this.mti = N + 1; }
  initGenrand(s) {
    const mt = this.mt;
    mt[0] = s >>> 0;
    for (let i = 1; i < N; i++) mt[i] = (mul(1812433253, mt[i - 1] ^ (mt[i - 1] >>> 30)) + i) >>> 0;
    this.mti = N;
  }
  initByArray(key) {
    const mt = this.mt;
    this.initGenrand(19650218);
    let i = 1, j = 0;
    for (let k = Math.max(N, key.length); k; k--) {
      mt[i] = ((mt[i] ^ mul(mt[i - 1] ^ (mt[i - 1] >>> 30), 1664525)) + key[j] + j) >>> 0;
      i++; j++;
      if (i >= N) { mt[0] = mt[N - 1]; i = 1; }
      if (j >= key.length) j = 0;
    }
    for (let k = N - 1; k; k--) {
      mt[i] = ((mt[i] ^ mul(mt[i - 1] ^ (mt[i - 1] >>> 30), 1566083941)) - i) >>> 0;
      i++;
      if (i >= N) { mt[0] = mt[N - 1]; i = 1; }
    }
    mt[0] = 0x80000000;
  }
  uint32() {
    const mt = this.mt;
    if (this.mti >= N) {
      for (let kk = 0; kk < N; kk++) {
        const y = (mt[kk] & 0x80000000) | (mt[(kk + 1) % N] & 0x7fffffff);
        mt[kk] = mt[(kk + 397) % N] ^ (y >>> 1) ^ (y & 1 ? 0x9908b0df : 0);
      }
      this.mti = 0;
    }
    let y = mt[this.mti++];
    y ^= y >>> 11; y ^= (y << 7) & 0x9d2c5680; y ^= (y << 15) & 0xefc60000; y ^= y >>> 18;
    return y >>> 0;
  }
  res53() { const a = this.uint32() >>> 5, b = this.uint32() >>> 6; return (a * 67108864.0 + b) * (1.0 / 9007199254740992.0); }
}

export class PyRandom {
  constructor(seed = 0) { this.gen = new MT19937(); this.seed(seed); }
  seed(n) {
    const key = []; let s = Math.abs(Math.trunc(n));
    do { key.push(s % 4294967296 >>> 0); s = Math.floor(s / 4294967296); } while (s > 0);
    this.gen.initByArray(key);
  }
  random() { return this.gen.res53(); }
  getrandbits(k) { return k <= 0 ? 0 : this.gen.uint32() >>> (32 - k); }   // k <= 32 covers every list here
  randbelow(n) {
    const k = 32 - Math.clz32(n);                                              // n.bit_length()
    let r = this.getrandbits(k);
    while (r >= n) r = this.getrandbits(k);
    return r;
  }
  choice(seq) {
    if (!seq.length) throw new Error('Cannot choose from an empty sequence');
    return seq[this.randbelow(seq.length)];
  }
}
