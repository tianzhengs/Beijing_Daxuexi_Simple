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


def md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()


def cap_recognize(cap):
    return DdddOcr().classification(denoise(cap))


def denoise(cap):
    img = Image.open(BytesIO(cap))
    steps = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1))
    _PX_BACKGROUND = (250, 250, 250)
    _PX_TARGET = (250, 0, 0)
    threshold, repeat = 7, 2

    for _ in range(repeat):
        for j in range(img.width):
            for i in range(img.height):
                px = img.getpixel((j, i))
                if px == _PX_BACKGROUND:
                    continue
                count = 0
                if px[0] < px[1] + px[2]:
                    count = 2
                for x, y in steps:
                    if 0 <= j + x < img.width and 0 <= i + y < img.height:
                        if img.getpixel((j + x, i + y)) == _PX_BACKGROUND:
                            count += 1
                if count >= threshold:
                    img.putpixel((j, i), _PX_BACKGROUND)
                else:
                    img.putpixel((j, i), _PX_TARGET)

    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


if __name__ == '__main__':
    import requests
    import re

    bjySession = requests.session()
    bjySession.timeout = 5  # set session timeout
    touch = bjySession.get(url="https://m.bjyouth.net/site/login")
    capUrl = "https://m.bjyouth.net" + re.findall(
        r'src="(/site/captcha.+)" alt=', touch.text)[0]
    cap1 = bjySession.get(url=capUrl).content
    cap2 = denoise(cap1)

    img = Image.open(BytesIO(cap1))
    img.show()

    img = Image.open(BytesIO(cap2))
    img.show()
