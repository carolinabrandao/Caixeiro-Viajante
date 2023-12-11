import tsplib95



from twiceAroundtheTree import TwiceAroundtheTree
from christofides import Christofides


instancias = "instancias/"

instancias_info = {}

with open('tp2_datasets.txt', 'r') as file:
    # Pula a primeira linha, que geralmente contém cabeçalhos
    next(file)

    for line in file:
        dataset, nos, limiar_str = line.strip().split()
        
        # Verifica se o limiar está no formato [x, y]
        if '[' in limiar_str:
            limiar = eval(limiar_str)  # Avalia a string como uma lista
            limiar = sum(limiar) / len(limiar)  # Calcula a média
        else:
            limiar = int(limiar_str)

        instancias_info[dataset] = [int(nos), limiar]



#create csv file to store results
with open('results.csv', 'w') as file:
    file.write("Instância,Algoritmo,Nós,Limiar,Resultado,Qualidade,Tempo de execução(s),Memória(bytes)\n")



twice = True
christofides = True

for arquivo in instancias_info.keys():

    
    instancia = arquivo.split(".")[0]
    file_name = arquivo + ".tsp"
    problem = tsplib95.load(instancias + file_name)
    print("Trabalhando na instância", instancia)

        
    #pegar numero de nos e limiar
    nos = instancias_info[instancia][0]
    limiar = instancias_info[instancia][1]

    if twice:
        peso, tempo, memoria = TwiceAroundtheTree(problem).twiceAroundTheTreeTSP()

        qualidade = (peso / limiar)

        if tempo > 1800:
            print(" Tempo de execução excedido, instâncias com o número de nós",nos, "não serão executadas para o algoritmo Twice Around the Tree")
            twice = False

        if twice:
            with open('results.csv', 'a') as file:
                file.write(f"{instancia},Twice Around the Tree,{nos},{limiar},{peso},{qualidade},{tempo},{memoria}\n")


    if christofides:
        peso, tempo, memoria = Christofides(problem).christofidesTSP()
        qualidade = (peso / limiar)

        if tempo > 1800:
            print(" Tempo de execução excedido, instâncias com o número de nós",nos, "não serão executadas para o algoritmo de Christofides")
            christofides = False
            
        if christofides:
            with open('results.csv', 'a') as file:
                file.write(f"{instancia},Christofides,{nos},{limiar},{peso},{qualidade},{tempo},{memoria}\n")

    
