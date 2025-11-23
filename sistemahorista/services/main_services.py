from sistemahorista.forms import *
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
import hashlib



class MainServices:

    @staticmethod
    def criar_usuario(form_usuario):

        if not form_usuario.is_valid():
            raise ValidationError(form_usuario.errors)

        user=form_usuario.save(commit=False)
        user.set_password(form_usuario.cleaned_data['password'])
        user.is_active=False
        user.save()

        return user







