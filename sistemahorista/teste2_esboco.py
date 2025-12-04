def fibonacci_teste2(limite):
    if limite <=0:
        if limite <0:
            raise ValueError('o numero deve ser maior que zero')
        return []
    if limite==1:
       return [1]
    if limite==2:
        return[1,1]
    sequencia=[1,1,2]

    for i in range(3,limite):
        termo_anterior=sequencia[-1]
        if termo_anterior %2==0:
            proximo_termo=sequencia[-1]+sequencia[-2]+sequencia[-3]
        else:
            proximo_termo=sequencia[-1]+sequencia[-2]
        sequencia.append(proximo_termo)
    return sequencia[:limite]

print(fibonacci_teste2(11))
teste=[1-1-2-4-7-11-18-36-65-101-166]








