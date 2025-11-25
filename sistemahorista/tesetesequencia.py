tamanho_sequencia=int(input('digite tamanho da sequencia'))
sequencia = []


while len(sequencia)< tamanho_sequencia:
    valor = int(input('digite um valor'))
    sequencia.append(valor)
maior_valor_sequencia=max(sequencia)
minimo_valor_sequencia=min(sequencia)
print(sequencia)
print(maior_valor_sequencia)
print(minimo_valor_sequencia)

