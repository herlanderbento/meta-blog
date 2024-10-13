
import jwt
import datetime
from django.conf import settings
from typing import Any, Dict, Optional

from src.core.shared.application.token_generator import ITokenGenerator


class JwtAuthService(ITokenGenerator):
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = "HS256"
        self.expiration_delta = datetime.timedelta(seconds=3600)

    def generate(self, payload: Dict[str, Any]) -> str:
        expiration = datetime.datetime.now(datetime.timezone.utc) + self.expiration_delta
        payload["exp"] = expiration

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None  
        except jwt.InvalidTokenError:
            return None 

    def verify_token(self, token: str) -> bool:
        return self.decode_token(token) is not None
