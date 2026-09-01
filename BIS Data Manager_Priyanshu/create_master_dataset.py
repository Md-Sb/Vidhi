import json
import os


# =========================================================
# VIDI MASTER BIS DATASET BUILDER
# =========================================================

STRUCTURED_FOLDER = r"C:\Users\USER\VIDI\output\structured"

OUTPUT_FILE = r"C:\Users\USER\VIDI\output\master_bis_dataset.json"


# =========================================================
# REQUIRED METADATA FIELDS
# =========================================================

REQUIRED_METADATA = [
    "standard_number",
    "title",
    "edition",
    "status",
    "sector",
    "product",
    "source",
    "filename"
]


# =========================================================
# LOAD STRUCTURED DOCUMENTS
# =========================================================

documents = []

print("=" * 50)
print("VIDI MASTER BIS DATASET BUILDER")
print("=" * 50)

files = sorted(
    filename
    for filename in os.listdir(STRUCTURED_FOLDER)
    if filename.endswith("_structured.json")
)

print(f"Structured documents found: {len(files)}")


# =========================================================
# PROCESS EACH DOCUMENT
# =========================================================

for filename in files:

    path = os.path.join(
        STRUCTURED_FOLDER,
        filename
    )

    print()
    print("-" * 50)
    print(f"Processing: {filename}")

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

    except Exception as error:

        print(f"❌ Could not read {filename}")
        print(error)
        continue


    metadata = data.get(
        "metadata",
        {}
    )

    clauses = data.get(
        "clauses",
        [] 
    )


    # =====================================================
    # CHECK METADATA
    # =====================================================

    missing_metadata = []

    for field in REQUIRED_METADATA:

        if not metadata.get(field):

            missing_metadata.append(field)


    if missing_metadata:

        print(
            "⚠️ Missing metadata:",
            ", ".join(missing_metadata)
        )

    else:

        print("✅ Metadata complete")


    # =====================================================
    # CHECK CLAUSES
    # =====================================================

    print(
        f"✅ Clauses loaded: {len(clauses)}"
    )


    # =====================================================
    # BUILD DOCUMENT OBJECT
    # =====================================================

    document = {

        "metadata": {

            "standard_number":
                metadata.get(
                    "standard_number",
                    ""
                ),

            "title":
                metadata.get(
                    "title",
                    ""
                ),

            "edition":
                metadata.get(
                    "edition",
                    ""
                ),

            "status":
                metadata.get(
                    "status",
                    ""
                ),

            "sector":
                metadata.get(
                    "sector",
                    ""
                ),

            "product":
                metadata.get(
                    "product",
                    ""
                ),

            "source":
                metadata.get(
                    "source",
                    "BIS"
                ),

            "filename":
                metadata.get(
                    "filename",
                    ""
                )
        },

        "clauses": clauses

    }


    documents.append(
        document
    )


# =========================================================
# MASTER DATASET
# =========================================================

master_dataset = {

    "dataset_name":
        "VIDI BIS Standards Dataset",

    "dataset_version":
        "1.0",

    "description":
        "Structured dataset of Indian Standards documents for the VIDI AI assistant.",

    "source":
        "Bureau of Indian Standards (BIS)",

    "document_count":
        len(documents),

    "documents":
        documents

}


# =========================================================
# SAVE MASTER DATASET
# =========================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        master_dataset,
        f,
        ensure_ascii=False,
        indent=2
    )


# =========================================================
# FINAL REPORT
# =========================================================

total_clauses = sum(
    len(document["clauses"])
    for document in documents
)


print()
print("=" * 50)
print("MASTER DATASET CREATED")
print("=" * 50)

print(
    f"Documents: {len(documents)}"
)

print(
    f"Total clauses: {total_clauses}"
)

print(
    f"Output: {OUTPUT_FILE}"
)

print()
print("✅ MASTER BIS DATASET READY")
print("=" * 50)
