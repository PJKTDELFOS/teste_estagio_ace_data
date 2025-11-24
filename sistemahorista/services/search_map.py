from sistemahorista.models import *



mapa_modelos = {
    'funcionario': {
        'queryset': Funcionario.objects.all(),
        'campos': ['nome_funcionario', ]
        # 'Arquivos' removido porque FileField não é pesquisável por texto
    }
}
