from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth import  logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.list import View,ListView
from django.shortcuts import redirect,render
from django.views.generic.edit import DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from datetime import date,timedelta
from django.core.paginator import Paginator
from django.db.models import F, FloatField, ExpressionWrapper,Prefetch,DateField,Func,Case,When,Value,IntegerField


# Create your views here.

#<______________________________views de suporte_____________________________________________>#

class Login(LoginView):
    template_name = 'sistemahorista/login.html'
    success_url = reverse_lazy('sistemahorista:tela_inicial')
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        messages.success(self.request,f'usuario {form.get_user().username} logado com sucesso')
        return super().form_valid(form)

    def form_invalid(self, form):
        usuario_ativo=form.get_user().is_active
        senha_valida=form.get_user().check_password(form.data['password'])
        if not usuario_ativo:
            messages.warning(self.request, f'Usuario ainda nao esta ativo no sistema, procure o administrador')

        if not senha_valida:
            messages.warning(self.request, f'Senha Invalida')

        return super().form_invalid(form)

class Logout(LoginRequiredMixin,View):

    def get(self,*args,**kwargs):
        logout(self.request)
        return redirect('sistemahorista:login_sistema')










def paginainicial(request):
    return render(request, 'sistemahorista/tela_inicial_vazia.html')