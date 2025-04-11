from typing import Callable

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7

# Constants
BIT_SALT_LENGTH = 16

BIT_INIT_VECTOR_LENGTH = 16

BIT_PBKDF2HMAC_LENGTH = 32

BIT_PADDING_LENGTH = 128

PBKDF2HMAC_ITERATIONS = 100_000

# Static objects
CRYPTO_DEFAULT_BACKEND = default_backend()

CRYPTO_PADDING_HANDLER = PKCS7(BIT_PADDING_LENGTH)

# Type hints
ExHandler = Callable[[Exception], None]
