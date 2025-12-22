from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, role="User", password=None):
        if email is None:
            ValueError("email field is required...")

        email = self.normalize_email(email=email)    
        user = self.model(
            first_name = first_name,
            last_name=last_name,
            email=email,
            role=role
        )

        user.is_active=True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_slave(self, first_name, last_name, email , password=None):
        user = self.create_user(first_name, last_name ,email, role="Slave", password=password)
        user.is_slave=True
        user.save(using=self._db)
        return user
    
    def create_master(self, first_name, last_name, email , password=None):
        user = self.create_user(first_name, last_name ,email, role="Master", password=password)
        user.is_master=True
        user.save(using=self._db)
        return user
    
    def create_admin(self, first_name, last_name, email, password=None):
        user = self.create_user(first_name, last_name, email, role="Admin", password=password)
        user.is_slave=True
        user.is_admin=True
        user.is_master=True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(first_name, last_name, email, role="SuperUser", password=password)
        user.is_slave=True
        user.is_admin=True
        user.is_master=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
    
