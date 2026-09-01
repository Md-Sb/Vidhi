import json
import os


# =========================================================
# VIDI BIS CHUNK DATASET QA
# =========================================================

CHUNK_FILE = r"C:\Users\Sampriti\Desktop\VIDHI\BIS Data Manager_Priyanshu\output\chunks\bis_chunks.json"


print("=" * 55)
print("VIDI BIS CHUNK DATASET QA")
print("=" * 55)


# =========================================================
# LOAD DATA
# =========================================================

with open(
    CHUNK_FILE,
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)


chunks = data.get("chunks", [])


print(
    f"Chunks found: {len(chunks)}"
)


# =========================================================
# COUNTERS
# =========================================================

critical_errors = 0
warnings = 0


# =========================================================
# REQUIRED FIELDS
# =========================================================

required_fields = [
    "chunk_id",
    "standard_number",
    "title",
    "clause_number",
    "page_start",
    "page_end",
    "source",
    "filename",
    "chunk_index",
    "chunk_count",
    "text"
]


# =========================================================
# TRACK DUPLICATES
# =========================================================

chunk_ids = set()

duplicate_ids = []

empty_chunks = []

missing_fields = []

invalid_pages = []

invalid_chunk_indexes = []


# =========================================================
# CHECK EACH CHUNK
# =========================================================

for chunk in chunks:

    chunk_id = chunk.get(
        "chunk_id",
        ""
    )


    # -----------------------------------------------------
    # Required fields
    # -----------------------------------------------------

    missing = []

    for field in required_fields:

        if field not in chunk:

            missing.append(field)


    if missing:

        missing_fields.append(
            (
                chunk_id,
                missing
            )
        )


    # -----------------------------------------------------
    # Duplicate chunk ID
    # -----------------------------------------------------

    if chunk_id in chunk_ids:

        duplicate_ids.append(
            chunk_id
        )

    else:

        chunk_ids.add(
            chunk_id
        )


    # -----------------------------------------------------
    # Empty text
    # -----------------------------------------------------

    text = chunk.get(
        "text",
        ""
    )


    if not isinstance(text, str) or not text.strip():

        empty_chunks.append(
            chunk_id
        )


    # -----------------------------------------------------
    # Page validation
    # -----------------------------------------------------

    page_start = chunk.get(
        "page_start"
    )

    page_end = chunk.get(
        "page_end"
    )


    if (
        not isinstance(page_start, int)
        or not isinstance(page_end, int)
        or page_start <= 0
        or page_end < page_start
    ):

        invalid_pages.append(
            chunk_id
        )


    # -----------------------------------------------------
    # Chunk index validation
    # -----------------------------------------------------

    chunk_index = chunk.get(
        "chunk_index"
    )

    chunk_count = chunk.get(
        "chunk_count"
    )


    if (
        not isinstance(chunk_index, int)
        or not isinstance(chunk_count, int)
        or chunk_index < 1
        or chunk_count < 1
        or chunk_index > chunk_count
    ):

        invalid_chunk_indexes.append(
            chunk_id
        )


# =========================================================
# RESULTS
# =========================================================

print()
print("------------------------------------------")


if missing_fields:

    print(
        f"❌ Chunks with missing fields: "
        f"{len(missing_fields)}"
    )

    for item in missing_fields[:10]:

        print(
            "   ",
            item
        )

    critical_errors += len(
        missing_fields
    )

else:

    print(
        "✅ Required fields present"
    )


# ---------------------------------------------------------

if duplicate_ids:

    print(
        f"❌ Duplicate chunk IDs: "
        f"{len(duplicate_ids)}"
    )

    for chunk_id in duplicate_ids[:10]:

        print(
            "   ",
            chunk_id
        )

    critical_errors += len(
        duplicate_ids
    )

else:

    print(
        "✅ No duplicate chunk IDs"
    )


# ---------------------------------------------------------

if empty_chunks:

    print(
        f"❌ Empty chunks: "
        f"{len(empty_chunks)}"
    )

    for chunk_id in empty_chunks[:10]:

        print(
            "   ",
            chunk_id
        )

    critical_errors += len(
        empty_chunks
    )

else:

    print(
        "✅ No empty chunks"
    )


# ---------------------------------------------------------

if invalid_pages:

    print(
        f"❌ Invalid page ranges: "
        f"{len(invalid_pages)}"
    )

    critical_errors += len(
        invalid_pages
    )

else:

    print(
        "✅ Page ranges valid"
    )


# ---------------------------------------------------------

if invalid_chunk_indexes:

    print(
        f"❌ Invalid chunk indexes: "
        f"{len(invalid_chunk_indexes)}"
    )

    critical_errors += len(
        invalid_chunk_indexes
    )

else:

    print(
        "✅ Chunk indexes valid"
    )


# =========================================================
# STANDARD DISTRIBUTION
# =========================================================

print()
print("------------------------------------------")
print("CHUNKS BY STANDARD")
print("------------------------------------------")


standard_counts = {}


for chunk in chunks:

    standard = chunk.get(
        "standard_number",
        "UNKNOWN"
    )

    standard_counts[standard] = (
        standard_counts.get(
            standard,
            0
        ) + 1
    )


for standard, count in standard_counts.items():

    print(
        f"{standard} : {count} chunks"
    )


# =========================================================
# CLAUSE TRACEABILITY
# =========================================================

print()
print("------------------------------------------")
print("TRACEABILITY CHECK")
print("------------------------------------------")


traceability_errors = []


for chunk in chunks:

    required_trace = [
        "standard_number",
        "clause_number",
        "page_start",
        "page_end",
        "filename"
    ]


    for field in required_trace:

        value = chunk.get(field)

        if value is None or value == "":

            traceability_errors.append(
                (
                    chunk.get(
                        "chunk_id",
                        "UNKNOWN"
                    ),
                    field
                )
            )


if traceability_errors:

    print(
        f"❌ Traceability errors: "
        f"{len(traceability_errors)}"
    )

    for error in traceability_errors[:10]:

        print(
            "   ",
            error
        )

    critical_errors += len(
        traceability_errors
    )

else:

    print(
        "✅ Every chunk has source traceability"
    )


# =========================================================
# SAMPLE CHUNKS
# =========================================================

print()
print("------------------------------------------")
print("SAMPLE CHUNKS")
print("------------------------------------------")


for chunk in chunks[:5]:

    print()
    print(
        "Chunk ID:",
        chunk["chunk_id"]
    )

    print(
        "Standard:",
        chunk["standard_number"]
    )

    print(
        "Clause:",
        chunk["clause_number"]
    )

    print(
        "Pages:",
        f"{chunk['page_start']}-{chunk['page_end']}"
    )

    print(
        "Text:",
        chunk["text"][:150].replace(
            "\n",
            " "
        ),
        "..."
    )


# =========================================================
# FINAL REPORT
# =========================================================

print()
print("=" * 55)
print("FINAL CHUNK QA REPORT")
print("=" * 55)

print(
    f"Total chunks       : {len(chunks)}"
)

print(
    f"Critical errors    : {critical_errors}"
)

print(
    f"Warnings           : {warnings}"
)


if critical_errors == 0:

    print()
    print(
        "✅ CHUNK DATASET PASSED CRITICAL QA"
    )

    print(
        "✅ READY FOR RAG / EMBEDDING PIPELINE"
    )

else:

    print()
    print(
        "❌ CHUNK DATASET REQUIRES CORRECTION"
    )


print("=" * 55)
