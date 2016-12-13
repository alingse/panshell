# coding=utf-8
# author@alingse
# 2016.12.08

from copy import deepcopy

maxDigits = 131
biRadixBase = 2
biRadixBits = 16
bitsPerDigit = biRadixBits
biRadix = 2**16
biHalfRadix = 2**15
biRadixSquared = biRadix * biRadix
maxDigitVal = biRadix - 1
lowBitMasks = [0, 1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535]
highBitMasks = [0, 32768, 49152, 57344, 61440, 63488, 64512, 65024, 65280, 65408, 65472, 65504, 65520, 65528, 65532, 65534, 65535]
hexToChar = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
hexatrigesimalToChar = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
charToHex = dict(zip(hexatrigesimalToChar, range(len(hexatrigesimalToChar))))
hex4 = lambda d: hex(d)[2:].zfill(4)


class BigInt(object):

    def __init__(self):
        self.length = maxDigits
        self.digits = [0 for i in range(maxDigits)]
        self.isNeg = False

    @classmethod
    def bigZero(cls):
        b = BigInt()
        return b

    @classmethod
    def bigOne(cls):
        b = BigInt()
        b.digits[0] = 1
        return b

    @classmethod
    def from_hex(cls, hexs):
        b = BigInt()
        length = len(hexs)
        n = (length - 1)/4 + 1
        for i in range(n):
            p = length - 4 * i
            char4 = hexs[max(0, p - 4): p]
            b.digits[i] = int(char4, 16)
        return b

    @classmethod
    def from_string(cls, string, radix):
        m = BigInt()

        isNeg = bool(string[0] == '-')
        start = 1 if isNeg else 0

        b = BigInt.bigOne()

        for d in reversed(range(start, len(string))):
            g = charToHex[string[d].lower()]
            h = biMultiplyDigit(b, g)
            m = m + h
            b = biMultiplyDigit(b, radix)

        m.isNeg = isNeg
        return m

    @property
    def high_index(self):
        for i in reversed(range(self.length)):
            if self.digits[i] != 0:
                break
        return i

    def to_hex(self):
        digits = self.digits[:self.high_index + 1]
        hexs = map(hex4, reversed(digits))
        return ''.join(hexs)

    def to_string(self, n):
        c = BigInt()
        c.digits[0] = n

        o, m = biDivideModulo(self, c)
        a = hexatrigesimalToChar[m.digits[0]]

        while o > BigInt.bigZero():
            o, m = biDivideModulo(o, c)
            a += hexatrigesimalToChar[m.digits[0]]

        a = a[::-1]
        if self.isNeg:
            a = "-" + a
        return a

    def num_bits(self):
        index = self.high_index
        num = index * bitsPerDigit + bitsPerDigit

        e = self.digits[index]
        for i in range(bitsPerDigit):
            if (e & 32768) != 0:
                break
            e = e << 1
        return num - i

    def __cmp__(self, b):
        if self.isNeg != b.isNeg:
            if self.isNeg:
                return -1
            return 1

        for i in reversed(range(self.length)):
            if self.digits[i] > b.digits[i]:
                if self.isNeg:
                    return -1
                return 1
            if self.digits[i] < b.digits[i]:
                if self.isNeg:
                    return 1
                return -1
        return 0

    def __add__(self, b):

        if self.isNeg != b.isNeg:
            b2 = deepcopy(b)
            b2.isNeg = not b.isNeg
            a = self - b2
            return a
        else:
            a = BigInt()
            f = 0
            for i in range(self.length):
                e = self.digits[i] + b.digits[i] + f
                a.digits[i] = e & 65535
                f = 1 if e >= biRadix else 0

            a.isNeg = self.isNeg
            return a

    def __sub__(self, b):

        if self.isNeg != b.isNeg:
            b2 = deepcopy(b)
            b2.isNeg = not b.isNeg
            a = self + b2
            return a
        else:
            a = BigInt()
            e = 0

            for i in range(self.length):
                f = self.digits[i] - b.digits[i] + e
                a.digits[i] = f & 65535
                if a.digits[i] < 0:
                    a.digits[i] += biRadix
                e = -1 if f < 0 else 0

            if e == -1:
                e = 0
                for i in range(self.length):
                    f = 0 - a.digits[i] + e
                    a.digits[i] = f & 65535
                    if a.digits[i] < 0:
                        a.digits[i] += biRadix

                    e = -1 if f < 0 else 0

                a.isNeg = not self.isNeg
            else:
                a.isNeg = self.isNeg

            return a

    def shiftleft(self, n):
        q, r = divmod(n, bitsPerDigit)
        d = bitsPerDigit - r

        a = BigInt()
        a.digits[q:] = self.digits[0:a.length - q]

        for i in reversed(range(1, a.length)):
            t1 = (a.digits[i] << r) & maxDigitVal
            t2 = (a.digits[i-1] & highBitMasks[r]) >> d
            a.digits[i] = t1 | t2

        a.digits[0] = ((a.digits[1] << r) & maxDigitVal)
        a.isNeg = self.isNeg
        return a

    def shiftright(self, h):
        q, r = divmod(h, bitsPerDigit)
        d = bitsPerDigit - r

        a = BigInt()
        a.digits[q:] = self.digits[0:self.length - q]

        for i in range(self.length - 1):
            t1 = (a.digits[i] >> r)
            t2 = ((a.digits[i + 1] & lowBitMasks[r]) << d)
            a.digits[i] = t1 | t2

        a.digits[a.length - 1] = a.digits[a.length - 1] >> r
        a.isNeg = self.isNeg
        return a


def biMultiplyByRadixPower(b, c):
    a = BigInt()
    a.digits[c:] = b.digits[0:a.length - c]
    return a


def biDivideByRadixPower(b, c):
    a = BigInt()
    a.digits[0: a.length - c] = b.digits[c:]
    return a


def biModuloByRadixPower(b, c):
    a = BigInt()
    a.digits[:c] = b.digits[:c]
    return a


def biMultiply(h, g):
    o = BigInt()

    b = h.high_index
    m = g.high_index

    for i in range(m + 1):
        f = 0

        for j in range(b + 1):
            a = o.digits[i + j] + h.digits[j] * g.digits[i] + f
            o.digits[i + j] = a & maxDigitVal
            f = a >> biRadixBits

        o.digits[i + b + 1] = f

    o.isNeg = h.isNeg != g.isNeg
    return o


def biMultiplyDigit(a, g):
    result = BigInt()

    f = a.high_index
    e = 0
    for b in range(f + 1):
        d = result.digits[b] + a.digits[b] * g + e
        result.digits[b] = d & maxDigitVal
        e = d >> biRadixBits

    result.digits[f + 1] = e
    return result


def biDivideModulo(g, f):
    a = g.num_bits()
    e = f.num_bits()
    d = f.isNeg

    if a < e:
        if g.isNeg:
            o = BigInt.bigOne()
            o.isNeg = not f.isNeg
            g.isNeg = False
            f.isNeg = False
            m = f - g
            g.isNeg = True
            f.isNeg = d
        else:
            o = BigInt()
            m = deepcopy(g)
        return [o, m]

    o = BigInt()
    m = g

    k = (e - 1) / bitsPerDigit

    h = 0
    while f.digits[k] < biHalfRadix:
        f = f.shiftleft(1)
        h += 1
        e += 1

        k = (e + 1) / bitsPerDigit

    m = m.shiftleft(h)
    a += h

    u = (a + 1) / bitsPerDigit

    B = biMultiplyByRadixPower(f, u - k)

    while m >= B:
        o.digits[u - k] += 1
        m = m - B

    for z in range(u, k, -1):
        l = 0 if z >= m.length else m.digits[z]
        A = 0 if z - 1 >= m.length else m.digits[z - 1]
        w = 0 if z - 2 >= m.length else m.digits[z - 2]
        v = 0 if k >= f.length else f.digits[k]
        c = 0 if k - 1 >= f.length else f.digits[k - 1]

        if l == v:
            o.digits[z - k - 1] = maxDigitVal
        else:
            o.digits[z - k - 1] = (l * biRadix + A) / v

        s = o.digits[z - k - 1] * ((v * biRadix) + c)
        p = (l * biRadixSquared) + ((A * biRadix) + w)

        while s > p:
            o.digits[z - k - 1] -= 1
            s = o.digits[z - k - 1] * ((v * biRadix) | c)
            p = (l * biRadix * biRadix) + ((A * biRadix) + w)

        B = biMultiplyByRadixPower(f, z - k - 1)
        m = m - biMultiplyDigit(B, o.digits[z - k - 1])
        if m.isNeg:
            m = m + B
            o.digits[z - k - 1] -= 1

    m = m.shiftright(h)
    o.isNeg = bool(g.isNeg != d)
    if g.isNeg:
        if d:
            o += BigInt.bigOne()
        else:
            o -= BigInt.bigOne()

        f = f.shiftright(h)
        m = f - m

    if m.digits[0] == 0 and m.high_index == 0:
        m.isNeg = False

    return [o, m]


def biDivide(a, b):
    o, m = biDivideModulo(a, b)
    return o


class BarrettMu(object):

    def __init__(self, a):
        self.modulus = deepcopy(a)
        self.k = self.modulus.high_index + 1

        b = BigInt()
        b.digits[2 * self.k] = 1
        self.mu = biDivide(b, self.modulus)
        self.bkplus1 = BigInt()
        self.bkplus1.digits[self.k + 1] = 1
        self.modulo = self.BarrettMu_modulo
        self.multiplyMod = self.BarrettMu_multiplyMod
        self.powMod = self.BarrettMu_powMod

    def BarrettMu_modulo(self, h):
        g = biDivideByRadixPower(h, self.k - 1)
        e = biMultiply(g, self.mu)
        d = biDivideByRadixPower(e, self.k + 1)
        k = biMultiply(d, self.modulus)
        b = biModuloByRadixPower(k, self.k + 1)

        c = biModuloByRadixPower(h, self.k + 1)

        a = c - b
        if a.isNeg:
            a += self.bkplus1

        while a >= self.modulus:
            a = a - self.modulus

        return a

    def BarrettMu_multiplyMod(self, a, c):
        b = biMultiply(a, c)
        return self.modulo(b)

    def BarrettMu_powMod(self, c, f):
        b = BigInt()
        b.digits[0] = 1
        d = c
        e = f

        while True:
            if (e.digits[0] & 1) != 0:
                b = self.multiplyMod(b, d)

            e = e.shiftright(1)
            if e.digits[0] == 0 and e.high_index == 0:
                break
            d = self.multiplyMod(d, d)
        return b


class RSAKeyPair(object):

    def __init__(self, e, d, public_key):
        self.e = BigInt.from_hex(e)
        self.d = BigInt.from_hex(d)
        self.public_key = BigInt.from_hex(public_key)

        self.chunkSize = 2 * self.public_key.high_index
        self.radix = 16
        self.barrett = BarrettMu(self.public_key)

    def encrypt(self, string):
        h = map(ord, string)
        q, r = divmod(len(h), self.chunkSize)
        if r > 0:
            h += [0]*(self.chunkSize - r)
            q += 1

        chars = []
        for i in range(q):
            c = BigInt()

            d = i * self.chunkSize
            for e in range(self.chunkSize/2):
                c.digits[e] = h[d + 2 * e]
                c.digits[e] += h[d + 2 * e + 1] << 8
            b = self.barrett.powMod(c, self.e)
            if self.radix == 16:
                m = b.to_hex()
            else:
                m = b.to_string()
            chars.append(m)
        enc = ' '.join(chars)
        return enc

    def decrypt(self, enc):
        chars = enc.split(" ")
        a = ""
        for char in chars:
            if self.radix == 16:
                c = BigInt.from_hex(char)
            else:
                c = BigInt.from_string(char, self.radix)

            b = self.barrett.powMod(c, self.radix)
            for i in range(b.high_index + 1):
                a += chr(b.digits[i] & 255)
                a += chr(b.digits[i] >> 8)

        if ord(a[-1]) == 0:
            a = a[: -1]
        return a


if __name__ == '__main__':
    e = '10001'
    d = ''
    public_key = 'B3C61EBBA4659C4CE3639287EE871F1F48F7930EA977991C7AFE3CC442FEA49643212E7D570C853F368065CC57A2014666DA8AE7D493FD47D171C0D894EEE3ED7F99F6798B7FFD7B5873227038AD23E3197631A8CB642213B9F27D4901AB0D92BFA27542AE890855396ED92775255C977F5C302F1E7ED4B1E369C12CB6B1822F'

    rsa_pair = RSAKeyPair(e, d, public_key)
    password = '1234567'
    s = rsa_pair.encrypt(password)
    print(s)
