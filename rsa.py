import random
from hashlib import sha256
from secrets import compare_digest
from primes import primes

def gcd(a, b):
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

def extended_gcd(e, fi_arg):
    fi = fi_arg
    x, x1, y, y1 = 0, 1, 1, 0
    while fi:
        coeff = e//fi
        e, fi = fi, e-coeff*fi
        x, x1 = x1 - coeff*x, x
        y, y1 = y1 - coeff*y, y
    return x1%fi_arg


def create_e(fi):
    for i in range(len(primes)): # або змінити на бін пошук
        if primes[i] >= fi:
            break
    while True:
        e = primes[random.randint(0,i)]
        if gcd(e, fi) == 1:
            return e

def create_keys():
    n = 0
    while n <= 1500:
        p1 = primes[random.randint(10, 20)]
        p2 = primes[random.randint(10, 30)]
        while p1 == p2:
            p2 = primes[random.randint(10,30)]
        n = p1 * p2
    fi= (p1-1)*(p2-1)
    e = create_e(fi)
    d = extended_gcd(e, fi)
    return n, e, d

def encrypt(message, en):
    e, n = en
    blocks= []
    for i in range(len(message)):
        number = (ord(message[i]) ** e) % n
        blocks.append(str(number))
    return " ".join(blocks)

def decrypt(blocks, dn):
    d, n = dn
    blocks, message = blocks.split(' '), ""
    for number in blocks:
        letter_index = ((int(number)) ** d) % n
        message += chr(letter_index)
    return message

def main():
    """check with hashing"""

    n, e, d = create_keys()
    print(n, e, d)

    m = "lrkngdlknf;wlrjmclfj"
    sha256_digest_1 = sha256(m.encode("utf-8"))
    digest_1 = sha256_digest_1.digest()
    hexdigest_1 = sha256_digest_1.hexdigest()

    encrypted = encrypt(m, (e, n))
    print("ENCRYPTED",encrypted)
    decrypted = decrypt(encrypted, (d, n))
    print("DECRYPTED", decrypted)

    sha256_digest_2 = sha256(decrypted.encode("utf-8"))
    digest_2 = sha256_digest_2.digest()
    hexdigest_2 = sha256_digest_2.hexdigest()
    print(compare_digest(digest_1, digest_2))
    print(compare_digest(hexdigest_1, hexdigest_2))

if __name__ == "__main__":
    main()
