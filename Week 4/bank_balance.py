#TODO: Create a variable “customer_name” that takes the input from the customer as to what their name is.
customer_name = input("Hello human, please enter your name: ")
# Create a variable “starting_balance” and assign it the value of $5000.25
starting_balance = 5000.25
# Create a print function that welcomes the customer and tells them their starting balance. 
print(f"Welcome {customer_name}, to the Sekol Bank and Trust. Your balance is {starting_balance}.")
# Create a variable, “pay_check”, that takes the input of the customer and asks how much of their paycheck they would like to deposit. This needs to be a float
pay_check = float(input(f"Hi {customer_name}. How much of your check would you like to deposit? "))
# *** Remember that “input” makes the user input a string, you will need to cast the datatype from a string to a float.
# Create a variable “expenditure_item” and assign it to what the customer spent money on. This will need to be an input from the customer. 
expenditure_item = input("What did you buy? ")
# Create a variable, “expenditure”, and assign it the value from the user in the amount that they spent on it.
expenditure = float(input("Enter the amount that you spent: "))
# print(f"{customer_name}, {pay_check}, {expenditure_item}, {expenditure}") # Testing
# Create a function called “checking_balance” with the parameters of: user_name, balance, deposits, expense_item and expense_amount.
def checking_balance(user_name, balance, deposits, expense_item, expense_amount):
# In the function create a variable “ending_balance” that takes the values passed in through the parameters. (customer_name = user_name, starting_balance=balance, pay_check = deposits, expenditure_items = expense_item and expenditure = expense_amount). The ending_balance will be equal to the balance + deposits - expense_amount.
    ending_balance = balance + deposits - expense_amount 
# In the function, print a message to the customer of their updated ending_balance after they spent money on their expenditure. 
    print(f"Hi {user_name}. After you deposited {deposits} and spent {expense_amount} on {expense_item}, your new ending balance is {ending_balance}")

# Call the checking_balance and test your code. Your output should look like the following:
checking_balance(customer_name, starting_balance, pay_check, expenditure_item, expenditure)
