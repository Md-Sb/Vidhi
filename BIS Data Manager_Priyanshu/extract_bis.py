import pymupdf
import json
import os


# =========================================================
# VIDI BIS DATA MANAGER
# PDF TEXT EXTRACTION + METADATA
# =========================================================

# Project folders
PDF_FOLDER = r"C:\Users\USER\VIDI\bis_pdfs"
OUTPUT_FOLDER = r"C:\Users\USER\VIDI\output"
METADATA_FILE = r"C:\Users\USER\VIDI\metadata\bis_metadata.json"


# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# =========================================================
# LOAD BIS METADATA
# =========================================================

with open(METADATA_FILE, "r", encoding="utf-8") as file:
    metadata_list = json.load(file)


# Create a lookup dictionary using filename
metadata_by_filename = {
    item["filename"]: item
    for item in metadata_list
}


# =========================================================
# EXTRACT ONE PDF
# =========================================================

def extract_pdf(pdf_path):

    filename = os.path.basename(pdf_path)

    print(f"\nProcessing: {filename}")

    # -----------------------------------------------------
    # Find metadata for this PDF
    # -----------------------------------------------------

    if filename not in metadata_by_filename:

        print(f"WARNING: No metadata found for {filename}")
        print("Skipping this file.")

        return

    document_metadata = metadata_by_filename[filename]


    # -----------------------------------------------------
    # Open PDF
    # -----------------------------------------------------

    document = pymupdf.open(pdf_path)

    pages = []


    # -----------------------------------------------------
    # Extract page-by-page
    # -----------------------------------------------------

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text")

        page_data = {
            "page_number": page_number,
            "text": text
        }

        pages.append(page_data)


    # Close PDF
    document.close()


    # -----------------------------------------------------
    # Create final JSON
    # -----------------------------------------------------

    result = {
        "metadata": document_metadata,
        "pages": pages
    }


    # -----------------------------------------------------
    # Save JSON
    # -----------------------------------------------------

    json_filename = os.path.splitext(filename)[0] + ".json"

    output_path = os.path.join(
        OUTPUT_FOLDER,
        json_filename
    )


    with open(output_path, "w", encoding="utf-8") as file:

        json.dump(
            result,
            file,
            ensure_ascii=False,
            indent=2
        )


    print(f"Pages extracted: {len(pages)}")
    print(f"JSON created: {output_path}")


# =========================================================
# PROCESS ALL BIS PDFs
# =========================================================

print("==========================================")
print("VIDI BIS DATA MANAGER")
print("==========================================")


# Check PDF folder

if not os.path.exists(PDF_FOLDER):

    print("ERROR: BIS PDF folder not found.")

else:

    pdf_files = [
        file
        for file in os.listdir(PDF_FOLDER)
        if file.lower().endswith(".pdf")
    ]


    print(f"PDF files found: {len(pdf_files)}")


    # Process every PDF

    for filename in pdf_files:

        pdf_path = os.path.join(
            PDF_FOLDER,
            filename
        )

        try:

            extract_pdf(pdf_path)

        except Exception as error:

            print(
                f"ERROR processing {filename}: {error}"
            )


print("\n==========================================")
print("DATA EXTRACTION COMPLETE")
print("==========================================")