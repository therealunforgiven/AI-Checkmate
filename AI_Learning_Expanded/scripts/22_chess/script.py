print("=== Chess: Piece Values ===")
values = {"pawn": 1, "knight": 3, "bishop": 3, "rook": 5, "queen": 9, "king": "infinite"}
for piece, val in values.items():
    print(f"{piece.title()}: {val}")
print("Material advantage often decides games.")
print("Script complete.")
