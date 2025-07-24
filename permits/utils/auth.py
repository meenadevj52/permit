from rest_framework.authtoken.models import Token

def get_user_token(user):
  token, _ = Token.objects.get_or_create(user=user)
  return token