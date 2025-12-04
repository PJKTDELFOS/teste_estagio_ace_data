"""
URL configuration for sistemarh project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from sistemahorista.sistem_views.dependente_views import CadastrarDependente, AtualizarDependente, DeletarDependente
from sistemahorista.sistem_views.funcionario_views import (
    ListarFuncionarios, CadastrarFuncionario, AtualizarFuncionario, DeletarFuncionario, Funcionario_detalhe)
from sistemahorista.sistem_views.salario_views import CadastrarSalario, AtualizarSalario, DeletarSalario
from sistemahorista.sistem_views.user_views import Cadastro_usuario, ListarUsuario, AtualizarUsuario, DeletarUsuario
from sistemahorista.views import Login, Logout, paginainicial, Busca,fibonacci,receber_array

app_name = 'sistemahorista'
urlpatterns = [
    # <______________________________Urls de suporte_____________________________________________>#
    path('', Login.as_view(), name='login_sistema'),
    path('logout/', Logout.as_view(), name='logout_sistema'),
    path('telainicial/', paginainicial, name='tela_inicial'),

    path('busca', Busca.as_view(), name='busca_dinamica'),
    path('fibonacci/', fibonacci, name='fibonacci'),
    path('receber_array/', receber_array, name='receber_array '),

# <______________________________Urls de usuario_____________________________________________>#

    path('cadastro_usuario/', Cadastro_usuario.as_view(), name='cadastro_usuario'),
    path('tabela_usuarios', ListarUsuario.as_view(), name='tabela_usuarios'),
    path('tabela_usuarios/<int:pk>/atualizar_usuario/', AtualizarUsuario.as_view(), name='atualizar_usuario'),
    path('tabela_usuarios/<int:pk>/deletar_usuario/', DeletarUsuario.as_view(), name='deletar_usuario'),
 # <______________________________Urls de Funcionarios_____________________________________________>#

    path('tabela_funcionarios', ListarFuncionarios.as_view(), name='tabela_funcionarios'),
    path('cadastro_funcionario/', CadastrarFuncionario.as_view(), name='cadastro_funcionario'),
    path('tabela_usuarios/<int:pk>/atualizar_funcionario/',
         AtualizarFuncionario.as_view(), name='atualizar_funcionario'),
    path('tabela_usuarios/<int:pk>/deletar_funcionario/',
         DeletarFuncionario.as_view(), name='deletar_funcionario'),
    path('tabela_usuarios/<int:pk>/ficha_funcionario/',
         Funcionario_detalhe.as_view(), name='detalhe_funcionario'),

# <______________________________Urls de Dependente_____________________________________________>#

    path('tabela_usuarios/<int:pk>/cadastro_dependente/',
         CadastrarDependente.as_view(), name='cadastrar_dependente'),

    path('tabela_usuarios/<int:pk>/atualizar_dependente/',
         AtualizarDependente.as_view(), name='atualizar_dependente'),
    path('tabela_usuarios/<int:func_pk>/deletar_dependente/<int:pk>',
         DeletarDependente.as_view(), name='deletar_dependente'),

# <______________________________Urls de Salario_____________________________________________>#

    path('tabela_usuarios/<int:pk>/cadastro_salario/',
         CadastrarSalario.as_view(), name='cadastrar_salario'),

    path('tabela_usuarios/<int:pk>/atualizar_salario/',
         AtualizarSalario.as_view(), name='atualizar_salario'),
    path('tabela_usuarios/<int:func_pk>/deletar_salario/<int:pk>',
         DeletarSalario.as_view(), name='deletar_salario'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
