from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


def sign_cipher_text(sender_private_key: Ed25519PrivateKey, message: bytes) -> bytes:
    """Sign message with identity private key. Returns signature bytes."""
    return sender_private_key.sign(message)


def verify_signature(
    sender_public_key: Ed25519PublicKey,
    message: bytes,
    signature: bytes,
) -> None:
    """Verify signature. Raises InvalidSignature if verification fails."""
    sender_public_key.verify(signature, message)
