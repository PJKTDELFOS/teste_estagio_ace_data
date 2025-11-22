from django.contrib import admin
from.models import *

# Register your models here.
class SalarioInLine(admin.TabularInline):
    model=Salario
    extra=1
    # fk_name = 'salario'
    readonly_fields = ('salario_bruto_formatado','salario_liquido_formatado',)
    fields = ('quantidade_horas_trabalhadas','salario_bruto_formatado','salario_liquido_formatado',)



class DependenteElegivelInLine(admin.TabularInline):
    model=DependenteElegivel
    extra=1
    # fk_name = 'dependenteelegivel'
    ordering = ('-idade',)
    fields = ('nome_dependente','idade',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display=['usuario']
    search_fields=['usuario']
    list_filter=['usuario']
    list_per_page=10
    list_max_show_all=100

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    inlines = SalarioInLine,DependenteElegivelInLine
    list_display=['nome_funcionario','salario_hora','get_numero_dependentes']
    search_fields=['nome_funcionario',]
    list_filter=['nome_funcionario',]
    list_per_page=10
    list_max_show_all=100

    def get_numero_dependentes(self,obj):
        return DependenteElegivel.objects.filter(responsavel=obj.pk).count()
    get_numero_dependentes.short_description='Numero de dependentes'





