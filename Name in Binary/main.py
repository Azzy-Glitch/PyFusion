name = input("Enter your name: ")

binary_result = " ".join(format(ord(char), '08b') for char in name)

print("Binary:", binary_result)
