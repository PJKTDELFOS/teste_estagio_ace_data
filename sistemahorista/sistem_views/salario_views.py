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
from sistemahorista.forms import *
from sistemahorista.models import *
from datetime import date,timedelta
from django.core.paginator import Paginator
from django.db.models import F, FloatField, ExpressionWrapper,Prefetch,DateField,Func,Case,When,Value,IntegerField
from django.views.generic.edit import DeleteView,CreateView,UpdateView


class CadastrarSalario(LoginRequiredMixin,CreateView):
    model = Salario
    form_class = SalarioForm
    template_name = 'sistemahorista/cadastro_att_salario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_salario'] = context['form']
        context['modo'] = 'criação'
        return context

    def get_initial(self):
        funcionario_pk=self.kwargs.get('pk')
        funcionario=Funcionario.objects.get(pk=funcionario_pk)
        self.funcionario_instance=funcionario

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs['funcionario_instance'] = self.funcionario_instance
        return kwargs

    def form_valid(self, form):
        form.instance.funcionario=self.funcionario_instance
        form.save()
        return render(
            self.request,
            'sistemahorista/popup_fechar.html',

        )

    def form_invalid(self, form):
        messages.error(self.request, 'Operação Invalida')
        return super().form_invalid(form)


class AtualizarSalario(LoginRequiredMixin,UpdateView):
    model = Salario
    form_class = SalarioForm
    template_name = 'sistemahorista/cadastro_att_salario.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funcionario_obj=self.object.funcionario
        # context['form_salario'] = SalarioForm(instance=self.object)
        context['form_salario'] = context['form']
        context['funcionario']=funcionario_obj
        context['modo'] = 'edição'
        return context


    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        funcionario_instance = self.object.funcionario
        kwargs['funcionario_instance'] = funcionario_instance
        return kwargs

    def form_valid(self, form):

        form.save()
        return render(
            self.request,
            'sistemahorista/popup_fechar.html',

        )

    def form_invalid(self, form):
        messages.error(self.request, 'Operação Invalida')
        return super().form_invalid(form)


class DeletarSalario(LoginRequiredMixin,View):

    def post(self,request,*args,**kwargs):
        funcionariopk = get_object_or_404(Funcionario, pk=kwargs['func_pk'])
        salario=get_object_or_404(Salario,pk=kwargs['pk'])
        try:
            salario.delete()
            messages.warning(request, 'Registro de salario excluído com sucesso!')
            return redirect(
                reverse('sistemahorista:detalhe_funcionario', kwargs={'pk':funcionariopk.pk})
            )
        except Exception as e:
            messages.error(request, f'Erro ao excluir registro {e}')
            return redirect(
                reverse('sistemahorista:detalhe_funcionario', kwargs={'pk': funcionariopk.pk})
            )
