import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

User = get_user_model()

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None
        
        jwt_token = self.get_the_token_from_header(jwt_token)

        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.filter(id=payload['user_id']).first()

            print(f"user {user}")
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except Exception as e:
            raise ParseError(str(e))

        return (user, jwt_token)

    @classmethod
    def get_the_token_from_header(cls, token):
        return token.replace('Bearer ', '').strip()
