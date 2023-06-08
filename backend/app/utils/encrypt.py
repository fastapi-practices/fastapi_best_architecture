#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AESCipher:
    def __init__(self, key: bytes | str):
        """
        :param key: 密钥，16/24/32 bytes 或 16 进制字符串
        """
        self.key = key if isinstance(key, bytes) else bytes.fromhex(key)

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        AES 加密

        :param plaintext: 加密前的明文
        :return:
        """
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(cipher.algorithm.block_size).padder()  # type: ignore
        padded_plaintext = padder.update(plaintext) + padder.finalize()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return iv + ciphertext

    def decrypt(self, ciphertext: bytes | str) -> bytes:
        """
        AES 解密

        :param ciphertext: 解密前的密文, bytes 或 16 进制字符串
        :return:
        """
        ciphertext = ciphertext if isinstance(ciphertext, bytes) else bytes.fromhex(ciphertext)
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(cipher.algorithm.block_size).unpadder()  # type: ignore
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext
