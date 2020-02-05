from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class CustomUserManager(UserManager):
    pass


class User(AbstractUser):
    email = models.CharField(unique=True, max_length=254)
    is_author = models.BooleanField(default=False)

    class Meta(AbstractUser.Meta):
        pass
        # db_table = 'auth_user'
        #swappable = 'AUTH_USER_MODEL'

    def get_absolute_url(self):
        return reverse('blog:author', args=[str(self.id)])

    # def save(self, *args, **kwargs):
    #     self.email = self.email.lower()
    #     self.username = self.username.lower()
    #     return super(User, self).save(*args, **kwargs)
