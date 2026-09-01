# VIDI BIS DATA DICTIONARY

## Project

VIDI – AI Assistant for Indian Standards

## Dataset Source

Bureau of Indian Standards (BIS)

## Documents

1. IS 14543:2024 – Packaged Drinking Water
2. IS 18698:2026 – DME Blended LPG
3. IS 19690:2026 – Video and Digital Games

## Dataset Statistics

- BIS Documents: 3
- Total RAG Chunks: 86
- IS 14543:2024: 41 chunks
- IS 18698:2026: 25 chunks
- IS 19690:2026: 20 chunks

## Chunk Fields

| Field | Description |
|---|---|
| chunk_id | Unique identifier for each chunk |
| standard_number | BIS standard number |
| title | Full title of the standard |
| clause_number | BIS clause number |
| heading | Clause heading |
| page_start | Starting page of source content |
| page_end | Ending page of source content |
| source | Source organization |
| filename | Original BIS PDF filename |
| chunk_index | Position of chunk within the clause |
| chunk_count | Total chunks generated from the clause |
| text | Extracted BIS content |

## Data Pipeline

PDF
→ Page-wise text extraction
→ Metadata extraction
→ Clause structuring
→ Data QA
→ Master dataset
→ Semantic chunking
→ Chunk QA
→ JSONL RAG dataset

## Data Integrity

The dataset was validated for:

- Missing required fields
- Duplicate chunk IDs
- Empty chunks
- Invalid page ranges
- Invalid chunk indexes
- Source traceability

Final chunk QA result:

Critical Errors: 0
Warnings: 0

Therefore, the dataset is ready for the RAG/embedding pipeline.