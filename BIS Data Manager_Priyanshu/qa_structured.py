import json
import os
import re


# =========================================================
# VIDI STRUCTURED BIS DATA - QUALITY CHECK
# =========================================================

STRUCTURED_FOLDER = r"C:\Users\USER\VIDI\output\structured"


def clause_to_tuple(clause_number):
    """Convert 4.2.1 into (4, 2, 1)."""
    return tuple(int(x) for x in clause_number.split("."))


def check_document(file_path):

    filename = os.path.basename(file_path)

    print("\n==========================================")
    print(f"QA CHECK: {filename}")
    print("==========================================")

    # -----------------------------------------------------
    # Load JSON
    # -----------------------------------------------------

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    metadata = data.get("metadata", {})
    clauses = data.get("clauses", [])

    errors = []
    warnings = []

    # -----------------------------------------------------
    # Metadata check
    # -----------------------------------------------------

    required_metadata = [
        "standard_number",
        "title",
        "edition",
        "status",
        "sector",
        "product",
        "source",
        "filename"
    ]

    for field in required_metadata:
        if not metadata.get(field):
            errors.append(f"Missing metadata: {field}")

    if not errors:
        print("✅ Metadata complete")

    # -----------------------------------------------------
    # Clause existence
    # -----------------------------------------------------

    if not clauses:
        errors.append("No clauses found")
    else:
        print(f"✅ Clauses found: {len(clauses)}")

    # -----------------------------------------------------
    # Duplicate clause numbers
    # -----------------------------------------------------

    clause_numbers = [
        clause.get("clause_number")
        for clause in clauses
    ]

    duplicates = {
        number
        for number in clause_numbers
        if clause_numbers.count(number) > 1
    }

    if duplicates:
        warnings.append(
            f"Duplicate clause numbers: {sorted(duplicates)}"
        )
    else:
        print("✅ No duplicate clause numbers")

    # -----------------------------------------------------
    # Empty headings / text
    # -----------------------------------------------------

    empty_heading = []
    empty_text = []

    for clause in clauses:

        number = clause.get("clause_number", "UNKNOWN")

        if not clause.get("heading", "").strip():
            empty_heading.append(number)

        if not clause.get("text", "").strip():
            empty_text.append(number)

    if empty_heading:
        warnings.append(
            f"Clauses with empty headings: {empty_heading}"
        )
    else:
        print("✅ Clause headings present")

    if empty_text:
        warnings.append(
            f"Clauses with empty text: {empty_text}"
        )
    else:
        print("✅ Clause text present")

    # -----------------------------------------------------
    # Page range validation
    # -----------------------------------------------------

    bad_pages = []

    for clause in clauses:

        number = clause.get("clause_number")

        start = clause.get("page_start")
        end = clause.get("page_end")

        if not isinstance(start, int) or not isinstance(end, int):
            bad_pages.append(number)

        elif start > end:
            bad_pages.append(number)

        elif start < 1:
            bad_pages.append(number)

    if bad_pages:
        errors.append(
            f"Invalid page ranges: {bad_pages}"
        )
    else:
        print("✅ Page ranges valid")

    # -----------------------------------------------------
    # Clause numbering format
    # -----------------------------------------------------

    invalid_numbers = []

    clause_pattern = re.compile(
        r"^\d+(?:\.\d+){0,3}$"
    )

    for number in clause_numbers:

        if not number or not clause_pattern.match(number):
            invalid_numbers.append(number)

    if invalid_numbers:
        warnings.append(
            f"Unusual clause numbers: {invalid_numbers}"
        )
    else:
        print("✅ Clause numbering format valid")

    # -----------------------------------------------------
    # Hierarchy check
    # -----------------------------------------------------

    hierarchy_problems = []

    for i in range(1, len(clauses)):

        previous = clause_numbers[i - 1]
        current = clause_numbers[i]

        if not previous or not current:
            continue

        prev_tuple = clause_to_tuple(previous)
        curr_tuple = clause_to_tuple(current)

        # A subclause should not jump to an impossible depth.
        if len(curr_tuple) > len(prev_tuple) + 1:
            hierarchy_problems.append(
                f"{previous} → {current}"
            )

    if hierarchy_problems:
        warnings.append(
            "Possible hierarchy jumps: "
            + str(hierarchy_problems[:10])
        )
    else:
        print("✅ Clause hierarchy looks reasonable")

    # -----------------------------------------------------
    # Print first 10 clauses for manual inspection
    # -----------------------------------------------------

    print("\nFIRST 10 STRUCTURED CLAUSES")
    print("------------------------------------------")

    for clause in clauses[:10]:

        print(
            f"{clause.get('clause_number')} | "
            f"Pages {clause.get('page_start')}-"
            f"{clause.get('page_end')} | "
            f"{clause.get('heading')}"
        )

    # -----------------------------------------------------
    # Results
    # -----------------------------------------------------

    if errors:

        print("\n❌ ERRORS")

        for error in errors:
            print("   -", error)

    else:

        print("\n✅ No critical errors found")

    if warnings:

        print("\n⚠️ WARNINGS")

        for warning in warnings:
            print("   -", warning)

    else:

        print("✅ No warnings")

    return errors, warnings


# =========================================================
# PROCESS ALL STRUCTURED FILES
# =========================================================

print("==========================================")
print("VIDI BIS STRUCTURED DATA QA")
print("==========================================")

files = [
    file
    for file in os.listdir(STRUCTURED_FOLDER)
    if file.endswith("_structured.json")
]

print(f"Structured documents found: {len(files)}")


total_errors = 0
total_warnings = 0


for filename in files:

    path = os.path.join(
        STRUCTURED_FOLDER,
        filename
    )

    try:

        errors, warnings = check_document(path)

        total_errors += len(errors)
        total_warnings += len(warnings)

    except Exception as error:

        print(
            f"❌ ERROR reading {filename}: {error}"
        )

        total_errors += 1


# =========================================================
# FINAL REPORT
# =========================================================

print("\n==========================================")
print("FINAL QA REPORT")
print("==========================================")

print(f"Critical errors : {total_errors}")
print(f"Warnings        : {total_warnings}")

if total_errors == 0:

    print("\n✅ STRUCTURED DATA PASSED CRITICAL QA")

else:

    print("\n❌ STRUCTURED DATA NEEDS CORRECTION")

print("==========================================")