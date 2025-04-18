from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .contants import TOKEN_EXPIRE_TIME

class CustomTokenAuthentication(BaseAuthentication):
    """
    Custom authentication class to handle user authentication.
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:
        Authorization: <key_word> <your-token>
    """

    keyword = 'Token'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        
        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
        
        return self.authenticate_credentials(token)
    
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')
        
        #Check if token has expired
        if token.created < timezone.now() - timedelta(seconds=TOKEN_EXPIRE_TIME):
            token.delete() # Delete expired token
            raise exceptions.AuthenticationFailed('Token has expired')

        return (token.user, token)
    
    def authenticate_header(self, request):
        """
        Returns the string to be sent in the WWW-Authenticate header.
        """
        return self.keyword
