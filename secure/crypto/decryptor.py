from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.padding import PKCS7

from secure.crypto.commons import CRYPTO_DEFAULT_BACKEND, BIT_PADDING_LENGTH
from secure.crypto.key import SecureKey


class SecureDecryptor:
    def __init__(self, password: str):
        self.password = password

    def decrypt(self, encrypted_data: bytes) -> bytes:
        padding = PKCS7(BIT_PADDING_LENGTH).unpadder()

        salt = encrypted_data[:16]
        init_vector = encrypted_data[16:32]

        key = SecureKey(self.password, salt)

        resolver = Cipher(
            key.aes,
            key.cbc(init_vector),
            backend=CRYPTO_DEFAULT_BACKEND
        ).decryptor()

        bin_encrypted_text = (
                resolver.update(encrypted_data[32:]) +
                resolver.finalize()
        )

        return (
                padding.update(bin_encrypted_text) +
                padding.finalize()
        )
