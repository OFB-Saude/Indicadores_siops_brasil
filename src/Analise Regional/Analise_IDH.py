# Pacotes 
from database import *
import  numpy as np
import plotly.express as px
import logging
import os
import sys
import csv
import pathlib 

# Definindo a função de deflação 
def deflação(serie):
    IPCA = {'2013':5.91068325533108,'2014':6.40747079590815,'2015':10.6730281339751,'2016':6.28798821322138,'2017':2.94742132043471,'2018':3.74558117019155,'2019':4.30615161715953}
    deflation = {}
    inflação={'2019':1}
    a=[]
    for i in range(2018,2012,-1):
        a.append(IPCA[str(i)]/100)
        inflação[str(i)] = (1-sum(a))
    for ano in serie.keys():
        if ano not in ['Estado','IDH','Porte','Região']:
            lista = []  
            for series in serie[ano]:
                lista.append(series*inflação[ano])
            deflation[ano]= lista
        else:
            deflation[ano]= serie[ano]
    return(deflation)

# Exportando os dados para csv 
def list_csv(dic,to):
    data =[]
    for keys in dic.keys():
        row = [str(keys)]
        for value in dic[keys]:
            row.append(str(value))
        data.append(row)

    f = open('outputs_N_NE/'+to+'.csv','w')
    writer = csv.writer(f)
    writer.writerows(data)
    f.close()
        
# Importando os dados 
try:
   dados_apuração = (Populacao.select(Populacao.Estado,Populacao.Ano,Populacao.População,Populacao.IDH,Populacao.Porte,Receitas_apuracao_sps_estadual.campo,Receitas_apuracao_sps_estadual.Receitas_realizadas_Bimestre).distinct().join(Receitas_apuracao_sps_estadual, on=((Populacao.Estado == Receitas_apuracao_sps_estadual.estado) &(Populacao.Ano == Receitas_apuracao_sps_estadual.ano))))
   dados_adicionais = (Populacao.select(Populacao.Estado,Populacao.Ano,Populacao.População,Populacao.IDH,Populacao.Porte,Receitas_adicionais_financiamento_estadual.campo,Receitas_adicionais_financiamento_estadual.Receitas_realizadas_Bimestre).distinct().join(Receitas_adicionais_financiamento_estadual, on=((Populacao.Estado == Receitas_adicionais_financiamento_estadual.estado) &(Populacao.Ano == Receitas_adicionais_financiamento_estadual.ano))))
except Exception as e:
   print(e)

# Segregando os dados por IDH
# 1. Receita Total por IDH - Milhoes
Tabela = {'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for idh in  ['Muito Alto','Alto','Médio']:
    numerador = []
    for anos in range(2013,2020):
        for dados in list(dados_apuração.dicts()):
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['IDH'] == idh and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre']/1000000)
        Tabela[str(anos)].append(sum(numerador))
    Tabela['IDH'].append(idh)

list_csv(Tabela,"Receita Total por IDH")

# 2. Receita Total por IDH - Per Capita 
Tabela = {'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for idh in ['Muito Alto','Alto','Médio']:
    numerador = []
    denominador =[]
    for anos in range(2013,2020):
        for dados in list(dados_apuração.dicts()):
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['IDH'] == idh and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
                denominador.append(int(dados['População']))
        Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['IDH'].append(idh)

list_csv(Tabela,"Receita Total per capita por IDH")

# 3. Receita Líquida - Milhões
Tabela = {'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for idh in ['Muito Alto','Alto','Médio']:
    numerador = []
    for anos in range(2013,2020):
        for dados in list(dados_apuração.dicts()):
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['IDH'] == idh and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre']/1000000)
        Tabela[str(anos)].append(sum(numerador))
    Tabela['IDH'].append(idh)

list_csv(Tabela,"Receita Liquida por IDH")

# 4. Receita Total por IDH - Per Capita 
Tabela = {'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for idh in ['Muito Alto','Alto','Médio']:
    numerador = []
    denominador =[]
    for anos in range(2013,2020):
        for dados in list(dados_apuração.dicts()):
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['IDH'] == idh and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
                denominador.append(int(dados['População']))
        Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['IDH'].append(idh)

list_csv(Tabela,"Receita Liquida per capita por IDH")
# 5.Receita de Transferências Constitucionais e Legais da União 
Tabela = {'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for idh in  ['Muito Alto','Alto','Médio']:
    numerador = []
    for anos in range(2013,2020):
        for dados in list(dados_apuração.dicts()):
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['IDH'] == idh and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre']/1000000)
        Tabela[str(anos)].append(sum(numerador))
    Tabela['IDH'].append(idh)

list_csv(Tabela,"Receita de Transferências Constitucionais e Legais da União por IDH")
# 6. Receita Total por IDH - Per Capita 
Tabela = {'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for idh in ['Muito Alto','Alto','Médio']:
    numerador = []
    denominador =[]
    for anos in range(2013,2020):
        for dados in list(dados_apuração.dicts()):
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['IDH'] == idh and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
                denominador.append(int(dados['População']))
        Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['IDH'].append(idh)

list_csv(Tabela,"Receita de Transferências Constitucionais e Legais da União per capita por IDH")

# 7.Indicador de Capacidade 
Tabela = {'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for idh in ['Muito Alto','Alto','Médio']:
    numerador = []
    denominador =[]
    for anos in range(2013,2020):
        for dados in list(dados_apuração.dicts()):
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['IDH'] == idh and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['IDH'] == idh and dados['Ano']==anos:
                denominador.append(dados['Receitas_realizadas_Bimestre'])
    Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['IDH'].append(idh)

list_csv(Tabela,"Indicador de Capacidade por IDH")

# 8. Indicador de Depêndencia
Tabela = {'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for idh in ['Muito Alto','Alto','Médio']:
    numerador = []
    denominador =[]
    for anos in range(2013,2020):
        for dados in list(dados_apuração.dicts()):
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['IDH'] == idh and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['IDH'] == idh and dados['Ano']==anos:
                denominador.append(dados['Receitas_realizadas_Bimestre'])
    Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['IDH'].append(idh)

list_csv(Tabela,"Indicador de Dependencia por IDH")

# 9. Indicador Dependencia Sus
Tabela = {'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for idh in ['Muito Alto','Alto','Médio']:
    numerador = []
    denominador =[]
    for anos in range(2013,2020):
        for dados in list(dados_adicionais.dicts()):
            if dados['campo'] == 'Provenientes da União' and dados['IDH'] == idh and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['IDH'] == idh and dados['Ano']==anos:
                denominador.append(dados['Receitas_realizadas_Bimestre'])
    Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['IDH'].append(idh)

list_csv(Tabela,"Indicador de Dependencia Sus por IDH")

# 10. Receitas Adicionais Totais 
Tabela = {'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for idh in  ['Muito Alto','Alto','Médio']:
    numerador = []
    for anos in range(2013,2020):
        for dados in list(dados_adicionais.dicts()):
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['IDH'] == idh and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre']/1000000)
        Tabela[str(anos)].append(sum(numerador))
    Tabela['IDH'].append(idh)

list_csv(Tabela," Receitas Adicionais Totais  por IDH")
# 11. Receitas Adicionais per capita 
Tabela = {'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for idh in ['Muito Alto','Alto','Médio']:
    numerador = []
    denominador =[]
    for anos in range(2013,2020):
        for dados in list(dados_adicionais.dicts()):
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['IDH'] == idh and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
                denominador.append(int(dados['População']))
        Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['IDH'].append(idh)

list_csv(Tabela," Receitas Adicionais per capita por IDH")
