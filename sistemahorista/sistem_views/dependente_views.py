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
from django.core.exceptions import ValidationError



class CadastrarDependente(LoginRequiredMixin,CreateView):
    model = DependenteElegivel
    form_class = DependenteElegivelForm
    template_name = 'sistemahorista/cadastro_att_dependente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_dependente'] = context['form']
        context['modo'] = 'criação'
        return context

    def get_initial(self):
        funcionario_pk=self.kwargs.get('pk')
        funcionario=Funcionario.objects.get(pk=funcionario_pk)
        self.funcionario_instance=funcionario


    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs['responsavel_instance'] = self.funcionario_instance
        return kwargs

    def form_valid(self, form):
        form.instance.responsavel=self.funcionario_instance
        form.save()
        return render(
            self.request,
            'sistemahorista/popup_fechar.html',

        )

    def form_invalid(self, form):
        messages.error(self.request, 'Operação Invalida')
        return super().form_invalid(form)


class AtualizarDependente(LoginRequiredMixin,UpdateView):
    model = DependenteElegivel
    form_class = DependenteElegivelForm
    template_name = 'sistemahorista/cadastro_att_dependente.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funcionario_obj=self.object.responsavel
        context['form_dependente'] = DependenteElegivelForm(instance=self.object)
        context['form_dependente'] = context['form']
        context['funcionario']=funcionario_obj
        context['modo'] = 'edição'
        return context


    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        funcionario_obj = self.object.responsavel
        kwargs['responsavel_instance'] = funcionario_obj
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


class DeletarDependente(LoginRequiredMixin,View):

    def post(self,request,*args,**kwargs):
        funcionariopk = get_object_or_404(Funcionario, pk=kwargs['func_pk'])
        dependente=get_object_or_404(DependenteElegivel,pk=kwargs['pk'])
        try:
            dependente.delete()
            messages.warning(request, 'dependente excluído com sucesso!')
            return redirect(
                reverse('sistemahorista:detalhe_funcionario', kwargs={'pk':funcionariopk.pk})
            )
        except ValidationError as e:
            messages.error(request, 'Erro ao deletar dependente')
            return redirect(
                reverse('sistemahorista:detalhe_funcionario', kwargs={'pk': funcionariopk.pk})
            )














