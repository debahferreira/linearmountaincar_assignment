from sarsa_linear_agent import LinearSarsaAgent
from feature_extractors import RBFFeatureExtractor
import gymnasium as gym
import pandas as pd

"""
Executar uma comparação de hiperparâmetros em 10 repetições de 50 mil steps cada, por configuração.

Registrar o número de passos até 10 sucessos para cada execução.

Produzir boxplots comparando distribuições para as 5 configurações mais relevantes.
"""

def run_experiment(env, alpha, decay, max_steps, target_successes):

    feature_extractor = RBFFeatureExtractor(env)
    agent = LinearSarsaAgent(env, feature_extractor, learning_rate=alpha, epsilon_decay= decay)
    
    total_steps = 0
    succes_count = 0

    state, _ = agent.env.reset()
    action = agent.act(state)

    while total_steps < max_steps and succes_count < target_successes:
        total_steps += 1
        next_state, reward, terminated, truncated, _ = agent.env.step(action)
        done = terminated or truncated

        if not done:
            next_action = agent.act(next_state)
        else:
            next_action = 0

        agent.updateQ(state, action, reward, next_state, next_action, done)

        if terminated == True:
            succes_count += 1

        if terminated or truncated:
            agent.decay_epsilon()
            state, _ = agent.env.reset()
            action = agent.act(state)
        else:
            state = next_state
            action = next_action
        
    return total_steps

def main():
    REPS = 10
    MAX_STEPS = 50000
    TARGET_SUCC = 10

    results = []
    learning_rates = [0.01, 0.05, 0.1, 0.2]
    epsilon_decays = [0.95, 0.99, 0.995]

    env = gym.make("MountainCar-v0")

    for rep in range(REPS):
        for alpha in learning_rates:
            for decay in epsilon_decays:
                total_steps = run_experiment(env, alpha, decay, MAX_STEPS, TARGET_SUCC)
                results.append({
                    "learning_rate": alpha,
                    "epsilon_decay": decay,
                    "total_steps": total_steps
                })

    df = pd.DataFrame(results)
    df.to_csv("resultados.csv", index=False)

    env.close()

if __name__ == "__main__":
    main()