import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
import matplotlib.pyplot as plt

# ================================================
# Parte I – Estatísticas Descritivas
# ================================================
df = pd.read_csv('dataset_7.csv')

# Seleção de colunas numéricas
num_cols = df.select_dtypes(include='number').columns

# Cálculo das estatísticas
estat = pd.DataFrame(index=num_cols)
estat['média']       = df[num_cols].mean()
estat['mediana']     = df[num_cols].median()
estat['mínimo']      = df[num_cols].min()
estat['máximo']      = df[num_cols].max()
estat['25%']         = df[num_cols].quantile(0.25)
estat['75%']         = df[num_cols].quantile(0.75)
estat['desvio_std']  = df[num_cols].std()
estat['variância']   = df[num_cols].var()
estat['coef_var']    = estat['desvio_std'] / estat['média']

print("=== Parte I: Estatísticas Descritivas ===")
print(estat)


# ================================================
# Parte II – Regressão Linear Múltipla e Diagnósticos
# ================================================
# 1. Tratamento de variáveis categóricas
df2 = df.dropna().copy()
df2['tipo_processador'] = df2['tipo_processador'].str.replace(' ', '_')

df_model = pd.get_dummies(
    df2,
    columns=['sistema_operacional', 'tipo_hd', 'tipo_processador'],
    drop_first=True
)

# 2. Ajuste do modelo completo (Modelo 1)
y_var = 'tempo_resposta'
X_vars = '+'.join([col for col in df_model.columns if col != y_var])
modelo1 = smf.ols(f'{y_var} ~ {X_vars}', data=df_model).fit()

print("\n=== Parte II: Modelo 1 (todas as variáveis) ===")
print(modelo1.summary())


# 3. Diagnósticos do Modelo 1
# Multicolinearidade (VIF)
vif_df = pd.DataFrame({
    'Variável': modelo1.model.exog_names,
    'VIF': [variance_inflation_factor(modelo1.model.exog, i)
            for i in range(modelo1.model.exog.shape[1])]
})
print("\n=== VIF das Variáveis (Modelo 1) ===")
print(vif_df)

# Heterocedasticidade (Breusch-Pagan)
lm_stat, lm_p, f_stat, f_p = het_breuschpagan(modelo1.resid, modelo1.model.exog)
print(f"\nBreusch-Pagan LM p-value (Modelo 1) = {lm_p:.4f}")

plt.figure()
plt.scatter(modelo1.fittedvalues, modelo1.resid)
plt.axhline(0, linestyle='--')
plt.xlabel('Valores Ajustados')
plt.ylabel('Resíduos')
plt.title('Resíduos vs Ajustados (Modelo 1)')
plt.show()


# ================================================
# Parte III – Comparação de Modelos
# ================================================
# Modelo 2: excluindo 'armazenamento_tb' (variável não significativa)
exclude_var = 'armazenamento_tb'
X_vars2 = '+'.join([col for col in df_model.columns if col not in [y_var, exclude_var]])
modelo2 = smf.ols(f'{y_var} ~ {X_vars2}', data=df_model).fit()

print("\n=== Parte III: Modelo 2 (sem armazenamento_tb) ===")
print(modelo2.summary())

# Comparação de métricas
print(f"\nAdj. R² Modelo 1: {modelo1.rsquared_adj:.4f}")
print(f"Adj. R² Modelo 2: {modelo2.rsquared_adj:.4f}")
print(f"F-statistic Modelo 1: {modelo1.fvalue:.2f}, p-value = {modelo1.f_pvalue:.2e}")
print(f"F-statistic Modelo 2: {modelo2.fvalue:.2f}, p-value = {modelo2.f_pvalue:.2e}")

# Teste F para comparação de modelos aninhados
f_test = modelo1.compare_f_test(modelo2)
print(f"\nTeste F (Modelo 1 vs Modelo 2): F = {f_test[0]:.2f}, p-value = {f_test[1]:.4f}, df diff = {int(f_test[2])}")

# Fim do script
