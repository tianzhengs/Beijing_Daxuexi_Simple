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


ocr = DdddOcr()
def cap_recognize(cap):
    return ocr.classification(denoise(cap))


def denoise(cap):
    img = Image.open(BytesIO(cap))
    _STEPS_LAYER_1 = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1))
    STEPS8 = _STEPS_LAYER_1
    _PX_WHITE = (250, 250, 250)

    def _denoise(img, steps, threshold, repeat):
        for _ in range(repeat):
            for j in range(img.width):
                for i in range(img.height):
                    px = img.getpixel((j, i))
                    if px == _PX_WHITE:  # 自身白
                        continue
                    count = 0
                    if px[0] < px[1] + px[2]:
                        count = 2
                    for x, y in steps:
                        j2 = j + y
                        i2 = i + x
                        if 0 <= j2 < img.width and 0 <= i2 < img.height:  # 边界内
                            if img.getpixel((j2, i2)) == _PX_WHITE:  # 周围白
                                count += 1
                        else:  # 边界外全部视为黑
                            count += 1
                    if count >= threshold:
                        img.putpixel((j, i), _PX_WHITE)

        return img

    def denoise8(img, steps=STEPS8, threshold=7, repeat=2):
        """ 考虑外一周的降噪 """
        return _denoise(img, steps, threshold, repeat)

    buf = BytesIO()
    denoise8(img).save(buf, format='PNG')
    byte_im = buf.getvalue()
    return byte_im
