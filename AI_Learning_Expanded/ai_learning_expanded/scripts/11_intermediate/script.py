print("=== Intermediate: File Handling ===")
import os
fname = "test_output.txt"
with open(fname, "w") as f:
    f.write("Hello from intermediate script 11\n")
print(f"Wrote {fname}")
print("Script complete.")
