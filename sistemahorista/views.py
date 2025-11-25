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
from sistemahorista.services.main_services import MainServices
from sistemahorista.services.search_map import mapa_modelos

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


class Busca(LoginRequiredMixin,View):

    def get(self, request):
        termo=request.GET.get('q','').strip()
        resultados={}
        if termo:
            for modelo_nome,info in mapa_modelos.items():
                queryset=info['queryset']
                campos=info['campos']
                qs_resultados=MainServices.busca_centralizada(queryset,termo,campos)

                if qs_resultados.exists():
                    resultados[modelo_nome]=qs_resultados


        return render(request, f'sistemahorista/busca.html', {
            'termo': termo,
            'resultados': resultados,
        })

@login_required()
def paginainicial(request):
    return render(request, 'sistemahorista/tela_inicial_vazia.html')


@login_required()
def fibonacci(request):
    sequencia = []
    esta_na_sequencia = False
    limite_sequencia_fibonacci=None

    if request.method=='POST':
        try:
            limite_sequencia_fibonacci = int(request.POST.get('numero'))

            if limite_sequencia_fibonacci <0:
                raise ValueError('o numero deve ser maior que zero')

            a,b=0,1
            if  limite_sequencia_fibonacci >=1:
                sequencia.append(a)
            if limite_sequencia_fibonacci >=2:
                sequencia.append(b)

            for _ in range(2,limite_sequencia_fibonacci):
                c=a+b
                sequencia.append(c)
                a=b
                b=c
        except ValueError as e:
            sequencia=[f'erro{e}']
            esta_na_sequencia = False

    if limite_sequencia_fibonacci in sequencia:
        esta_na_sequencia = True
    contexto={
        'resultado_sequencia':sequencia,
        'numero_na_sequencia': esta_na_sequencia,
         'numero_digitado':limite_sequencia_fibonacci
    }
    return render(request,'sistemahorista/fibonacci.html',contexto)



