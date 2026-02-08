from typing import Any, TypedDict
from .aead import decrypt_ciphertext, encrypt_plaintext
from .dh import shared_secret_generate
from .hkdf import derived_key_generate
from .identity import sign_cipher_text, verify_signature


# Wire format: what the client sends to the server / recipient gets from server.
class MessagePayload(TypedDict, total=False):
    ciphertext: bytes | str
    nonce: bytes | str
    signature: bytes | str
    sender_id: str
    recipient_id: str




#Encrypt and sign a message for the recipient.
def send_message(
    plaintext: bytes,
    *,
    sender_identity_private: Any,
    sender_dh_private: Any,
    recipient_dh_public: Any,
    sender_id: str = "",
    recipient_id: str = "",
) -> MessagePayload:
    
    #1. DH: shared_secret 
    shared_secret = shared_secret_generate(sender_dh_private, recipient_dh_public)

    # 2. HKDF: same context as receive_message so both sides derive same key
    derived_key = derived_key_generate(shared_secret)

    # 3. AEAD: returns (nonce, ciphertext) so we can put nonce in payload
    nonce, cipher_text = encrypt_plaintext(plaintext, derived_key)

    # 4. Identity: sign ciphertext and capture signature for payload
    signature = sign_cipher_text(sender_identity_private, cipher_text)

    # 5. Build and return payload (opaque to server)
    return {
        "ciphertext": cipher_text,
        "nonce": nonce,
        "signature": signature,
        "sender_id": sender_id,
        "recipient_id": recipient_id,
    }

#Verify signature and decrypt payload. Returns plaintext.
def receive_message(
    payload: MessagePayload | dict[str, Any],
    *,
    receiver_dh_private: Any,
    sender_identity_public: Any,
    sender_dh_public: Any,
) -> bytes:
   
    for key in ("ciphertext", "nonce", "signature"):
        if key not in payload:
            raise ValueError(f"Payload missing required field: {key!r}")

    # 1. Verify signature (reject if tampered or wrong sender)
    verify_signature(sender_identity_public, payload["ciphertext"], payload["signature"])

    # 2. DH: same shared secret as sender (receiver private + sender public)
    shared_secret = shared_secret_generate(receiver_dh_private, sender_dh_public)

    # 3. HKDF: same context as send_message -> same derived key
    derived_key = derived_key_generate(shared_secret)

    # 4. AEAD decrypt
    plain_text = decrypt_ciphertext(payload["ciphertext"], payload["nonce"], derived_key)
    
    #5. Return plaintext.
    return plain_text
    
    


