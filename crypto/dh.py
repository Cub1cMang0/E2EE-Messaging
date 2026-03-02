from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey
)

def shared_secret_generate(sender_private_key: X25519PrivateKey, receiver_public_key: X25519PublicKey) -> bytes:
    shared_key = sender_private_key.exchange(receiver_public_key)
    return shared_key