import numpy as np

# Parâmetros do algoritmo
POP_SIZE = 100  # Tamanho da população
NUM_GENERATIONS = 200  # Número de gerações
CROSSOVER_PROB = 0.8  # Probabilidade de cruzamento
MUTATION_PROB = 0.1  # Probabilidade de mutação
SIGMA = 0.5  # Desvio padrão da mutação gaussiana
BOUNDS = [-5, 5]  # Limites das variáveis
NUM_VARS = 10  # Número de variáveis (x1, ..., x10)

# Função objetivo
def obj_fun(x):
    return np.sum(x**2)

# Inicialização da população
def initialize_population():
    return np.random.uniform(BOUNDS[0], BOUNDS[1], (POP_SIZE, NUM_VARS))

# Seleção por torneio
def tournament_selection(population, fitness, tournament_size=3):
    indices = np.random.choice(len(population), tournament_size)
    tournament_fitness = fitness[indices]
    return population[indices[np.argmin(tournament_fitness)]]

# Cruzamento de ponto único
def crossover(parent1, parent2):
    if np.random.rand() < CROSSOVER_PROB:
        point = np.random.randint(1, NUM_VARS)
        child1 = np.concatenate((parent1[:point], parent2[point:]))
        child2 = np.concatenate((parent2[:point], parent1[point:]))
        return child1, child2
    return parent1.copy(), parent2.copy()

# Mutação gaussiana
def mutate(individual):
    for i in range(len(individual)):
        if np.random.rand() < MUTATION_PROB:
            individual[i] += np.random.normal(0, SIGMA)
            individual[i] = np.clip(individual[i], BOUNDS[0], BOUNDS[1])
    return individual

# Algoritmo genético
def genetic_algorithm():
    # Inicialização
    population = initialize_population()
    best_individual = None
    best_fitness = float('inf')
    
    for generation in range(NUM_GENERATIONS):
        # Avaliação
        fitness = np.array([obj_fun(ind) for ind in population])
        
        # Atualizar melhor solução
        min_fitness_idx = np.argmin(fitness)
        if fitness[min_fitness_idx] < best_fitness:
            best_fitness = fitness[min_fitness_idx]
            best_individual = population[min_fitness_idx].copy()
        
        # Nova população
        new_population = []
        new_population.append(best_individual)  # Elitismo
        
        # Gerar novos indivíduos
        while len(new_population) < POP_SIZE:
            # Seleção
            parent1 = tournament_selection(population, fitness)
            parent2 = tournament_selection(population, fitness)
            
            # Cruzamento
            child1, child2 = crossover(parent1, parent2)
            
            # Mutação
            child1 = mutate(child1)
            child2 = mutate(child2)
            
            new_population.extend([child1, child2])
        
        # Atualizar população
        population = np.array(new_population[:POP_SIZE])
        
        # Imprimir progresso
        if generation % 50 == 0:
            print(f"Geração {generation}: Melhor aptidão = {best_fitness}")
    
    return best_individual, best_fitness

# Executar o algoritmo
best_solution, best_fitness = genetic_algorithm()
print("\nMelhor solução encontrada:", best_solution)
print("Valor da função objetivo:", best_fitness)
