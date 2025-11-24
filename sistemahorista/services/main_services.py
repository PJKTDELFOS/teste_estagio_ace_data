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

    @staticmethod
    def busca_centralizada(queryset, termo, campos):
        if not termo:
            return queryset.none()
        termo=str(termo).strip().lower()
        q_match = Q()
        palavras=termo.split()
        q_text_match=Q()
        for palavra in palavras:
            q_or_palavra_em_campos=Q()
            for campo in campos:
                q_or_palavra_em_campos |= Q(**{f'{campo}__icontains': palavra})
            q_text_match |= q_or_palavra_em_campos

        return queryset.filter(q_text_match).distinct()











