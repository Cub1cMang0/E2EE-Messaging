# Server handoff: what to store where

Simple outline for the server team. The crypto layer runs only on clients; the server stores and routes data only.

---

## Where private keys live

**Private keys exist only on the client (user’s device).**

|                 Key                | Where it lives |                          Who has it                           |
|------------------------------------|----------------|---------------------------------------------------------------|
| **Identity private key** (Ed25519) | Client only    | The user’s app; used to sign outgoing messages.               |
| **DH private key** (X25519)        | Client only    | The user’s app; used to derive shared secrets for encryption. |

- The server **never** receives, stores, or has access to either private key.
- Clients generate and keep private keys locally (e.g. in memory or secure storage). They **upload only the corresponding public keys** to the server for the registry.
- If the server ever sees a “private key” field, treat it as a bug or misconfiguration—the server must not store or use it.

---

## 1. Store this

### User registry (per user)

|--------Field----------|------------------What it is----------------------|------------------------Why-----------------------|
|-----------------------|--------------------------------------------------|--------------------------------------------------|
| `user_id`             | Username or unique id | Routing, identity        |
| `identity_public_key` | Ed25519 public key (bytes, often base64 in JSON) | So others can **verify** messages from this user |
| `dh_public_key`       | X25519 public key (bytes, often base64)          | So others can **encrypt** messages to this user  |

Clients register/update these at login. Server only stores and returns them.

### Messages (per message)

|     Field      |          What it is          |                Why                 |
|----------------|------------------------------|------------------------------------|
| `recipient_id` | Who gets the message         | Routing                            |
| `sender_id`    | Who sent it                  | Display; crypto is in payload      |
| `ciphertext`   | Encrypted body (opaque blob) | Stored as-is; **do not decrypt**   |
| `nonce`        | Opaque blob                  | Recipient needs it to decrypt      |
| `signature`    | Opaque blob                  | Recipient uses it to verify sender |

Server stores the whole payload and delivers it to `recipient_id`. No parsing or crypto on these fields.

---

## 2. Never store or do this

- **Do not** store: private keys (identity or DH), derived keys, or message plaintext.
- **Do not** decrypt, verify signatures, or do key agreement. Clients do all crypto.

---

## 3. API to align on

|         Action          |                                              Server responsibility                                               |
|-------------------------|------------------------------------------------------------------------------------------------------------------|
| **Register/update keys**| Accept `user_id`, `identity_public_key`, `dh_public_key`; store/overwrite for that user.                         |
| **Get keys for a user** | Given `user_id`, return `identity_public_key` and `dh_public_key`.                                               |
| **Send message**        | Accept payload `{ sender_id, recipient_id, ciphertext, nonce, signature }`; store and deliver to `recipient_id`. |
| **Get my messages**     | Given `recipient_id` (or auth), return list of payloads for that recipient.                                      |

Agree with the client team on encoding (e.g. base64 for JSON). Crypto layer works in bytes; client encodes/decodes at the boundary.

---

## 4. One sentence

**Server stores and serves (1) public keys per user and (2) opaque message payloads; it never stores private keys or plaintext and never decrypts or verifies—only store and route.**
