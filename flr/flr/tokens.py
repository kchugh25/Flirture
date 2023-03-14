from django.contrib.auth.tokens import PasswordResetTokenGenerator

from six import text_type

class TokenGenereator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user, timestamp):
        return(
            
        )