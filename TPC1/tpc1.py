import matplotlib.pyplot as plt


'''
Max Idade : 77
Min Idade : 28
i = 1000
for b in a:
    if i > int(b['idade']):
        i = int(b['idade'])

print(i)
'''

def loadCSV():    
    a = []
    with open("TPC1/myheart.csv") as file:
        i = 0
        firstline = True
        for line in file:
            if firstline:
                keys = "".join(line.split()).split(',')
                firstline = False
            else:
                values = line.split(",")
                try:
                    values[0] = int(values[0])
                    values[2] = int(values[2])
                    values[3] = int(values[3])
                    values[4] = int(values[4])
                    values[5] = int(values[5])
                except ValueError:
                    print(f"Valor inválido na linha {i}!")
                    continue

                i+=1
                a.append({keys[n]:values[n] for n in range(0,len(keys))})
    return a

def temDoenca(dic):
    return dic['temDoença'] == 1

def distribuicaoSexo(a):
    dist = {"M": 0, "F": 0}
    for dic in a:
        if temDoenca(dic):
            if dic['sexo'] == "M":
                dist["M"]+=1
            else:
                dist["F"]+=1

    return dist

def distribuicaoEtaria(a):
    dist = {}
    for dic in a:
        if dic['temDoença'] == 1:
            idade = dic['idade']
            if idade not in dist:
                dist[idade] = 1
            else:
                dist[idade] += 1

    dist = dict(sorted(dist.items(), key=lambda item: item[0]))

    lower = 30
    interval = 4
    top = lower + interval

    faixaEtaria = (lower,top)
    finalDist = {faixaEtaria:0}
    for age in dist:
        while age > top:
            lower = top + 1
            top = lower + interval
            faixaEtaria = (lower,top)
            finalDist[faixaEtaria] = 0

        finalDist[faixaEtaria] += dist[age]

    return finalDist


def distribuicaoColesterol(a):
    dist = {}
    for dic in a:
        if dic['temDoença'] == 1:
            colesterol = dic['colesterol']
            if colesterol not in dist:
                dist[colesterol] = 1
            else:
                dist[colesterol] += 1

    dist = dict(sorted(dist.items(), key=lambda item: item[0]))

    lower = min(dist)
    interval = 9
    top = lower + interval

    nivelColesterol = (lower,top)
    finalDist = {nivelColesterol:0}
    for colesterol in dist:
        while colesterol > top:
            lower = top + 1
            top = lower + interval
            nivelColesterol = (lower,top)
            finalDist[nivelColesterol] = 0

        finalDist[nivelColesterol] += dist[colesterol]

    return finalDist


def printTable(title, key_title, value_title, dictionary):
    print()
    print(f"{title}\n{key_title:<15} | {value_title}")
    print("-" * 25)
    for key, value in dictionary.items():
        print(f"{str(key):<15} | {value}")
    print()



a = loadCSV()


menu = """
------------------Menu------------------
Distribução por Sexo: 1
Distribução por Idade: 2
Distribução por Niveis de Colestrol: 3
Sair: 0
----------------------------------------
"""

print(menu)
opcao = int(input("Opção: "))
while opcao != 0:
    if opcao == 1:
        distS = distribuicaoSexo(a)
        printTable("Distribuição por sexo", "Sexo", "Total", distS) 

        # Gráfico da distribuição de sexo
        plt.subplot(1, 3, 1)
        # values = distr_sex.values()
        plt.bar(distS.keys(),distS.values())
        plt.title('Distribuição pelo sexo')
        plt.show()


    elif opcao == 2:
        distE = distribuicaoEtaria(a)
        printTable("Distribuição Etária", "Idade", "Total", distE)

        # Gráfico da distribuição de idade
        plt.subplot(1, 3, 2)
        ageKeys = list(map(lambda x: str(x).replace('(','[').replace(')',']'),distE.keys()))
        plt.barh(ageKeys, list(distE.values()))
        plt.title('Distribuição pela idade')
        plt.show()


    elif opcao == 3:
        distC = distribuicaoColesterol(a)
        #Remove Entries with value 0
        distC = {x:y for x,y in distC.items() if y!=0}

        printTable("Distribuição por Colestrol", "Colestrol", "Total", distC)

        # Gráfico da distribuição de níveis de colesterol
        plt.subplot(1, 3, 3)
        colKeys = list(map(lambda x: str(x).replace('(','[').replace(')',']'),distC.keys()))
        plt.barh(colKeys, list(distC.values()))
        plt.title('Distribuição pelos níveis de colesterol')
        plt.show()

    else:
        print("Opção Inválida!")
        
    input("Pressione Enter para continuar!")

    print(menu)
    opcao = int(input("Opção: "))

print("Adeus!")
