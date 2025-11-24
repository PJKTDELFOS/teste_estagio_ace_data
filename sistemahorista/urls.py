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

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from sistemahorista.sistem_views import ListarUsuario
from sistemahorista.views import Login,Logout,paginainicial
from sistemahorista.sistem_views.user_views import Cadastro_usuario


app_name='sistemahorista'
urlpatterns = [
#<______________________________Urls de suporte_____________________________________________>#
    path('', Login.as_view(), name='login_sistema'),
    path('logout/', Logout.as_view(), name='logout_sistema'),
    path('telainicial/', paginainicial, name='tela_inicial'),

#<______________________________Urls de usuario_____________________________________________>#

    path('cadastro_usuario/', Cadastro_usuario.as_view(), name='cadastro_usuario'),
    path('tabela_usuarios',ListarUsuario.as_view(),name='tabela_usuarios')



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
