import random

size = 4
num_elementos = size ** 2
config = random.sample(range(0, num_elementos), num_elementos)

print(config)


print(random.sample(range(1, num_elementos+1), num_elementos))
