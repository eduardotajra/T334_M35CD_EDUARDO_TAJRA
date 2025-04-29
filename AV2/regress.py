import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm



db = pd.read_csv('aula_24_04.csv')

# Quantidade de NaN

qt_nulos = db.isna().sum().sum()

print("valores nulos: ", qt_nulos, '\n')

# entre cpu_cores e tempo_resposta
corr1 = db['cpu_cores'].corr(db['tempo_resposta'])

print("Correlação entre cpu_cores e tempo_resposta: ", corr1, '\n')

# entre ram_gb e latencia_ms
corr2 = db['ram_gb'].corr(db['latencia_ms'])

print("Correlação entre ram_gb e latencia_ms: ", corr2, '\n')

# Mínimos Quadrados Ordinários

modelo = smf.ols(
    formula='tempo_resposta ~ cpu_cores + ram_gb + latencia_ms + armazenamento_tb',
    data=db
).fit()

# Valor estimado dos coeficientes

coef = modelo.params
coef_ordenados = [
    coef['Intercept'],
    coef['cpu_cores'],
    coef['ram_gb'],
    coef['latencia_ms'],
    coef['armazenamento_tb']
]

# Arredondar para 2 casas decimais

coef_2d = [round(c, 2) for c in coef_ordenados]

# Formatação

saida = '; '.join(f'{c:.2f}' for c in coef_2d)

print('Intercepto e variáveis explicativas: ', saida, '\n')

# P-Valores

pvals = modelo.pvalues
print('P-valores dos coeficientes:\n', pvals, '\n')

# Array com todos os coeficientes significativos

significancia = 0.05
significativas = pvals[pvals < significancia].index.tolist()

print(f'Coeficientes significativos (p < {significancia}):')

for nome in significativas:
    print(f'  - {nome}  (p = {pvals[nome]:.3e})')

# R² (coeficiente de determinação)

r2 = modelo.rsquared

print('\nR²: ',r2,'\n')

# R² ajustado

r2_adj = modelo.rsquared_adj

print('R² ajustado: ',r2_adj,'\n')

# Sumário

x = db[['cpu_cores','ram_gb','latencia_ms','armazenamento_tb']]
x = sm.add_constant(x)
y = db['tempo_resposta']

modelo = sm.OLS(y, x, missing='drop').fit()
coef_fmt = '; '.join(f'{modelo.params[v]:.2f}' for v in ['const',
                                                         'cpu_cores',
                                                         'ram_gb',
                                                         'latencia_ms',
                                                         'armazenamento_tb'])
print('Intercepto e variáveis explicativas:', coef_fmt)

print(modelo.summary())

