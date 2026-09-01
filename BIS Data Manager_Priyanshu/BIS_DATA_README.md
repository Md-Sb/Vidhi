# VIDI BIS DATA MANAGER PACKAGE

## Purpose

This package contains processed BIS standards prepared for integration
with the VIDI Retrieval-Augmented Generation (RAG) system.

## Source Documents

The dataset currently contains three BIS standards:

- IS 14543:2024
- IS 18698:2026
- IS 19690:2026

## Files

### master_bis_dataset.json

Complete structured dataset containing all BIS documents and clauses.

### bis_chunks.json

Authoritative semantic chunk dataset with complete metadata and
source traceability.

### bis_chunks.jsonl

JSON Lines version prepared for embedding/vector database pipelines.

## Dataset Size

Total chunks: 86

Distribution:

IS 14543:2024 → 41
IS 18698:2026 → 25
IS 19690:2026 → 20

## Traceability

Every chunk contains:

- Standard number
- Clause number
- Page range
- Original filename
- Source
- Exact extracted text

This allows the VIDI system to retrieve information while maintaining
traceability to the original BIS document.

## QA Status

Master dataset:

Critical errors: 0

Chunk dataset:

Critical errors: 0
Warnings: 0

## Handoff

The `bis_chunks.jsonl` file can be supplied to the embedding/RAG
development team.

Expected downstream pipeline:

JSONL
→ Embedding Model
→ Vector Database
→ Retriever
→ LLM
→ VIDI Assistant