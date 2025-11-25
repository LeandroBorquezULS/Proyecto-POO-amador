"""
auth.py

Manejo de autenticación local: creación de contraseña la primera vez,
almacenamiento de hash + salt en archivo JSON (fuera del código),
verificación mediante PBKDF2-HMAC (SHA256).

Archivo por defecto: auth.json (en el mismo directorio).
"""

import os
import json
import hashlib
import secrets
from typing import Tuple
 
#AUTH_FILE = os.path.join(os.path.expanduser("~"), ".amador_auth.json")
AUTH_FILE = ("auth.json")
# Si quieres que quede en el directorio del proyecto en vez del home,
# puedes cambiar la ruta por: AUTH_FILE = "auth.json"


def _generar_salt() -> bytes:
    """Genera un salt criptográficamente seguro."""
    return secrets.token_bytes(16)


def _hash_password(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    """
    Hashea la contraseña con PBKDF2-HMAC-SHA256.

    Args:
        password (str): Contraseña en texto plano.
        salt (bytes): Salt.
        iterations (int): Número de iteraciones.

    Returns:
        bytes: Hash derivado.
    """
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)


def existe_contrasena() -> bool:
    """Retorna True si ya existe un archivo de autenticación con hash."""
    return os.path.exists(AUTH_FILE)


def establecer_contrasena(password: str) -> None:
    """
    Establece la contraseña por primera vez y la guarda (salt + hash).

    Args:
        password (str): Contraseña en texto plano.
    """
    salt = _generar_salt()
    derived = _hash_password(password, salt)
    payload = {
        "salt": salt.hex(),
        "hash": derived.hex(),
        "iterations": 200_000
    }
    with open(AUTH_FILE, 'w', encoding='utf-8') as f:
        json.dump(payload, f)


def verificar_contrasena(password: str) -> bool:
    """
    Verifica si la contraseña dada coincide con la almacenada.

    Args:
        password (str): Contraseña en texto plano.

    Returns:
        bool: True si coincide.
    """
    if not existe_contrasena():
        return False
    with open(AUTH_FILE, 'r', encoding='utf-8') as f:
        payload = json.load(f)
    salt = bytes.fromhex(payload["salt"])
    expected = bytes.fromhex(payload["hash"])
    iterations = payload.get("iterations", 200_000)
    derived = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)
    return secrets.compare_digest(derived, expected)
