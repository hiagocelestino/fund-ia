import numpy as np
import matplotlib.pyplot as plt


POP_SIZE = 100
NUM_VARS = 10
BOUNDS = [-5, 5]
CROSSOVER_PROB = 0.8
MUTATION_PROB = 0.1
SIGMA = 0.5
NUM_GENERATIONS = 200

def obj_fun(x):
    return np.sum(x**2)

def initialize_population():
    return np.random.uniform(BOUNDS[0], BOUNDS[1], (POP_SIZE, NUM_VARS))

def tournament_selection(population, fitness, tournament_size=3):
    indices = np.random.choice(len(population), tournament_size)
    return population[indices[np.argmin(fitness[indices])]]

def crossover(parent1, parent2, crossover_prob):
    if np.random.rand() < crossover_prob:
        point = np.random.randint(1, NUM_VARS)
        return (
            np.concatenate((parent1[:point], parent2[point:])),
            np.concatenate((parent2[:point], parent1[point:]))
        )
    return parent1.copy(), parent2.copy()

def mutate(individual, mutation_prob, sigma):
    for i in range(len(individual)):
        if np.random.rand() < mutation_prob:
            individual[i] += np.random.normal(0, sigma)
            individual[i] = np.clip(individual[i], BOUNDS[0], BOUNDS[1])
    return individual

def genetic_algorithm(num_generations, crossover_prob, mutation_prob, sigma):
    population = initialize_population()
    best_fitness = float('inf')
    best_individual = None
    
    for _ in range(num_generations):
        fitness = np.array([obj_fun(ind) for ind in population])
        min_idx = np.argmin(fitness)
        if fitness[min_idx] < best_fitness:
            best_fitness = fitness[min_idx]
            best_individual = population[min_idx].copy()
        
        new_population = [best_individual]  # elitismo
        
        while len(new_population) < POP_SIZE:
            p1 = tournament_selection(population, fitness)
            p2 = tournament_selection(population, fitness)
            c1, c2 = crossover(p1, p2, crossover_prob)
            new_population.append(mutate(c1, mutation_prob, sigma))
            if len(new_population) < POP_SIZE:
                new_population.append(mutate(c2, mutation_prob, sigma))
        
        population = np.array(new_population[:POP_SIZE])
    
    return best_fitness

def test_parameter(param_name, values, base_params):
    results = []
    for val in values:
        params = base_params.copy()
        params[param_name] = val
        fitness = genetic_algorithm(
            num_generations=params['NUM_GENERATIONS'],
            crossover_prob=params['CROSSOVER_PROB'],
            mutation_prob=params['MUTATION_PROB'],
            sigma=params['SIGMA']
        )
        results.append(fitness)
        print(f"{param_name}={val}: fitness={fitness:.4f}")
    return results

# Parâmetros base fixos
base_params = {
    'NUM_GENERATIONS': 200,
    'CROSSOVER_PROB': 0.8,
    'MUTATION_PROB': 0.1,
    'SIGMA': 0.5
}

def plot_single_param(title, param_name, values):
    results = test_parameter(param_name, values, base_params)
    plt.figure(figsize=(8, 5))
    plt.plot(values, results, marker='o', linestyle='-')
    plt.title(f"Efeito de {param_name} na melhor aptidão")
    plt.xlabel(param_name)
    plt.ylabel("Melhor aptidão")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Gerar gráficos separados
plot_single_param("Número de Gerações", "NUM_GENERATIONS", [50, 100, 200, 400])
plot_single_param("Probabilidade de Crossover", "CROSSOVER_PROB", [0.2, 0.5, 0.8, 1.0])
plot_single_param("Probabilidade de Mutação", "MUTATION_PROB", [0.01, 0.05, 0.1, 0.2])
plot_single_param("Sigma da Mutação", "SIGMA", [0.1, 0.3, 0.5, 1.0])
