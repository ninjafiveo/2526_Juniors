# Greeting

def greet_print(name):
    print(f"Hi, {name}")

greet_print("Bob")


player_1 = greet_print("Ninja")
player_2 = greet_print("Samurai")

print(f"Hello. {player_1}. Please select your super power: 1, 2, 3, 4")
print(f"Hello. {player_2}. Please select your super power: 1, 2, 3, 4")

def greet_return(name):
    return f"Hi, {name}"

msg_1 = greet_return("George")
msg_2 = greet_return("Fred")
print(msg_1)
print(msg_1)
print(msg_1)
print(msg_1)
print(msg_2)
