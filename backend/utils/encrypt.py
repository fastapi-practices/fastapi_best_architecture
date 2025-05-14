#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import os

from typing import Any

from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from itsdangerous import URLSafeSerializer

from backend.common.log import log


class AESCipher:
    """AES ENCRYPTOR"""

    def __init__(self, key: bytes | str) -> None:
        """
        INITIALIZE AES ENCRYPTION

        :param key: key, 16/24/32 bytes or 16 digit string
        :return:
        """
        self.key = key if isinstance(key, bytes) else bytes.fromhex(key)

    def encrypt(self, plaintext: bytes | str) -> bytes:
        """
        AES ENCRYPTION

        :param plaintext: pre-encrypted express
        :return:
        """
        if not isinstance(plaintext, bytes):
            plaintext = str(plaintext).encode('utf-8')
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(cipher.algorithm.block_size).padder()  # type: ignore
        padded_plaintext = padder.update(plaintext) + padder.finalize()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return iv + ciphertext

    def decrypt(self, ciphertext: bytes | str) -> str:
        """
        AES DECRYPT

        :param ciphertext: secret before decryption, bytes or 16 digit string
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
        return plaintext.decode('utf-8')


class Md5Cipher:
    """MD5 ENCRYPTOR"""

    @staticmethod
    def encrypt(plaintext: bytes | str) -> str:
        """
        MD5 ENCRYPTION

        :param plaintext: pre-encrypted express
        :return:
        """
        md5 = hashlib.md5()
        if not isinstance(plaintext, bytes):
            plaintext = str(plaintext).encode('utf-8')
        md5.update(plaintext)
        return md5.hexdigest()


class ItsDCipher:
    """ItsDangerous Encryptor"""

    def __init__(self, key: bytes | str) -> None:
        """
        Initialize ItsDangerous encryption

        :param key: key, 16/24/32 bytes or 16 digit string
        :return:
        """
        self.key = key if isinstance(key, bytes) else bytes.fromhex(key)

    def encrypt(self, plaintext: Any) -> str:
        """
        ItsDangerous Encryption

        :param plaintext: pre-encrypted express
        :return:
        """
        serializer = URLSafeSerializer(self.key)
        try:
            ciphertext = serializer.dumps(plaintext)
        except Exception as e:
            log.error(f'ItsDangerous encrypt failed: {e}')
            ciphertext = Md5Cipher.encrypt(plaintext)
        return ciphertext

    def decrypt(self, ciphertext: str) -> Any:
        """
        ItsDangerous Decrypt

        :param ciphertext: secret before decryption
        :return:
        """
        serializer = URLSafeSerializer(self.key)
        try:
            plaintext = serializer.loads(ciphertext)
        except Exception as e:
            log.error(f'ItsDangerous decrypt failed: {e}')
            plaintext = ciphertext
        return plaintext
