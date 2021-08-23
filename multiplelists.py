def create1(n): 
    output = []
    for i in range(n):
        output.append(range(1,i+2)) # append a list, not a number.
    return output

print(create1(6))