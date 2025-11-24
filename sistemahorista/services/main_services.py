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
        termo_limpo_num = ''.join(filter(str.isdigit, termo))
        hash_num = hashlib.sha256(termo_limpo_num.encode('utf-8')).hexdigest()
        hash_email = hashlib.sha256(termo.lower().encode('utf-8')).hexdigest()
        q_hash_match = Q()
        if 'cpf_hash' in campos:
            q_hash_match |= Q(cpf_hash__iexact=hash_num)
        if 'tel_contato_hash' in campos:
            q_hash_match |= Q(tel_contato_hash__iexact=hash_num)
        if 'email_hash' in campos:
            q_hash_match |= Q(email_hash__iexact=hash_email)
        q_text_match = Q()
        palavras = termo.split()
        for palavra in palavras:
            q_or_palavra = Q()
            for campo in campos:
                if campo not in ['cpf_hash', 'tel_contato_hash', 'email_hash']:
                    q_or_palavra |= Q(
                        **{f'{campo}__icontains': palavra}
                    )

            if q_text_match:
                q_text_match &= q_or_palavra
            else:
                q_text_match = q_or_palavra
        q_final = q_hash_match | q_text_match
        return queryset.filter(q_final).distinct()











