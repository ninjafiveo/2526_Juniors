print("Functions Below")
# How to define a function
# Start with def
# Indentation and Spacing matters
x = 10
def sample_function():
    print(f"{x} You ran the function.")
#call the function below
sample_function() # This code will output "{x} You ran the function." to the console/terminal

# Pass Values into the function to do math. 
def do_addition(x, y):
    sum = x + y
    print(sum)

do_addition(3,10) # Whatever numbers you place in here, it will add them together, because of the do_addition() function

# Take input from the user and pass that value through the function.
num_1 = float(input("Please enter a number:"))
num_2 = float(input("Please enter another number:"))

do_addition(num_1, num_2)

your_name = input("Welcome traveler, what is your name? ")
your_age = int(input(f"Hi {your_name}. What is your age? "))

def npc_response():
    if your_age < 50:
        print("Hi there young traveler. I have a quest for you.")
    elif your_age >= 50:
        print("Whoa, you're a tad too old. Go sit on the rocking chair and Cracker Barrel and take a load off, grandpa.")
    else:
        print("Something went wrong. Cannot compute. Level 5 error. Rebooting.")

npc_response()

