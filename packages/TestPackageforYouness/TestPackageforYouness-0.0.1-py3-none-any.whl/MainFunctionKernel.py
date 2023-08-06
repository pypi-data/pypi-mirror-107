# Function Package kernel

#Functions
def Printer():
    return "I'm here"

def factorial(n):
    if n==0: return 1
    else: return n*factorial(n-1)

print(Printer())
print(factorial(6))




