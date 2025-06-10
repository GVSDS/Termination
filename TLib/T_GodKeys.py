from .T_imports import *


class GodKeys:
    def __init__(self, key=None):
        self.key = key if key else b"TerminationGodKeyAndLOVE3GZSorry"
        self.aesgcm = AESGCM(self.key)
    def IsGK(self, data) -> bool:
        if isinstance(data, bytes):
            return len(data) >= 28 and data[:4] == b"GKBD"
        elif isinstance(data, str):
            return len(data) >= 56 and data.startswith("GKBD")
        return False
    def encrypt(self, s: str) -> bytes:
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, repr(s).encode(), None)
        return b"GKBD" + nonce + ciphertext
    def decrypt(self, s: bytes, con=False) -> str:
        if not self.IsGK(s):
            return s if con else Exception("Invalid GKBD format")
        nonce, ciphertext = s[4:16], s[16:]
        try:
            plaintext = self.aesgcm.decrypt(nonce, ciphertext, None)
            return ast.literal_eval(plaintext.decode())
        except (ValueError, SyntaxError):
            return plaintext.decode() if con else Exception("Invalid data")
    def encrypt_16(self, s: str) -> str:
        binary = self.encrypt(s)
        return "GKBD" + binary[4:].hex()
    def decrypt_16(self, s: str, con=False) -> str:
        if not self.IsGK(s):
            return s if con else Exception("Invalid GKBD hex format")
        try:
            binary = b"GKBD" + bytes.fromhex(s[4:])
            return self.decrypt(binary, con)
        except ValueError:
            return s if con else Exception("Invalid hex data")