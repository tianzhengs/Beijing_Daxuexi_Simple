from base64 import b64encode
from io import BytesIO

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from PIL import Image
from ddddocr import DdddOcr


def encrypt(t):
    public_key = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD5uIDebA2qU746e/NVPiQSBA0Q3J8/G23zfrwMz4qoip1vuKaVZykuMtsAkCJFZhEcmuaOVl8nAor7cz/KZe8ZCNInbXp2kUQNjJiOPwEhkGiVvxvU5V5vCK4mzGZhhawF5cI/pw2GJDSKbXK05YHXVtOAmg17zB1iJf+ie28TbwIDAQAB\n-----END PUBLIC KEY-----"
    rsa_key = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsa_key)
    cipher_text = b64encode(cipher.encrypt(t.encode()))
    return cipher_text.decode()


def cap_recognize(cap):
    return DdddOcr().classification(denoise(cap))


def denoise(cap):
    img = Image.open(BytesIO(cap))
    steps = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1))
    _PX_WHITE = (250, 250, 250)
    threshold, repeat = 7, 2

    for _ in range(repeat):
        for j in range(img.width):
            for i in range(img.height):
                px = img.getpixel((j, i))
                if px == _PX_WHITE:
                    continue
                count = 0
                if px[0] < px[1] + px[2]:
                    count = 2
                for x, y in steps:
                    if 0 <= j + x < img.width and 0 <= i + y < img.height:
                        if img.getpixel((j + x, i + y)) == _PX_WHITE:
                            count += 1
                if count >= threshold:
                    img.putpixel((j, i), _PX_WHITE)

    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()
