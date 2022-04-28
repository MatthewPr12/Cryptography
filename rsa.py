import random
from hashlib import sha256
from secrets import compare_digest
from primes import primes

def gcd(a, b):
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

def extended_gcd(e, fi):
    x, x1, y, y1 = 0, 1, 1, 0
    while (fi != 0):
        coeff = e // fi
        e, fi = fi, e - coeff * fi
        x1, x = x, x1 - coeff * x
        y1, y = y, y1 - coeff * y
    return x1

def create_e(fi):
    while True:
        e = random.randrange(2, fi)
        if e in primes and (gcd(e, fi) == 1):
            return e

def create_keys(p1, p2):
    p1 = primes[random.randint(150,350)]
    p2 = primes[random.randint(150,350)]
    n = p1 * p2
    fi= (p1-1)*(p2-1)
    e = create_e(fi)
    d = extended_gcd(e, fi)
    if (d < 0):
        d += fi
    return n, e, d

def encrypt(message, n, e, counter):
    message, blocks= message.lower(), []

    for i in range(len(message)):
        number = ord(message[i])-counter # number in alphabet
        number = (number**e)%n           # encoded
        blocks.append(str(number))
    return " ".join(blocks)


def decrypt(blocks, d, n, counter):
    blocks = blocks.split(' ')
    message = ""

    for number in blocks:
        letter_index = ((int(number))**d)%n
        letter = chr(letter_index+counter)

        message+=letter
    return message


def main():
    """check with hashing"""
    p1, p2 = 123, 127 #change to random choice among primes or input
    
    n, e, d = create_keys(p1, p2)
    print(n, e, d)

    m = "тест"
    if ord(m[0]) < 130:
        counter = 97
    else:
        counter = 1072
    sha256_digest_1 = sha256(m.encode("utf-8"))
    digest_1 = sha256_digest_1.digest()
    hexdigest_1 = sha256_digest_1.hexdigest()

    encrypted = encrypt(m, n, e, counter)
    print(encrypted)
    decrypted = decrypt(encrypted, d, n, counter)
    print(decrypted)

    sha256_digest_2 = sha256(decrypted.encode("utf-8"))
    digest_2 = sha256_digest_2.digest()
    hexdigest_2 = sha256_digest_2.hexdigest()
    print(compare_digest(digest_1, digest_2))
    print(compare_digest(hexdigest_1, hexdigest_2))
    
main()
