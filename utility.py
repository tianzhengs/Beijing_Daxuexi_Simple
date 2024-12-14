from base64 import b64encode

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA

def encrypt(t):
    # public_key = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD5uIDebA2qU746e/NVPiQSBA0Q3J8/G23zfrwMz4qoip1vuKaVZykuMtsAkCJFZhEcmuaOVl8nAor7cz/KZe8ZCNInbXp2kUQNjJiOPwEhkGiVvxvU5V5vCK4mzGZhhawF5cI/pw2GJDSKbXK05YHXVtOAmg17zB1iJf+ie28TbwIDAQAB\n-----END PUBLIC KEY-----" # The public key before 2024-12-14 update, and you can still see this public key in Dev Tools today
    public_key = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsqHqBWhMMNHuPzALvF6j0WzQQQgS9jt/xjOmOhmBGVxkmxiRa02eg9ihV8NWt1IboK8cON3VTQbZLjMG83mAjMK1MD7O0ITUHDF+MyBhkwJ6oK3LV60ZNeRsdzSl3P4hFJjC2PYK3tL7yyATT/R4KE0xnDe4TY2uCTl40ZMqhc7JlV9tMElfEIGuzp+rPpRUVTyNIDkeOMrHNFVTZRoghxX9Jnrg9QQSMEBLXf+BLtKbkmPkz6jMJPF4OrerZ4TPopUM20/qKYQHZ6eqAgpz0UFbGUE46xMaMlz3NJBR75YSlPlX4P2OtL+57RzAEdJNqGwx0Ksq5+q0d3xa+W7lQQIDAQAB\n-----END PUBLIC KEY-----"
    rsa_key = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsa_key)
    cipher_text = b64encode(cipher.encrypt(t.encode()))
    return cipher_text.decode()
