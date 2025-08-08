from django.contrib.auth.base_user import BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email=None, correo_electronico=None, password=None, **extra_fields):
        correo = correo_electronico or email
        if not correo:
            raise ValueError('El email es obligatorio')
        correo = self.normalize_email(correo)
        user = self.model(correo_electronico=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, correo_electronico=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, correo_electronico=correo_electronico, password=password, **extra_fields)

