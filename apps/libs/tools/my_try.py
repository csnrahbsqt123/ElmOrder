import random

code = [str(random.randint(0, 9)) for x in range(4)]
code = "".join(code)
print(code)
