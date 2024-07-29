# Falta implementar Chomsky corretamente

def converter_gramatica(arquivo):
    gramatica = {}
    with open(arquivo, 'r') as arquivo:
        for linha in arquivo:
            lado_esquerdo, lado_direito = linha.strip().split("->")
            lado_esquerdo = lado_esquerdo.strip()
            producoes = [producao.strip() for producao in lado_direito.split("|")]
            gramatica[lado_esquerdo] = producoes
    return gramatica

def formatar_gramatica(gramatica):
    for simbolo, producoes in gramatica.items():
        print(f"{simbolo} -> {' | '.join(producoes)}")

def remover_producoes_vazias(gramatica):
    producoes_vazias = {simbolo for simbolo, producoes in gramatica.items() if '#' in producoes} # estou utilizando '#' para representar vazio
    nova_gramatica = {simbolo: [p for p in producoes if p != '#'] for simbolo, producoes in gramatica.items()}
    
    while True:
        modificou = False
        for simbolo_vazio in producoes_vazias:
            for simbolo, producoes in list(nova_gramatica.items()):
                novas_producoes = []
                for producao in producoes:
                    if simbolo_vazio in producao:
                        novas_producoes.append(producao.replace(simbolo_vazio, ''))
                novas_producoes = list(set(novas_producoes) - set(producoes))
                if novas_producoes:
                    nova_gramatica[simbolo].extend(novas_producoes)
                    modificou = True
        if not modificou:
            break
    
    return nova_gramatica

def substituir_producoes_unitarias(gramatica):
    nova_gramatica = {simbolo: list(producoes) for simbolo, producoes in gramatica.items()}
    modificou = True

    while modificou:
        modificou = False
        for simbolo, producoes in list(nova_gramatica.items()):
            novas_producoes = []
            for producao in producoes:
                if len(producao) == 1 and producao.isupper():
                    novas_producoes.extend(nova_gramatica[producao])
                else:
                    novas_producoes.append(producao)
            novas_producoes = list(set(novas_producoes))
            if set(novas_producoes) != set(nova_gramatica[simbolo]):
                nova_gramatica[simbolo] = novas_producoes
                modificou = True

    return nova_gramatica

def remover_simbolos_inuteis(gramatica):
    simbolo_inicial = 'S'
    alcancaveis = set()
    a_explorar = [simbolo_inicial]
    
    while a_explorar:
        simbolo = a_explorar.pop()
        if simbolo not in alcancaveis:
            alcancaveis.add(simbolo)
            if simbolo in gramatica:
                for producao in gramatica[simbolo]:
                    for letra in producao:
                        if letra.isupper() and letra not in alcancaveis:
                            a_explorar.append(letra)
    
    nova_gramatica = {simbolo: producoes for simbolo, producoes in gramatica.items() if simbolo in alcancaveis}
    
    return nova_gramatica

def fatorar_a_esquerda(gramatica):
    nova_gramatica = {}
    contador = 0

    for simbolo, producoes in gramatica.items():
        prefixos = {}
        for producao in producoes:
            if len(producao) > 0:
                prefixo = producao[0]
                sufixo = producao[1:]
                if prefixo not in prefixos:
                    prefixos[prefixo] = []
                prefixos[prefixo].append(sufixo)
        
        nova_producoes = []
        for prefixo, sufixos in prefixos.items():
            if len(sufixos) > 1:
                novo_simbolo = f"{simbolo}{contador}"
                contador += 1
                nova_gramatica[novo_simbolo] = [s if s else '#' for s in sufixos]
                nova_producoes.append(prefixo + novo_simbolo)
            else:
                nova_producoes.append(prefixo + sufixos[0])
        nova_gramatica[simbolo] = nova_producoes

    return nova_gramatica

def remover_recursao_esquerda(gramatica):
    nova_gramatica = {}
    contador = 0

    for simbolo, producoes in gramatica.items():
        recursivas = [p for p in producoes if p.startswith(simbolo)]
        nao_recursivas = [p for p in producoes if not p.startswith(simbolo)]
        
        if recursivas:
            novo_simbolo = f"{simbolo}{contador}"
            contador += 1
            nova_gramatica[simbolo] = [p + novo_simbolo for p in nao_recursivas]
            nova_gramatica[novo_simbolo] = [p[len(simbolo):] + novo_simbolo for p in recursivas] + ['#']
        else:
            nova_gramatica[simbolo] = producoes
    
    return nova_gramatica

# def forma_normal_de_chomsky(gramatica):
#     # Passo 1: Introduzir novos não-terminais para os terminais
#     terminais = set()
#     for producoes in gramatica.values():
#         for producao in producoes:
#             terminais.update(letra for letra in producao if letra.islower())

#     terminal_para_nao_terminal = {}
#     nova_gramatica = {}

#     for terminal in terminais:
#         novo_nao_terminal = f"T{terminal}"
#         while novo_nao_terminal in nova_gramatica or novo_nao_terminal in gramatica:
#             novo_nao_terminal += "'"
#         terminal_para_nao_terminal[terminal] = novo_nao_terminal
#         nova_gramatica[novo_nao_terminal] = [terminal]

#     # Substituir terminais por novos não-terminais nas produções
#     nova_gramatica_com_termos_substituidos = {}
#     for simbolo, producoes in gramatica.items():
#         novas_producoes = []
#         for producao in producoes:
#             nova_producao = ''
#             for letra in producao:
#                 if letra.islower():
#                     nova_producao += terminal_para_nao_terminal[letra]
#                 else:
#                     nova_producao += letra
#             novas_producoes.append(nova_producao)
#         nova_gramatica_com_termos_substituidos[simbolo] = novas_producoes

#     # Passo 2: Dividir produções longas em produções binárias
#     nova_gramatica_final = nova_gramatica.copy()
#     contador = 0

#     for simbolo, producoes in nova_gramatica_com_termos_substituidos.items():
#         novas_producoes = []
#         for producao in producoes:
#             while len(producao) > 2:
#                 novo_nao_terminal = f"X{contador}"
#                 contador += 1
#                 nova_gramatica_final[novo_nao_terminal] = [producao[1:]]
#                 producao = producao[0] + novo_nao_terminal
#             novas_producoes.append(producao)
#         if simbolo not in nova_gramatica_final:
#             nova_gramatica_final[simbolo] = novas_producoes
#         else:
#             nova_gramatica_final[simbolo].extend(novas_producoes)

#     return nova_gramatica_final

def forma_normal_de_greibach(gramatica):
    nova_gramatica = {}
    for simbolo, producoes in gramatica.items():
        novas_producoes = []
        for producao in producoes:
            if producao:
                if producao[0].islower():
                    novas_producoes.append(producao)
                else:
                    novo_simbolo = f"{simbolo}'"
                    while novo_simbolo in nova_gramatica or novo_simbolo in gramatica:
                        novo_simbolo += "'"
                    nova_gramatica[simbolo] = [producao[0] + novo_simbolo]
                    nova_gramatica[novo_simbolo] = [producao[1:]]
            else:
                nova_gramatica[simbolo] = novas_producoes
    
    return nova_gramatica

arquivo = 'gramatica.txt'
gramatica = converter_gramatica(arquivo)

print("Gramática original:")
formatar_gramatica(gramatica)
print()

gramatica_sem_vazio = remover_producoes_vazias(gramatica)
print("Gramática sem produções vazias:")
formatar_gramatica(gramatica_sem_vazio)
print()

gramatica_sem_unitarias = substituir_producoes_unitarias(gramatica_sem_vazio)
print("Gramática após substituição de produções unitárias:")
formatar_gramatica(gramatica_sem_unitarias)
print()

gramatica_sem_inuteis = remover_simbolos_inuteis(gramatica_sem_unitarias)
print("Gramática sem símbolos inúteis:")
formatar_gramatica(gramatica_sem_inuteis)
print()

gramatica_sem_recursao = remover_recursao_esquerda(gramatica_sem_inuteis)
print("Gramática sem recursão à esquerda:")
formatar_gramatica(gramatica_sem_recursao)
print()

gramatica_fatorada = fatorar_a_esquerda(gramatica_sem_recursao)
print("Gramática após fatoração à esquerda:")
formatar_gramatica(gramatica_fatorada)
print()

# gramatica_chomsky = forma_normal_de_chomsky(gramatica_sem_inuteis)
# print("Gramática na Forma Normal de Chomsky:")
# formatar_gramatica(gramatica_chomsky)
# print()

gramatica_greibach = forma_normal_de_greibach(gramatica_sem_inuteis)
print("Gramática na Forma Normal de Greibach:")
formatar_gramatica(gramatica_greibach)
