import json
import os
import re


# =========================================================
# VIDI BIS DATA VALIDATOR
# =========================================================

OUTPUT_FOLDER = r"C:\Users\USER\VIDI\output"


print("==========================================")
print("VIDI BIS DATA VALIDATION")
print("==========================================")


# ---------------------------------------------------------
# Find JSON files
# ---------------------------------------------------------

json_files = [
    file
    for file in os.listdir(OUTPUT_FOLDER)
    if file.lower().endswith(".json")
]


print(f"JSON files found: {len(json_files)}")


# ---------------------------------------------------------
# Validation function
# ---------------------------------------------------------

def validate_json(json_path):

    filename = os.path.basename(json_path)

    print("\n------------------------------------------")
    print(f"Checking: {filename}")
    print("------------------------------------------")


    # Load JSON
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)


    # -----------------------------------------------------
    # Check metadata
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


    metadata = data.get("metadata", {})


    missing_metadata = [
        field
        for field in required_metadata
        if not metadata.get(field)
    ]


    if missing_metadata:

        print("❌ Missing metadata:")
        print(missing_metadata)

    else:

        print("✅ Metadata complete")


    # -----------------------------------------------------
    # Check pages
    # -----------------------------------------------------

    pages = data.get("pages", [])


    if not pages:

        print("❌ No pages found")
        return


    print(f"✅ Pages found: {len(pages)}")


    # -----------------------------------------------------
    # Check page numbers
    # -----------------------------------------------------

    expected_page = 1
    page_number_errors = []


    for page in pages:

        actual_page = page.get("page_number")


        if actual_page != expected_page:

            page_number_errors.append(
                (expected_page, actual_page)
            )


        expected_page += 1


    if page_number_errors:

        print("❌ Page number errors:")
        print(page_number_errors)

    else:

        print("✅ Page numbers sequential")


    # -----------------------------------------------------
    # Check empty pages
    # -----------------------------------------------------

    empty_pages = []


    for page in pages:

        text = page.get("text", "").strip()


        if len(text) == 0:

            empty_pages.append(
                page.get("page_number")
            )


    if empty_pages:

        print("⚠️ Empty pages:")
        print(empty_pages)

    else:

        print("✅ No empty pages")


    # -----------------------------------------------------
    # Search for BIS structural elements
    # -----------------------------------------------------

    complete_text = "\n".join(
        page.get("text", "")
        for page in pages
    )


    # Clause patterns such as:
    # 1
    # 1.1
    # 2
    # 3.1
    # 4.2.1

    clause_pattern = r"(?m)^\s*\d+(?:\.\d+){0,3}\s+"


    clauses = re.findall(
        clause_pattern,
        complete_text
    )


    if clauses:

        print(
            f"✅ Possible clause numbers detected: {len(clauses)}"
        )

    else:

        print("⚠️ No obvious clause numbers detected")


    # -----------------------------------------------------
    # Search for common BIS headings
    # -----------------------------------------------------

    headings = [
        "SCOPE",
        "REFERENCES",
        "TERMS AND DEFINITIONS",
        "REQUIREMENTS",
        "SAMPLING",
        "TEST METHODS",
        "MARKING",
        "PACKING",
        "ANNEX"
    ]


    found_headings = []


    upper_text = complete_text.upper()


    for heading in headings:

        if heading in upper_text:

            found_headings.append(heading)


    if found_headings:

        print("✅ BIS headings detected:")

        for heading in found_headings:

            print(f"   - {heading}")

    else:

        print("⚠️ No common BIS headings detected")


    # -----------------------------------------------------
    # Text size
    # -----------------------------------------------------

    character_count = len(complete_text)


    print(
        f"✅ Extracted characters: {character_count:,}"
    )


# =========================================================
# RUN VALIDATION
# =========================================================

for filename in json_files:

    path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )


    try:

        validate_json(path)

    except Exception as error:

        print(
            f"❌ ERROR validating {filename}: {error}"
        )


print("\n==========================================")
print("VALIDATION COMPLETE")
print("==========================================")