# Number of credits to graduate = 120. Write the statement below to check.
#Constant
credits_to_graduate = 120

def check_credits():
    numb_credits = int(input("How many credits do you have? "))

    if numb_credits >= credits_to_graduate:
        print(f"Congrats you have enough.") 
    else:
        numb_short = credits_to_graduate - numb_credits
        print(f"I'm sorry you still need {numb_short} to graduate.")
    
    
    def option_to_run_again():
        run_again = input("Do you want to run again? y/n: ")
        if run_again == "y":
            check_credits()
        elif run_again == "n":
            print("Thanks for using the SekolBot300. Have a great day.")
        else:
            print("You did not enter 'y' or 'n'. Please try again.")
            option_to_run_again()

    option_to_run_again()


####
##
#
#


check_credits()


