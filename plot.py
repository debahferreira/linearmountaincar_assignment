import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
plt.show()

