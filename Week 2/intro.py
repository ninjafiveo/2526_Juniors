# Below are my notes for coding.
# Here are more practice notes.

# Print Statement - This is used to output to the Terminal AKA Console. 
print("Mr. Sekol is the coolest teacher in the galaxy. Ask Mr. Wright.") # Now click the carrot/play button to run.

#Variables - These can change value based on user input or you can just assign a value to them. 
player_name = "Bob"
print(player_name)
# Concatenation - Combine Strings + Variables to form an output. 
print("Welcome "+ player_name +", it's great to have you here.")
player_name = "Steve" # Changed the name of the variable. See it varies. Hence the name variable. 
print("Welcome ", player_name, ", it's great to have you here.") # You can also use commas instead of "+"

# Pass through the variable into the output
print(f"Welcome, {player_name}, it's great to have you here.") #With the f in front of the string we can pass through the value of the variable.

#User Input - create a variable and ask user for input.
country_of_origin = input(f"Well {player_name}, can you tell me the country you're from? ")
print(f"{player_name} is from {country_of_origin}.")


