from base64 import b64encode

from secure.crypto.commons import ExHandler
from secure.crypto.encryptor import SecureEncryptor


class SecureExporter:
    def __init__(self, password: str):
        self.encryptor = SecureEncryptor(password)

    def export(self, data: bytes, ex_handler: ExHandler) -> str:
        try:
            with self.encryptor.encrypt(data) as sd:
                return b64encode(sd.read()).decode('utf-8')

        except Exception as ex:
            ex_handler(ex)
