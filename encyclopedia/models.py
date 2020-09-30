from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class User(AbstractUser):
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.username

class Entry(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=4000)

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = ['title']

    def __str__(self):
        return self.title