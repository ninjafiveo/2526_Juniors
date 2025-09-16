# Create a program that takes in the number of pennies from the user and outputs the fewest denominations as possible.
# Example: 27 pennies = 1 quarter and 2 pennies.
# Example: 56 pennies = 2 quarter, 1 nickel and 1 penny.
# Example: 10022 pennies = 1 one hundred dollar bill, 2 dimes and 2 pennies.

def run_pennies():
    print("Welcome to my Pennies from Heaven Application.")
    print("This program converts a total number of pennies into the fewest number of dollar bills and coins.")
    total_pennies = int(input("Enter the number of pennies you have: ")) # Converts string to int.
    # Alternative option for converting a string to an int - see lines 11 & 12.
    # total_pennies = input("Enter the number of pennies you have: ") # Converts string to int.
    # total_pennies = int(total_pennies)
    def pennies_to_change(total_pennies):
        # Dollar Bills Calculation
        dollars = total_pennies // 100 # Use Floor Division (round down) to tell me max number of $1 bills in the change.
        total_pennies = total_pennies % 100 # Assigns remainder or total_pennies to total_pennies.
        # print(dollars) # Prints number of dollar bills
        # print(total_pennies) # Prints remainding pennies.

        # Quarter Calculations
        quarters = total_pennies // 25
        total_pennies = total_pennies % 25
        # print(quarters)
        # print(total_pennies)

        # Dime Calculations
        dimes = total_pennies // 10
        total_pennies = total_pennies % 10
        
        # Nickels Calculations
        nickels = total_pennies // 5
        total_pennies = total_pennies % 5

        remainder_pennies = total_pennies

        print(f"Dollars = {dollars}")
        print(f"Quarters = {quarters}")
        print(f"Dimes = {dimes}")
        print(f"Nickels = {nickels}")
        print(f"Pennies = {remainder_pennies}")

    pennies_to_change(total_pennies)



# Call the function to run it.
run_pennies()
