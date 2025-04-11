import logging
from base64 import b64decode

from secure.crypto.commons import ExHandler
from secure.crypto.decryptor import SecureDecryptor

log = logging.getLogger(__name__)


class SecureImporter:
    def __init__(self, password: str):
        self.resolver = SecureDecryptor(password)

    def resolve(self, data: str, ex_handler: ExHandler) -> bytes:
        try:
            bin_data = b64decode(data)
            return self.resolver.decrypt(bin_data)

        except Exception as ex:
            ex_handler(ex)
