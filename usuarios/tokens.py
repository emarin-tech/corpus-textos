from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Clave: ata el token SOLO a pk + timestamp + email_verificado
        # Cambiar is_active, password, o last_login NO lo invalida.
        return f"{user.pk}{timestamp}{getattr(user, 'email_verificado', False)}"

email_token_generator = EmailVerificationTokenGenerator()
