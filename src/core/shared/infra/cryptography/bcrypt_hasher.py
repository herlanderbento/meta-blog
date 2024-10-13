import bcrypt

from src.core.shared.application.cryptography import ICryptography


class BcryptHasher(ICryptography):

    def hash(self, plain: str) -> str:
        salt = bcrypt.gensalt(8)
        hashed_password = bcrypt.hashpw(plain.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    def verify(self, plain: str, hash: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), hash.encode("utf-8"))
