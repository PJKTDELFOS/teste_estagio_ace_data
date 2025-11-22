from curses.ascii import isdigit

from django import forms
from django.contrib.auth import get_user_model
from.models import Salario,Funcionario,DependenteElegivel
from decimal import Decimal



User=get_user_model()

class UsuarioForm(forms.ModelForm):
    username = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['username'].required = False
            self.fields['password'].required = False

    def clean(self):
        cleaned_data = super().clean()
        username_data = cleaned_data.get('username')
        password_data = cleaned_data.get('password')
        email_data = cleaned_data.get('email')

        if not self.instance.pk:
            if not password_data:
                self.add_error(
                    'password',
                    'Preenchimento de senha obrigatorio para cadastro de novos usuarios'
                )

            if not username_data:
                self.add_error('username',
                               'Preenchimento de nome de usuario obrigatorio para cadastro de novos usuarios')
        if password_data and len(password_data) < 6:
            self.add_error('password',
                           'Senha deve ter no minimo 6 caracteres')


        usuario_db=User.objects.none()
        if username_data:
            usuario_db = User.objects.filter(
                username__iexact=username_data
            )

        email_db = User.objects.none()
        if email_data:
            email_db = User.objects.filter(
                email__iexact=email_data
            )


        if self.instance.pk:
            usuario_db = usuario_db.exclude(pk=self.instance.pk)
            email_db = email_db.exclude(pk=self.instance.pk)

        if usuario_db.exists():
            self.add_error(
                'username',
                f'o usuario {username_data} ja existe no banco de dados'
            )
        if email_db.exists():
            self.add_error(
                'email',
                f'o email {email_data} ja existe no banco de dados'
            )

        return cleaned_data

class FuncionarioForm(forms.ModelForm):
    nome_funcionario = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    salario_hora = forms.DecimalField(max_digits=10, decimal_places=2, required=True,
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Funcionario
        fields = ['nome_funcionario', 'salario_hora']

    def __init__(self):
        super(FuncionarioForm, self).__init__()
        if self.instance and self.instance.pk:
            self.fields['nome_funcionario'].required = False
            self.fields['salario_hora'].required = True

    def clean(self):
        cleaned_data = super().clean()
        nome_funcionario_data = cleaned_data.get('nome_funcionario')
        salario_hora_data = cleaned_data.get('salario_hora')


        if not self.instance.pk:
            if not nome_funcionario_data:
                self.add_error(
                    'nome_funcionario',
                    'Preenchimento obrigatorio do nome do funcionario'
                )

            if not salario_hora_data:
                self.add_error('salario_hora',
                               'Preenchimento obrigatorio  do salario-hora do funcionario')
        if salario_hora_data <0.00:
            self.add_error('salario_hora',
                           'Digite o salario corretamente, valor negativo')


        if salario_hora_data is not None and  not isinstance(salario_hora_data,
                          (int,float,Decimal)):
            self.add_error('salario_hora',
                           'Digite um valor correto')


        return cleaned_data

class DependenteElegivelForm(forms.ModelForm):

    responsavel_pelo_dependente=forms.CharField(
        label='Responsavel pelo dependente',
        required=False,
        widget=forms.TextInput(
            attrs={
                'readonly':'readonly',
                'class':'form-control'
            }
        )
    )


    nome_dependente = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    idade = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DependenteElegivel
        fields = ['responsavel','nome_dependente', 'idade']

    def __init__(self,*args,**kwargs):

        self.responsavel_instance=kwargs.pop('responsavel_instance',None)
        super(DependenteElegivelForm, self).__init__(*args,**kwargs)
        self.fields['responsavel'].required=True

        funcionario_obj=None

        if self.responsavel_instance:
            funcionario_obj=self.responsavel_instance
        elif self.instance and self.instance.pk:
            funcionario_obj=self.instance.responsavel

            self.fields['nome_dependente'].required=False
            self.fields['idade'].required=False

        if funcionario_obj:
            self.fields['responsavel_pelo_dependente'].initial=funcionario_obj.nome_funcionario
            self.fields['responsavel'].initial=funcionario_obj.pk








