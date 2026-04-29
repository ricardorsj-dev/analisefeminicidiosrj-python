import pandas as pd 
import numpy as np

#Carregar a base de dados

df = pd.read_csv('BaseFeminicidioEvolucaoMensalCisp.csv', sep=';', encoding='latin1')

#Padronizar nomes de colunas 

df.columns = df.columns.str.strip()

#Converter tipos de dados 

df['Ano'] = df['Ano'].astype(int)
df['Mês'] = df['Mês'].astype(int)

#Renomear colunas para facilitar uso, pois o acento pode dar erro

df = df.rename(columns={'Município': 'Municipio',
                        'Feminicídio': 'Feminicidio',
                        'Tentativa de feminicídio': 'Tentativa'})

#Criar coluna total 

df['Total'] = df['Feminicidio'] + df['Tentativa']

#ANALISE DAS REGIOES 

risp_analise = df.groupby('RISP')[['Feminicidio', 'Tentativa']].sum()

risp_analise['Total'] = risp_analise.sum(axis=1)

risp_maior = risp_analise.sort_values(by='Total', ascending=False)

print(risp_maior)

#MES COM MAIOR OCORRENCIA 

mes_analise = df.groupby('Mês')[['Feminicidio', 'Tentativa']].sum()

mes_analise['Total'] = mes_analise.sum(axis=1)

mes_critico = mes_analise.sort_values(by='Total', ascending=False)

print(mes_critico)

#MUNICIPIO COM MAIOR ÍNDICE DOS CRIMES

municipio_analise = df.groupby('Municipio')[['Feminicidio', 'Tentativa']].sum()

municipio_analise['Total'] = municipio_analise.sum(axis=1)

municipio_ranking = municipio_analise.sort_values(by='Total', ascending=False)

print(municipio_ranking.head(10))

#EVOLUÇAO DOS CRIMES ENTRE 2016-2026

ano_analise = df.groupby('Ano')[['Feminicidio', 'Tentativa']].sum()

ano_analise['Total'] = ano_analise[['Feminicidio', 'Tentativa']].sum(axis=1)

ano_analise = ano_analise.sort_index()

#CRESCIMENTO PERCENTUAL NO PERIODO 2016-2026

crescimento = ((ano_analise.loc[2026] - ano_analise.loc[2016]) / ano_analise.loc[2016]) * 100

print('Crescimento percentual de 2016 a 2026:')
print(crescimento.round(1))

#EVOLUÇÃO AO LONGOS DOS ANOS 

import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))

plt.plot(ano_analise.index, ano_analise['Feminicidio'], marker='o', label='Feminicídio')
plt.plot(ano_analise.index, ano_analise['Tentativa'], marker='o', label='Tentativa')
plt.plot(ano_analise.index, ano_analise['Total'], marker='o', label='Total')

plt.title('Evolução dos casos (2016-2026)')
plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.grid()

plt.legend(title='Tipo')

plt.show()

#EVOLUCAO PELAS AISP

aisp_analise = df.groupby(['Ano', 'AISP'])[['Feminicidio', 'Tentativa']].sum().reset_index()

aisp_analise['Total'] = aisp_analise[['Feminicidio', 'Tentativa']].sum(axis=1)

pivot_aisp = aisp_analise.pivot(index='Ano', columns='AISP', values='Total')

top_aisp = aisp_analise.groupby('AISP')['Total'].sum().sort_values(ascending=False).head(5).index

pivot_top = pivot_aisp[top_aisp]

pivot_top.plot(figsize=(10,6), marker='o')

plt.title('Evolução das Top 5 AISP')
plt.xlabel('Ano')
plt.ylabel('Casos')
plt.grid()

plt.show()

#OCORRENCIAS NAS REGIOES 

risp_analise.plot(kind='bar', figsize=(10,6))

plt.title('Casos por RISP')
plt.xlabel('RISP')
plt.ylabel('Quantidade')
plt.xticks(rotation=0)
plt.grid(axis='y')

plt.legend(title='Tipo')

plt.show()

#MESES MAIS CRITICOS 

mes_analise = mes_analise.sort_index()

mes_analise.plot(marker='o', figsize=(10,6))

plt.title('Casos por Mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade')
plt.grid()

plt.legend(title='Tipo')

plt.show()

#Top10 Municipios mais violentos 

top10 = municipio_analise.sort_values(by='Total', ascending=False).head(10)

top10.plot(kind='barh', figsize=(10,6))

plt.title('Top 10 Municípios com mais casos')
plt.xlabel('Quantidade')
plt.ylabel('Município')
plt.gca().invert_yaxis()
plt.grid(axis='x')

plt.legend(title='Tipo')

plt.show()








