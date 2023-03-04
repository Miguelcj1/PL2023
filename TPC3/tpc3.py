import re
import math
import json


def printTable(title, key_title, value_title, dictionary, width = 5, separator = "|"):
    print(f"{title}")
    header = f"{key_title:<{width}} | {value_title}"
    print(header)
    print("-" * len(header))
    for key, value in dictionary.items():
        print(f"{str(key):<{width}} {separator} {value}")
    print()

# a)Calcula a frequência de processos por ano (primeiro elemento da data);
def processosAno(data):
    dic = {}
    for processo in data:
        date = processo['date']
        ano = date.split('-')[0]
        if ano in dic:
            dic[ano] += 1
        else:
            dic[ano] = 1
        dic = dict(sorted(dic.items(), key=lambda x:x[1], reverse=True))
    return dic


def get_seculo(ano):
    return math.ceil(ano/100)


# b) Calcula a frequência de nomes próprios (o primeiro em cada nome) e apelidos (o ultimo em cada nome) por séculos e apresenta os 5 mais usados;
def frequenciaNomes(data, size):
    dicF = {}
    dicL = {}
    for processo in data:
        date = processo['date']
        ano = int(date.split('-')[0])
        seculo = get_seculo(ano)

        nomes = set()
        for n in ['nome', 'pai', 'mae']:
            if n in processo:
                nomes.add(processo[n])
        
        if 'relacoes' in processo:
            for tup in processo['relacoes']:
                nomes.add(tup[0])
        
        for nome in nomes:
            listaNomes = nome.split()
            if len(listaNomes) > 1:
                firstN = listaNomes[0]
                lastN = listaNomes[-1]
            if seculo in dicF:
                if firstN in dicF[seculo]:
                    dicF[seculo][firstN] += 1
                else:
                    dicF[seculo][firstN] = 1
            else:
                dicF[seculo] = {firstN : 1}

            if seculo in dicL:
                if lastN in dicL[seculo]:
                    dicL[seculo][lastN] += 1
                else:
                    dicL[seculo][lastN] = 1
            else:
                dicL[seculo] = {lastN : 1}

    dicF = dict(sorted(dicF.items(), key=lambda x:x[0]))
    dicL = dict(sorted(dicL.items(), key=lambda x:x[0]))

    stringF = ""
    stringL = ""

    for key in dicF:
        stringF += f"TOP 5 nomes proprios do século {key}:\n"
        seculo = dicF[key]
        seculo = dict(sorted(seculo.items(), key=lambda x:x[1], reverse=True))
        for i, k in enumerate(seculo):
            i+=1
            stringF += f"{i}º -> {k} : {seculo[k]}\n"
            if i == size:
                stringF += "\n"
                break

    for key in dicL:
        stringL += f"TOP 5 apelidos do século {key}:\n"
        seculo = dicL[key]
        seculo = dict(sorted(seculo.items(), key=lambda x:x[1], reverse=True))
        for i, k in enumerate(seculo):
            i+=1
            stringL += f"{i}º -> {k} : {seculo[k]}\n"
            if i == size:
                stringL += "\n"
                break

    return stringF,stringL


# c) Calcula a frequência dos vários tipos de relação: irmão, sobrinho, etc.;
def frequenciaRelacoes(data):
    freq = {}
    for processo in data:
        if 'relacoes' in processo:
            listaR = processo['relacoes']
            for _,relacao in listaR:
                if relacao in freq:
                    freq[relacao] += 1
                else:
                    freq[relacao] = 1

    freq = dict(sorted(freq .items(), key=lambda x:x[1], reverse=True))
    return freq


# d) Converta os 20 primeiros registos num novo ficheiro de output mas em formato Json.
def dataToJSON(data, n):
    with open(f'data{n}.json', 'w') as file:
        json.dump(data[:n], file, indent=2)



with open('processos.txt') as file:
    data = []
    expRe = r'(([A-Z][a-z ,]+)+),(\w+\s*\w*\s*\w+)\.\s*Proc.\d+'
    er = re.compile(expRe)

    for line in file:
        line = line.strip()
        if line:
            campos = re.split(r'::+', line)
            campos = list(filter(None, campos))

            dic = {}
            for i, c in enumerate(campos):
                if i == 0:
                    dic['pasta'] = c
                elif i == 1:
                    dic['date'] = c
                elif i == 2:
                    dic['nome'] = c
                elif i == 3:
                    dic['pai'] = c
                elif i == 4:
                    dic['mae'] = c
                elif i == 5:
                    dic['observacoes'] = c
                    matches = er.finditer(c)
                    relacoes = []
                    for match in matches:
                        relacao = match.group(3)
                        nomes = match.group(1)
                        tup = (nomes, relacao)
                        relacoes.append(tup)
                    dic['relacoes'] = relacoes
            
            data.append(dic)



menu = """
------------------Menu------------------
Frequência de processos por ano: 1
Frequência de nomes e apelidos por século: 2
Frequência de relações: 3
Processos para json: 4
Sair: 0
----------------------------------------
"""

print(menu)
opcao = int(input("Opção: "))
while opcao != 0:
    if opcao == 1:
        # a) Calcula a frequência de processos por ano (primeiro elemento da data);
        exA = processosAno(data)
        printTable("Distribuição de processos por ano", "Ano", "Nº de processos", exA)

    elif opcao == 2:
        # b) Calcula a frequência de nomes próprios (o primeiro em cada nome) e apelidos (o ultimo em cada nome) por séculos e apresenta os 5 mais usados;
        nomes, apelidos = frequenciaNomes(data, 5)
        print(nomes)
        print(apelidos)

    elif opcao == 3:
        # c) Calcula a frequência dos vários tipos de relação: irmão, sobrinho, etc.;
        exC = frequenciaRelacoes(data)
        printTable("Frequencias dos vários tipos de relação", "Relação", "Nº de relações", exC, width=25)

    elif opcao == 4:
        # d) Converta os 20 primeiros registos num novo ficheiro de output mas em formato Json.
        n = int(input("Quantos processos quer converter?"))
        dataToJSON(data, n)

    else:
        print("Opção Inválida!")
        
    input("Pressione Enter para continuar!")

    print(menu)
    opcao = int(input("Opção: "))

print("Adeus!")
      