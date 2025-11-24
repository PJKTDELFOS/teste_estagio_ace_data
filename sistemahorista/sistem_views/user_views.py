from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth import  logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.list import View,ListView
from django.shortcuts import redirect,render
from django.views.generic.edit import DeleteView
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sistemahorista.forms import *
from sistemahorista.models import *
from datetime import date,timedelta
from django.core.paginator import Paginator
from django.db.models import F, FloatField, ExpressionWrapper,Prefetch,DateField,Func,Case,When,Value,IntegerField
from sistemahorista.services.main_services import MainServices
from django.contrib.auth import get_user_model

User=get_user_model() #quando one to one field, usar isso para capturar o User



class ListarUsuario(LoginRequiredMixin,ListView):
    model = User
    template_name = 'sistemahorista/tabela_usuario.html'
    context_object_name = 'usuarios'
    paginate_by = 10



class Cadastro_usuario(View):
    template_name='sistemahorista/cadastro_att_usuario.html'

    def get(self,request,*args,**kwargs):
        return render(
            request,self.template_name,
            {'form_usuario':UsuarioForm(),
             'modo':'criação'}
        )

    def post(self,request,*args,**kwargs):
        form_usuario=UsuarioForm(request.POST)
        try:
            MainServices.criar_usuario(form_usuario)
            messages.success(request, 'Usuario cadastrado com sucesso')
            return redirect(reverse('sistemahorista:tabela_usuarios'))# fazer a tabela depois
        except ValidationError as e:
            messages.error(request,'erro ao cadastrar usuario')
            # form_usuario.is_valid()
            return render(
                request,self.template_name,
                {'form_usuario':form_usuario,
                 'modo':'criação'}
            )











