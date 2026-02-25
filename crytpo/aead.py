import os
from nacl.bindings import (
    crypto_aead_xchacha20poly1305_ietf_encrypt,
    crypto_aead_xchacha20poly1305_ietf_decrypt
)

def encrypt_plaintext(plain_text: bytes, derived_key: bytes) -> tuple[bytes, bytes]:
    nonce = os.urandom(24)
    cipher_text = crypto_aead_xchacha20poly1305_ietf_encrypt(plain_text, None, nonce, derived_key)
    return nonce, cipher_text


def decrypt_ciphertext(cipher_text: bytes, nonce: bytes, derived_key: bytes) -> bytes:
    """Decrypt AEAD ciphertext. Raises if tag verification fails (tampered or wrong key)."""
    return crypto_aead_xchacha20poly1305_ietf_decrypt(cipher_text, None, nonce, derived_key)

