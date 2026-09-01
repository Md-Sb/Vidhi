import json
import os
import re


# =========================================================
# VIDI BIS SEMANTIC CHUNK BUILDER
# =========================================================

MASTER_FILE = r"C:\Users\USER\VIDI\output\master_bis_dataset.json"

OUTPUT_FOLDER = r"C:\Users\USER\VIDI\output\chunks"

OUTPUT_FILE = os.path.join(
    OUTPUT_FOLDER,
    "bis_chunks.json"
)


# Maximum approximate characters for a chunk.
# Normal BIS clauses smaller than this remain intact.
MAX_CHARS = 3000


# =========================================================
# CREATE OUTPUT DIRECTORY
# =========================================================

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# =========================================================
# LOAD MASTER DATASET
# =========================================================

print("=" * 55)
print("VIDI BIS SEMANTIC CHUNK BUILDER")
print("=" * 55)

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


print(
    f"Documents loaded: {len(documents)}"
)


# =========================================================
# HELPER: NORMALIZE WHITESPACE
# =========================================================

def clean_text(text):

    if not text:
        return ""

    # Preserve paragraph/line separation where possible
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:

        line = re.sub(
            r"[ \t]+",
            " ",
            line
        ).strip()

        if line:

            cleaned_lines.append(
                line
            )

    return "\n".join(
        cleaned_lines
    ).strip()


# =========================================================
# HELPER: SPLIT LARGE TEXT
# =========================================================

def split_large_text(text, max_chars=MAX_CHARS):

    text = text.strip()

    if len(text) <= max_chars:

        return [text]


    # -----------------------------------------------------
    # First try paragraph boundaries
    # -----------------------------------------------------

    paragraphs = re.split(
        r"\n\s*\n",
        text
    )


    chunks = []

    current = ""


    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue


        # -------------------------------------------------
        # If adding the paragraph stays within the limit
        # -------------------------------------------------

        if (
            not current
            or len(current) + len(paragraph) + 1
            <= max_chars
        ):

            if current:

                current += "\n\n"

            current += paragraph

            continue


        # -------------------------------------------------
        # Save current chunk
        # -------------------------------------------------

        if current:

            chunks.append(
                current.strip()
            )


        # -------------------------------------------------
        # Very large paragraph
        # -------------------------------------------------

        if len(paragraph) > max_chars:

            sentences = re.split(
                r"(?<=[.!?])\s+",
                paragraph
            )

            current = ""

            for sentence in sentences:

                sentence = sentence.strip()

                if not sentence:
                    continue


                if (
                    not current
                    or len(current) + len(sentence) + 1
                    <= max_chars
                ):

                    if current:

                        current += " "

                    current += sentence

                else:

                    chunks.append(
                        current.strip()
                    )

                    current = sentence


        else:

            current = paragraph


    if current:

        chunks.append(
            current.strip()
        )


    return chunks


# =========================================================
# BUILD CHUNKS
# =========================================================

all_chunks = []

total_documents = 0
total_clauses = 0


for document in documents:

    total_documents += 1

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
        ""
    )

    title = metadata.get(
        "title",
        ""
    )

    source = metadata.get(
        "source",
        "BIS"
    )

    filename = metadata.get(
        "filename",
        ""
    )


    print()
    print("-" * 55)
    print(
        f"Standard: {standard_number}"
    )
    print(
        f"Clauses: {len(clauses)}"
    )


    total_clauses += len(clauses)


    # =====================================================
    # PROCESS CLAUSES
    # =====================================================

    for clause in clauses:

        clause_number = clause.get(
            "clause_number",
            ""
        )

        heading = clean_text(
            clause.get(
                "heading",
                ""
            )
        )

        text = clean_text(
            clause.get(
                "text",
                ""
            )
        )

        page_start = clause.get(
            "page_start"
        )

        page_end = clause.get(
            "page_end"
        )


        # -------------------------------------------------
        # Combine heading + text for retrieval
        # -------------------------------------------------

        if heading and text:

            full_text = (
                f"{heading}\n\n{text}"
            )

        elif heading:

            full_text = heading

        else:

            full_text = text


        full_text = full_text.strip()


        # -------------------------------------------------
        # Skip completely empty clauses
        # -------------------------------------------------

        if not full_text:

            print(
                f"⚠️ Skipping empty clause: "
                f"{clause_number}"
            )

            continue


        # -------------------------------------------------
        # Split only if necessary
        # -------------------------------------------------

        text_parts = split_large_text(
            full_text
        )


        # =================================================
        # CREATE CHUNKS
        # =================================================

        for index, chunk_text in enumerate(
            text_parts,
            start=1
        ):


            # -------------------------------------------------
            # Stable chunk ID
            # -------------------------------------------------

            safe_standard = re.sub(
                r"[^A-Za-z0-9]+",
                "_",
                standard_number
            ).strip("_")


            safe_clause = re.sub(
                r"[^A-Za-z0-9]+",
                "_",
                clause_number
            ).strip("_")


            chunk_id = (
                f"{safe_standard}"
                f"_CLAUSE_{safe_clause}"
                f"_CHUNK_{index}"
            )


            # -------------------------------------------------
            # Chunk object
            # -------------------------------------------------

            chunk = {

                "chunk_id":
                    chunk_id,

                "standard_number":
                    standard_number,

                "title":
                    title,

                "clause_number":
                    clause_number,

                "heading":
                    heading,

                "page_start":
                    page_start,

                "page_end":
                    page_end,

                "source":
                    source,

                "filename":
                    filename,

                "chunk_index":
                    index,

                "chunk_count":
                    len(text_parts),

                "text":
                    chunk_text
            }


            all_chunks.append(
                chunk
            )


# =========================================================
# BUILD FINAL CHUNK DATASET
# =========================================================

chunk_dataset = {

    "dataset_name":
        "VIDI BIS RAG Chunk Dataset",

    "dataset_version":
        "1.0",

    "source":
        "Bureau of Indian Standards (BIS)",

    "document_count":
        total_documents,

    "clause_count":
        total_clauses,

    "chunk_count":
        len(all_chunks),

    "chunks":
        all_chunks
}


# =========================================================
# SAVE
# =========================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chunk_dataset,
        f,
        ensure_ascii=False,
        indent=2
    )


# =========================================================
# FINAL REPORT
# =========================================================

print()
print("=" * 55)
print("CHUNKING COMPLETE")
print("=" * 55)

print(
    f"Documents processed : {total_documents}"
)

print(
    f"Clauses processed   : {total_clauses}"
)

print(
    f"Chunks created      : {len(all_chunks)}"
)

print(
    f"Output file         : {OUTPUT_FILE}"
)

print()
print(
    "✅ BIS RAG CHUNK DATASET CREATED"
)

print("=" * 55)