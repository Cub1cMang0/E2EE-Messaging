# test_crypto.py — unit tests for crypto protocol
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.exceptions import InvalidSignature

from .protocol import send_message, receive_message, MessagePayload


def _make_keypairs():
    """Sender and recipient DH + sender identity keys."""
    sender_dh_private = X25519PrivateKey.generate()
    sender_dh_public = sender_dh_private.public_key()
    recipient_dh_private = X25519PrivateKey.generate()
    recipient_dh_public = recipient_dh_private.public_key()
    sender_identity_private = Ed25519PrivateKey.generate()
    sender_identity_public = sender_identity_private.public_key()
    return {
        "sender_dh_private": sender_dh_private,
        "sender_dh_public": sender_dh_public,
        "recipient_dh_private": recipient_dh_private,
        "recipient_dh_public": recipient_dh_public,
        "sender_identity_private": sender_identity_private,
        "sender_identity_public": sender_identity_public,
    }


class TestSendReceiveRoundtrip(unittest.TestCase):
    """Round-trip encrypt/decrypt with valid keys."""

    def test_roundtrip_returns_original_plaintext(self):
        keys = _make_keypairs()
        plaintext = b"Hello, secret world!"
        payload = send_message(
            plaintext,
            sender_identity_private=keys["sender_identity_private"],
            sender_dh_private=keys["sender_dh_private"],
            recipient_dh_public=keys["recipient_dh_public"],
        )
        decrypted = receive_message(
            payload,
            receiver_dh_private=keys["recipient_dh_private"],
            sender_identity_public=keys["sender_identity_public"],
            sender_dh_public=keys["sender_dh_public"],
        )
        self.assertEqual(decrypted, plaintext)

    def test_roundtrip_empty_plaintext(self):
        keys = _make_keypairs()
        plaintext = b""
        payload = send_message(
            plaintext,
            sender_identity_private=keys["sender_identity_private"],
            sender_dh_private=keys["sender_dh_private"],
            recipient_dh_public=keys["recipient_dh_public"],
        )
        decrypted = receive_message(
            payload,
            receiver_dh_private=keys["recipient_dh_private"],
            sender_identity_public=keys["sender_identity_public"],
            sender_dh_public=keys["sender_dh_public"],
        )
        self.assertEqual(decrypted, plaintext)

    def test_sender_id_recipient_id_preserved(self):
        keys = _make_keypairs()
        payload = send_message(
            b"test",
            sender_identity_private=keys["sender_identity_private"],
            sender_dh_private=keys["sender_dh_private"],
            recipient_dh_public=keys["recipient_dh_public"],
            sender_id="alice",
            recipient_id="bob",
        )
        self.assertEqual(payload.get("sender_id"), "alice")
        self.assertEqual(payload.get("recipient_id"), "bob")


class TestPayloadShape(unittest.TestCase):
    """send_message return value has required fields."""

    def test_payload_has_required_fields(self):
        keys = _make_keypairs()
        payload = send_message(
            b"x",
            sender_identity_private=keys["sender_identity_private"],
            sender_dh_private=keys["sender_dh_private"],
            recipient_dh_public=keys["recipient_dh_public"],
        )
        self.assertIn("ciphertext", payload)
        self.assertIn("nonce", payload)
        self.assertIn("signature", payload)
        self.assertIsInstance(payload["ciphertext"], bytes)
        self.assertIsInstance(payload["nonce"], bytes)
        self.assertIsInstance(payload["signature"], bytes)
        self.assertGreater(len(payload["ciphertext"]), 0)
        self.assertGreater(len(payload["nonce"]), 0)
        self.assertGreater(len(payload["signature"]), 0)


class TestReceiveMessageValidation(unittest.TestCase):
    """receive_message rejects bad or incomplete payloads."""

    def test_raises_on_missing_ciphertext(self):
        keys = _make_keypairs()
        payload = send_message(
            b"x",
            sender_identity_private=keys["sender_identity_private"],
            sender_dh_private=keys["sender_dh_private"],
            recipient_dh_public=keys["recipient_dh_public"],
        )
        del payload["ciphertext"]
        with self.assertRaises(ValueError) as ctx:
            receive_message(
                payload,
                receiver_dh_private=keys["recipient_dh_private"],
                sender_identity_public=keys["sender_identity_public"],
                sender_dh_public=keys["sender_dh_public"],
            )
        self.assertIn("ciphertext", str(ctx.exception))

    def test_raises_on_missing_nonce(self):
        keys = _make_keypairs()
        payload = send_message(
            b"x",
            sender_identity_private=keys["sender_identity_private"],
            sender_dh_private=keys["sender_dh_private"],
            recipient_dh_public=keys["recipient_dh_public"],
        )
        del payload["nonce"]
        with self.assertRaises(ValueError) as ctx:
            receive_message(
                payload,
                receiver_dh_private=keys["recipient_dh_private"],
                sender_identity_public=keys["sender_identity_public"],
                sender_dh_public=keys["sender_dh_public"],
            )
        self.assertIn("nonce", str(ctx.exception))

    def test_raises_on_missing_signature(self):
        keys = _make_keypairs()
        payload = send_message(
            b"x",
            sender_identity_private=keys["sender_identity_private"],
            sender_dh_private=keys["sender_dh_private"],
            recipient_dh_public=keys["recipient_dh_public"],
        )
        del payload["signature"]
        with self.assertRaises(ValueError) as ctx:
            receive_message(
                payload,
                receiver_dh_private=keys["recipient_dh_private"],
                sender_identity_public=keys["sender_identity_public"],
                sender_dh_public=keys["sender_dh_public"],
            )
        self.assertIn("signature", str(ctx.exception))


class TestTampering(unittest.TestCase):
    """Tampered payloads fail verification or decryption."""

    def test_tampered_ciphertext_fails(self):
        keys = _make_keypairs()
        payload = send_message(
            b"secret",
            sender_identity_private=keys["sender_identity_private"],
            sender_dh_private=keys["sender_dh_private"],
            recipient_dh_public=keys["recipient_dh_public"],
        )
        payload = dict(payload)
        payload["ciphertext"] = payload["ciphertext"][:1] + b"x" + payload["ciphertext"][2:]
        with self.assertRaises(InvalidSignature):
            receive_message(
                payload,
                receiver_dh_private=keys["recipient_dh_private"],
                sender_identity_public=keys["sender_identity_public"],
                sender_dh_public=keys["sender_dh_public"],
            )

    def test_tampered_signature_fails(self):
        keys = _make_keypairs()
        payload = send_message(
            b"secret",
            sender_identity_private=keys["sender_identity_private"],
            sender_dh_private=keys["sender_dh_private"],
            recipient_dh_public=keys["recipient_dh_public"],
        )
        payload = dict(payload)
        payload["signature"] = payload["signature"][:1] + b"x" + payload["signature"][2:]
        with self.assertRaises(InvalidSignature):
            receive_message(
                payload,
                receiver_dh_private=keys["recipient_dh_private"],
                sender_identity_public=keys["sender_identity_public"],
                sender_dh_public=keys["sender_dh_public"],
            )

    def test_wrong_recipient_cannot_decrypt(self):
        """Message encrypted for recipient A cannot be decrypted by recipient B (different DH pair)."""
        keys = _make_keypairs()
        # Third keypair = different "recipient"
        other_dh_private = X25519PrivateKey.generate()
        other_dh_public = other_dh_private.public_key()
        payload = send_message(
            b"secret",
            sender_identity_private=keys["sender_identity_private"],
            sender_dh_private=keys["sender_dh_private"],
            recipient_dh_public=keys["recipient_dh_public"],
        )
        with self.assertRaises(Exception):
            receive_message(
                payload,
                receiver_dh_private=other_dh_private,
                sender_identity_public=keys["sender_identity_public"],
                sender_dh_public=keys["sender_dh_public"],
            )

    def test_wrong_sender_identity_fails_verification(self):
        """Payload signed by A fails when verified with B's public key."""
        keys = _make_keypairs()
        other_identity_private = Ed25519PrivateKey.generate()
        other_identity_public = other_identity_private.public_key()
        payload = send_message(
            b"secret",
            sender_identity_private=keys["sender_identity_private"],
            sender_dh_private=keys["sender_dh_private"],
            recipient_dh_public=keys["recipient_dh_public"],
        )
        with self.assertRaises(InvalidSignature):
            receive_message(
                payload,
                receiver_dh_private=keys["recipient_dh_private"],
                sender_identity_public=other_identity_public,
                sender_dh_public=keys["sender_dh_public"],
            )


if __name__ == "__main__":
    unittest.main()
