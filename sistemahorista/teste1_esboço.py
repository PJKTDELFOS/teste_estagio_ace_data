'''
1) Desenvolver um sistema para calcular o valor que será pago a um empregado horista. O
usuário deverá informar o valor do salário hora, a quantidade de horas trabalhadas no
mês e a quantidade de filhos menores de 14 anos. A partir daí o sistema deve calcular o
salário bruto, salário família e o salário líquido do empregado (salário bruto + salário
família). Para o cálculo do salário família, levar em consideração:
a) Se o salário bruto for até R$ 788,00 o salário família será de R$ 30,50 para cada
filho.
b) Se o salário bruto for acima de R$ 788,00 até R$ 1.100,00 o salário família será de
R$ 18,50 por filho.
c) Se o salário bruto for acima de R$ 1.100,00 o salário família será de R$ 11,90 por
filho.
'''

class Empregado:
    def __init__(self,nome,valor_hora,quantidade_horas,quantidade_filhos):
        self.nome=nome
        self.quantidade_horas=quantidade_horas
        self.valor_hora=valor_hora
        self.quantidade_filhos=quantidade_filhos


    def salario_familia(self):
        salario_bruto=self.salario_bruto()
        if salario_bruto<=788:
            salario_filho=30.50
            salario_familia=self.quantidade_filhos*salario_filho
            return salario_familia
        elif 788 < salario_bruto <=1100:
            salario_filho=18.50
            salario_familia=self.quantidade_filhos*salario_filho
            return salario_familia
        elif salario_bruto >1100:
            salario_filho=11.90
            salario_familia=self.quantidade_filhos*salario_filho
            return salario_familia

    def salario_bruto(self):
        return self.quantidade_horas*self.valor_hora


    def salario_liquido(self):
        salario_bruto=self.salario_bruto()
        salario_familia=self.salario_familia()
        return salario_bruto+salario_familia

    def relatorio(self):
        print(f'Nome completo: {self.nome}\n'
              f'Dependentes:{self.quantidade_filhos}\n'
              f'Horas trabalhadas:{self.quantidade_horas} horas no mes\n'
              f'Salário bruto:R$ {self.salario_bruto():.2f}\n'
              f'Salário familia:R$ {self.salario_familia():.2f} \n'
              f'Salário total liquido: R$:{self.salario_liquido():.2f}')



func=Empregado('albert',5,176,3)
func.relatorio()



