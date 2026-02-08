import os
from cryptography.hazmat.primitives.ciphers.aead import XChaCha20Poly1305

def encrypt_plaintext(plain_text: bytes, derived_key: bytes) -> tuple[bytes, bytes]:
    chacha = XChaCha20Poly1305(derived_key)
    nonce = os.urandom(24)
    cipher_text = chacha.encrypt(nonce, plain_text, None)
    return nonce, cipher_text


def decrypt_ciphertext(cipher_text: bytes, nonce: bytes, derived_key: bytes) -> bytes:
    """Decrypt AEAD ciphertext. Raises if tag verification fails (tampered or wrong key)."""
    chacha = XChaCha20Poly1305(derived_key)
    return chacha.decrypt(nonce, cipher_text, None)

