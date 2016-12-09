# coding=utf-8
# author@alingse
# 2016.12.08

from __future__ import print_function
from copy import deepcopy
import math

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
chunksf = lambda data, n: [data[i:i+n] for i in range(0, len(data), n)]
reverse = lambda x: x[::-1]
hex4 = lambda d: hex(d)[2:].zfill(4)


class BigInt(object):

    def __init__(self):
        self.length = maxDigits
        self.digits = [0 for i in range(maxDigits)]
        self.isNeg = False

    @classmethod
    def from_hex(cls, hexs):
        b = cls()

        hexs = reverse(hexs)
        chunks = chunksf(hexs, 4)
        chunks = map(reverse, chunks)
        for i in range(len(chunks)):
            b.digits[i] = int(chunks[i], 16)
        return b

    @property
    def high_index(self):
        for i in range(len(self.digits) -1, -1, -1):
            if self.digits[i] != 0:
                break
        return i

    def to_hex(self):
        digits = self.digits[:self.high_index + 1]
        digits = reverse(digits)
        hexs = map(hex4, digits)
        return ''.join(hexs)

    def to_string(self, n):
        c = BigInt()
        c.digits[0] = n

        o, m = biDivideModulo(self, c)
        a = hexatrigesimalToChar[m.digits[0]]

        while o > bigZero:
            o, m = biDivideModulo(o, c)
            a += hexatrigesimalToChar[m.digits[0]]

        a = reverse(a)
        if self.isNeg:
            a = "-" + a
        return a

    def num_bits(self):
        f = self.high_index
        e = self.digits[f]
        b = (f + 1) * bitsPerDigit
        for i in range(bitsPerDigit):
            if (e & 32768) != 0:
                break
            e = e * 2
        return b - i

    def __cmp__(self, c):
        if self.isNeg != c.isNeg:
            if self.isNeg:
                return -1
            return 1

        for b in reversed(range(self.length)):
            if self.digits[b] > c.digits[b]:
                if self.isNeg:
                    return -1
                return 1
            if self.digits[b] < c.digits[b]:
                if self.isNeg:
                    return 1
                return -1
        return 0

    def __add__(self, g):

        if self.isNeg != g.isNeg:
            g.isNeg = not g.isNeg
            a = self - g
            g.isNeg = not g.isNeg
            return a
        else:
            a = BigInt()
            f = 0
            for i in range(len(self.digits)):
                e = self.digits[i] + g.digits[i] + f
                a.digits[i] = e & 65535
                f = 1 if e >= biRadix else 0

            a.isNeg = self.isNeg
            return a

    def __sub__(self, g):

        if self.isNeg != g.isNeg:
            g.isNeg = not g.isNeg
            a = self + g
            g.isNeg = not g.isNeg
            return a
        else:
            a = BigInt()
            e = 0

            for i in range(len(self.digits)):
                f = self.digits[i] - g.digits[i] + e            
                a.digits[i] = f & 65535
                if a.digits[i] < 0:
                    a.digits[i] += biRadix
                e = -1 if f < 0 else 0

            if e == -1:
                e = 0
                for i in range(len(self.digits)):
                    f = 0 - a.digits[i] + e
                    a.digits[i] = f & 65535
                    if a.digits[i] < 0:
                        a.digits[i] += biRadix

                    e = -1 if f < 0 else 0

                a.isNeg = not self.isNeg
            else:
                a.isNeg = self.isNeg

            return a

    def shiftleft(self, h):
        d = math.floor(1.0 * h / bitsPerDigit)
        d = int(d)

        g = h % bitsPerDigit
        c = bitsPerDigit - g

        a = BigInt()

        a.digits[d:] = self.digits[0 : len(a.digits) - d]

        for i in range(len(a.digits) - 1, 0, -1):
            t1 = (a.digits[i] << g) & maxDigitVal
            t2 = (a.digits[i-1] & highBitMasks[g]) >> c
            a.digits[i] =  t1 | t2 

        a.digits[0] = ((a.digits[1] << g) & maxDigitVal)
        a.isNeg = self.isNeg
        return a

    def shiftright(self, h):
        d = math.floor(1.0 * h / bitsPerDigit)
        d = int(d)

        f = h % bitsPerDigit
        g = bitsPerDigit - f

        a = BigInt()
        a.digits[d:] = self.digits[0 : len(self.digits) - d]


        for i in range(len(a.digits) - 1):
            t1 = (a.digits[i] >> f)
            t2 = ((a.digits[i + 1] & lowBitMasks[f]) << g)
            a.digits[i] = t1 | t2

        a.digits[len(a.digits) - 1] =  a.digits[len(a.digits) - 1] >> f
        a.isNeg = self.isNeg;
        return a        


def biMultiplyByRadixPower(b, c):
    a = BigInt()
    a.digits[c:] = b.digits[0 : len(a.digits) - c]
    return a


def biDivideByRadixPower(b, c):
    a = BigInt()
    a.digits[0: len(a.digits) - c] = b.digits[c:]
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
            o.digits[i + j] = a &  maxDigitVal
            f =  a >> biRadixBits

        o.digits[i + b + 1] = f

    o.isNeg = h.isNeg != g.isNeg
    return o


def biMultiplyDigit(a, g):
    result = BigInt()

    f = a.high_index
    e = 0
    for b in range(f + 1):
        d = result.digits[b] + a.digits[b] *g + e
        result.digits[b] = d & maxDigitVal
        e = d >> biRadixBits

    result.digits[f + 1] =  e
    return result


def biDivideModulo(g, f):
    a = g.num_bits()
    e = f.num_bits()
    d = f.isNeg

    if a < e:
        if g.isNeg:
            o = deepcopy(bigOne)
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

    k = math.ceil(e * 1.0 / bitsPerDigit) - 1
    k = int(k)

    h = 0
    while f.digits[k] < biHalfRadix:
        f = f.shiftleft(1)
        h += 1
        e += 1

        k = math.ceil(e * 1.0 / bitsPerDigit) - 1
        k = int(k)

    m = m.shiftleft(h)
    a += h

    u = math.ceil(a * 1.0 / bitsPerDigit) - 1
    u = int(u)

    B = biMultiplyByRadixPower(f, u - k)

    while m >= B:
        o.digits[u - k] += 1
        m = m - B

    for z in range(u, k, -1):
        l = 0 if z >= len(m.digits) else m.digits[z]
        A = 0 if z - 1 >= len(m.digits) else m.digits[z - 1]
        w = 0 if z - 2 >= len(m.digits) else m.digits[z - 2]
        v = 0 if k >= len(f.digits) else f.digits[k]
        c = 0 if k - 1 >= len(f.digits) else f.digits[k - 1]

        if l == v:
            o.digits[z - k - 1] = maxDigitVal
        else:
            o.digits[z - k - 1] = int(math.floor((1.0 * l * biRadix + A) / v))

        s = o.digits[z - k - 1] *  ((v * biRadix) + c)
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
            o += bigOne
        else:
            o -= bigOne

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

    def __init__(self, b, c, public_key):
        self.e = BigInt.from_hex(b)
        self.d = BigInt.from_hex(c)
        self.m = BigInt.from_hex(public_key)

        self.chunkSize = 2 * self.m.high_index
        self.radix = 16
        self.barrett = BarrettMu(self.m)


def encryptedString(l, o):
    h = []
    b = len(o)

    for f in range(b):
        h.append(ord(o[f]))
    # h = map(ord, o)

    while len(h) % l.chunkSize != 0:
        h.append(0)

    g = len(h)
    p = ""
    for f in range(0, g, l.chunkSize):
        c = BigInt()

        d = f
        for e in range(0, l.chunkSize, 2):
            c.digits[e] = h[d]
            c.digits[e] += h[d + 1] << 8
            d += 2
        n = l.barrett.powMod(c, l.e)
        m = n.to_hex() if l.radix  == 16 else n.to_string(l.radix)
        p += m + " "

    p = p[:-1]
    return p


def decryptedString(e, f):
    h = f.split(" ")
    a = ""
    for i in range(len(h)):
        if e.radix == 16:
            b = BigInt.from_hex(h[i])
        else:
            b = biFromString(h[i], e.radix)

        g = e.barrett.powMod(b, e.radix)

        for j in range(biHighIndex(g) + 1):
            a += chr(g.digits[j]&255)
            a += chr(g.digits[j]>>8)

    if ord(a[len(a) - 1]) == 0:
        a = a[:len(a) - 1]

    return a



if __name__ == '__main__':
    b = '10001'
    c = ''
    public_key = 'B3C61EBBA4659C4CE3639287EE871F1F48F7930EA977991C7AFE3CC442FEA49643212E7D570C853F368065CC57A2014666DA8AE7D493FD47D171C0D894EEE3ED7F99F6798B7FFD7B5873227038AD23E3197631A8CB642213B9F27D4901AB0D92BFA27542AE890855396ED92775255C977F5C302F1E7ED4B1E369C12CB6B1822F'

    p = RSAKeyPair(b, c, public_key)
    # print(p.e.digits)
    # print(p.d.digits)
    # print(p.m.digits)
    # print(p.chunkSize)
    # print(p.barrett.k)
    # print(p.barrett.modulus.digits)
    # print(p.barrett.mu.digits)
    password = '0'
    s = encryptedString(p, password)
    print(s)
    # decryptedString(p, s)
