print("=== Intermediate: List Comprehensions ===")
squares = [x*x for x in range(1, 11)]
print("Squares 1-10:", squares)
evens = [x for x in range(20) if x % 2 == 0]
print("Evens under 20:", evens)
print("Script complete.")
