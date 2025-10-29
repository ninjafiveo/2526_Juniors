# Import the module
import random

# Get random integer between 1 and 20 (Like rolling a D20)

roll = random.randint(1, 20)
print(f"You rolled a {roll}.")

# Pick up random item from a list.
loot_drops =["Sword of a Thousand Truths", "Shield of Doom", "Health Potion #9", "Bitcoin of Plunder", "Shoes of Swiftiness", "Banana of Nutrition", "Mana Potion of the Witches Eye", "Hat of Fake News"]
my_loot = random.choice(loot_drops)
print(f"You found {my_loot}. Success!")

players = ["Thunderous Monk", "Ninjafiveo", "Hitogoroshi", "Mad Cow", "Bob"]
random.shuffle(players)
print(f"The turn order is: {players}")