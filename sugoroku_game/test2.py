import random

i = [ k for k in range(1, 10)]
print(i)

p = random.choice(i)

print(p)

i.remove(p)

print(i)
