from functions import *
import matplotlib.pyplot as plt
from numpy import arange
import random
import time
import csv

def SingleMaximalIteration(compoundList, times, significanceValue=0.0000001):
    maximals = list()
    maximalsTimes = list()
    totalPeaks = 0

    for i in range(2, len(compoundList)-1):
        if compoundList[i-1] + significanceValue < compoundList[i] and compoundList[i] > compoundList[i+1] + significanceValue:
            maximals.append(compoundList[i])
            maximalsTimes.append(times[i])
            totalPeaks += 1  

    return maximals, maximalsTimes, totalPeaks


def ExtractMaximals(times: list, xList: list, rList: list, eList: list):

    t= time.time()
    xMaximals, xMaximalsTimes, xTotalPeaks = SingleMaximalIteration(xList, times)     
    print(f"Tempo uma iteração maximais: {time.time()-t}") 
    rMaximals, rMaximalsTimes, rTotalPeaks = SingleMaximalIteration(rList, times)                
    eMaximals, eMaximalsTimes, eTotalPeaks = SingleMaximalIteration(eList, times)        
    
    return xMaximals, xMaximalsTimes, rMaximals, rMaximalsTimes, eMaximals, eMaximalsTimes, xTotalPeaks, rTotalPeaks, eTotalPeaks

def ExtractPeriodsMeans(xMaximalsTimes: list, rMaximalsTimes: list, eMaximalsTimes: list):
    t = time.time()
    xPeriodsMean = CalculatePeriods(xMaximalsTimes)
    print(f"Tempo uma iteração maximais: {time.time()-t}") 
    rPeriodsMean = CalculatePeriods(rMaximalsTimes)
    ePeriodsMean = CalculatePeriods(eMaximalsTimes)

    return xPeriodsMean, rPeriodsMean, ePeriodsMean

def CalculatePeriods(maximalsTimesList: list):
    if (len(maximalsTimesList) == 0):
        return 
    listPeriods = list()
    for i in range(1, len(maximalsTimesList)):
        listPeriods.append(abs(maximalsTimesList[i]-maximalsTimesList[i-1]))

    if (len(listPeriods) == 0):
        return 

    return sum(listPeriods) / len(listPeriods)

def PlotResults(paramsDict: dict = {}, showPeriods: bool = False, listResults: list= []):
    times: list; xList: list; rList: list; eList: list
    xMaximals: list; xMaximalsTimes: list; rMaximals: list; rMaximalsTimes: list; eMaximals: list; eMaximalsTimes: list; xPeriodsMean: int; rPeriodsMean: int; ePeriodsMean: int
    if len(listResults) == 0:
        assert len(paramsDict) > 0, "Dicionário não pode estar vazio."
        times, xList, rList, eList = Simulation(paramsDict)
    else:    
        if len(paramsDict) > 0 and len(listResults) > 0:
            raise ValueError("Se foi fornecido um dicionário, não pode fornecer uma lista de resultados.")
        times, xList, rList, eList = listResults[0], listResults[1], listResults[2], listResults[3]
        xPeriodsMean, rPeriodsMean, ePeriodsMean = listResults[4], listResults[5], listResults[6]
        xMaximals,xMaximalsTimes,rMaximals,rMaximalsTimes,eMaximals,eMaximalsTimes = listResults[7] , listResults[8] , listResults[9] , listResults[10] , listResults[11] , listResults[12]

    xLen = len(xList); rLen = len(xList); eLen = len(xList); timesLen = len(times)

    if not(xLen == rLen == eLen == timesLen):
        raise ValueError("o tamanho de todas as listas tem que ser igual.")

    plt.plot(times, xList, color='lightblue')
    plt.plot(times, rList, color='red')
    plt.plot(times, eList, color='yellow')
    plt.legend(["X", "R", "E"])
    plt.xlabel("Unidade de tempo")
    plt.ylabel("Concentração")
    plt.title("Oscilações do sistema biológico")

    if not(showPeriods):
        plt.show()
        return

    if (len(paramsDict) > 0):
        xMaximals, xMaximalsTimes, rMaximals, rMaximalsTimes, eMaximals, eMaximalsTimes, xPeriodsMean, rPeriodsMean, ePeriodsMean, *_ = GetPeriods(times, xList, rList, eList, xLen)

    totalPeriodMean = (xPeriodsMean+rPeriodsMean+ePeriodsMean)/3

    plt.scatter(xMaximalsTimes, xMaximals, marker='o', c='lightblue')
    plt.scatter(rMaximalsTimes, rMaximals, marker='o', c='red')
    plt.scatter(eMaximalsTimes, eMaximals, marker='o', c='yellow')

    baseYText = 3.920

    plt.gcf().set_size_inches(17,8)

    plt.text(323, baseYText, "Períodos médios entre oscilações:", c="white", fontsize=14, font='monospace', fontweight=600, bbox=dict(boxstyle="square", ec=(1., 0.5, 0.5), fc=(1., 0.8, 0.8)))
    baseYText -= 0.276
    plt.text(343, baseYText, f"X: {xPeriodsMean:.2f}", fontsize=11, font='monospace', fontweight=400)
    plt.text(383, baseYText, f"R: {rPeriodsMean:.2f}", fontsize=11, font='monospace', fontweight=400)
    plt.text(423, baseYText, f"E: {ePeriodsMean:.2f}", fontsize=11, font='monospace', fontweight=400)


    print(f"Período médio entre máximos para o composto X: {xPeriodsMean}")
    print(f"Período médio entre máximos para o composto R: {rPeriodsMean}")
    print(f"Período médio entre máximos para o composto E: {ePeriodsMean}")
    print(f"Período médio entre máximos para todos os compostos: {totalPeriodMean}")
    plt.show()
    print("bah")

def GetPeriods(times, xList, rList, eList, returnNPeaks=False):
    xMaximals, xMaximalsTimes, rMaximals, rMaximalsTimes, eMaximals, eMaximalsTimes, xTotalPeaks, rTotalPeaks, eTotalPeaks = ExtractMaximals(times, xList, rList, eList)

    if (returnNPeaks):
        lenX = len(xMaximalsTimes); lenR = len(rMaximalsTimes); lenE = len(eMaximalsTimes)
        if ((lenX < 4 and lenR < 4 and lenE < 4) or (lenX < 2 or lenR < 2 or lenE < 2)):
            raise ValueError("Número de maximais encontrados insuficiente")
        
    xPeriodsMean, rPeriodsMean, ePeriodsMean = ExtractPeriodsMeans(xMaximalsTimes, rMaximalsTimes, eMaximalsTimes)
    if (returnNPeaks):
        if xPeriodsMean == None or rPeriodsMean == None or ePeriodsMean == None:
            raise ValueError("Uma das médias encontradas é nula")

    return xMaximals,xMaximalsTimes,rMaximals,rMaximalsTimes,eMaximals,eMaximalsTimes,xPeriodsMean,rPeriodsMean,ePeriodsMean, xTotalPeaks, rTotalPeaks, eTotalPeaks

def SearchLowerUpperPeriods(lowerThreshold: float, upperThreshold: float, symmetricalSearch: bool = True, satisfiableNumber: int = 20):
    """
    :param float lowerThreshold: valor máximo para considerar um período menor
    :param float upperThreshold: valor mínimo para considerar um período maior
    :param bool symmetricalSearch: indica se a busca utilizando aumento dos valores dos parâmetros só poderá retornar resultados com períodos maiores e vice-versa. Padrão True.
    :param int satisfiableNumber: número de resultados exigido para cada busca por período
    :return: as listas com os períodos maiores e menores, se conseguir achar o número específicado para pelo menos uma delas. Caso contrário returna None.

    """
    if (symmetricalSearch):
        t0 = time.time()
        upper = SearchPeriods(True, lowerThreshold, upperThreshold, satisfiableNumber/2)
        print(time.time()-t0)
        lower = SearchPeriods(False, lowerThreshold, upperThreshold, satisfiableNumber/2)

        upper.extend(lower)
        return upper
    else:
        upper = SearchPeriods(True, lowerThreshold, upperThreshold, satisfiableNumber)

    return upper



def SearchPeriods(increase: bool, lowerThreshold: float, upperThreshold: float, satisfiableNumber = 3):

    if increase:
        valuesArray = arange(0.07, 2.11, 0.07)
        enzimeVariable = "EEp"
    else:
        valuesArray = arange(-0.07, -0.71, -0.07)
        enzimeVariable = "E"

    satisfiableData = list()
    templateDict = dict()
    newDict = dict()

    templateDict = paramsDict.copy() #Cria o dicionário novo com os mesmos valores do original
    if increase:
        population = [a for a in templateDict.keys() if a not in ("dt", "t0", "tf", "EEp", "kmx", "kx")]
    else:
        population = [a for a in templateDict.keys() if a not in ("dt", "t0", "tf", "E", "R", "kdx", "kbasx", "kmk", "kmp", "kmx", "kx")]

    for i in valuesArray: #Para cada valor a adicionar a mais      
        for key in population:            
            if (len(satisfiableData) >= satisfiableNumber):
                return satisfiableData

            try:
                newDict = templateDict.copy() #Cria um novo dicionário que conterá os valores desta simulação
                newDict[key] += i

                times, XList, RList, EList = Simulation(newDict)
                assert len(XList) == len(RList) == len(EList) == len(times), "O tamanho de todas as listas tem que ser igual."
                
                xMaximals,xMaximalsTimes,rMaximals,rMaximalsTimes,eMaximals,eMaximalsTimes, xPeriodMeans, rPeriodMeans, ePeriodMeans, *_ = GetPeriods(times, XList, RList, EList, True)
                totalMean = (xPeriodMeans+rPeriodMeans+ePeriodMeans)/3

                if((xPeriodMeans < lowerThreshold or rPeriodMeans < lowerThreshold or ePeriodMeans < lowerThreshold) or (xPeriodMeans > upperThreshold or rPeriodMeans > upperThreshold or ePeriodMeans > upperThreshold)):
                    satisfiableData.append([times, XList, RList, EList, xPeriodMeans, rPeriodMeans, ePeriodMeans, xMaximals,xMaximalsTimes,rMaximals,rMaximalsTimes,eMaximals,eMaximalsTimes, newDict, key, newDict[key]])
            except ValueError:
                continue
    return satisfiableData
          

# PlotResults(paramsDict, True)

satisfiableData = SearchLowerUpperPeriods(14.10, 18.10, True, satisfiableNumber=100)

with open('file.txt', 'w') as file:
    for data in satisfiableData:
        file.writelines("\nDicionario modificado:\n")
        file.writelines(f"{data[14]} : {data[13][data[14]]}\n")
        file.writelines("\n")
        file.writelines(f"Media X: {data[4]:.2f}, media R: {data[5]:.2f}, media E: {data[6]:.2f}\n" )

s = []
x =[]
r =[]
k = []
EEp = []
Et =[]
ks = []
kdx =[]
kdr = []
kr =[]
kp = []
kbasx =[]
kmx = []
kx =[]
kmk = []
kmp = []

for data in satisfiableData:
    if data[14] == "S":
        s.append([data[4], data[5], data[6], data[15]])
    if data[14] == "X":
        x.append([data[4], data[5], data[6], data[15]])
    if data[14] == "R":
        r.append([data[4], data[5], data[6], data[15]])
    if data[14] == "K":
        k.append([data[4], data[5], data[6], data[15]])
    if data[14] == "EEp":
        EEp.append([data[4], data[5], data[6], data[15]])
    if data[14] == "Et":
        Et.append([data[4], data[5], data[6], data[15]])
    if data[14] == "ks":
        ks.append([data[4], data[5], data[6], data[15]])
    if data[14] == "kdx":
        kdx.append([data[4], data[5], data[6], data[15]])
    if data[14] == "kdr":
        kdr.append([data[4], data[5], data[6], data[15]])
    if data[14] == "kr":
        kr.append([data[4], data[5], data[6], data[15]])
    if data[14] == "kp":
        kp.append([data[4], data[5], data[6], data[15]])
    if data[14] == "kbasx":
        kbasx.append([data[4], data[5], data[6], data[15]])
    if data[14] == "kmx":
        kmx.append([data[4], data[5], data[6], data[15]])
    if data[14] == "kx":
        kx.append([data[4], data[5], data[6], data[15]])
    if data[14] == "kmk":
        kmk.append([data[4], data[5], data[6], data[15]])
    if data[14] == "Kmp":
        kmp.append([data[4], data[5], data[6], data[15]])
def SinglePlot(s, x, r, k, EEp, Et, ks, kdx, kdr, kr, kp, kbasx, kmx, kx, kmk, kmp, index):
    for a in s:
        plt.scatter(a[3], a[index]) 

    for a in x:
        plt.scatter(a[3], a[index])   

    for a in r:
        plt.scatter(a[3], a[index])   

    for a in k:
        plt.scatter(a[3], a[index])  

    for a in EEp:
        plt.scatter(a[3], a[index])  

    for a in Et:
        plt.scatter(a[3], a[index])  

    for a in ks:
        plt.scatter(a[3], a[index])  

    for a in kdx:
        plt.scatter(a[3], a[index])  

    for a in kdr:
        plt.scatter(a[3], a[index])  

    for a in kr:
        plt.scatter(a[3], a[index])  

    for a in kp:
        plt.scatter(a[3], a[index])  

    for a in kbasx:
        plt.scatter(a[3], a[index])  

    for a in kmx:
        plt.scatter(a[3], a[index])

    for a in kmk:
        plt.scatter(a[3], a[index])

    for a in kmp:
        plt.scatter(a[3], a[index]) 

    for a in kx:
        plt.scatter(a[3], a[index])

# SinglePlot(s, x, r, k, EEp, Et, ks, kdx, kdr, kr, kp, kbasx, kmx, kx, kmk, kmp, 0)

# plt.ylabel('Período médio X')
# plt.xlabel('Valor do parâmetro')
# plt.legend(["s","x","r","k","EEp","Et","ks","kdx","kdr","kr","kp","kbasx","kmx","kmk","kmp","kx"])
# plt.show()

# SinglePlot(s, x, r, k, EEp, Et, ks, kdx, kdr, kr, kp, kbasx, kmx, kx, kmk, kmp, 1)

# plt.ylabel('Período médio R')
# plt.xlabel('Valor do parâmetro')
# plt.legend(["s","x","r","k","EEp","Et","ks","kdx","kdr","kr","kp","kbasx","kmx","kmk","kmp","kx"])
# plt.show()

# SinglePlot(s, x, r, k, EEp, Et, ks, kdx, kdr, kr, kp, kbasx, kmx, kx, kmk, kmp, 2)

# plt.ylabel('Período médio E')
# plt.xlabel('Valor do parâmetro')
# plt.legend(["s","x","r","k","EEp","Et","ks","kdx","kdr","kr","kp","kbasx","kmx","kmk","kmp","kx"])
# plt.show()

print("bah")

for data in random.sample(satisfiableData, 3):
    PlotResults(showPeriods=True, listResults=data)

                #population = [a for a in newDict.keys() if a not in ("dt", "t0", "tf", enzimeVariable)] #Tomar cuidado com quais parâmetros alterar
                # secondKeys = random.sample(population,random.randint(1, 15)) #Seleciona aleatoriamente 1 a 15 para aumentar também
                # for secondKey in secondKeys:
                #     if secondKey == key:
                #         continue
                #     newDict[secondKey] += random.uniform(i*1/4, i*3/4)
    
    







    