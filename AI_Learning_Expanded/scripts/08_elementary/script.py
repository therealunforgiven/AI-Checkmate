print("Script 08: Error handling")
try:
    result = 10 / 2
    print(f"Result: {result}")
except ZeroDivisionError:
    print("Cannot divide by zero")
print("Try/except example complete.")
