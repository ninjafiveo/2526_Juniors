# Conditional Logic
# Operators ==, !=, >, <, <=, >=

num_1 = 10
num_2 = 20

def condition_check():
    if num_1 == 10: #True
        print(f"num_1 = {num_1}")

    if num_1 == 20:# False
        print(f"num_1 = {num_1}")
    elif num_1 < 20: # True
        print(f"num_1 is less than 20.")
    elif num_1 < num_2: #True # This condition won't print because the above elif is true. Program exits after that.
        print(f"num_1 is less than num_2.")
    else:
        print("I don't know what happen. Level 5 Error.")

# condition_check()

