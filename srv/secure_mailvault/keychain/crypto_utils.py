import base64
import os
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def load_encryption_key() -> bytes:
    """Load a 32-byte AES key from ENCRYPTION_KEY (base64-encoded)."""
    key_b64 = os.environ.get("ENCRYPTION_KEY")
    if not key_b64:
        raise RuntimeError("ENCRYPTION_KEY is not set")

    try:
        key = base64.b64decode(key_b64)
    except (base64.binascii.Error, ValueError) as exc:  # type: ignore[attr-defined]
        raise ValueError("ENCRYPTION_KEY must be valid base64") from exc

    if len(key) != 32:
        raise ValueError("ENCRYPTION_KEY must decode to exactly 32 bytes for AES-256")
    return key


def encrypt_data(plaintext: str, key: Optional[bytes] = None) -> bytes:
    """Encrypt plaintext with AES-256-GCM, returning nonce + ciphertext + tag."""
    key_to_use = key or load_encryption_key()
    aesgcm = AESGCM(key_to_use)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), associated_data=None)
    return nonce + ciphertext


def decrypt_data(ciphertext: Optional[bytes], key: Optional[bytes] = None) -> str:
    """Decrypt AES-256-GCM data that was stored as nonce + ciphertext + tag."""
    if not ciphertext:
        return ""
    key_to_use = key or load_encryption_key()
    nonce, payload = ciphertext[:12], ciphertext[12:]
    aesgcm = AESGCM(key_to_use)
    return aesgcm.decrypt(nonce, payload, associated_data=None).decode("utf-8")
