# test_crypto.py (in project root)
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from .protocol import send_message, receive_message

# Generate keypairs for sender and receiver
sender_dh_private = X25519PrivateKey.generate()
sender_dh_public = sender_dh_private.public_key()
recipient_dh_private = X25519PrivateKey.generate()
recipient_dh_public = recipient_dh_private.public_key()

sender_identity_private = Ed25519PrivateKey.generate()
sender_identity_public = sender_identity_private.public_key()
 
# Encrypt & sign
plaintext = b"Hello, secret world!"
payload = send_message(
    plaintext,
    sender_identity_private=sender_identity_private,
    sender_dh_private=sender_dh_private,
    recipient_dh_public=recipient_dh_public,
)

# Decrypt & verify
decrypted = receive_message(
    payload,
    receiver_dh_private=recipient_dh_private,
    sender_identity_public=sender_identity_public,
    sender_dh_public=sender_dh_public,
)

print(decrypted.decode("utf-8"))

assert decrypted == plaintext
print("Crypto round-trip OK!")

# Run python -m crypto.test_crypto from root