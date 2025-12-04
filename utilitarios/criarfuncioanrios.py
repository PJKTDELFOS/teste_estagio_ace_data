import os
import sys
from datetime import datetime
from pathlib import Path
from random import choice

import django
from django.conf import settings
DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 30


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistemarh.settings')
django.setup()
if __name__ =='__main__':
    from sistemahorista.models import Funcionario,Salario,DependenteElegivel
    import faker
    Funcionario.objects.all().delete()
    Salario.objects.all().delete()
    DependenteElegivel.objects.all().delete()
    fake=faker.Faker('pt_BR')


    django_funcionarios=[Funcionario(nome_funcionario=fake.name(),
                                     salario_hora=fake.random_int(min=10,max=50))
                                    for _ in range(NUMBER_OF_OBJECTS)]

    dependentes=[
        DependenteElegivel(
            responsavel=choice(django_funcionarios),
            nome_dependente=fake.name(),
            idade=fake.random_int(min=10,max=14)
        )for _ in range (NUMBER_OF_OBJECTS)
    ]
    salario_django=[
        Salario(
            funcionario=choice(django_funcionarios),
            quantidade_horas_trabalhadas=fake.random_int(min=10,max=50) )
            for _ in range( NUMBER_OF_OBJECTS)
    ]


    Funcionario.objects.bulk_create(django_funcionarios)
    DependenteElegivel.objects.bulk_create(dependentes)
    if DependenteElegivel.objects.exists():
        for dependente in DependenteElegivel.objects.all():
            dependente.save()
            Salario.objects.bulk_create(salario_django)
            for salario in Salario.objects.all():
                salario.save()










