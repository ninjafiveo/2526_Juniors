import math
# You're a coach and you want to figure how many Overwatch teams you can assemble?
# Minimum Number of Players per team is 5.

coach_name = input("Hi Coach what is your name? ")
team_name = input("What is your team name? ")

#Constant
min_num_players = int(5)

num_of_players = int(input("How many players do you have? "))

def calc_num_of_teams():
    min_number_of_teams = num_of_players / min_num_players
    print(type(min_number_of_teams))
    print(f"The Minimum # of Teams you Can have are: {min_number_of_teams}")

calc_num_of_teams()










