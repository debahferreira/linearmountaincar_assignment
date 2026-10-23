from sarsa_linear_agent import LinearSarsaAgent
from feature_extractors import FeatureExtractor, RBFFeatureExtractor
import numpy as np
import gymnasium as gym

"""
Executar uma comparação de hiperparâmetros em 10 repetições de 50 mil steps cada, por configuração.

Registrar o número de passos até 10 sucessos para cada execução.

Produzir boxplots comparando distribuições para as 5 configurações mais relevantes.
"""
REPS = 10

steps_to_target = []
learning_rates = [0.005, 0.01, 0.05]
epsilon_decays = [0.95, 0.99, 0.995]

env = gym.make("MountainCar-v0")

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