var_1 = input("Please enter your first number: ") #Takes data in as a string
var_2 = input("Please enter your second number: ") #Takes data in as a string
# Adding these two numbers together won't work because they are strings. We must cast them to correct datatype, a float.
var_1 = float(var_1)
var_2 = float(var_2)

# Addition
sum = var_1 + var_2
print(f"{var_1} + {var_2} = {sum}")

# Subtraction
difference = var_1-var_2
print(f"{var_1} - {var_2} = {difference}")

# Multiplication
product = var_1*var_2
print(f"{var_1} * {var_2} = {product}")

# Division
quotient = var_1/var_2
print(f"{var_1} / {var_2} = {quotient}")

# Power
the_power = var_1 ** var_2
print(f"{var_1} ** {var_2} = {the_power}")