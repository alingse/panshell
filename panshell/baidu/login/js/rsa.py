# coding=utf-8
# author@alingse
# 2016.12.08

from __future__ import print_function
from copy import deepcopy
import math

maxDigits = 131
ZERO_ARRAY = [0 for i in range(maxDigits)]

biRadixBase = 2
biRadixBits = 16
bitsPerDigit = biRadixBits
biRadix = 2**16
biHalfRadix = 2**15
biRadixSquared = biRadix * biRadix
maxDigitVal = biRadix - 1
maxInteger = 9999999999999998
lowBitMasks = [0, 1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535]
highBitMasks = [0, 32768, 49152, 57344, 61440, 63488, 64512, 65024, 65280, 65408, 65472, 65504, 65520, 65528, 65532, 65534, 65535]
hexToChar = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
hexatrigesimalToChar = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
chunksf = lambda data,n: [data[i:i+n] for i in range(0, len(data), n)]
reverse = lambda x: x[::-1]

class F(object):
    pass
console = F()
console.log = print

class BigInt(object):

    def __init__(self):
        self.digits = deepcopy(ZERO_ARRAY)
        self.isNeg = False

    def set_hex(self):
        pass


def biFromHex(hexs):
    b = BigInt()

    hexs = reverse(hexs)
    chunks = chunksf(hexs, 4)
    chunks = map(reverse, chunks)

    for i in range(len(chunks)):
        chunk = chunks[i]
        b.digits[i] = int(chunk, 16)

    return b


def biHighIndex(b):
    a = len(b.digits) - 1
    while a >0 and b.digits[a] ==0:
        a -= 1
    return a


def digitToHex(c):
    b = 15
    a = ''

    for i in range(4):
        a += hexToChar[c & b]
        c = c >> 4    

    return reverse(a)


def biToHex(b):
    a = ''
    d = biHighIndex(b)
    for i in range(d + 1):
        c = d - i
        a += digitToHex(b.digits[c])
    return a


def biToString(d, f):
    c = BigInt()
    c.digits[0] = f

    e = biDivideModulo(d, c)
    a = hexatrigesimalToChar[e[1].digits[0]]

    while biCompare(e[0], bigZero) == 1:
        e = biDivideModulo(e[0], c)
        a += hexatrigesimalToChar[e[1].digits[0]]

    a = reverse(a)
    if d.isNeg:
        a = "-" + a

    return a


def biNumBits(c):
    f = biHighIndex(c)
    e = c.digits[f]
    b = (f + 1) * bitsPerDigit

    for i in range(bitsPerDigit):
        if (e & 32768) != 0:
            break
        e = e * 2
    return b - i


def biCompare(a, c):
    if a.isNeg != c.isNeg:
        return -1 if a.isNeg else 1

    for i in range(len(a.digits)):
        b = len(a.digits) - i - 1

        if a.digits[b] != c.digits[b]:
            if a.isNeg:
                return -1 if a.digits[b] > c.digits[b] else 1
            else:
                return -1 if a.digits[b] < c.digits[b] else 1

    return 0


def biAdd(b, g):
    if b.isNeg != g.isNeg:
        g.isNeg = not g.isNeg
        a = biSubtract(b, g)
        g.isNeg = not g.isNeg
        return a
    else:
        a = BigInt()
        f = 0
        for i in range(len(b.digits)):
            e = b.digits[i] + g.digits[i] + f
            a.digits[i] = e & 65535
            f = 1 if e >= biRadix else 0

        a.isNeg = b.isNeg
        return a


def biSubtract(b, g):
    if b.isNeg != g.isNeg:
        g.isNeg = not g.isNeg
        a = biAdd(b, g)
        g.isNeg = not g.isNeg
        return a
    else:
        a = BigInt()
        e = 0

        for i in range(len(b.digits)):
            f = b.digits[i] - g.digits[i] + e            
            a.digits[i] = f & 65535
            if a.digits[i] < 0:
                a.digits[i] += biRadix
            e = -1 if f < 0 else 0

        if e == -1:
            e = 0
            for i in range(len(b.digits)):
                f = 0 - a.digits[i] + e
                a.digits[i] = f & 65535
                if a.digits[i] < 0:
                    a.digits[i] += biRadix

                e = -1 if f < 0 else 0

            a.isNeg = not b.isNeg
        else:
            a.isNeg = b.isNeg

        return a


def arrayCopy(e, h, c, g, f):
    a = min(h + f, len(e))

    for i in range(h, a):
        c[g + i] = e[h + i]


def biShiftLeft(b, h):
    d = math.floor(1.0* h / bitsPerDigit)
    d = int(d)

    a = BigInt()

    arrayCopy(b.digits, 0, a.digits, d, len(a.digits) - d)
    # a.digits[d:] = b.digits[0 : len(a.digits) - d]
    g = h % bitsPerDigit
    c = bitsPerDigit - g

    e = len(a.digits) - 1
    f = e -1
    for i in range(e, 0, -1):
        a.digits[i] = ((a.digits[i] << g) & maxDigitVal) | ((a.digits[i-1] & highBitMasks[g]) >> c)

    a.digits[0] = ((a.digits[i] << g) & maxDigitVal)
    a.isNeg = b.isNeg
    return a


def biShiftRight(b, h):
    c = math.floor(1.0 * h / bitsPerDigit)
    c = int(c)

    a = BigInt()
    arrayCopy(b.digits, c, a.digits, 0, len(b.digits) - c)
    # a.digits[c:] = b.digits[0 : len(b.digits) - c]

    f = h % bitsPerDigit
    g = bitsPerDigit - f

    for i in range(len(a.digits) - 1):
        a.digits[i] = (a.digits[i] >> f) | ((a.digits[i + 1] & lowBitMasks[f]) << g)

    a.digits[len(a.digits) - 1] =  a.digits[len(a.digits) - 1] >> f    
    a.isNeg = b.isNeg;
    return a


def biMultiplyByRadixPower(b, c):
    a = BigInt()
    arrayCopy(b.digits, 0, a.digits, c, len(a.digits) - c)
    # a.digits[c:] = b.digits[0 : len(a.digits) - c]
    return a


def biDivideByRadixPower(b, c):
    a = BigInt()
    # arrayCopy(b.digits, c, a.digits, 0, len(a.digits) - c)
    a.digits[0: len(a.digits) - c] = b.digits[c:]
    return a


def biModuloByRadixPower(b, c):
    a = BigInt()
    arrayCopy(b.digits, 0, a.digits, 0, c)
    return a


def biMultiply(h, g):
    o = BigInt()
    
    b = biHighIndex(h)
    m = biHighIndex(g)

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

    f = biHighIndex(a)
    e = 0
    for b in range(f + 1):
        d = result.digits[b] + a.digits[b] *g + e
        result.digits[b] = d & maxDigitVal
        e = d >> biRadixBits

    result.digits[f + 1] =  e
    return result


def biDivideModulo(g, f):
    a = biNumBits(g)
    e = biNumBits(f)
    d = f.isNeg

    if a < e:
        if g.isNeg:
            o = deepcopy(bigOne)
            o.isNeg = not f.isNeg
            g.isNeg = False
            f.isNeg = False
            m = biSubtract(f, g)
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
        f = biShiftLeft(f, 1)
        h += 1
        e += 1

        k = math.ceil(e * 1.0 / bitsPerDigit) - 1
        k = int(k)

    m = biShiftLeft(m, h)    
    a += h

    u = math.ceil(a * 1.0 / bitsPerDigit) - 1
    u = int(u)

    B = biMultiplyByRadixPower(f, u - k)

    while biCompare(m, B) != -1:
        o.digits[u - k] += 1
        m = biSubtract(m, B)

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
        tttt = biMultiplyDigit(B, o.digits[z - k - 1])
        m = biSubtract(m, tttt)
        if m.isNeg:
            m = biAdd(m, B)
            o.digits[z - k - 1] -= 1



    m = biShiftRight(m, h)
    o.isNeg = bool(g.isNeg != d)    
    if g.isNeg:
        if d:
            o = biAdd(o, bigOne)
        else:
            o = biSubtract(o, bigOne)
        f = biShiftRight(f, h)
        m = biSubtract(f, m)

    if m.digits[0] == 0 and biHighIndex(m) == 0:
        m.isNeg = False

    return [o, m]


def biDivide(a, b):
    o, m = biDivideModulo(a, b)
    return o


class BarrettMu(object):

    def __init__(self, a):
        self.modulus = deepcopy(a)
        self.k = biHighIndex(self.modulus) + 1

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

        a = biSubtract(c, b)        
        if a.isNeg:
            a = biAdd(a, self.bkplus1)

        f = biCompare(a, self.modulus) >= 0
        while f:
            a = biSubtract(a, self.modulus)
            biCompare(a, self.modulus) >= 0

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

            e = biShiftRight(e, 1)
            console.log(e.digits[0],biHighIndex(e))
            if e.digits[0] == 0 and biHighIndex(e) == 0:
                break
            d = self.multiplyMod(d, d)
        return b


class RSAKeyPair(object):

    def __init__(self, b, c, public_key):
        self.e = biFromHex(b);
        self.d = biFromHex(c);
        self.m = biFromHex(public_key);

        self.chunkSize = 2 * biHighIndex(self.m)
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
        m = biToHex(n) if l.radix  == 16 else biToString(n, l.radix)
        p += m + " "

    p = p[:-1]
    return p



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
    # console.log(p.barrett.bkplus1.digits)
    # console.log(p.barrett.mu.digits)
    password = '0'
    s = encryptedString(p, password)
    print(s)
