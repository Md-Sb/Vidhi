import json
import os

INPUT_FILE = r"C:\Users\USER\VIDI\output\chunks\bis_chunks.json"
OUTPUT_FILE = r"C:\Users\USER\VIDI\output\chunks\bis_chunks.jsonl"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

chunks = data["chunks"]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for chunk in chunks:
        f.write(
            json.dumps(
                chunk,
                ensure_ascii=False
            ) + "\n"
        )

print("=" * 50)
print("VIDI BIS JSONL GENERATION")
print("=" * 50)
print(f"Chunks converted : {len(chunks)}")
print(f"Output file      : {OUTPUT_FILE}")
print()
print("✅ JSONL FILE CREATED")
print("=" * 50)