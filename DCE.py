# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 10:03:26 2022

@author: danut
"""

"Discrete Choice experiment:Sustainable vs non sustainable"
import pandas as pd
import numpy as np
dati = pd.read_csv (r'C:\Users\danut\OneDrive\Desktop\Magistrale\Esami dati\finanza comportamentale\File risposte.csv',encoding=("ISO-8859-1"))
#tolgo le prime 2 colonne inutili di infomrativa privacy e data
dati= dati.drop('Data',1)
dati= dati.drop('Informativa',1)

#per qualche motivo la colonna eta aveva problemi a leggerla all'inizio quindi l'ho rinominata per evitare futuri problemi
dati.rename(columns = {'Eta ':'ETA'}, inplace = True)

#indice green
dati = dati.assign(Indice_green= dati['Green']+dati['Comportamento'])

#indice di conoscenza finanziaria
Indice_FK=[0]*224
for i in range(len(dati)):
    ConFin= 0
    if dati.loc[i,'Interesse']==('102'):ConFin=ConFin+1
    if dati.loc[i,'Interesse']==('100'):ConFin=ConFin-1
    if dati.loc[i,'Rendimento']==('Vero') : ConFin = ConFin +1 
    if dati.loc[i,'Rendimento']==('Falso') :ConFin = ConFin -1
    if dati.loc[i,'Diversificazione']==('Vero') : ConFin = ConFin +1
    if dati.loc[i,'Diversificazione']==('Falso') :ConFin = ConFin -1
    if dati.loc[i,'Grafico1']==('Fondo 1') :ConFin=ConFin +1
    if dati.loc[i,'Grafico1']==('Fondo 2') :ConFin=ConFin -1
    if dati.loc[i,'Grafico1']==('Fondo 3') :ConFin=ConFin -1
    if dati.loc[i,'Grafico2']==('Fondo 3'):ConFin=ConFin +1
    if dati.loc[i,'Grafico2']==('Fondo 2'): ConFin=ConFin -1
    if dati.loc[i,'Grafico2']==('Fondo 1'): ConFin=ConFin -1
    Indice_FK[i]=ConFin
dati['Indice_FK'] =Indice_FK   
DataSet_sociodemo= dati.filter(['Genere','ETA','Istruzione','Ottimismo','Indice_green','Indice_FK'])

#finita parte sociodemo
Descr=DataSet_sociodemo.describe(include='all')
print(DataSet_sociodemo)

#parte choiceset
#togli percentuale e mesi/anno
#le ho tolte per evitare l'errore 
Attributi_livelli_A=pd.DataFrame([['4','25','3','10'],
                   ['4','25','3','0'],
                   ['4','25','12','10'],
                   ['4','25','12','0'],
                   ['4','16','3','10'],
                   ['4','16','3','0'],
                   ['4','16','12','10'],
                   ['4','16','12','0'],
                   ['2','25','3','10'],
                   ['2','25','3','0'],
                   ['2','25','12','10'],
                   ['2','25','12','0'],
                   ['2','16','3','10'],
                   ['2','16','3','0'],
                   ['2','16','12','10'],
                   ['2','16','12','0']])
Attributi_livelli_B=pd.DataFrame([['2','16','12','0'],
                   ['2','16','12','-5'],
                   ['2','16','3','0'],
                   ['2','16','3','-5'],
                   ['2','25','12','0'],
                   ['2','25','12','-5'],
                   ['2','25','3','0'],
                   ['2','25','3','-5'],
                   ['4','16','12','0'],
                   ['4','16','12','-5'],
                   ['4','16','3','0'],
                   ['4','16','3','-5'],
                   ['4','25','12','0'],
                   ['4','25','12','-5'],
                   ['4','25','3','0'],
                   ['4','25','3','-5']])
#tipo di dati nelle colonne degli attributi
Attributi_livelli_A.astype('int').dtypes
Attributi_livelli_B.astype('int').dtypes

#nome colonne e righe per facilitare la lettura e la chiamata dopo
Attributi_livelli_A.columns=['Rischio_A','Rendimento_A','Scadenza_A','RiduzioneCO2_A']
Attributi_livelli_B.columns=['Rischio_B','Rendimento_B','Scadenza_B','RiduzioneCO2_B']
Attributi_livelli_A.index=['Choice1','Choice2','Choice3','Choice4','Choice5','Choice6','Choice7','Choice8','Choice9','Choice10','Choice11','Choice12','Choice13','Choice14','Choice15','Choice16']
Attributi_livelli_B.index=['Choice1','Choice2','Choice3','Choice4','Choice5','Choice6','Choice7','Choice8','Choice9','Choice10','Choice11','Choice12','Choice13','Choice14','Choice15','Choice16']
#meglio dividere in attributi e livelli A e attributi e livelli B

#comincio a costruire il dataset in forma long, inserendo domanda dopo domanda
from xlogit.utils import wide_to_long

#scelta numero 1
ChoiceSet=pd.DataFrame(data=dati,columns=['Choice1'])
Rischio_C1A=[0]*224
Rischio_C1B=[0]*224
Rendimento_C1A=[0]*224
Rendimento_C1B=[0]*224
Scadenza_C1A=[0]*224
Scadenza_C1B=[0]*224
Riduzione_C1A=[0]*224
Riduzione_C1B=[0]*224
PerColonnaNulla=[0]*224
for i in range(len(ChoiceSet)):
    Rischio_C1A[i]=Attributi_livelli_A.loc['Choice1','Rischio_A'];
    Rischio_C1B[i]=Attributi_livelli_B.loc['Choice1','Rischio_B'];
    Rendimento_C1A[i]=Attributi_livelli_A.loc['Choice1','Rendimento_A'];
    Rendimento_C1B[i]=Attributi_livelli_B.loc['Choice1','Rendimento_B'];
    Scadenza_C1A[i]=Attributi_livelli_A.loc['Choice1','Scadenza_A'];
    Scadenza_C1B[i]=Attributi_livelli_B.loc['Choice1','Scadenza_B'];
    Riduzione_C1A[i]=Attributi_livelli_A.loc['Choice1','RiduzioneCO2_A'];
    Riduzione_C1B[i]=Attributi_livelli_B.loc['Choice1','RiduzioneCO2_B']; 
ChoiceSet['Rischio1_InvestimentoA1']=Rischio_C1A
ChoiceSet['Rischio1_InvestimentoB1']=Rischio_C1B
ChoiceSet['Rischio1_NonInvesto1']=PerColonnaNulla

ChoiceSet['Rendimento1_InvestimentoA1']=Rendimento_C1A
ChoiceSet['Rendimento1_InvestimentoB1']=Rendimento_C1B
ChoiceSet['Rendimento1_NonInvesto1']=PerColonnaNulla

ChoiceSet['Scadenza1_InvestimentoA1']=Scadenza_C1A
ChoiceSet['Scadenza1_InvestimentoB1']=Scadenza_C1B
ChoiceSet['Scadenza1_NonInvesto1']=PerColonnaNulla

ChoiceSet['RiduzioneCo21_InvestimentoA1']=Riduzione_C1A
ChoiceSet['RiduzioneCo21_InvestimentoB1']=Riduzione_C1B
ChoiceSet['RiduzioneCo21_NonInvesto1']=PerColonnaNulla
Big_dati=pd.concat([DataSet_sociodemo, ChoiceSet], axis=1)
Big_dati.insert(0, 'Indice_Persona', Big_dati.index)
Big_dati_long = wide_to_long(Big_dati,id_col='Indice_Persona', alt_list=['InvestimentoA1','InvestimentoB1','NonInvesto1'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')

#scelta 2
ChoiceSet2=pd.DataFrame(data=dati,columns=['Choice2'])
Rischio_C2A=[0]*224
Rischio_C2B=[0]*224
Rendimento_C2A=[0]*224
Rendimento_C2B=[0]*224
Scadenza_C2A=[0]*224
Scadenza_C2B=[0]*224
Riduzione_C2A=[0]*224
Riduzione_C2B=[0]*224
for i in range(len(ChoiceSet2)):
    Rischio_C2A[i]=Attributi_livelli_A.loc['Choice2','Rischio_A'];
    Rischio_C2B[i]=Attributi_livelli_B.loc['Choice2','Rischio_B'];
    Rendimento_C2A[i]=Attributi_livelli_A.loc['Choice2','Rendimento_A'];
    Rendimento_C2B[i]=Attributi_livelli_B.loc['Choice2','Rendimento_B'];
    Scadenza_C2A[i]=Attributi_livelli_A.loc['Choice2','Scadenza_A'];
    Scadenza_C2B[i]=Attributi_livelli_B.loc['Choice2','Scadenza_B'];
    Riduzione_C2A[i]=Attributi_livelli_A.loc['Choice2','RiduzioneCO2_A'];
    Riduzione_C2B[i]=Attributi_livelli_B.loc['Choice2','RiduzioneCO2_B']; 
ChoiceSet2['Rischio2_InvestimentoA2']=Rischio_C2A
ChoiceSet2['Rischio2_InvestimentoB2']=Rischio_C2B
ChoiceSet2['Rischio2_NonInvesto2']=PerColonnaNulla

ChoiceSet2['Rendimento2_InvestimentoA2']=Rendimento_C2A
ChoiceSet2['Rendimento2_InvestimentoB2']=Rendimento_C2B
ChoiceSet2['Rendimento2_NonInvesto2']=PerColonnaNulla

ChoiceSet2['Scadenza2_InvestimentoA2']=Scadenza_C2A
ChoiceSet2['Scadenza2_InvestimentoB2']=Scadenza_C2B
ChoiceSet2['Scadenza2_NonInvesto2']=PerColonnaNulla

ChoiceSet2['RiduzioneCo22_InvestimentoA2']=Riduzione_C2A
ChoiceSet2['RiduzioneCo22_InvestimentoB2']=Riduzione_C2B
ChoiceSet2['RiduzioneCo22_NonInvesto2']=PerColonnaNulla
Big_dati2=pd.concat([DataSet_sociodemo, ChoiceSet2], axis=1)
Big_dati2.insert(0, 'Indice_Persona', Big_dati2.index)
Big_dati2.rename(columns = {'Rischio2_InvestimentoA2':'Rischio1_InvestimentoA2'}, inplace = True)
Big_dati2.rename(columns = {'Rischio2_InvestimentoB2':'Rischio1_InvestimentoB2'}, inplace = True)
Big_dati2.rename(columns = {'Rischio2_NonInvesto2':'Rischio1_NonInvesto2'}, inplace = True)
Big_dati2.rename(columns = {'Rendimento2_InvestimentoA2':'Rendimento1_InvestimentoA2'}, inplace = True)
Big_dati2.rename(columns = {'Rendimento2_InvestimentoB2':'Rendimento1_InvestimentoB2'}, inplace = True)
Big_dati2.rename(columns = {'Rendimento2_NonInvesto2':'Rendimento1_NonInvesto2'}, inplace = True)
Big_dati2.rename(columns = {'Scadenza2_InvestimentoA2':'Scadenza1_InvestimentoA2'}, inplace = True)
Big_dati2.rename(columns = {'Scadenza2_InvestimentoB2':'Scadenza1_InvestimentoB2'}, inplace = True)
Big_dati2.rename(columns = {'Scadenza2_NonInvesto2':'Scadenza1_NonInvesto2'}, inplace = True)
Big_dati2.rename(columns = {'RiduzioneCo22_InvestimentoA2':'RiduzioneCo21_InvestimentoA2'}, inplace = True)
Big_dati2.rename(columns = {'RiduzioneCo22_InvestimentoB2':'RiduzioneCo21_InvestimentoB2'}, inplace = True)
Big_dati2.rename(columns = {'RiduzioneCo22_NonInvesto2':'RiduzioneCo21_NonInvesto2'}, inplace = True)
Big_dati_long2 = wide_to_long(Big_dati2,id_col='Indice_Persona', alt_list=['InvestimentoA2','InvestimentoB2','NonInvesto2'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')

Big_dati_long=Big_dati_long.append(Big_dati_long2)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice2'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice2'],axis=1)


#scelta 3
ChoiceSet3=pd.DataFrame(data=dati,columns=['Choice3'])
Rischio_C3A=[0]*224
Rischio_C3B=[0]*224
Rendimento_C3A=[0]*224
Rendimento_C3B=[0]*224
Scadenza_C3A=[0]*224
Scadenza_C3B=[0]*224
Riduzione_C3A=[0]*224
Riduzione_C3B=[0]*224
for i in range(len(ChoiceSet3)):
    Rischio_C3A[i]=Attributi_livelli_A.loc['Choice3','Rischio_A'];
    Rischio_C3B[i]=Attributi_livelli_B.loc['Choice3','Rischio_B'];
    Rendimento_C3A[i]=Attributi_livelli_A.loc['Choice3','Rendimento_A'];
    Rendimento_C3B[i]=Attributi_livelli_B.loc['Choice3','Rendimento_B'];
    Scadenza_C3A[i]=Attributi_livelli_A.loc['Choice3','Scadenza_A'];
    Scadenza_C3B[i]=Attributi_livelli_B.loc['Choice3','Scadenza_B'];
    Riduzione_C3A[i]=Attributi_livelli_A.loc['Choice3','RiduzioneCO2_A'];
    Riduzione_C3B[i]=Attributi_livelli_B.loc['Choice3','RiduzioneCO2_B']; 
ChoiceSet3['Rischio3_InvestimentoA3']=Rischio_C3A
ChoiceSet3['Rischio3_InvestimentoB3']=Rischio_C3B
ChoiceSet3['Rischio3_NonInvesto3']=PerColonnaNulla

ChoiceSet3['Rendimento3_InvestimentoA3']=Rendimento_C3A
ChoiceSet3['Rendimento3_InvestimentoB3']=Rendimento_C3B
ChoiceSet3['Rendimento3_NonInvesto3']=PerColonnaNulla

ChoiceSet3['Scadenza3_InvestimentoA3']=Scadenza_C3A
ChoiceSet3['Scadenza3_InvestimentoB3']=Scadenza_C3B
ChoiceSet3['Scadenza3_NonInvesto3']=PerColonnaNulla

ChoiceSet3['RiduzioneCo23_InvestimentoA3']=Riduzione_C3A
ChoiceSet3['RiduzioneCo23_InvestimentoB3']=Riduzione_C3B
ChoiceSet3['RiduzioneCo23_NonInvesto3']=PerColonnaNulla
Big_dati3=pd.concat([DataSet_sociodemo, ChoiceSet3], axis=1)
Big_dati3.insert(0, 'Indice_Persona', Big_dati3.index)
Big_dati3.rename(columns = {'Rischio3_InvestimentoA3':'Rischio1_InvestimentoA3'}, inplace = True)
Big_dati3.rename(columns = {'Rischio3_InvestimentoB3':'Rischio1_InvestimentoB3'}, inplace = True)
Big_dati3.rename(columns = {'Rischio3_NonInvesto3':'Rischio1_NonInvesto3'}, inplace = True)
Big_dati3.rename(columns = {'Rendimento3_InvestimentoA3':'Rendimento1_InvestimentoA3'}, inplace = True)
Big_dati3.rename(columns = {'Rendimento3_InvestimentoB3':'Rendimento1_InvestimentoB3'}, inplace = True)
Big_dati3.rename(columns = {'Rendimento3_NonInvesto3':'Rendimento1_NonInvesto3'}, inplace = True)
Big_dati3.rename(columns = {'Scadenza3_InvestimentoA3':'Scadenza1_InvestimentoA3'}, inplace = True)
Big_dati3.rename(columns = {'Scadenza3_InvestimentoB3':'Scadenza1_InvestimentoB3'}, inplace = True)
Big_dati3.rename(columns = {'Scadenza3_NonInvesto3':'Scadenza1_NonInvesto3'}, inplace = True)
Big_dati3.rename(columns = {'RiduzioneCo23_InvestimentoA3':'RiduzioneCo21_InvestimentoA3'}, inplace = True)
Big_dati3.rename(columns = {'RiduzioneCo23_InvestimentoB3':'RiduzioneCo21_InvestimentoB3'}, inplace = True)
Big_dati3.rename(columns = {'RiduzioneCo23_NonInvesto3':'RiduzioneCo21_NonInvesto3'}, inplace = True)
Big_dati_long3 = wide_to_long(Big_dati3,id_col='Indice_Persona', alt_list=['InvestimentoA3','InvestimentoB3','NonInvesto3'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long3)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice3'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice3'],axis=1)

#scelta 4
ChoiceSet4=pd.DataFrame(data=dati,columns=['Choice4'])
Rischio_C4A=[0]*224
Rischio_C4B=[0]*224
Rendimento_C4A=[0]*224
Rendimento_C4B=[0]*224
Scadenza_C4A=[0]*224
Scadenza_C4B=[0]*224
Riduzione_C4A=[0]*224
Riduzione_C4B=[0]*224
for i in range(len(ChoiceSet4)):
    Rischio_C4A[i]=Attributi_livelli_A.loc['Choice4','Rischio_A'];
    Rischio_C4B[i]=Attributi_livelli_B.loc['Choice4','Rischio_B'];
    Rendimento_C4A[i]=Attributi_livelli_A.loc['Choice4','Rendimento_A'];
    Rendimento_C4B[i]=Attributi_livelli_B.loc['Choice4','Rendimento_B'];
    Scadenza_C4A[i]=Attributi_livelli_A.loc['Choice4','Scadenza_A'];
    Scadenza_C4B[i]=Attributi_livelli_B.loc['Choice4','Scadenza_B'];
    Riduzione_C4A[i]=Attributi_livelli_A.loc['Choice4','RiduzioneCO2_A'];
    Riduzione_C4B[i]=Attributi_livelli_B.loc['Choice4','RiduzioneCO2_B']; 
ChoiceSet4['Rischio4_InvestimentoA4']=Rischio_C4A
ChoiceSet4['Rischio4_InvestimentoB4']=Rischio_C4B
ChoiceSet4['Rischio4_NonInvesto4']=PerColonnaNulla

ChoiceSet4['Rendimento4_InvestimentoA4']=Rendimento_C4A
ChoiceSet4['Rendimento4_InvestimentoB4']=Rendimento_C4B
ChoiceSet4['Rendimento4_NonInvesto4']=PerColonnaNulla

ChoiceSet4['Scadenza4_InvestimentoA4']=Scadenza_C4A
ChoiceSet4['Scadenza4_InvestimentoB4']=Scadenza_C4B
ChoiceSet4['Scadenza4_NonInvesto4']=PerColonnaNulla

ChoiceSet4['RiduzioneCo24_InvestimentoA4']=Riduzione_C4A
ChoiceSet4['RiduzioneCo24_InvestimentoB4']=Riduzione_C4B
ChoiceSet4['RiduzioneCo24_NonInvesto4']=PerColonnaNulla
Big_dati4=pd.concat([DataSet_sociodemo, ChoiceSet4], axis=1)
Big_dati4.insert(0, 'Indice_Persona', Big_dati4.index)
Big_dati4.rename(columns = {'Rischio4_InvestimentoA4':'Rischio1_InvestimentoA4'}, inplace = True)
Big_dati4.rename(columns = {'Rischio4_InvestimentoB4':'Rischio1_InvestimentoB4'}, inplace = True)
Big_dati4.rename(columns = {'Rischio4_NonInvesto4':'Rischio1_NonInvesto4'}, inplace = True)
Big_dati4.rename(columns = {'Rendimento4_InvestimentoA4':'Rendimento1_InvestimentoA4'}, inplace = True)
Big_dati4.rename(columns = {'Rendimento4_InvestimentoB4':'Rendimento1_InvestimentoB4'}, inplace = True)
Big_dati4.rename(columns = {'Rendimento4_NonInvesto4':'Rendimento1_NonInvesto4'}, inplace = True)
Big_dati4.rename(columns = {'Scadenza4_InvestimentoA4':'Scadenza1_InvestimentoA4'}, inplace = True)
Big_dati4.rename(columns = {'Scadenza4_InvestimentoB4':'Scadenza1_InvestimentoB4'}, inplace = True)
Big_dati4.rename(columns = {'Scadenza4_NonInvesto4':'Scadenza1_NonInvesto4'}, inplace = True)
Big_dati4.rename(columns = {'RiduzioneCo24_InvestimentoA4':'RiduzioneCo21_InvestimentoA4'}, inplace = True)
Big_dati4.rename(columns = {'RiduzioneCo24_InvestimentoB4':'RiduzioneCo21_InvestimentoB4'}, inplace = True)
Big_dati4.rename(columns = {'RiduzioneCo24_NonInvesto4':'RiduzioneCo21_NonInvesto4'}, inplace = True)
Big_dati_long4 = wide_to_long(Big_dati4,id_col='Indice_Persona', alt_list=['InvestimentoA4','InvestimentoB4','NonInvesto4'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long4)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice4'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice4'],axis=1)

#scelta 5
ChoiceSet5=pd.DataFrame(data=dati,columns=['Choice5'])
Rischio_C5A=[0]*224
Rischio_C5B=[0]*224
Rendimento_C5A=[0]*224
Rendimento_C5B=[0]*224
Scadenza_C5A=[0]*224
Scadenza_C5B=[0]*224
Riduzione_C5A=[0]*224
Riduzione_C5B=[0]*224
for i in range(len(ChoiceSet5)):
    Rischio_C5A[i]=Attributi_livelli_A.loc['Choice5','Rischio_A'];
    Rischio_C5B[i]=Attributi_livelli_B.loc['Choice5','Rischio_B'];
    Rendimento_C5A[i]=Attributi_livelli_A.loc['Choice5','Rendimento_A'];
    Rendimento_C5B[i]=Attributi_livelli_B.loc['Choice5','Rendimento_B'];
    Scadenza_C5A[i]=Attributi_livelli_A.loc['Choice5','Scadenza_A'];
    Scadenza_C5B[i]=Attributi_livelli_B.loc['Choice5','Scadenza_B'];
    Riduzione_C5A[i]=Attributi_livelli_A.loc['Choice5','RiduzioneCO2_A'];
    Riduzione_C5B[i]=Attributi_livelli_B.loc['Choice5','RiduzioneCO2_B']; 
ChoiceSet5['Rischio5_InvestimentoA5']=Rischio_C5A
ChoiceSet5['Rischio5_InvestimentoB5']=Rischio_C5B
ChoiceSet5['Rischio5_NonInvesto5']=PerColonnaNulla

ChoiceSet5['Rendimento5_InvestimentoA5']=Rendimento_C5A
ChoiceSet5['Rendimento5_InvestimentoB5']=Rendimento_C5B
ChoiceSet5['Rendimento5_NonInvesto5']=PerColonnaNulla

ChoiceSet5['Scadenza5_InvestimentoA5']=Scadenza_C5A
ChoiceSet5['Scadenza5_InvestimentoB5']=Scadenza_C5B
ChoiceSet5['Scadenza5_NonInvesto5']=PerColonnaNulla

ChoiceSet5['RiduzioneCo25_InvestimentoA5']=Riduzione_C5A
ChoiceSet5['RiduzioneCo25_InvestimentoB5']=Riduzione_C5B
ChoiceSet5['RiduzioneCo25_NonInvesto5']=PerColonnaNulla
Big_dati5=pd.concat([DataSet_sociodemo, ChoiceSet5], axis=1)
Big_dati5.insert(0, 'Indice_Persona', Big_dati5.index)
Big_dati5.rename(columns = {'Rischio5_InvestimentoA5':'Rischio1_InvestimentoA5'}, inplace = True)
Big_dati5.rename(columns = {'Rischio5_InvestimentoB5':'Rischio1_InvestimentoB5'}, inplace = True)
Big_dati5.rename(columns = {'Rischio5_NonInvesto5':'Rischio1_NonInvesto5'}, inplace = True)
Big_dati5.rename(columns = {'Rendimento5_InvestimentoA5':'Rendimento1_InvestimentoA5'}, inplace = True)
Big_dati5.rename(columns = {'Rendimento5_InvestimentoB5':'Rendimento1_InvestimentoB5'}, inplace = True)
Big_dati5.rename(columns = {'Rendimento5_NonInvesto5':'Rendimento1_NonInvesto5'}, inplace = True)
Big_dati5.rename(columns = {'Scadenza5_InvestimentoA5':'Scadenza1_InvestimentoA5'}, inplace = True)
Big_dati5.rename(columns = {'Scadenza5_InvestimentoB5':'Scadenza1_InvestimentoB5'}, inplace = True)
Big_dati5.rename(columns = {'Scadenza5_NonInvesto5':'Scadenza1_NonInvesto5'}, inplace = True)
Big_dati5.rename(columns = {'RiduzioneCo25_InvestimentoA5':'RiduzioneCo21_InvestimentoA5'}, inplace = True)
Big_dati5.rename(columns = {'RiduzioneCo25_InvestimentoB5':'RiduzioneCo21_InvestimentoB5'}, inplace = True)
Big_dati5.rename(columns = {'RiduzioneCo25_NonInvesto5':'RiduzioneCo21_NonInvesto5'}, inplace = True)
Big_dati_long5 = wide_to_long(Big_dati5,id_col='Indice_Persona', alt_list=['InvestimentoA5','InvestimentoB5','NonInvesto5'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long5)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice5'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice5'],axis=1)

#scelta 6
ChoiceSet6=pd.DataFrame(data=dati,columns=['Choice6'])
Rischio_C6A=[0]*224
Rischio_C6B=[0]*224
Rendimento_C6A=[0]*224
Rendimento_C6B=[0]*224
Scadenza_C6A=[0]*224
Scadenza_C6B=[0]*224
Riduzione_C6A=[0]*224
Riduzione_C6B=[0]*224
for i in range(len(ChoiceSet6)):
    Rischio_C6A[i]=Attributi_livelli_A.loc['Choice6','Rischio_A'];
    Rischio_C6B[i]=Attributi_livelli_B.loc['Choice6','Rischio_B'];
    Rendimento_C6A[i]=Attributi_livelli_A.loc['Choice6','Rendimento_A'];
    Rendimento_C6B[i]=Attributi_livelli_B.loc['Choice6','Rendimento_B'];
    Scadenza_C6A[i]=Attributi_livelli_A.loc['Choice6','Scadenza_A'];
    Scadenza_C6B[i]=Attributi_livelli_B.loc['Choice6','Scadenza_B'];
    Riduzione_C6A[i]=Attributi_livelli_A.loc['Choice6','RiduzioneCO2_A'];
    Riduzione_C6B[i]=Attributi_livelli_B.loc['Choice6','RiduzioneCO2_B']; 
ChoiceSet6['Rischio6_InvestimentoA6']=Rischio_C6A
ChoiceSet6['Rischio6_InvestimentoB6']=Rischio_C6B
ChoiceSet6['Rischio6_NonInvesto6']=PerColonnaNulla

ChoiceSet6['Rendimento6_InvestimentoA6']=Rendimento_C6A
ChoiceSet6['Rendimento6_InvestimentoB6']=Rendimento_C6B
ChoiceSet6['Rendimento6_NonInvesto6']=PerColonnaNulla

ChoiceSet6['Scadenza6_InvestimentoA6']=Scadenza_C6A
ChoiceSet6['Scadenza6_InvestimentoB6']=Scadenza_C6B
ChoiceSet6['Scadenza6_NonInvesto6']=PerColonnaNulla

ChoiceSet6['RiduzioneCo26_InvestimentoA6']=Riduzione_C6A
ChoiceSet6['RiduzioneCo26_InvestimentoB6']=Riduzione_C6B
ChoiceSet6['RiduzioneCo26_NonInvesto6']=PerColonnaNulla
Big_dati6=pd.concat([DataSet_sociodemo, ChoiceSet6], axis=1)
Big_dati6.insert(0, 'Indice_Persona', Big_dati6.index)
Big_dati6.rename(columns = {'Rischio6_InvestimentoA6':'Rischio1_InvestimentoA6'}, inplace = True)
Big_dati6.rename(columns = {'Rischio6_InvestimentoB6':'Rischio1_InvestimentoB6'}, inplace = True)
Big_dati6.rename(columns = {'Rischio6_NonInvesto6':'Rischio1_NonInvesto6'}, inplace = True)
Big_dati6.rename(columns = {'Rendimento6_InvestimentoA6':'Rendimento1_InvestimentoA6'}, inplace = True)
Big_dati6.rename(columns = {'Rendimento6_InvestimentoB6':'Rendimento1_InvestimentoB6'}, inplace = True)
Big_dati6.rename(columns = {'Rendimento6_NonInvesto6':'Rendimento1_NonInvesto6'}, inplace = True)
Big_dati6.rename(columns = {'Scadenza6_InvestimentoA6':'Scadenza1_InvestimentoA6'}, inplace = True)
Big_dati6.rename(columns = {'Scadenza6_InvestimentoB6':'Scadenza1_InvestimentoB6'}, inplace = True)
Big_dati6.rename(columns = {'Scadenza6_NonInvesto6':'Scadenza1_NonInvesto6'}, inplace = True)
Big_dati6.rename(columns = {'RiduzioneCo26_InvestimentoA6':'RiduzioneCo21_InvestimentoA6'}, inplace = True)
Big_dati6.rename(columns = {'RiduzioneCo26_InvestimentoB6':'RiduzioneCo21_InvestimentoB6'}, inplace = True)
Big_dati6.rename(columns = {'RiduzioneCo26_NonInvesto6':'RiduzioneCo21_NonInvesto6'}, inplace = True)
Big_dati_long6 = wide_to_long(Big_dati6,id_col='Indice_Persona', alt_list=['InvestimentoA6','InvestimentoB6','NonInvesto6'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long6)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice6'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice6'],axis=1)

#scelta 7
ChoiceSet7=pd.DataFrame(data=dati,columns=['Choice7'])
Rischio_C7A=[0]*224
Rischio_C7B=[0]*224
Rendimento_C7A=[0]*224
Rendimento_C7B=[0]*224
Scadenza_C7A=[0]*224
Scadenza_C7B=[0]*224
Riduzione_C7A=[0]*224
Riduzione_C7B=[0]*224
for i in range(len(ChoiceSet7)):
    Rischio_C7A[i]=Attributi_livelli_A.loc['Choice7','Rischio_A'];
    Rischio_C7B[i]=Attributi_livelli_B.loc['Choice7','Rischio_B'];
    Rendimento_C7A[i]=Attributi_livelli_A.loc['Choice7','Rendimento_A'];
    Rendimento_C7B[i]=Attributi_livelli_B.loc['Choice7','Rendimento_B'];
    Scadenza_C7A[i]=Attributi_livelli_A.loc['Choice7','Scadenza_A'];
    Scadenza_C7B[i]=Attributi_livelli_B.loc['Choice7','Scadenza_B'];
    Riduzione_C7A[i]=Attributi_livelli_A.loc['Choice7','RiduzioneCO2_A'];
    Riduzione_C7B[i]=Attributi_livelli_B.loc['Choice7','RiduzioneCO2_B']; 
ChoiceSet7['Rischio7_InvestimentoA7']=Rischio_C7A
ChoiceSet7['Rischio7_InvestimentoB7']=Rischio_C7B
ChoiceSet7['Rischio7_NonInvesto7']=PerColonnaNulla

ChoiceSet7['Rendimento7_InvestimentoA7']=Rendimento_C7A
ChoiceSet7['Rendimento7_InvestimentoB7']=Rendimento_C7B
ChoiceSet7['Rendimento7_NonInvesto7']=PerColonnaNulla

ChoiceSet7['Scadenza7_InvestimentoA7']=Scadenza_C7A
ChoiceSet7['Scadenza7_InvestimentoB7']=Scadenza_C7B
ChoiceSet7['Scadenza7_NonInvesto7']=PerColonnaNulla

ChoiceSet7['RiduzioneCo27_InvestimentoA7']=Riduzione_C7A
ChoiceSet7['RiduzioneCo27_InvestimentoB7']=Riduzione_C7B
ChoiceSet7['RiduzioneCo27_NonInvesto7']=PerColonnaNulla
Big_dati7=pd.concat([DataSet_sociodemo, ChoiceSet7], axis=1)
Big_dati7.insert(0, 'Indice_Persona', Big_dati7.index)
Big_dati7.rename(columns = {'Rischio7_InvestimentoA7':'Rischio1_InvestimentoA7'}, inplace = True)
Big_dati7.rename(columns = {'Rischio7_InvestimentoB7':'Rischio1_InvestimentoB7'}, inplace = True)
Big_dati7.rename(columns = {'Rischio7_NonInvesto7':'Rischio1_NonInvesto7'}, inplace = True)
Big_dati7.rename(columns = {'Rendimento7_InvestimentoA7':'Rendimento1_InvestimentoA7'}, inplace = True)
Big_dati7.rename(columns = {'Rendimento7_InvestimentoB7':'Rendimento1_InvestimentoB7'}, inplace = True)
Big_dati7.rename(columns = {'Rendimento7_NonInvesto7':'Rendimento1_NonInvesto7'}, inplace = True)
Big_dati7.rename(columns = {'Scadenza7_InvestimentoA7':'Scadenza1_InvestimentoA7'}, inplace = True)
Big_dati7.rename(columns = {'Scadenza7_InvestimentoB7':'Scadenza1_InvestimentoB7'}, inplace = True)
Big_dati7.rename(columns = {'Scadenza7_NonInvesto7':'Scadenza1_NonInvesto7'}, inplace = True)
Big_dati7.rename(columns = {'RiduzioneCo27_InvestimentoA7':'RiduzioneCo21_InvestimentoA7'}, inplace = True)
Big_dati7.rename(columns = {'RiduzioneCo27_InvestimentoB7':'RiduzioneCo21_InvestimentoB7'}, inplace = True)
Big_dati7.rename(columns = {'RiduzioneCo27_NonInvesto7':'RiduzioneCo21_NonInvesto7'}, inplace = True)
Big_dati_long7 = wide_to_long(Big_dati7,id_col='Indice_Persona', alt_list=['InvestimentoA7','InvestimentoB7','NonInvesto7'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long7)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice7'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice7'],axis=1)

#scelta 8
ChoiceSet8=pd.DataFrame(data=dati,columns=['Choice8'])
Rischio_C8A=[0]*224
Rischio_C8B=[0]*224
Rendimento_C8A=[0]*224
Rendimento_C8B=[0]*224
Scadenza_C8A=[0]*224
Scadenza_C8B=[0]*224
Riduzione_C8A=[0]*224
Riduzione_C8B=[0]*224
for i in range(len(ChoiceSet8)):
    Rischio_C8A[i]=Attributi_livelli_A.loc['Choice8','Rischio_A'];
    Rischio_C8B[i]=Attributi_livelli_B.loc['Choice8','Rischio_B'];
    Rendimento_C8A[i]=Attributi_livelli_A.loc['Choice8','Rendimento_A'];
    Rendimento_C8B[i]=Attributi_livelli_B.loc['Choice8','Rendimento_B'];
    Scadenza_C8A[i]=Attributi_livelli_A.loc['Choice8','Scadenza_A'];
    Scadenza_C8B[i]=Attributi_livelli_B.loc['Choice8','Scadenza_B'];
    Riduzione_C8A[i]=Attributi_livelli_A.loc['Choice8','RiduzioneCO2_A'];
    Riduzione_C8B[i]=Attributi_livelli_B.loc['Choice8','RiduzioneCO2_B']; 
ChoiceSet8['Rischio8_InvestimentoA8']=Rischio_C8A
ChoiceSet8['Rischio8_InvestimentoB8']=Rischio_C8B
ChoiceSet8['Rischio8_NonInvesto8']=PerColonnaNulla

ChoiceSet8['Rendimento8_InvestimentoA8']=Rendimento_C8A
ChoiceSet8['Rendimento8_InvestimentoB8']=Rendimento_C8B
ChoiceSet8['Rendimento8_NonInvesto8']=PerColonnaNulla

ChoiceSet8['Scadenza8_InvestimentoA8']=Scadenza_C8A
ChoiceSet8['Scadenza8_InvestimentoB8']=Scadenza_C8B
ChoiceSet8['Scadenza8_NonInvesto8']=PerColonnaNulla

ChoiceSet8['RiduzioneCo28_InvestimentoA8']=Riduzione_C8A
ChoiceSet8['RiduzioneCo28_InvestimentoB8']=Riduzione_C8B
ChoiceSet8['RiduzioneCo28_NonInvesto8']=PerColonnaNulla
Big_dati8=pd.concat([DataSet_sociodemo, ChoiceSet8], axis=1)
Big_dati8.insert(0, 'Indice_Persona', Big_dati8.index)
Big_dati8.rename(columns = {'Rischio8_InvestimentoA8':'Rischio1_InvestimentoA8'}, inplace = True)
Big_dati8.rename(columns = {'Rischio8_InvestimentoB8':'Rischio1_InvestimentoB8'}, inplace = True)
Big_dati8.rename(columns = {'Rischio8_NonInvesto8':'Rischio1_NonInvesto8'}, inplace = True)
Big_dati8.rename(columns = {'Rendimento8_InvestimentoA8':'Rendimento1_InvestimentoA8'}, inplace = True)
Big_dati8.rename(columns = {'Rendimento8_InvestimentoB8':'Rendimento1_InvestimentoB8'}, inplace = True)
Big_dati8.rename(columns = {'Rendimento8_NonInvesto8':'Rendimento1_NonInvesto8'}, inplace = True)
Big_dati8.rename(columns = {'Scadenza8_InvestimentoA8':'Scadenza1_InvestimentoA8'}, inplace = True)
Big_dati8.rename(columns = {'Scadenza8_InvestimentoB8':'Scadenza1_InvestimentoB8'}, inplace = True)
Big_dati8.rename(columns = {'Scadenza8_NonInvesto8':'Scadenza1_NonInvesto8'}, inplace = True)
Big_dati8.rename(columns = {'RiduzioneCo28_InvestimentoA8':'RiduzioneCo21_InvestimentoA8'}, inplace = True)
Big_dati8.rename(columns = {'RiduzioneCo28_InvestimentoB8':'RiduzioneCo21_InvestimentoB8'}, inplace = True)
Big_dati8.rename(columns = {'RiduzioneCo28_NonInvesto8':'RiduzioneCo21_NonInvesto8'}, inplace = True)
Big_dati_long8 = wide_to_long(Big_dati8,id_col='Indice_Persona', alt_list=['InvestimentoA8','InvestimentoB8','NonInvesto8'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long8)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice8'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice8'],axis=1)

#scelta 9
ChoiceSet9=pd.DataFrame(data=dati,columns=['Choice9'])
Rischio_C9A=[0]*224
Rischio_C9B=[0]*224
Rendimento_C9A=[0]*224
Rendimento_C9B=[0]*224
Scadenza_C9A=[0]*224
Scadenza_C9B=[0]*224
Riduzione_C9A=[0]*224
Riduzione_C9B=[0]*224
for i in range(len(ChoiceSet9)):
    Rischio_C9A[i]=Attributi_livelli_A.loc['Choice9','Rischio_A'];
    Rischio_C9B[i]=Attributi_livelli_B.loc['Choice9','Rischio_B'];
    Rendimento_C9A[i]=Attributi_livelli_A.loc['Choice9','Rendimento_A'];
    Rendimento_C9B[i]=Attributi_livelli_B.loc['Choice9','Rendimento_B'];
    Scadenza_C9A[i]=Attributi_livelli_A.loc['Choice9','Scadenza_A'];
    Scadenza_C9B[i]=Attributi_livelli_B.loc['Choice9','Scadenza_B'];
    Riduzione_C9A[i]=Attributi_livelli_A.loc['Choice9','RiduzioneCO2_A'];
    Riduzione_C9B[i]=Attributi_livelli_B.loc['Choice9','RiduzioneCO2_B']; 
ChoiceSet9['Rischio9_InvestimentoA9']=Rischio_C9A
ChoiceSet9['Rischio9_InvestimentoB9']=Rischio_C9B
ChoiceSet9['Rischio9_NonInvesto9']=PerColonnaNulla

ChoiceSet9['Rendimento9_InvestimentoA9']=Rendimento_C9A
ChoiceSet9['Rendimento9_InvestimentoB9']=Rendimento_C9B
ChoiceSet9['Rendimento9_NonInvesto9']=PerColonnaNulla

ChoiceSet9['Scadenza9_InvestimentoA9']=Scadenza_C9A
ChoiceSet9['Scadenza9_InvestimentoB9']=Scadenza_C9B
ChoiceSet9['Scadenza9_NonInvesto9']=PerColonnaNulla

ChoiceSet9['RiduzioneCo29_InvestimentoA9']=Riduzione_C9A
ChoiceSet9['RiduzioneCo29_InvestimentoB9']=Riduzione_C9B
ChoiceSet9['RiduzioneCo29_NonInvesto9']=PerColonnaNulla
Big_dati9=pd.concat([DataSet_sociodemo, ChoiceSet9], axis=1)
Big_dati9.insert(0, 'Indice_Persona', Big_dati9.index)
Big_dati9.rename(columns = {'Rischio9_InvestimentoA9':'Rischio1_InvestimentoA9'}, inplace = True)
Big_dati9.rename(columns = {'Rischio9_InvestimentoB9':'Rischio1_InvestimentoB9'}, inplace = True)
Big_dati9.rename(columns = {'Rischio9_NonInvesto9':'Rischio1_NonInvesto9'}, inplace = True)
Big_dati9.rename(columns = {'Rendimento9_InvestimentoA9':'Rendimento1_InvestimentoA9'}, inplace = True)
Big_dati9.rename(columns = {'Rendimento9_InvestimentoB9':'Rendimento1_InvestimentoB9'}, inplace = True)
Big_dati9.rename(columns = {'Rendimento9_NonInvesto9':'Rendimento1_NonInvesto9'}, inplace = True)
Big_dati9.rename(columns = {'Scadenza9_InvestimentoA9':'Scadenza1_InvestimentoA9'}, inplace = True)
Big_dati9.rename(columns = {'Scadenza9_InvestimentoB9':'Scadenza1_InvestimentoB9'}, inplace = True)
Big_dati9.rename(columns = {'Scadenza9_NonInvesto9':'Scadenza1_NonInvesto9'}, inplace = True)
Big_dati9.rename(columns = {'RiduzioneCo29_InvestimentoA9':'RiduzioneCo21_InvestimentoA9'}, inplace = True)
Big_dati9.rename(columns = {'RiduzioneCo29_InvestimentoB9':'RiduzioneCo21_InvestimentoB9'}, inplace = True)
Big_dati9.rename(columns = {'RiduzioneCo29_NonInvesto9':'RiduzioneCo21_NonInvesto9'}, inplace = True)
Big_dati_long9 = wide_to_long(Big_dati9,id_col='Indice_Persona', alt_list=['InvestimentoA9','InvestimentoB9','NonInvesto9'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long9)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice9'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice9'],axis=1)

#scelta 10
ChoiceSet10=pd.DataFrame(data=dati,columns=['Choice10'])
Rischio_C10A=[0]*224
Rischio_C10B=[0]*224
Rendimento_C10A=[0]*224
Rendimento_C10B=[0]*224
Scadenza_C10A=[0]*224
Scadenza_C10B=[0]*224
Riduzione_C10A=[0]*224
Riduzione_C10B=[0]*224
for i in range(len(ChoiceSet10)):
    Rischio_C10A[i]=Attributi_livelli_A.loc['Choice10','Rischio_A'];
    Rischio_C10B[i]=Attributi_livelli_B.loc['Choice10','Rischio_B'];
    Rendimento_C10A[i]=Attributi_livelli_A.loc['Choice10','Rendimento_A'];
    Rendimento_C10B[i]=Attributi_livelli_B.loc['Choice10','Rendimento_B'];
    Scadenza_C10A[i]=Attributi_livelli_A.loc['Choice10','Scadenza_A'];
    Scadenza_C10B[i]=Attributi_livelli_B.loc['Choice10','Scadenza_B'];
    Riduzione_C10A[i]=Attributi_livelli_A.loc['Choice10','RiduzioneCO2_A'];
    Riduzione_C10B[i]=Attributi_livelli_B.loc['Choice10','RiduzioneCO2_B']; 
ChoiceSet10['Rischio10_InvestimentoA10']=Rischio_C10A
ChoiceSet10['Rischio10_InvestimentoB10']=Rischio_C10B
ChoiceSet10['Rischio10_NonInvesto10']=PerColonnaNulla

ChoiceSet10['Rendimento10_InvestimentoA10']=Rendimento_C10A
ChoiceSet10['Rendimento10_InvestimentoB10']=Rendimento_C10B
ChoiceSet10['Rendimento10_NonInvesto10']=PerColonnaNulla

ChoiceSet10['Scadenza10_InvestimentoA10']=Scadenza_C10A
ChoiceSet10['Scadenza10_InvestimentoB10']=Scadenza_C10B
ChoiceSet10['Scadenza10_NonInvesto10']=PerColonnaNulla

ChoiceSet10['RiduzioneCo210_InvestimentoA10']=Riduzione_C10A
ChoiceSet10['RiduzioneCo210_InvestimentoB10']=Riduzione_C10B
ChoiceSet10['RiduzioneCo210_NonInvesto10']=PerColonnaNulla
Big_dati10=pd.concat([DataSet_sociodemo, ChoiceSet10], axis=1)
Big_dati10.insert(0, 'Indice_Persona', Big_dati10.index)
Big_dati10.rename(columns = {'Rischio10_InvestimentoA10':'Rischio1_InvestimentoA10'}, inplace = True)
Big_dati10.rename(columns = {'Rischio10_InvestimentoB10':'Rischio1_InvestimentoB10'}, inplace = True)
Big_dati10.rename(columns = {'Rischio10_NonInvesto10':'Rischio1_NonInvesto10'}, inplace = True)
Big_dati10.rename(columns = {'Rendimento10_InvestimentoA10':'Rendimento1_InvestimentoA10'}, inplace = True)
Big_dati10.rename(columns = {'Rendimento10_InvestimentoB10':'Rendimento1_InvestimentoB10'}, inplace = True)
Big_dati10.rename(columns = {'Rendimento10_NonInvesto10':'Rendimento1_NonInvesto10'}, inplace = True)
Big_dati10.rename(columns = {'Scadenza10_InvestimentoA10':'Scadenza1_InvestimentoA10'}, inplace = True)
Big_dati10.rename(columns = {'Scadenza10_InvestimentoB10':'Scadenza1_InvestimentoB10'}, inplace = True)
Big_dati10.rename(columns = {'Scadenza10_NonInvesto10':'Scadenza1_NonInvesto10'}, inplace = True)
Big_dati10.rename(columns = {'RiduzioneCo210_InvestimentoA10':'RiduzioneCo21_InvestimentoA10'}, inplace = True)
Big_dati10.rename(columns = {'RiduzioneCo210_InvestimentoB10':'RiduzioneCo21_InvestimentoB10'}, inplace = True)
Big_dati10.rename(columns = {'RiduzioneCo210_NonInvesto10':'RiduzioneCo21_NonInvesto10'}, inplace = True)
Big_dati_long10 = wide_to_long(Big_dati10,id_col='Indice_Persona', alt_list=['InvestimentoA10','InvestimentoB10','NonInvesto10'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long10)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice10'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice10'],axis=1)

#scelta 11
ChoiceSet11=pd.DataFrame(data=dati,columns=['Choice11'])
Rischio_C11A=[0]*224
Rischio_C11B=[0]*224
Rendimento_C11A=[0]*224
Rendimento_C11B=[0]*224
Scadenza_C11A=[0]*224
Scadenza_C11B=[0]*224
Riduzione_C11A=[0]*224
Riduzione_C11B=[0]*224
for i in range(len(ChoiceSet11)):
    Rischio_C11A[i]=Attributi_livelli_A.loc['Choice11','Rischio_A'];
    Rischio_C11B[i]=Attributi_livelli_B.loc['Choice11','Rischio_B'];
    Rendimento_C11A[i]=Attributi_livelli_A.loc['Choice11','Rendimento_A'];
    Rendimento_C11B[i]=Attributi_livelli_B.loc['Choice11','Rendimento_B'];
    Scadenza_C11A[i]=Attributi_livelli_A.loc['Choice11','Scadenza_A'];
    Scadenza_C11B[i]=Attributi_livelli_B.loc['Choice11','Scadenza_B'];
    Riduzione_C11A[i]=Attributi_livelli_A.loc['Choice11','RiduzioneCO2_A'];
    Riduzione_C11B[i]=Attributi_livelli_B.loc['Choice11','RiduzioneCO2_B']; 
ChoiceSet11['Rischio11_InvestimentoA11']=Rischio_C11A
ChoiceSet11['Rischio11_InvestimentoB11']=Rischio_C11B
ChoiceSet11['Rischio11_NonInvesto11']=PerColonnaNulla

ChoiceSet11['Rendimento11_InvestimentoA11']=Rendimento_C11A
ChoiceSet11['Rendimento11_InvestimentoB11']=Rendimento_C11B
ChoiceSet11['Rendimento11_NonInvesto11']=PerColonnaNulla

ChoiceSet11['Scadenza11_InvestimentoA11']=Scadenza_C11A
ChoiceSet11['Scadenza11_InvestimentoB11']=Scadenza_C11B
ChoiceSet11['Scadenza11_NonInvesto11']=PerColonnaNulla

ChoiceSet11['RiduzioneCo211_InvestimentoA11']=Riduzione_C11A
ChoiceSet11['RiduzioneCo211_InvestimentoB11']=Riduzione_C11B
ChoiceSet11['RiduzioneCo211_NonInvesto11']=PerColonnaNulla
Big_dati11=pd.concat([DataSet_sociodemo, ChoiceSet11], axis=1)
Big_dati11.insert(0, 'Indice_Persona', Big_dati11.index)
Big_dati11.rename(columns = {'Rischio11_InvestimentoA11':'Rischio1_InvestimentoA11'}, inplace = True)
Big_dati11.rename(columns = {'Rischio11_InvestimentoB11':'Rischio1_InvestimentoB11'}, inplace = True)
Big_dati11.rename(columns = {'Rischio11_NonInvesto11':'Rischio1_NonInvesto11'}, inplace = True)
Big_dati11.rename(columns = {'Rendimento11_InvestimentoA11':'Rendimento1_InvestimentoA11'}, inplace = True)
Big_dati11.rename(columns = {'Rendimento11_InvestimentoB11':'Rendimento1_InvestimentoB11'}, inplace = True)
Big_dati11.rename(columns = {'Rendimento11_NonInvesto11':'Rendimento1_NonInvesto11'}, inplace = True)
Big_dati11.rename(columns = {'Scadenza11_InvestimentoA11':'Scadenza1_InvestimentoA11'}, inplace = True)
Big_dati11.rename(columns = {'Scadenza11_InvestimentoB11':'Scadenza1_InvestimentoB11'}, inplace = True)
Big_dati11.rename(columns = {'Scadenza11_NonInvesto11':'Scadenza1_NonInvesto11'}, inplace = True)
Big_dati11.rename(columns = {'RiduzioneCo211_InvestimentoA11':'RiduzioneCo21_InvestimentoA11'}, inplace = True)
Big_dati11.rename(columns = {'RiduzioneCo211_InvestimentoB11':'RiduzioneCo21_InvestimentoB11'}, inplace = True)
Big_dati11.rename(columns = {'RiduzioneCo211_NonInvesto11':'RiduzioneCo21_NonInvesto11'}, inplace = True)
Big_dati_long11 = wide_to_long(Big_dati11,id_col='Indice_Persona', alt_list=['InvestimentoA11','InvestimentoB11','NonInvesto11'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long11)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice11'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice11'],axis=1)

#scelta 12
ChoiceSet12=pd.DataFrame(data=dati,columns=['Choice12'])
Rischio_C12A=[0]*224
Rischio_C12B=[0]*224
Rendimento_C12A=[0]*224
Rendimento_C12B=[0]*224
Scadenza_C12A=[0]*224
Scadenza_C12B=[0]*224
Riduzione_C12A=[0]*224
Riduzione_C12B=[0]*224
for i in range(len(ChoiceSet12)):
    Rischio_C12A[i]=Attributi_livelli_A.loc['Choice12','Rischio_A'];
    Rischio_C12B[i]=Attributi_livelli_B.loc['Choice12','Rischio_B'];
    Rendimento_C12A[i]=Attributi_livelli_A.loc['Choice12','Rendimento_A'];
    Rendimento_C12B[i]=Attributi_livelli_B.loc['Choice12','Rendimento_B'];
    Scadenza_C12A[i]=Attributi_livelli_A.loc['Choice12','Scadenza_A'];
    Scadenza_C12B[i]=Attributi_livelli_B.loc['Choice12','Scadenza_B'];
    Riduzione_C12A[i]=Attributi_livelli_A.loc['Choice12','RiduzioneCO2_A'];
    Riduzione_C12B[i]=Attributi_livelli_B.loc['Choice12','RiduzioneCO2_B']; 
ChoiceSet12['Rischio12_InvestimentoA12']=Rischio_C12A
ChoiceSet12['Rischio12_InvestimentoB12']=Rischio_C12B
ChoiceSet12['Rischio12_NonInvesto12']=PerColonnaNulla

ChoiceSet12['Rendimento12_InvestimentoA12']=Rendimento_C12A
ChoiceSet12['Rendimento12_InvestimentoB12']=Rendimento_C12B
ChoiceSet12['Rendimento12_NonInvesto12']=PerColonnaNulla

ChoiceSet12['Scadenza12_InvestimentoA12']=Scadenza_C12A
ChoiceSet12['Scadenza12_InvestimentoB12']=Scadenza_C12B
ChoiceSet12['Scadenza12_NonInvesto12']=PerColonnaNulla

ChoiceSet12['RiduzioneCo212_InvestimentoA12']=Riduzione_C12A
ChoiceSet12['RiduzioneCo212_InvestimentoB12']=Riduzione_C12B
ChoiceSet12['RiduzioneCo212_NonInvesto12']=PerColonnaNulla
Big_dati12=pd.concat([DataSet_sociodemo, ChoiceSet12], axis=1)
Big_dati12.insert(0, 'Indice_Persona', Big_dati12.index)
Big_dati12.rename(columns = {'Rischio12_InvestimentoA12':'Rischio1_InvestimentoA12'}, inplace = True)
Big_dati12.rename(columns = {'Rischio12_InvestimentoB12':'Rischio1_InvestimentoB12'}, inplace = True)
Big_dati12.rename(columns = {'Rischio12_NonInvesto12':'Rischio1_NonInvesto12'}, inplace = True)
Big_dati12.rename(columns = {'Rendimento12_InvestimentoA12':'Rendimento1_InvestimentoA12'}, inplace = True)
Big_dati12.rename(columns = {'Rendimento12_InvestimentoB12':'Rendimento1_InvestimentoB12'}, inplace = True)
Big_dati12.rename(columns = {'Rendimento12_NonInvesto12':'Rendimento1_NonInvesto12'}, inplace = True)
Big_dati12.rename(columns = {'Scadenza12_InvestimentoA12':'Scadenza1_InvestimentoA12'}, inplace = True)
Big_dati12.rename(columns = {'Scadenza12_InvestimentoB12':'Scadenza1_InvestimentoB12'}, inplace = True)
Big_dati12.rename(columns = {'Scadenza12_NonInvesto12':'Scadenza1_NonInvesto12'}, inplace = True)
Big_dati12.rename(columns = {'RiduzioneCo212_InvestimentoA12':'RiduzioneCo21_InvestimentoA12'}, inplace = True)
Big_dati12.rename(columns = {'RiduzioneCo212_InvestimentoB12':'RiduzioneCo21_InvestimentoB12'}, inplace = True)
Big_dati12.rename(columns = {'RiduzioneCo212_NonInvesto12':'RiduzioneCo21_NonInvesto12'}, inplace = True)
Big_dati_long12 = wide_to_long(Big_dati12,id_col='Indice_Persona', alt_list=['InvestimentoA12','InvestimentoB12','NonInvesto12'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long12)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice12'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice12'],axis=1)

#scelta 13
ChoiceSet13=pd.DataFrame(data=dati,columns=['Choice13'])
Rischio_C13A=[0]*224
Rischio_C13B=[0]*224
Rendimento_C13A=[0]*224
Rendimento_C13B=[0]*224
Scadenza_C13A=[0]*224
Scadenza_C13B=[0]*224
Riduzione_C13A=[0]*224
Riduzione_C13B=[0]*224
for i in range(len(ChoiceSet13)):
    Rischio_C13A[i]=Attributi_livelli_A.loc['Choice13','Rischio_A'];
    Rischio_C13B[i]=Attributi_livelli_B.loc['Choice13','Rischio_B'];
    Rendimento_C13A[i]=Attributi_livelli_A.loc['Choice13','Rendimento_A'];
    Rendimento_C13B[i]=Attributi_livelli_B.loc['Choice13','Rendimento_B'];
    Scadenza_C13A[i]=Attributi_livelli_A.loc['Choice13','Scadenza_A'];
    Scadenza_C13B[i]=Attributi_livelli_B.loc['Choice13','Scadenza_B'];
    Riduzione_C13A[i]=Attributi_livelli_A.loc['Choice13','RiduzioneCO2_A'];
    Riduzione_C13B[i]=Attributi_livelli_B.loc['Choice13','RiduzioneCO2_B']; 
ChoiceSet13['Rischio13_InvestimentoA13']=Rischio_C13A
ChoiceSet13['Rischio13_InvestimentoB13']=Rischio_C13B
ChoiceSet13['Rischio13_NonInvesto13']=PerColonnaNulla

ChoiceSet13['Rendimento13_InvestimentoA13']=Rendimento_C13A
ChoiceSet13['Rendimento13_InvestimentoB13']=Rendimento_C13B
ChoiceSet13['Rendimento13_NonInvesto13']=PerColonnaNulla

ChoiceSet13['Scadenza13_InvestimentoA13']=Scadenza_C13A
ChoiceSet13['Scadenza13_InvestimentoB13']=Scadenza_C13B
ChoiceSet13['Scadenza13_NonInvesto13']=PerColonnaNulla

ChoiceSet13['RiduzioneCo213_InvestimentoA13']=Riduzione_C13A
ChoiceSet13['RiduzioneCo213_InvestimentoB13']=Riduzione_C13B
ChoiceSet13['RiduzioneCo213_NonInvesto13']=PerColonnaNulla
Big_dati13=pd.concat([DataSet_sociodemo, ChoiceSet13], axis=1)
Big_dati13.insert(0, 'Indice_Persona', Big_dati13.index)
Big_dati13.rename(columns = {'Rischio13_InvestimentoA13':'Rischio1_InvestimentoA13'}, inplace = True)
Big_dati13.rename(columns = {'Rischio13_InvestimentoB13':'Rischio1_InvestimentoB13'}, inplace = True)
Big_dati13.rename(columns = {'Rischio13_NonInvesto13':'Rischio1_NonInvesto13'}, inplace = True)
Big_dati13.rename(columns = {'Rendimento13_InvestimentoA13':'Rendimento1_InvestimentoA13'}, inplace = True)
Big_dati13.rename(columns = {'Rendimento13_InvestimentoB13':'Rendimento1_InvestimentoB13'}, inplace = True)
Big_dati13.rename(columns = {'Rendimento13_NonInvesto13':'Rendimento1_NonInvesto13'}, inplace = True)
Big_dati13.rename(columns = {'Scadenza13_InvestimentoA13':'Scadenza1_InvestimentoA13'}, inplace = True)
Big_dati13.rename(columns = {'Scadenza13_InvestimentoB13':'Scadenza1_InvestimentoB13'}, inplace = True)
Big_dati13.rename(columns = {'Scadenza13_NonInvesto13':'Scadenza1_NonInvesto13'}, inplace = True)
Big_dati13.rename(columns = {'RiduzioneCo213_InvestimentoA13':'RiduzioneCo21_InvestimentoA13'}, inplace = True)
Big_dati13.rename(columns = {'RiduzioneCo213_InvestimentoB13':'RiduzioneCo21_InvestimentoB13'}, inplace = True)
Big_dati13.rename(columns = {'RiduzioneCo213_NonInvesto13':'RiduzioneCo21_NonInvesto13'}, inplace = True)
Big_dati_long13 = wide_to_long(Big_dati13,id_col='Indice_Persona', alt_list=['InvestimentoA13','InvestimentoB13','NonInvesto13'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long13)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice13'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice13'],axis=1)

#scelta 14
ChoiceSet14=pd.DataFrame(data=dati,columns=['Choice14'])
Rischio_C14A=[0]*224
Rischio_C14B=[0]*224
Rendimento_C14A=[0]*224
Rendimento_C14B=[0]*224
Scadenza_C14A=[0]*224
Scadenza_C14B=[0]*224
Riduzione_C14A=[0]*224
Riduzione_C14B=[0]*224
for i in range(len(ChoiceSet14)):
    Rischio_C14A[i]=Attributi_livelli_A.loc['Choice14','Rischio_A'];
    Rischio_C14B[i]=Attributi_livelli_B.loc['Choice14','Rischio_B'];
    Rendimento_C14A[i]=Attributi_livelli_A.loc['Choice14','Rendimento_A'];
    Rendimento_C14B[i]=Attributi_livelli_B.loc['Choice14','Rendimento_B'];
    Scadenza_C14A[i]=Attributi_livelli_A.loc['Choice14','Scadenza_A'];
    Scadenza_C14B[i]=Attributi_livelli_B.loc['Choice14','Scadenza_B'];
    Riduzione_C14A[i]=Attributi_livelli_A.loc['Choice14','RiduzioneCO2_A'];
    Riduzione_C14B[i]=Attributi_livelli_B.loc['Choice14','RiduzioneCO2_B']; 
ChoiceSet14['Rischio14_InvestimentoA14']=Rischio_C14A
ChoiceSet14['Rischio14_InvestimentoB14']=Rischio_C14B
ChoiceSet14['Rischio14_NonInvesto14']=PerColonnaNulla

ChoiceSet14['Rendimento14_InvestimentoA14']=Rendimento_C14A
ChoiceSet14['Rendimento14_InvestimentoB14']=Rendimento_C14B
ChoiceSet14['Rendimento14_NonInvesto14']=PerColonnaNulla

ChoiceSet14['Scadenza14_InvestimentoA14']=Scadenza_C14A
ChoiceSet14['Scadenza14_InvestimentoB14']=Scadenza_C14B
ChoiceSet14['Scadenza14_NonInvesto14']=PerColonnaNulla

ChoiceSet14['RiduzioneCo214_InvestimentoA14']=Riduzione_C14A
ChoiceSet14['RiduzioneCo214_InvestimentoB14']=Riduzione_C14B
ChoiceSet14['RiduzioneCo214_NonInvesto14']=PerColonnaNulla
Big_dati14=pd.concat([DataSet_sociodemo, ChoiceSet14], axis=1)
Big_dati14.insert(0, 'Indice_Persona', Big_dati14.index)
Big_dati14.rename(columns = {'Rischio14_InvestimentoA14':'Rischio1_InvestimentoA14'}, inplace = True)
Big_dati14.rename(columns = {'Rischio14_InvestimentoB14':'Rischio1_InvestimentoB14'}, inplace = True)
Big_dati14.rename(columns = {'Rischio14_NonInvesto14':'Rischio1_NonInvesto14'}, inplace = True)
Big_dati14.rename(columns = {'Rendimento14_InvestimentoA14':'Rendimento1_InvestimentoA14'}, inplace = True)
Big_dati14.rename(columns = {'Rendimento14_InvestimentoB14':'Rendimento1_InvestimentoB14'}, inplace = True)
Big_dati14.rename(columns = {'Rendimento14_NonInvesto14':'Rendimento1_NonInvesto14'}, inplace = True)
Big_dati14.rename(columns = {'Scadenza14_InvestimentoA14':'Scadenza1_InvestimentoA14'}, inplace = True)
Big_dati14.rename(columns = {'Scadenza14_InvestimentoB14':'Scadenza1_InvestimentoB14'}, inplace = True)
Big_dati14.rename(columns = {'Scadenza14_NonInvesto14':'Scadenza1_NonInvesto14'}, inplace = True)
Big_dati14.rename(columns = {'RiduzioneCo214_InvestimentoA14':'RiduzioneCo21_InvestimentoA14'}, inplace = True)
Big_dati14.rename(columns = {'RiduzioneCo214_InvestimentoB14':'RiduzioneCo21_InvestimentoB14'}, inplace = True)
Big_dati14.rename(columns = {'RiduzioneCo214_NonInvesto14':'RiduzioneCo21_NonInvesto14'}, inplace = True)
Big_dati_long14 = wide_to_long(Big_dati14,id_col='Indice_Persona', alt_list=['InvestimentoA14','InvestimentoB14','NonInvesto14'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long14)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice14'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice14'],axis=1)

#scelta 15
ChoiceSet15=pd.DataFrame(data=dati,columns=['Choice15'])
Rischio_C15A=[0]*224
Rischio_C15B=[0]*224
Rendimento_C15A=[0]*224
Rendimento_C15B=[0]*224
Scadenza_C15A=[0]*224
Scadenza_C15B=[0]*224
Riduzione_C15A=[0]*224
Riduzione_C15B=[0]*224
for i in range(len(ChoiceSet15)):
    Rischio_C15A[i]=Attributi_livelli_A.loc['Choice15','Rischio_A'];
    Rischio_C15B[i]=Attributi_livelli_B.loc['Choice15','Rischio_B'];
    Rendimento_C15A[i]=Attributi_livelli_A.loc['Choice15','Rendimento_A'];
    Rendimento_C15B[i]=Attributi_livelli_B.loc['Choice15','Rendimento_B'];
    Scadenza_C15A[i]=Attributi_livelli_A.loc['Choice15','Scadenza_A'];
    Scadenza_C15B[i]=Attributi_livelli_B.loc['Choice15','Scadenza_B'];
    Riduzione_C15A[i]=Attributi_livelli_A.loc['Choice15','RiduzioneCO2_A'];
    Riduzione_C15B[i]=Attributi_livelli_B.loc['Choice15','RiduzioneCO2_B']; 
ChoiceSet15['Rischio15_InvestimentoA15']=Rischio_C15A
ChoiceSet15['Rischio15_InvestimentoB15']=Rischio_C15B
ChoiceSet15['Rischio15_NonInvesto15']=PerColonnaNulla

ChoiceSet15['Rendimento15_InvestimentoA15']=Rendimento_C15A
ChoiceSet15['Rendimento15_InvestimentoB15']=Rendimento_C15B
ChoiceSet15['Rendimento15_NonInvesto15']=PerColonnaNulla

ChoiceSet15['Scadenza15_InvestimentoA15']=Scadenza_C15A
ChoiceSet15['Scadenza15_InvestimentoB15']=Scadenza_C15B
ChoiceSet15['Scadenza15_NonInvesto15']=PerColonnaNulla

ChoiceSet15['RiduzioneCo215_InvestimentoA15']=Riduzione_C15A
ChoiceSet15['RiduzioneCo215_InvestimentoB15']=Riduzione_C15B
ChoiceSet15['RiduzioneCo215_NonInvesto15']=PerColonnaNulla
Big_dati15=pd.concat([DataSet_sociodemo, ChoiceSet15], axis=1)
Big_dati15.insert(0, 'Indice_Persona', Big_dati15.index)
Big_dati15.rename(columns = {'Rischio15_InvestimentoA15':'Rischio1_InvestimentoA15'}, inplace = True)
Big_dati15.rename(columns = {'Rischio15_InvestimentoB15':'Rischio1_InvestimentoB15'}, inplace = True)
Big_dati15.rename(columns = {'Rischio15_NonInvesto15':'Rischio1_NonInvesto15'}, inplace = True)
Big_dati15.rename(columns = {'Rendimento15_InvestimentoA15':'Rendimento1_InvestimentoA15'}, inplace = True)
Big_dati15.rename(columns = {'Rendimento15_InvestimentoB15':'Rendimento1_InvestimentoB15'}, inplace = True)
Big_dati15.rename(columns = {'Rendimento15_NonInvesto15':'Rendimento1_NonInvesto15'}, inplace = True)
Big_dati15.rename(columns = {'Scadenza15_InvestimentoA15':'Scadenza1_InvestimentoA15'}, inplace = True)
Big_dati15.rename(columns = {'Scadenza15_InvestimentoB15':'Scadenza1_InvestimentoB15'}, inplace = True)
Big_dati15.rename(columns = {'Scadenza15_NonInvesto15':'Scadenza1_NonInvesto15'}, inplace = True)
Big_dati15.rename(columns = {'RiduzioneCo215_InvestimentoA15':'RiduzioneCo21_InvestimentoA15'}, inplace = True)
Big_dati15.rename(columns = {'RiduzioneCo215_InvestimentoB15':'RiduzioneCo21_InvestimentoB15'}, inplace = True)
Big_dati15.rename(columns = {'RiduzioneCo215_NonInvesto15':'RiduzioneCo21_NonInvesto15'}, inplace = True)
Big_dati_long15 = wide_to_long(Big_dati15,id_col='Indice_Persona', alt_list=['InvestimentoA15','InvestimentoB15','NonInvesto15'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long15)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice15'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice15'],axis=1)

#scelta 16
ChoiceSet16=pd.DataFrame(data=dati,columns=['Choice16'])
Rischio_C16A=[0]*224
Rischio_C16B=[0]*224
Rendimento_C16A=[0]*224
Rendimento_C16B=[0]*224
Scadenza_C16A=[0]*224
Scadenza_C16B=[0]*224
Riduzione_C16A=[0]*224
Riduzione_C16B=[0]*224
for i in range(len(ChoiceSet16)):
    Rischio_C16A[i]=Attributi_livelli_A.loc['Choice16','Rischio_A'];
    Rischio_C16B[i]=Attributi_livelli_B.loc['Choice16','Rischio_B'];
    Rendimento_C16A[i]=Attributi_livelli_A.loc['Choice16','Rendimento_A'];
    Rendimento_C16B[i]=Attributi_livelli_B.loc['Choice16','Rendimento_B'];
    Scadenza_C16A[i]=Attributi_livelli_A.loc['Choice16','Scadenza_A'];
    Scadenza_C16B[i]=Attributi_livelli_B.loc['Choice16','Scadenza_B'];
    Riduzione_C16A[i]=Attributi_livelli_A.loc['Choice16','RiduzioneCO2_A'];
    Riduzione_C16B[i]=Attributi_livelli_B.loc['Choice16','RiduzioneCO2_B']; 
ChoiceSet16['Rischio16_InvestimentoA16']=Rischio_C16A
ChoiceSet16['Rischio16_InvestimentoB16']=Rischio_C16B
ChoiceSet16['Rischio16_NonInvesto16']=PerColonnaNulla

ChoiceSet16['Rendimento16_InvestimentoA16']=Rendimento_C16A
ChoiceSet16['Rendimento16_InvestimentoB16']=Rendimento_C16B
ChoiceSet16['Rendimento16_NonInvesto16']=PerColonnaNulla

ChoiceSet16['Scadenza16_InvestimentoA16']=Scadenza_C16A
ChoiceSet16['Scadenza16_InvestimentoB16']=Scadenza_C16B
ChoiceSet16['Scadenza16_NonInvesto16']=PerColonnaNulla

ChoiceSet16['RiduzioneCo216_InvestimentoA16']=Riduzione_C16A
ChoiceSet16['RiduzioneCo216_InvestimentoB16']=Riduzione_C16B
ChoiceSet16['RiduzioneCo216_NonInvesto16']=PerColonnaNulla
Big_dati16=pd.concat([DataSet_sociodemo, ChoiceSet16], axis=1)
Big_dati16.insert(0, 'Indice_Persona', Big_dati16.index)
Big_dati16.rename(columns = {'Rischio16_InvestimentoA16':'Rischio1_InvestimentoA16'}, inplace = True)
Big_dati16.rename(columns = {'Rischio16_InvestimentoB16':'Rischio1_InvestimentoB16'}, inplace = True)
Big_dati16.rename(columns = {'Rischio16_NonInvesto16':'Rischio1_NonInvesto16'}, inplace = True)
Big_dati16.rename(columns = {'Rendimento16_InvestimentoA16':'Rendimento1_InvestimentoA16'}, inplace = True)
Big_dati16.rename(columns = {'Rendimento16_InvestimentoB16':'Rendimento1_InvestimentoB16'}, inplace = True)
Big_dati16.rename(columns = {'Rendimento16_NonInvesto16':'Rendimento1_NonInvesto16'}, inplace = True)
Big_dati16.rename(columns = {'Scadenza16_InvestimentoA16':'Scadenza1_InvestimentoA16'}, inplace = True)
Big_dati16.rename(columns = {'Scadenza16_InvestimentoB16':'Scadenza1_InvestimentoB16'}, inplace = True)
Big_dati16.rename(columns = {'Scadenza16_NonInvesto16':'Scadenza1_NonInvesto16'}, inplace = True)
Big_dati16.rename(columns = {'RiduzioneCo216_InvestimentoA16':'RiduzioneCo21_InvestimentoA16'}, inplace = True)
Big_dati16.rename(columns = {'RiduzioneCo216_InvestimentoB16':'RiduzioneCo21_InvestimentoB16'}, inplace = True)
Big_dati16.rename(columns = {'RiduzioneCo216_NonInvesto16':'RiduzioneCo21_NonInvesto16'}, inplace = True)
Big_dati_long16 = wide_to_long(Big_dati16,id_col='Indice_Persona', alt_list=['InvestimentoA16','InvestimentoB16','NonInvesto16'],alt_name='Choice',varying=['Rischio1','Rendimento1','Scadenza1','RiduzioneCo21'],sep='_')
Big_dati_long=Big_dati_long.append(Big_dati_long16)
Big_dati_long['Choice1']=Big_dati_long['Choice1'].fillna('')+Big_dati_long['Choice16'].fillna('')
Big_dati_long=Big_dati_long.drop(columns=['Choice16'],axis=1)

#loop che assegna indice a domanda di choiceset su 16
Id_Domande=[0]*10752
Contatore=0
for i in  range(0,10752,1):
    Id_Domande[i]=Contatore
    if i==671 or i==1343 or i==2015 or i==2687 or i==3359 or i==4031 or i==4703 or i==5375 or i==6047 or i==6719 or i==7391 or i==8063 or i==8735 or i==9407 or i==10079:
        Contatore=Contatore+1
#reset index perche va fino a 671 e poi rinizia per il processo di prima     
Big_dati_long=Big_dati_long.reset_index() 
Big_dati_long=Big_dati_long.drop(columns=['index'],axis=1)       
Big_dati_long.insert(1,'Id_Domande',Id_Domande)     
#colonna true-false per le y?? subito dopo choice  forse xlogit lo voleva cosi 
#rinomina tutte le colonne degli attributi nello stesso modo
Big_dati_long.rename(columns={'Choice':'Alternative','Rischio1':'Rischio','Rendimento1':'Rendimento%','Scadenza1':'Scadenza','RiduzioneCo21':'RiduzioneCO2%','Choice1':'Scelta'},inplace=True)



for i in range(len(Big_dati_long)):
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA1'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB1'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto1'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA2'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB2'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto2'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA3'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB3'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto3'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA4'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB4'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto4'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA5'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB5'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto5'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA6'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB6'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto6'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA7'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB7'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto7'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA8'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB8'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto8'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA9'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB9'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto9'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA10'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB10'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto10'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA11'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB11'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto11'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA12'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB12'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto12'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA13'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB13'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto13'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA14'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB14'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto14'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA15'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB15'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto15'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoA16'):Big_dati_long.loc[i,'Alternative']=('InvestimentoA');
    if Big_dati_long.loc[i,'Alternative']==('InvestimentoB16'):Big_dati_long.loc[i,'Alternative']=('InvestimentoB');
    if Big_dati_long.loc[i,'Alternative']==('NonInvesto16'):Big_dati_long.loc[i,'Alternative']=('NonInvesto');
    
#colonna true-false/0-1 per le y?? subito dopo choice? che sara la Y?  forse questo voleva xlogit per far girare la regressione. ormai e tardi
#l'ultimo annoso errore era che non gli andava bene la colonna delle alternative
################################################################################################################################   
# EXPLORATIVE DATA ANALYSIS
DataSet_sociodemo.head()
DataSet_sociodemo.tail()
DataSet_sociodemo.shape
DataSet_sociodemo.dtypes
Big_dati_long.shape
Big_dati_long.dtypes
DataSet_sociodemo.count()
Big_dati_long.count()
DataSet_sociodemo.describe(include='all')
from AUTOEDA import *
labels=["Investimento A","Investimento B","Non investo"]
Target='Scelta'
num_features,cat_features=numericalCategoricalSplit(Big_dati_long)
cat_features=cat_features.drop(columns=['Alternative','Rischio','Rendimento%','Scadenza','RiduzioneCO2%'])
proc,num_features,cat_features=EDA(Big_dati_long,labels,Target,data_summary_figsize=(6,6),corr_matrix_figsize=(6,6),corr_matrix_annot=True,pairplt=True)
#trasforma la riga di Scelta in 0,1,2 ovvero le y0=InvestimentoA, y1=InvestimentoB,y2=Non investo

from pandas_profiling import ProfileReport
design_report=ProfileReport(Big_dati_long)
design_report.to_file(output_file='report1.html')
##in fondo a pandas profiling c'e una analisi delle classi latenti
############################################################################################################################### 
import statsmodels.discrete.discrete_model 
import statsmodels.api as sm
import statsmodels
#colonne dummies per quelle non numeriche
#non converge lo stesso ma almeno ho un risultato anche se pessimo. Il problema erano le troppe variabili dummies
X_dum=pd.get_dummies(Big_dati_long1,prefix=['Rischio1', 'Rendimento1', 'Scadenza1',
       'RiduzioneCo21'],columns=['Rischio1', 'Rendimento1', 'Scadenza1',
              'RiduzioneCo21'])
feature_names=[ 'Rischio1_0', 'Rischio1_2',
'Rischio1_4', 'Rendimento1_0', 'Rendimento1_16', 'Rendimento1_25',
'Scadenza1_0', 'Scadenza1_12', 'Scadenza1_3', 'RiduzioneCo21_0',
'RiduzioneCo21_0', 'RiduzioneCo21_10']

X=X_dum[feature_names]
Xtilde = sm.add_constant(X)
y = Big_dati_long2['Choice2']
model = sm.MNLogit(y, Xtilde,missing='none')
result = model.fit(method='lbfgs')
beta=result.params
print(beta)
## test
tabellina2=result.summary2()
print(tabellina2)


X_dum2=pd.get_dummies(Big_dati_long2,prefix=['Genere', 'ETA', 'Istruzione'],columns=['Genere', 'ETA', 'Istruzione'])
feature_names=['Ottimismo', 'Indice_green', 'Indice_FK',
       'Genere_Donna', 'ETA_18-20',
       'ETA_21-29', 'ETA_30-39', 'ETA_40-49',
       'Istruzione_Diploma di scuola superiore o equivalente',
       'Istruzione_Dottorato', 'Istruzione_Laurea magistrale',
       'Istruzione_Laurea triennale']
X=X_dum[feature_names]
Xtilde = sm.add_constant(X)
y = X_dum['Scelta']
model = sm.MNLogit(y, Xtilde,missing='none')
result = model.fit(method='lbfgs')
beta=result.params
print(beta)
## test
tabellina2=result.summary2()
print(tabellina2)
###############################################################################################
from sklearn.linear_model import LogisticRegression
import numpy
logreg=LogisticRegression()
feature_names=['Rischio1', 'Rendimento1', 'Scadenza1',
       'RiduzioneCo21','Ottimismo',
       'Indice_green', 'Indice_FK']
alt=['NonInvesto3','InvestimentoA3','InvestimentoB3']
X=Big_dati_long3[feature_names]
y = Big_dati_long1['Choice1']
model= LogisticRegression(multi_class='multinomial', solver='bfgs')
#class=cross entropy loss
res=logreg.fit(X,y) 
beta=logreg.coef_
effetti=numpy.exp(beta)
#ero curioso se con solver diversi avessi lo stesso risultato e la riposta e no
model= LogisticRegression(multi_class='multinomial', solver='lbfgs')
res=logreg.fit(X,y) 
beta=logreg.coef_
effetti=numpy.exp(beta)
#invece cambiando il multiclass a one-versus-rest
model= LogisticRegression(multi_class='ovr', solver='lbfgs')
res=logreg.fit(X,y) 
beta=logreg.coef_
effetti=numpy.exp(beta)
#ultima cosa di cui sono curioso e se una sola domanda ha risultati molto diversi da tutto l'insieme
feature_names=['Rischio', 'Rendimento%', 'Scadenza',
       'RiduzioneCO2%','Ottimismo',
       'Indice_green', 'Indice_FK']
alt=['NonInvesto','InvestimentoA','InvestimentoB']
X=Big_dati_long[feature_names]
y = Big_dati_long['Scelta']
model= LogisticRegression(multi_class='ovr', solver='lbfgs')
res=logreg.fit(X,y) 
beta=logreg.coef_
effetti=numpy.exp(beta)


#purtroppo ho scoperto solo poco fa che la miglior libreria in quanto a ricchezza di elementi e biogeme. Certo quella ricchezza significa altrettanto tempo dedicato a capirne gli utensili...
## multicollinearita' con il Vif  serve per misurare la collinearità, si calcola per ogni colonna (per ogni variabile) 