# ANÁLISE SOBRE PROCESSOS DE COMPRAS DIRETAS DE PINHEIRAL

# Importando módulos
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# importar a tabela de compras a ser analisada
df_compras = pd.read_csv("compras_pinheiral.csv", sep=";")

# Remover a coluna centro de custos da tabela pois não traz nenhuma informação em nenhuma linha
df_compras = df_compras.drop(['Centro de custos'],axis=1)
df_compras

# Realizando conversão de datas do tipo objeto pata datetime
df_compras['Data da compra'] = pd.to_datetime(df_compras['Data da compra'], dayfirst=True)

# Criando uma coluna com os meses da compra na tabela
df_compras['Mês da compra'] = df_compras['Data da compra'].dt.month_name()

# Analisando os 10 fornecedores mais frequentes
fornecedores_mais_frequentes = df_compras['Fornecedor'].value_counts().reset_index().head(10)

# Convertendo os valores que estavam como objeto para numero
df_compras['Valor R$'] = df_compras['Valor R$'].str.replace(r'R\$|\.', '', regex=True) # retira os R$
df_compras['Valor R$'] = df_compras['Valor R$'].str.replace(r'\s+', '', regex=True) # retira espaços
df_compras['Valor R$'] = df_compras['Valor R$'].str.replace(',', '.', regex=True) # substitui as virgulas por pontos
df_compras['Valor R$'] = pd.to_numeric(df_compras['Valor R$']) # converte para numero

# Compra de Maior Valor

valor_maximo = df_compras['Valor R$'].max()
print(f'O valor maximo de uma compra foi de R${valor_maximo}.')

# Compra de Menor Valor

valor_minimo = df_compras['Valor R$'].min()
print(f'O valor minimo de uma compra foi de R${valor_minimo}.')

#Valor médio das compras

media = round(df_compras['Valor R$'].mean(), 2) #media arredondada com 2 casas decimais
print(f'O valor médio de uma compra foi de R${media}.')

#Media por fornecedor
media_por_fornecedor= df_compras.groupby("Fornecedor")['Valor R$'].mean().sort_values(ascending=False).reset_index()

# Top 10 fornecedores por media
top10 = media_por_fornecedor.head(10)

top10

# criando um filtro que filtra somente acima de 50000
filtro_media = media_por_fornecedor['Valor R$'] > 50000

# usando o filtro
media_filtrada_50mil = media_por_fornecedor[filtro_media]

media_filtrada_50mil

objeto_mais_comum = df_compras['Objeto'].value_counts().sort_values(ascending=False).reset_index()
objeto_mais_comum


# Valor por objeto
valor_objeto = df_compras.groupby('Objeto')['Valor R$'].sum().sort_values(ascending=False).reset_index()
valor_objeto 

#Verificando compras por mês
mes_compras = df_compras.groupby('Mês da compra')['Valor R$'].sum().sort_values(ascending=False)


#Plotando gráfico

mes_compras.plot(kind='bar', figsize=(12, 6))

plt.title('Compras por mês')

plt.xlabel("Meses")
plt.ylabel('Valor R$')

# Calculando total gasto
total_gasto = df_compras['Valor R$'].sum()

total_gasto

#Calculando top5 por fornecedor
total_top5 = media_por_fornecedor['Valor R$'].head(5).sum()

total_top5
mes_compras


#usando o top 5 fornecedor para calcular qual o percentual dos 5 dentro do valor total
percentual_top5 = (total_top5/total_gasto) * 100
percentual_top5


print(f'Os 5 maiores fornecedores da cidade correspondem a {percentual_top5:.0f}% dos gastos em compras diretas.')


#plotando novo gráfico com fornecedores acima de 50mil recebidos
media_filtrada_50mil = media_filtrada_50mil.sort_values(by="Valor R$",ascending=True)


media_filtrada_50mil.plot(kind='barh', figsize=(12, 6), x='Fornecedor', y='Valor R$', color='Red')
plt.title("Média dos 9 maiores fornecedores")
plt.xlabel('Valores')
plt.ylabel('Fornecedores')
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
