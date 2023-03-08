import re
import json
import math

funcionario = {
    'sum': sum,
    'max': max,
    'min': min,
    'media': lambda x:sum(x)/len(x),
    'mult': math.prod
}

file = 'TPC4/alunos.csv'

data = []
with open(file) as f:
    line  = f.readline()
    # Group1: Campo | Group3: tamanho da lista (3,5) | Group5: nome da função
    keys = re.finditer(r'([^,{\n]+)({([^}]+)}(\:\:(\w+))?)?', line)

    fields = []
    for key in keys:
        if(key.group(3) is None):
            field = key.group(1)
            fields.append((field,None,None,None))
        else:
            # Nome do Campo
            field = key.group(1)
            # Lista
            # Group 1: sizeN | Group 3: sizeM
            size = re.search(r'(\d+)(,(\d+))?', key.group(3))
            sizeN = int(size.group(1))
            if(size.group(3) is not None):
                sizeM = int(size.group(3))
            else:
                sizeM = None

            # Função sobre a lista
            func = key.group(5)
            fields.append((field,sizeN,sizeM,func))

    dic = {}
    for line in f:
        values = line.split(',')
        values[-1] = values[-1].strip()
        i=0
        for field in fields:
            value = values[i]
            if field[1] is None:
                dic[field[0]] = value
                i+=1
            else:
                sizeN = field[1]
                sizeM = field[2]
                lista = []
                j = 0
                while(j<sizeN):
                    lista.append(values[i])
                    j+=1
                    i+=1
                if sizeM:
                    while(j<sizeM):
                        if(values[i]):
                            lista.append(values[i])
                        j+=1
                        i+=1
                if field[3]:
                    lista = [int(x) for x in lista]
                    func = funcionario[field[3]]
                    dic[field[0] + '_' + field[3]] = str(func(lista))
                else:
                    dic[field[0]] = lista
        data.append(dic)
        dic = {}

#print(data)

with open('TPC4/data.json', 'w') as f:
    data = {"data": data} # opção para tornar o json legivel ao json-server
    json.dump(data, f, indent=2, ensure_ascii=False)
