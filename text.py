from rsa import encode, decode, generate_key, encode_b64, decode_b64


# 文本加密
def text_encode(text, public_key):
    en = list(map(lambda x: encode(x, public_key), text.encode('utf-8')))
    return '~'.join(list(map(lambda x: encode_b64(x), en)))


# 文本解密
def text_decode(text, private_key):
    de = list(map(lambda x: decode_b64(x), text.split('~')))
    try:
        b = bytes(map(lambda x: decode(x, private_key), de)).decode('utf-8')
        return b
    except ValueError:
        return "invalid private key"


if __name__ == '__main__':
    k = generate_key()
    enc = text_encode("中国真的很不错", k['public'])
    print(enc)
    print(text_decode(enc, k['private']))
