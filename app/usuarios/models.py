from django.db import models

class Usuario(models.Model):
    codUsuario = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=10)