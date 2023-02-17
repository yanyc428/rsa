import random

from pyunit_prime import get_large_prime_bit_size


def encode_b64(n):
    table = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'
    result = []
    temp = n
    if 0 == temp:
        result.append('0')
    else:
        while 0 < temp:
            result.append(table[temp % 64])
            temp //= 64
    return ''.join([x for x in reversed(result)])


def decode_b64(string):
    table = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
             "6": 6, "7": 7, "8": 8, "9": 9,
             "a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15, "g": 16,
             "h": 17, "i": 18, "j": 19, "k": 20, "l": 21, "m": 22, "n": 23,
             "o": 24, "p": 25, "q": 26, "r": 27, "s": 28, "t": 29, "u": 30,
             "v": 31, "w": 32, "x": 33, "y": 34, "z": 35,
             "A": 36, "B": 37, "C": 38, "D": 39, "E": 40, "F": 41, "G": 42,
             "H": 43, "I": 44, "J": 45, "K": 46, "L": 47, "M": 48, "N": 49,
             "O": 50, "P": 51, "Q": 52, "R": 53, "S": 54, "T": 55, "U": 56,
             "V": 57, "W": 58, "X": 59, "Y": 60, "Z": 61,
             "-": 62, "_": 63}
    result = 0
    for i in range(len(string)):
        result *= 64
        result += table[string[i]]
    return result


# 生成密钥 默认512位质数
def generate_key():
    return generate(get_large_prime_bit_size(512), get_large_prime_bit_size(512))


# 密钥编码
def key_encode(key):
    return encode_b64(key)


# 密钥解码
def key_decode(key):
    return decode_b64(key)


# 拓展欧几里得算法
def ex_gcd(a, b, x=[1, 0], y=[0, 1]):
    if b == 0:
        return [a, x[0], y[0]]
    q = a // b
    tx1 = x[0] - q * x[1]
    ty1 = y[0] - q * y[1]
    tx = [x[1], tx1]
    ty = [y[1], ty1]
    return ex_gcd(b, a % b, tx, ty)


# 快速幂运算与取余
# x^n mod mod
def func(x, n, mod):
    res = 1
    x %= mod
    while n != 0:
        if n & 1:  # 取n的2进制的最低位
            res = (res * x) % mod
        n >>= 1  # 相当于n//2
        x = (x * x) % mod
    return res


# 编码/加密
def encode(i, public_key):
    keys = public_key.split('RSA')
    return func(i, key_decode(keys[1]), key_decode(keys[0]))


# 解码/解密
def decode(i, private_key):
    keys = private_key.split('RSA')
    return func(i, key_decode(keys[1]), key_decode(keys[0]))


# 根据p和q生成密钥
def generate(p, q):
    if not get(p, q) or p == q:
        return "invalid p and q"
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = random.randint(2, phi_n)
    while ex_gcd(e, phi_n)[1] < 0 or not get(e, phi_n) or e == ex_gcd(e, phi_n)[1]:
        e = random.randint(2, phi_n)
    return {
        "public": key_encode(n) + 'RSA' + key_encode(e),
        "private": key_encode(n) + 'RSA' + key_encode(ex_gcd(e, phi_n)[1]),
        "p": p,
        "q": q,
        "n": n,
        "phi_n": phi_n
    }


# 检验n与m是否互质
def get(n, m):
    while m > 0:
        t = n % m
        n = m
        m = t
    if n == 1:
        return True
    return False


if __name__ == '__main__':
    k = generate_key()
    print(k)
    s = encode(176, k["public"])
    print(s)
    print(decode(s, k["private"]))
