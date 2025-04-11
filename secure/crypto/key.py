import os

from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from secure.crypto.commons import BIT_SALT_LENGTH, BIT_INIT_VECTOR_LENGTH, BIT_PBKDF2HMAC_LENGTH, PBKDF2HMAC_ITERATIONS, \
    CRYPTO_DEFAULT_BACKEND


class SecureKey:
    def __init__(self, password: str, salt: bytes = None):
        self.salt = salt or os.urandom(BIT_SALT_LENGTH)
        self.init_vector = os.urandom(BIT_INIT_VECTOR_LENGTH)
        self.key = self._generate(password)

    def _generate(self, password: str) -> bytes:
        return PBKDF2HMAC(
            algorithm=SHA256(),
            length=BIT_PBKDF2HMAC_LENGTH,
            salt=self.salt,
            iterations=PBKDF2HMAC_ITERATIONS,
            backend=CRYPTO_DEFAULT_BACKEND
        ).derive(password.encode('utf-8'))

    @property
    def aes(self) -> AES:
        return AES(self.key)

    def cbc(self, init_vector: bytes = None) -> CBC:
        return CBC(init_vector or self.init_vector)
