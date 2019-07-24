import pandas as pd
import numpy as np
import datetime



#import os
#print(os.getcwd())
# Out: /Users/shane/Documents/blog
# Display all of the files found in your current working directory
#print(os.listdir(os.getcwd())

#to_datetime()

data = pd.read_csv("FL8-12.07.csv", encoding = "ISO-8859-1",sep=";")
data["Fecha Entrega"] = pd.to_datetime(data["Fecha Entrega"])
dias = pd.DatetimeIndex(data["Fecha Entrega"]).day

data['Ano'] = pd.DatetimeIndex(data['Fecha Entrega']).year
data['Mes'] = pd.DatetimeIndex(data['Fecha Entrega']).day
data['Dia'] = pd.DatetimeIndex(data['Fecha Entrega']).month


#Para filtrar por operación completos = data[(data['tipo_pallet']=="Completo")&(data['Tipo de pedido']=="3019-RANCAGUA")]
completos = data[(data['tipo_pallet']=="Completo")]
#mixto = data[(data['tipo_pallet']=="Mixto")&(data['Tipo de pedido']=="3019-RANCAGUA")]


meses = pd.unique(data['Mes'])
dias = pd.unique(data['Dia'])
op = pd.unique(data['Tipo de pedido'])

skucompleto = np.unique(completos['Número de artículo'])
unicoscompleto = len(skucompleto)

values = []
for q in np.transpose(skucompleto):
    values.append(q)

min=13
max=0

for i in range(0,len(dias)):
    if int(dias[i]) < min:
        min = int(dias[i])
    if int(dias[i]) > max:
        max = int(dias[i])

rango = max-min+1

mcompletos = np.array(completos.values)
totalcargas = len(completos)
filas = np.shape(mcompletos)[0]
columnas = np.shape(mcompletos)[1]
bdafinitycompletoValores= np.zeros(shape=[unicoscompleto+1, unicoscompleto+1]).astype(str)
bdafinitycompleto= np.zeros(shape=[unicoscompleto+1, unicoscompleto+4]).astype(str)

cargasunicas = np.unique(completos['Número de departamento'])
skuporcarga= np.zeros(shape=[len(cargasunicas)+1, unicoscompleto+1]).astype(str)



mcompletos = np.array(completos.values)

for k in range(0, unicoscompleto):
    bdafinitycompletoValores[k+1 , 0] = skucompleto[k]
    bdafinitycompletoValores[0, k+1] = skucompleto[k]
    bdafinitycompleto[k + 1, 0] = skucompleto[k]
    bdafinitycompleto[k + 1, unicoscompleto+1] = skucompleto[k]
    bdafinitycompleto[0, k + 1] = skucompleto[k]
    skuporcarga[0,k+1]=skucompleto[k]

bdafinitycompleto[0, unicoscompleto+1] = "SKU"
bdafinitycompleto[0, unicoscompleto+2] = "Indice de Afinidad"
bdafinitycompleto[0, unicoscompleto+3] = "Ventas"

for k2 in range(0,len(cargasunicas)):
    skuporcarga[k2+1,0] = cargasunicas[k2]

# valor SKI skuporcarga[0,1], VALOR CARGA skuporcarga[1,0])

# valor de SKU mcompletos[:,10]
# valor de Staging mcompletos[:,6]
## Completos de RCGUA

# para mi columna sumar 1 al index print(values.index('450607')+1)
# para buscar en la lista es directo print(values[3])

for registros in range(0, len(mcompletos)):
    index_of_sku = np.where(skucompleto == mcompletos[registros, 10])[0][0]
    index_of_carga = np.where(cargasunicas == mcompletos[registros, 6])[0][0]
    skuporcarga[index_of_carga+1,index_of_sku+1]=float(skuporcarga[index_of_carga+1,index_of_sku+1])+1

pd.DataFrame(skuporcarga).to_csv("SkuXcarga.csv")

valores = []
valores2 = []

for carga in range(0,len(cargasunicas)):
    valores.clear()
    valores2.clear()
    for sku in range(0, len(skucompleto)):
        if float(skuporcarga[carga+1,sku+1]) > 0:
            valores.append(sku)
            valores2.append(float(skuporcarga[carga+1,sku+1]))


    for sku1 in range(0,len(valores)):
        bdafinitycompletoValores[valores[sku1] + 1, valores[sku1] + 1] = float(bdafinitycompletoValores[valores[sku1] + 1, valores[sku1] + 1])+float(valores2[sku1])
        for sku2 in range(0, len(valores)):
            if sku1<sku2:
                bdafinitycompletoValores[valores[sku1] + 1, valores[sku2] + 1] = float(
                    bdafinitycompletoValores[valores[sku1] + 1, valores[sku2] + 1]) + float(valores2[sku1])
                bdafinitycompletoValores[valores[sku2] + 1, valores[sku1] + 1] = float(
                    bdafinitycompletoValores[valores[sku2] + 1, valores[sku1] + 1]) + float(valores2[sku2])


#print(bdafinitycompletoValores)
pd.DataFrame(bdafinitycompletoValores).to_csv("AfinityValores.csv")
cantregistros = len(mcompletos)

totalfila = []
diagonal = []
denominador = []
cantafinidades = []

for j1 in range(1,len(bdafinitycompletoValores)):
    sum = 0
    sum2 = 0
    c = 0
    for j2 in range(1, len(bdafinitycompletoValores)):
        sum =  sum + float(bdafinitycompletoValores[j1,j2])
        if bdafinitycompletoValores[j1,j2] != '0.0':
            c=c+1
        if j1==j2:
            sum2 =sum2 +float(bdafinitycompletoValores[j1,j2])
    totalfila.append(sum)
    diagonal.append(sum2)
    denominador.append(sum-sum2)
    cantafinidades.append(c-1)

for i1 in range(1,len(bdafinitycompletoValores)):
    for i2 in range(1,len(bdafinitycompletoValores)):
        if i1==i2:
            bdafinitycompleto[i1,i2]=float(diagonal[i1-1])/cantregistros
        elif denominador[i1-1]!=0:
            bdafinitycompleto[i1, i2]=float(bdafinitycompletoValores[i1,i2])/denominador[i1-1]
        else:
            bdafinitycompleto[i1, i2] = ""
    bdafinitycompleto[i1, len(bdafinitycompletoValores)+1] = cantafinidades[i1 - 1]
    bdafinitycompleto[i1, len(bdafinitycompletoValores) + 2] = diagonal[i1 - 1]

print(bdafinitycompleto)
pd.DataFrame(bdafinitycompleto).to_csv("AfninidadIndices.csv")
