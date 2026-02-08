from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def derived_key_generate(shared_key: bytes) -> bytes:
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"e2ee_message_key",
    ).derive(shared_key)
    return derived_key
