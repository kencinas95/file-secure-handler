from io import BytesIO

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.padding import PKCS7

from secure.crypto.commons import CRYPTO_DEFAULT_BACKEND, BIT_PADDING_LENGTH
from secure.crypto.key import SecureKey


class SecureEncryptor:
    def __init__(self, password: str):
        self.key = SecureKey(password)

        self.cipher = Cipher(
            self.key.aes,
            self.key.cbc(),
            backend=CRYPTO_DEFAULT_BACKEND
        )

    def encrypt(self, data: bytes) -> BytesIO:
        encryptor = self.cipher.encryptor()

        padding = PKCS7(BIT_PADDING_LENGTH).padder()
        bin_padded_data = padding.update(data) + padding.finalize()

        bin_data = (
                self.key.salt +
                self.key.init_vector +
                encryptor.update(bin_padded_data) +
                encryptor.finalize()
        )

        result = BytesIO()
        result.write(bin_data)
        result.seek(0, 0)

        return result
