# E2EE Messaging Application

A custom end-to-end encrypted desktop messaging application written in Python. Messages are encrypted on the sender's device and can only be decrypted by the intended recipient — the server routes opaque ciphertext and never has access to message content.

---

## Table of Contents

- [How to Run](#how-to-run)
- [Code Description](#code-description)
- [Cryptographic Protocol](#cryptographic-protocol)
- [Open Source Software Used](#open-source-software-used)

---

## How to Run

### Prerequisites

Python 3.11+ and all dependencies installed:

```bash
pip install -r requirements.txt
```

### Step 1 — Start the Server

From the project root:

```bash
# Local development (binds to 127.0.0.1:8000)
python run_server.py local

# Network/deployment mode (binds to 0.0.0.0:8000)
python run_server.py server
```

On first run the server creates two files in the project root:
- `e2ee_messaging.db` — SQLite database (users, groups, group members)
- `server_dh_key.dat` — server's X25519 private key (persisted across restarts)

### Step 2 — Start the Client

In a separate terminal, from the `client/gui/` directory:

```bash
# Local mode (talks to 127.0.0.1:8000)
python client/gui/main.py local

# Server mode (talks to https://chat.yoshi.red)
python client/gui/main.py server
```

### Step 3 — Register and Log In

1. The login/register dialog opens. Switch to the **Register** tab.
2. Fill in:
   - **Username** — 8–32 alphanumeric/underscore characters
   - **Display Name** — 6–32 characters
   - **Password** — 8–64 characters, must contain uppercase, lowercase, a digit, and a symbol (`@$!%*?&`)
3. Click **Register**. On success the app auto-logs you in and opens the main chat window.
4. On future runs, use the **Login** tab with your username and password.

### Step 4 — Start a Chat

1. Click **Add Group** to open the group chat creation dialog.
2. Search for another registered user by display name and add them.
3. Name the chat and click **Create**. It appears in the sidebar immediately.
4. Click the chat to open it. Type a message and click **Send**.

Messages are encrypted on your device before being transmitted. Only the recipient can decrypt them.

### Step 5 — Run Unit Tests (Optional)

From the project root:

```bash
python -m pytest crypto/test_crypto.py -v
```

---

## Code Description

### Project Structure

```
E2EE-Messaging/
├── run_server.py                   # Uvicorn server entry point (local/server mode)
├── inspect_db.py                   # Dev utility to dump SQLite DB contents
├── requirements.txt                # Pinned Python dependencies
│
├── crypto/                         # Cryptographic primitives and protocol
│   ├── dh.py                       # X25519 Diffie-Hellman key exchange
│   ├── hkdf.py                     # HKDF-SHA256 key derivation
│   ├── aead.py                     # XChaCha20-Poly1305 AEAD encryption
│   ├── identity.py                 # Ed25519 signing and verification
│   ├── protocol.py                 # send_message() / receive_message() pipeline
│   └── test_crypto.py              # Unit tests for the protocol
│
├── server/
│   └── main.py                     # FastAPI app: REST endpoints + WebSocket relay
│
└── client/
    ├── gui/
    │   ├── main.py                 # Qt window classes (Login, MainWindow, AddNewGC)
    │   ├── app_gui.py              # Qt-compiled main chat window UI
    │   ├── app_gui.ui              # Qt Designer source
    │   ├── register_gui.py         # Qt-compiled login/register dialog UI
    │   ├── register_gui.ui         # Qt Designer source
    │   ├── add_new_gc.py           # Qt-compiled group chat creation dialog UI
    │   └── add_new_gc.ui           # Qt Designer source
    └── utilities/
        ├── database.py             # SQLAlchemy ORM models + SQLite setup
        ├── user_handling.py        # Registration, login, group chat logic
        ├── ws_client.py            # Persistent WebSocket client (QThread)
        ├── search_utility.py       # HTTP wrappers for user search
        └── config.py               # Base URL config (local / server mode)
```

### What Was Built

**Cryptographic Protocol (`crypto/`)**

Four focused modules compose a complete encrypt-sign / verify-decrypt pipeline assembled in `protocol.py`:

1. `dh.py` — performs X25519 ECDH to derive a shared secret from the sender's DH private key and the recipient's DH public key
2. `hkdf.py` — derives a 32-byte symmetric key from the shared secret using HKDF-SHA256 with a fixed context string (`b"e2ee_message_key"`)
3. `aead.py` — encrypts the plaintext with XChaCha20-Poly1305 using a 24-byte random nonce, producing an authenticated ciphertext
4. `identity.py` — signs the ciphertext with the sender's Ed25519 identity key so the recipient can verify who sent it

`protocol.py` exposes two functions:
- `send_message()` — runs the full DH → HKDF → AEAD encrypt → Ed25519 sign pipeline and returns a `MessagePayload` dict (`ciphertext`, `nonce`, `signature`, `sender_id`, `recipient_id`)
- `receive_message()` — verifies the signature first, then runs DH → HKDF → AEAD decrypt and returns the plaintext bytes

**Server (`server/main.py`)**

A FastAPI application providing:

| Endpoint | Purpose |
|---|---|
| `GET /pub_key` | Returns the server's X25519 public key (hex) |
| `POST /register` | Stores username, display name, and both public keys |
| `POST /login` | Authenticates via E2EE challenge-response: the client encrypts a JSON payload to the server's DH key and signs it; the server decrypts and verifies the signature |
| `GET /search_dn/{display_name}` | Returns a user's public keys by display name |
| `GET /search_un/{username}` | Returns a user's public keys by username |
| `POST /groups/create` | Creates a group chat and adds members (duplicate detection included) |
| `GET /users/{display_name}/groups` | Returns the user's group chats (requires a live Ed25519 signature for authorization) |
| `GET /groups/{group_id}` | Returns a single group chat |
| `GET /groups/{group_id}/members` | Returns display names of all group members |
| `GET /users` | Returns list of currently online users |
| `WS /ws/{username}` | WebSocket endpoint; server routes `message` payloads verbatim to the recipient without decrypting them |

The `ConnectionManager` singleton maps usernames to live WebSocket handles and routes messages via `send_raw()`.

**Persistent WebSocket Client (`client/utilities/ws_client.py`)**

`PersistentWebSocketClient` runs on a background `QThread` with its own `asyncio` event loop, keeping the GUI responsive. It:
- Connects to `ws://{host}/ws/{username}` on startup
- Maintains a `user_crypto_map` (display name → DH public key + identity public key + group ID) populated when a chat is opened
- Decrypts every incoming message using `receive_message()`, saves it to the local SQLite database, and emits a `message_received` Qt signal to update the UI
- Sends messages by calling `send_message()` on the plaintext and posting the base64-encoded payload over the WebSocket via `asyncio.run_coroutine_threadsafe`

**User Handling (`client/utilities/user_handling.py`)**

- `handle_registration()` — generates an Ed25519 identity key pair and an X25519 DH key pair, concatenates the 64 bytes of private key material, derives a storage key from the user's password via HKDF-SHA256 (with a 16-byte random salt), encrypts the bundle with AES-256-GCM, and writes `salt + nonce + ciphertext` to `{username}.dat` at the OS app-local-data path. Then POSTs the public keys to the server.
- `handle_login()` — reads `{username}.dat`, derives the storage key from the password, decrypts the private key bundle, and performs the E2EE login challenge against the server.
- `fetch_user_gcs()` — attaches a live Ed25519 signature to the request so the server can verify the requester's identity before returning their group list.

**Local Database (`client/utilities/database.py`)**

SQLAlchemy ORM with four models:
- `User` — username, display name, `id_pub_key` (hex), `dh_pub_key` (hex)
- `Group` — chat name, creator (FK), creation timestamp
- `Group_Member` — group ID (FK), user ID (FK), role (`admin` / `member`), join timestamp
- `Message` — group ID (FK), sender, plaintext message text, timestamp

`save_message()` and `get_messages()` persist decrypted messages locally on the client. The server has no access to this data.

**GUI (`client/gui/main.py`)**

Three PySide6 window classes:
- `Login_Register_Window` — two-panel dialog with regex-validated inputs and password strength enforcement; auto-logs in after successful registration
- `MainWindow` — main chat window; on chat selection it fetches the recipient's public keys, registers them with `PersistentWebSocketClient`, loads message history from the local DB, and wires the send button through the WebSocket client
- `AddNewGC_Window` — group chat creation dialog; emits a `new_gc_created(int)` Qt signal so `MainWindow` can add the new chat to the sidebar without a full refresh

---

## Cryptographic Protocol

This application implements a **custom static-key authenticated encryption protocol**:

```
send_message():
  1. DH(sender_dh_priv, recipient_dh_pub)       → 32-byte shared secret
  2. HKDF-SHA256(shared_secret)                  → 32-byte derived key
  3. XChaCha20-Poly1305 encrypt(plaintext, key)  → (nonce, ciphertext)
  4. Ed25519 sign(ciphertext)                    → signature
  5. Return {ciphertext, nonce, signature, sender_id, recipient_id}

receive_message():
  1. Ed25519 verify(ciphertext, signature)        — reject if invalid
  2. DH(receiver_dh_priv, sender_dh_pub)         → 32-byte shared secret
  3. HKDF-SHA256(shared_secret)                  → 32-byte derived key
  4. XChaCha20-Poly1305 decrypt(ciphertext, key) → plaintext
```

**Key sizes:** Ed25519 keys: 32 bytes each. X25519 keys: 32 bytes each. Symmetric key: 32 bytes. AEAD nonce: 24 bytes.

**Local key storage:** private keys are encrypted with AES-256-GCM under a key derived from the user's password via HKDF-SHA256 (16-byte random salt). The password never leaves the device.

**Authentication:** the server authenticates users cryptographically — it verifies the client's Ed25519 signature and decrypts a DH-keyed challenge payload. No password is ever sent to the server.

**Current limitations:**
- Static long-term DH keys — no forward secrecy
- No ratcheting (not Signal Protocol / X3DH / Double Ratchet)
- No offline message delivery (messages dropped if recipient is offline)
- Group chats are tracked in the database but do not yet have group-level E2EE key distribution

---

## Open Source Software Used

| Library | Version | Purpose |
|---|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | 0.128.0 | REST API framework and WebSocket support |
| [Uvicorn](https://www.uvicorn.org/) | 0.40.0 | ASGI server |
| [Starlette](https://www.starlette.io/) | 0.50.0 | ASGI foundation underlying FastAPI |
| [Pydantic](https://docs.pydantic.dev/) | 2.12.5 | Request/response data validation |
| [SQLAlchemy](https://www.sqlalchemy.org/) | 2.0.46 | ORM for SQLite (server + client share models) |
| [cryptography](https://cryptography.io/) | 46.0.5 | X25519, Ed25519, HKDF-SHA256, AES-256-GCM |
| [PyNaCl](https://pynacl.readthedocs.io/) | 1.6.2 | libsodium bindings for XChaCha20-Poly1305 |
| [websockets](https://websockets.readthedocs.io/) | 16.0 | Async WebSocket client |
| [PySide6](https://doc.qt.io/qtforpython/) | 6.10.2 | Qt6 Python bindings for the desktop GUI |
| [requests](https://requests.readthedocs.io/) | 2.32.5 | Synchronous HTTP client for REST calls |
| Python stdlib | — | `os`, `json`, `base64`, `asyncio`, `sqlite3` (via SQLAlchemy) |
