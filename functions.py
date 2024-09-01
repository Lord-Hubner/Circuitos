import math

def HillActivation(ligand, Km, n=1):
    ligand = round(ligand, 7)
    Km = round(Km, 7)
    return (ligand / Km)**n / (1 + (ligand / Km)**n)

def HillInibition(ligand, km, n=1):
    ligand = round(ligand, 7)
    Km = round(Km, 7)
    return 1 / (1 + (ligand / km)**n)


paramsDict = {
    "S" : 1, #Concentração inicial de S
    "X" : 1, #Concentração inicial de X
    "R" : 0, #Concentração inicial de R
    "K" : 1, #Concentração inicial de K
    "EEp" : 1, #Concentração de Enzima não fosforilada
    "Et" : 1, #Concentração total de Et = E + Ep
    "dt" : 0.02, #Variação de unidade de tempo por simulação
    "t0" : 0., #Tempo inicial das simulações
    "tf" : 500, #Tempo final das simulações
    "ks" : 1, #Taxa de formação de X por S
    "kdx" : 0.0, #Taxa de degradação de Xd
    "kdr" : 1, #Taxa de degradação de R
    "kr" : 1, #Taxa de E -> Ep por R
    "kp" : 1, #Taxa de formação de E por Ep
    "kbasx" : 0.1, #Taxa de formação basal de R por X
    "kmx" : 60, #Constante de Michaelis-Menten para a função de EEp em X -> R 
    "kx" : 60, #Taxa de formação de X -> R por EEp
    "kmk" : .1, #Constante de Michaelis-Menten para E -> EEp por R
    "kmp" : .1, #Constante de Michaelis-Menten para EEp -> E por K
}

def Simulation(params: dict):
    S, X, R, K, EEp, Et, dt, t0, tf = list(params.values())[:9]  #Variáveis de concentração e de tempo

    ks, kdx, kdr, kr, kp, kbasx, kmx, kx, kmk, kmp = list(params.values())[9:] #Variáveis de taxas e constantes

    ti = t0

    times = [ti]
    XList = [X]
    RList = [R]
    EList = [Et-EEp]

    while ti < tf:
        Xincrement = ks*S - kdx*X - kbasx*X - kx*HillActivation(X, kmx)*EEp
        Rincrement = -(kdr*R) + kbasx*X + kx*HillActivation(X, kmx)*EEp
        Eincrement = kr*HillActivation(Et-EEp, kmk)*R - kp*HillActivation(EEp, kmp)*K

        X += round(Xincrement*dt, 7)
        R += round(Rincrement*dt, 7)
        EEp += round(Eincrement*dt, 7)

        ti += round(dt, 7)

        times.append(ti)
        XList.append(X)
        RList.append(R)
        EList.append(Et-EEp)

    return times, XList, RList, EList



