
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
    with open("myheart.csv") as file:
        firstline = True
        for line in file:
            if firstline:
                keys = "".join(line.split()).split(',')
                firstline = False
            else:
                values = "".join(line.split()).split(',')
                a.append({keys[n]:values[n] for n in range(0,len(keys))})

    return a

def distribuicaoSexo(a):
    dist = {"M":0, "F":0}
    for dict in a:
        if dict['sexo'] == "M":
            dist["M"]+=1
        else:
            dist["F"]+=1

    return dist



a = loadCSV()
dist = distribuicaoSexo(a)

print(dist)