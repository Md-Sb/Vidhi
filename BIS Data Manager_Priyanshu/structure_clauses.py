import json
import os
import re


# =========================================================
# VIDI BIS CLAUSE STRUCTURER
# VERSION 4
# =========================================================

INPUT_FOLDER = r"C:\Users\USER\VIDI\output"
STRUCTURED_FOLDER = r"C:\Users\USER\VIDI\output\structured"

os.makedirs(STRUCTURED_FOLDER, exist_ok=True)


# =========================================================
# CLAUSE NUMBER PATTERN
# =========================================================

CLAUSE_PATTERN = re.compile(
    r"^\s*(\d+(?:\.\d+){0,3})\s+(.*)$"
)


# =========================================================
# VALID CLAUSE NUMBER
# =========================================================

def is_valid_clause_number(number):

    parts = number.split(".")

    try:
        values = [int(x) for x in parts]
    except ValueError:
        return False

    # BIS clauses cannot start with zero
    if values[0] <= 0:
        return False

    # No clause component can be zero
    if any(x <= 0 for x in values):
        return False

    # A clause number should normally contain at most
    # four levels:
    #
    # 5
    # 5.1
    # 5.1.1
    # 5.1.1.1
    #
    if len(values) > 4:
        return False

    return True

# =========================================================
# FALSE POSITIVE CHECK
# =========================================================

def is_probable_false_positive(number, text):

    text = text.strip()

    # Page/table numbers and numeric fragments
    if not text:
        return True

    if re.fullmatch(
        r"[\d\s.,/%°±\-]+",
        text
    ):
        return True

    # Common footer/header artifacts
    bad_phrases = [
        "free standard provided",
        "bsb edge",
        "copyright",
        "all rights reserved",
        "page",
    ]

    lower = text.lower()

    for phrase in bad_phrases:
        if phrase in lower:
            return True

    return False


# =========================================================
# DETECT CLAUSE
# =========================================================

def detect_clause(line):

    line = line.strip()

    if not line:
        return None

    match = CLAUSE_PATTERN.match(line)

    if not match:
        return None

    number = match.group(1)
    content = match.group(2).strip()

    # -----------------------------------------------------
    # Basic validation
    # -----------------------------------------------------

    if not is_valid_clause_number(number):
        return None

    # -----------------------------------------------------
    # IMPORTANT:
    #
    # A single large integer such as:
    #
    # 250 ml
    # 501
    # 2016
    # 1050
    #
    # is very unlikely to be a BIS clause.
    #
    # Real clauses usually have:
    #
    # 1
    # 2
    # 5
    # 5.1
    # 5.1.1
    #
    # Main clause numbers are therefore restricted to
    # a reasonable range.
    # -----------------------------------------------------

    parts = number.split(".")

    # Single-number clause
    if len(parts) == 1:

        main_number = int(parts[0])

        # Reject suspicious large numbers
        if main_number > 20:
            return None


    # -----------------------------------------------------
    # Reject obvious measurements / table values
    # -----------------------------------------------------

    if re.match(
        r"^\d+(?:\.\d+)?\s*"
        r"(ml|l|mg/l|mg|kg|g|°C|mm|cm|m|%)\b",
        content,
        re.IGNORECASE
    ):
        return None


    # -----------------------------------------------------
    # Reject very short numeric fragments
    # -----------------------------------------------------

    if re.fullmatch(
        r"[\d\s.,/%°±\-]+",
        content
    ):
        return None


    # -----------------------------------------------------
    # Reject known PDF footer/header artifacts
    # -----------------------------------------------------

    lower_content = content.lower()

    bad_phrases = [

        "free standard provided",

        "bsb edge",

        "copyright",

        "all rights reserved",

        "pri yanshu",

        "kolkata",

        "email",

        "page"

    ]

    for phrase in bad_phrases:

        if phrase in lower_content:
            return None


    # -----------------------------------------------------
    # Return valid clause
    # -----------------------------------------------------

    return {

        "clause_number": number,

        "content": content

    }
# =========================================================
# STRUCTURE ONE DOCUMENT
# =========================================================

def structure_document(input_path):

    filename = os.path.basename(input_path)

    print()
    print("=" * 42)
    print(f"Processing: {filename}")
    print("=" * 42)

    # -----------------------------------------------------
    # Load original page JSON
    # -----------------------------------------------------

    with open(
        input_path,
        "r",
        encoding="utf-8"
    ) as f:

        document = json.load(f)

    metadata = document.get(
        "metadata",
        {}
    )

    pages = document.get(
        "pages",
        []
    )

    clauses = []

    current_clause = None

    # =====================================================
    # PROCESS PAGE BY PAGE
    # =====================================================

    for page in pages:

        page_number = page.get(
            "page_number"
        )

        page_text = page.get(
            "text",
            ""
        )

        lines = page_text.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            detected = detect_clause(line)

            # =================================================
            # NEW CLAUSE
            # =================================================

            if detected:

                # ---------------------------------------------
                # Finish previous clause
                # ---------------------------------------------

                if current_clause:

                    current_clause["page_end"] = (
                        page_number
                    )

                    clauses.append(
                        current_clause
                    )

                # ---------------------------------------------
                # Determine whether inline content is a
                # heading or actual clause text.
                # ---------------------------------------------

                content = detected["content"]

                heading = ""
                text = ""

                # A short all-uppercase line is very likely
                # a main BIS heading.
                if (
                    len(content) <= 80
                    and content.upper() == content
                    and re.search(
                        r"[A-Z]",
                        content
                    )
                ):

                    heading = content

                else:

                    # Otherwise preserve it as clause text.
                    text = content

                # ---------------------------------------------
                # Start new clause
                # ---------------------------------------------

                current_clause = {

                    "clause_number":
                        detected[
                            "clause_number"
                        ],

                    "heading":
                        heading,

                    "page_start":
                        page_number,

                    "page_end":
                        page_number,

                    "text":
                        text

                }

            # =================================================
            # NORMAL TEXT
            # =================================================

            elif current_clause:

                if current_clause["text"]:

                    current_clause["text"] += "\n"

                current_clause["text"] += line


    # =====================================================
    # SAVE FINAL CLAUSE
    # =====================================================

    if current_clause:

        clauses.append(
            current_clause
        )


    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    unique = []

    seen = set()

    for clause in clauses:

        number = clause[
            "clause_number"
        ]

        if number in seen:

            continue

        seen.add(number)

        unique.append(
            clause
        )


    clauses = unique


    # =====================================================
    # SORT CLAUSES NUMERICALLY
    # =====================================================

    def sort_key(clause):

        return tuple(
            int(x)
            for x in clause[
                "clause_number"
            ].split(".")
        )

    clauses.sort(
        key=sort_key
    )


    # =====================================================
    # CLEAN TEXT
    # =====================================================

    for clause in clauses:

        clause["heading"] = (
            clause.get(
                "heading",
                ""
            )
            .strip()
        )

        clause["text"] = (
            clause.get(
                "text",
                ""
            )
            .strip()
        )


    # =====================================================
    # BUILD OUTPUT
    # =====================================================

    structured_document = {

        "metadata":
            metadata,

        "document_type":
            "BIS Indian Standard",

        "clauses":
            clauses

    }


    # =====================================================
    # SAVE
    # =====================================================

    output_filename = (
        os.path.splitext(filename)[0]
        + "_structured.json"
    )

    output_path = os.path.join(
        STRUCTURED_FOLDER,
        output_filename
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            structured_document,
            f,
            ensure_ascii=False,
            indent=2
        )


    print(
        f"Clauses detected: {len(clauses)}"
    )

    print(
        f"Structured JSON: {output_path}"
    )


# =========================================================
# MAIN
# =========================================================

print("=" * 42)
print("VIDI BIS CLAUSE STRUCTURER V4")
print("=" * 42)


json_files = [

    filename

    for filename in os.listdir(
        INPUT_FOLDER
    )

    if filename.lower().endswith(
        ".json"
    )

    and not filename.endswith(
        "_structured.json"
    )

]


print(
    f"Documents found: {len(json_files)}"
)


for filename in json_files:

    input_path = os.path.join(
        INPUT_FOLDER,
        filename
    )

    try:

        structure_document(
            input_path
        )

    except Exception as error:

        print(
            f"ERROR: {filename}"
        )

        print(error)


print()
print("=" * 42)
print("CLAUSE STRUCTURING COMPLETE")
print("=" * 42)