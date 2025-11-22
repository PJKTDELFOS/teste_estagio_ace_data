from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib import admin
from typing import List
# Create your models here.
'''
1) Desenvolver um sistema para calcular o valor que será pago a um empregado horista. 
Ousuário deverá informar o 
valor do salário hora, 
a quantidade de horas trabalhadas nomês e 
a quantidade de filhos menores de 14 anos. 

A partir daí o sistema deve calcular o
salário bruto, salário família e o salário líquido do empregado (salário bruto + salário
família). Para o cálculo do salário família, levar em consideração:
a) Se o salário bruto for até R$ 788,00 o salário família será de R$ 30,50 para cada
filho.
b) Se o salário bruto for acima de R$ 788,00 até R$ 1.100,00 o salário família será de
R$ 18,50 por filho.
c) Se o salário bruto for acima de R$ 1.100,00 o salário família será de R$ 11,90 por
filho.

comntinuar os testes de idade, e valor do salario
'''

class Usuario(models.Model):
    usuario=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,unique=True,null=False,
                                 blank=False,related_name='usuario',verbose_name='Usuário',max_length=255)



    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name='Usuário'
        verbose_name_plural='Usuários'


class Funcionario(models.Model):
    nome_funcionario=models.CharField(max_length=255,blank=False,null=False,verbose_name='Nome completo')
    salario_hora=models.DecimalField(max_digits=10,decimal_places=2,blank=False,null=False,verbose_name='salario-hora')


    def __str__(self):
        return self.nome_funcionario

    class Meta:
        verbose_name='Funcionário'
        verbose_name_plural='Funcionários'


class DependenteElegivel(models.Model):
    responsavel=models.ForeignKey(Funcionario,on_delete=models.CASCADE,blank=False,null=False,
                                  related_name='dependenteelegivel',
                                  verbose_name='Responsável')
    nome_dependente=models.CharField(max_length=255,blank=False,null=False,verbose_name='Nome completo')
    idade=models.IntegerField(blank=False,null=False,verbose_name='Idade')

    def __str__(self):
        return self.nome_dependente
    class Meta:
        verbose_name='Dependente'
        verbose_name_plural='Dependentes'



class Salario(models.Model):
    funcionario=models.ForeignKey(Funcionario,on_delete=models.CASCADE,blank=False,null=False,related_name='salario',
                                  verbose_name='Funcionario')
    quantidade_horas_trabalhadas = models.DecimalField(max_digits=10, decimal_places=2,
                                                       blank=False, null=False, verbose_name='Horas Trabalhadas')
    salario_liquido=models.DecimalField(max_digits=10, decimal_places=2,editable=False,null=True,blank=True)
    salario_bruto=models.DecimalField(max_digits=10, decimal_places=2,editable=False,null=True,blank=True)



    def __str__(self):
        return self.funcionario.nome_funcionario

    class Meta:
        verbose_name='Salario'
        verbose_name_plural='Salarios'


    def _calc_salario_bruto(self):
        horas_trabalhadas=self.quantidade_horas_trabalhadas
        salario_hora=self.funcionario.salario_hora
        salario_bruto=horas_trabalhadas*salario_hora
        self.salario_bruto=salario_bruto
        return salario_bruto



    def _calc_salario_liquido(self):
        salario_bruto = self._calc_salario_bruto()
        numero_de_dependentes=DependenteElegivel.objects.filter(responsavel=self.funcionario,idade__lte=14).count()

        if salario_bruto<=788:
            salario_familia=int(numero_de_dependentes)*30.5
            salario_liquido=salario_bruto+Decimal(salario_familia)
            self.salario_liquido=salario_liquido
            return salario_liquido
        elif 788 < salario_bruto <= 1100:
            salario_familia=int(numero_de_dependentes)*18.5
            salario_liquido = salario_bruto + Decimal(salario_familia)
            self.salario_liquido = salario_liquido
            return salario_liquido
        elif salario_bruto >1100:
            salario_familia=int(numero_de_dependentes)*11.9
            salario_liquido=salario_bruto+Decimal(salario_familia)
            self.salario_liquido = salario_liquido
            return salario_liquido


    def save(self,*args,**kwargs):
        salario_bruto=self._calc_salario_bruto()
        self.salario_bruto=salario_bruto

        salario_liquido=self._calc_salario_liquido()
        self.salario_liquido=salario_liquido
        super_save=super().save(*args,**kwargs)
        return super_save


    @property
    @admin.display(description='Salário Bruto')
    def salario_bruto_formatado(self):
        if self.salario_bruto:
            return f'R$ {self.salario_bruto:.2f}'
        return None


    @property
    @admin.display(description='Salário liquido')
    def salario_liquido_formatado(self):
        if self.salario_liquido:
            return f'R$ {self.salario_liquido:.2f}'
        return None










