import json
import os
import re


# =========================================================
# VIDI MASTER BIS DATASET VALIDATOR
# =========================================================

MASTER_FILE = r"C:\Users\Sampriti\Desktop\VIDHI\BIS Data Manager_Priyanshu\output\master_bis_dataset.json"

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


print("=" * 55)
print("VIDI MASTER BIS DATASET VALIDATION")
print("=" * 55)


# =========================================================
# LOAD DATASET
# =========================================================

with open(
    MASTER_FILE,
    "r",
    encoding="utf-8"
) as f:

    dataset = json.load(f)


documents = dataset.get(
    "documents",
    []
)


critical_errors = 0
warnings = 0


# =========================================================
# BASIC DATASET CHECK
# =========================================================

if not documents:

    print("❌ No documents found")
    critical_errors += 1

else:

    print(
        f"✅ Documents found: {len(documents)}"
    )


# =========================================================
# CHECK EACH DOCUMENT
# =========================================================

all_standard_numbers = set()


for document in documents:

    metadata = document.get(
        "metadata",
        {}
    )

    clauses = document.get(
        "clauses",
        []
    )

    standard_number = metadata.get(
        "standard_number",
        "UNKNOWN"
    )


    print()
    print("=" * 55)
    print(
        f"CHECKING: {standard_number}"
    )
    print("=" * 55)


    # -----------------------------------------------------
    # Metadata
    # -----------------------------------------------------

    missing = []

    for field in REQUIRED_METADATA:

        if not metadata.get(field):

            missing.append(field)


    if missing:

        print(
            "⚠️ Missing metadata:",
            ", ".join(missing)
        )

        warnings += 1

    else:

        print("✅ Metadata complete")


    # -----------------------------------------------------
    # Duplicate standard number
    # -----------------------------------------------------

    if standard_number in all_standard_numbers:

        print(
            "❌ Duplicate standard number"
        )

        critical_errors += 1

    else:

        all_standard_numbers.add(
            standard_number
        )


    # -----------------------------------------------------
    # Clause count
    # -----------------------------------------------------

    print(
        f"Clauses: {len(clauses)}"
    )

    if not clauses:

        print(
            "❌ No clauses found"
        )

        critical_errors += 1


    # -----------------------------------------------------
    # Clause validation
    # -----------------------------------------------------

    clause_numbers = set()

    invalid_clauses = []

    duplicate_clauses = []

    invalid_pages = []

    empty_content = []


    for clause in clauses:

        number = clause.get(
            "clause_number",
            ""
        )

        page_start = clause.get(
            "page_start"
        )

        page_end = clause.get(
            "page_end"
        )

        heading = clause.get(
            "heading",
            ""
        ).strip()

        text = clause.get(
            "text",
            ""
        ).strip()


        # ---------------------------------------------
        # Clause number
        # ---------------------------------------------

        if not re.fullmatch(
            r"\d+(?:\.\d+){0,3}",
            number
        ):

            invalid_clauses.append(
                number
            )


        # ---------------------------------------------
        # Duplicate clause number
        # ---------------------------------------------

        if number in clause_numbers:

            duplicate_clauses.append(
                number
            )

        else:

            clause_numbers.add(
                number
            )


        # ---------------------------------------------
        # Page validation
        # ---------------------------------------------

        if (
            not isinstance(page_start, int)
            or not isinstance(page_end, int)
            or page_start > page_end
        ):

            invalid_pages.append(
                number
            )


        # ---------------------------------------------
        # Content validation
        # ---------------------------------------------

        if not heading and not text:

            empty_content.append(
                number
            )


    # =====================================================
    # RESULTS
    # =====================================================

    if invalid_clauses:

        print(
            "⚠️ Invalid clause numbers:",
            invalid_clauses
        )

        warnings += 1

    else:

        print(
            "✅ Clause numbering valid"
        )


    if duplicate_clauses:

        print(
            "❌ Duplicate clauses:",
            duplicate_clauses
        )

        critical_errors += 1

    else:

        print(
            "✅ No duplicate clauses"
        )


    if invalid_pages:

        print(
            "❌ Invalid page ranges:",
            invalid_pages
        )

        critical_errors += 1

    else:

        print(
            "✅ Page ranges valid"
        )


    if empty_content:

        print(
            "⚠️ Clauses with no heading/text:",
            empty_content
        )

        warnings += 1

    else:

        print(
            "✅ All clauses contain content"
        )


# =========================================================
# FINAL REPORT
# =========================================================

print()
print("=" * 55)
print("FINAL MASTER DATASET QA REPORT")
print("=" * 55)

print(
    f"Documents validated : {len(documents)}"
)

print(
    f"Critical errors     : {critical_errors}"
)

print(
    f"Warnings            : {warnings}"
)


if critical_errors == 0:

    print()
    print(
        "✅ MASTER DATASET PASSED CRITICAL QA"
    )

else:

    print()
    print(
        "❌ MASTER DATASET REQUIRES CORRECTION"
    )


print("=" * 55)
