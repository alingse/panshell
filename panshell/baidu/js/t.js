//2016.06.22

var dpl10 = 15;
var lr10 = biFromNumber(1000000000000000);

function biFromDecimal(e) {
    var d = e.charAt(0) == "-";
    var c = d ? 1 : 0;
    var a;
    while (c < e.length && e.charAt(c) == "0") {
        ++c
    }
    if (c == e.length) {
        a = new BigInt()
    } else {
        var b = e.length - c;
        var f = b % dpl10;
        if (f == 0) {
            f = dpl10
        }
        a = biFromNumber(Number(e.substr(c, f)));
        c += f;
        while (c < e.length) {
            a = biAdd(biMultiply(a, lr10), biFromNumber(Number(e.substr(c, dpl10))));
            c += dpl10
        }
        a.isNeg = d
    }
    return a
}
function biFromNumber(c) {
    var a = new BigInt();
    a.isNeg = c < 0;
    c = Math.abs(c);
    var b = 0;
    while (c > 0) {
        a.digits[b++] = c & maxDigitVal;
        c >>= biRadixBits
    }
    return a
}
function biToDecimal(d) {
    var c = new BigInt();
    c.digits[0] = 10;
    var e = biDivideModulo(d, c);
    var a = String(e[1].digits[0]);
    while (biCompare(e[0], bigZero) == 1) {
        e = biDivideModulo(e[0], c);
        a += String(e[1].digits[0])
    }
    return (d.isNeg ? "-" : "") + reverseStr(a)
}

function biPow(c, e) {
    var b = bigOne;
    var d = c;
    while (true) {
        if ((e & 1) != 0) {
            b = biMultiply(b, d)
        }
        e >>= 1;
        if (e == 0) {
            break
        }
        d = biMultiply(d, d)
    }
    return b
}
function biPowMod(d, g, c) {
    var b = bigOne;
    var e = d;
    var f = g;
    while (true) {
        if ((f.digits[0] & 1) != 0) {
            b = biMultiplyMod(b, e, c)
        }
        f = biShiftRight(f, 1);
        if (f.digits[0] == 0 && biHighIndex(f) == 0) {
            break
        }
        e = biMultiplyMod(e, e, c)
    }
    return b
}


var public_key = 'B3C61EBBA4659C4CE3639287EE871F1F48F7930EA977991C7AFE3CC442FEA49643212E7D570C853F368065CC57A2014666DA8AE7D493FD47D171C0D894EEE3ED7F99F6798B7FFD7B5873227038AD23E3197631A8CB642213B9F27D4901AB0D92BFA27542AE890855396ED92775255C977F5C302F1E7ED4B1E369C12CB6B1822F'
var password = '1234567'
var p = new RSAKeyPair("10001", "",public_key);
pwd = encryptedString(p, password);
console.log(pwd);
