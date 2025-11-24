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



class Cadastro_usuario(CreateView):
    model = User
    form_class = UsuarioForm
    template_name = 'sistemahorista/cadastro_att_usuario.html'
    success_url = reverse_lazy('sistemahorista:tabela_usuarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_usuario'] = UsuarioForm()
        context['modo'] = 'criação'
        return context

    def form_valid(self, form):
        try:
            MainServices.criar_usuario(form)
            messages.success(self.request, 'Usuario cadastrado com sucesso')
            return super().form_valid(form)
        except ValidationError as e:
            messages.error(self.request, 'Erro ao cadastrar usuario')
            return super().form_invalid(form)

class AtualizarUsuario(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UsuarioForm
    template_name = 'sistemahorista/cadastro_att_usuario.html'
    success_url = reverse_lazy('sistemahorista:tabela_usuarios')
    context_object_name = 'usuario'
    pk_url_kwarg = 'pk'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_usuario'] = UsuarioForm(instance=self.object)
        context['modo'] = 'edição'
        return context

    def form_valid(self, form_usuario):
        messages.success(self.request, 'Usuario atualizado com sucesso')
        return super().form_valid(form_usuario)

    def form_invalid(self, form_usuario):
        messages.error(self.request, 'Erro ao atualizar usuario')
        return super().form_invalid(form_usuario)

class DeletarUsuario(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        usuario=get_object_or_404(User,pk=kwargs['pk'])
        try:
            usuario.delete()
            messages.warning(request, 'usuario excluído com sucesso!')
        except:
            messages.error(request, 'Erro ao excluir.')

        return redirect('sistemahorista:tabela_usuarios')
























