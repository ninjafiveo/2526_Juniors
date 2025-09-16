sw_chars = ["Luke Skywalker", "Darth Vader", "Wicket", "Jabba the Hut", "Bobbafett"]

print(sw_chars)
print(sw_chars[0])
print(sw_chars[4])
print(sw_chars[-1])
print(sw_chars[-2])

sw_chars[-2] = "Obe Wan Kenobe"
print(sw_chars[-2])

# Append - Add one to the end
sw_chars.append("Princess Leah")
print(sw_chars[-1])
sw_chars.append("Baby Yoda")
print(sw_chars[-1])

# pop - remove the last item from the list
sw_chars.pop()
print(sw_chars)

# Remove - remove item from list
sw_chars.remove("Wicket")
print(sw_chars)

# Sort - Alphabetical Order / Chronological
sw_chars.sort()
print(sw_chars)

# Reverse
sw_chars.reverse()
print(sw_chars)