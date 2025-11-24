from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth import  logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.list import View,ListView
from django.shortcuts import redirect,render
from django.views.generic.edit import DeleteView,CreateView,UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sistemahorista.forms import *
from sistemahorista.models import *
from datetime import date,timedelta
from django.core.paginator import Paginator
from django.db.models import F, FloatField, ExpressionWrapper,Prefetch,DateField,Func,Case,When,Value,IntegerField


class ListarFuncionarios(LoginRequiredMixin,ListView):
    model = Funcionario
    template_name = 'sistemahorista/tabela_funcionario.html'
    context_object_name = 'funcionarios'
    paginate_by = 10


class CadastrarFuncionario(LoginRequiredMixin,CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'sistemahorista/cadastro_att_funcionario.html'
    success_url = reverse_lazy('sistemahorista:tabela_funcionarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_funcionario'] = FuncionarioForm()
        context['modo'] = 'criação'
        return context

    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, 'Funcionario cadastrado com sucesso')
            return super().form_valid(form)
        except ValidationError as e:
            messages.error(self.request, 'Erro ao cadastrar funcionario')
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Operação Invalida')
        return super().form_invalid(form)

class AtualizarFuncionario(LoginRequiredMixin,UpdateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'sistemahorista/cadastro_att_funcionario.html'
    success_url = reverse_lazy('sistemahorista:tabela_funcionarios')
    context_object_name = 'funcionario'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_funcionario'] = FuncionarioForm(instance=self.object)
        context['modo'] = 'edição'
        return context

    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, 'Funcionario atualizado com sucesso')
            return super().form_valid(form)
        except ValidationError as e:
            messages.error(self.request, 'Erro ao atualizar funcionario')
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Operacao invalida')
        return super().form_invalid(form)

class DeletarFuncionario(LoginRequiredMixin,View):

    def post(self,request,*args,**kwargs):
        funcionario=get_object_or_404(Funcionario,pk=kwargs['pk'])
        try:
            funcionario.delete()
            messages.warning(request, 'funcionario excluído com sucesso!')
            return redirect('sistemahorista:tabela_funcionarios')
        except ValidationError as e:
            messages.error(request, 'Erro ao deletar funcionario')
            return redirect('sistemahorista:tabela_funcionarios')

class Funcionario_detalhe(LoginRequiredMixin,DetailView):
    model = Funcionario
    template_name = 'sistemahorista/fichafuncionario.html'
    context_object_name = 'funcionario'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salarios'] = Salario.objects.filter(funcionario=self.object)
        context['dependentes'] = DependenteElegivel.objects.filter(responsavel=self.object)

        return context













