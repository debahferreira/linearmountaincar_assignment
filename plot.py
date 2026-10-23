import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# boxplot para entender como fica variando mais hiperparâmetros

df = pd.read_csv("resultados.csv")

plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df, 
    x="learning_rate", 
    y="total_steps", 
    hue="epsilon_decay"
)

plt.title("Comparação de Desempenho por Hiperparâmetros")
plt.xlabel("Taxa de Aprendizagem (Learning Rate)")
plt.ylabel("Total de Passos até 10 Sucessos")

plt.savefig("todas_configuracoes.png")

# boxplot filtrando apenas os que escolhi

condicao_grupo_1 = (df["learning_rate"].isin([0.01, 0.05, 0.1, 0.2])) & (df["epsilon_decay"] == 0.995)
condicao_grupo_2 = (df["learning_rate"] == 0.2) & (df["epsilon_decay"] == 0.95)

df_filtrado = df[condicao_grupo_1 | condicao_grupo_2].copy()

df_filtrado["config"] = (
    "LR: " + df_filtrado["learning_rate"].astype(str) + 
    " | Decay: " + df_filtrado["epsilon_decay"].astype(str)
)

plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df_filtrado, 
    x= "config", 
    y="total_steps"
)

plt.title("Comparação das 5 Configurações Selecionadas")
plt.xlabel("Configuração (Learning Rate e Epsilon Decay)")
plt.ylabel("Total de Passos até 10 Sucessos")
plt.xticks(rotation=45)
plt.tight_layout()  # Ajusta as margens para não cortar os textos inclinados

plt.savefig("boxplot.png")