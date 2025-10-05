# CNE ML Offline

This repository contains an offline, on-premise proof of concept for parsing, validating, and approving Portuguese electoral candidate lists delivered as PDF, Word, or Excel files.

## Project layout
- **api/** – FastAPI backend handling job ingestion, preview retrieval, CSV download, approval, and model lifecycle endpoints.
- **worker/** – Asynchronous pipeline that performs render → OCR (stub) → segment → extract → normalize → validate → CSV generation and updates job metadata.
- **web/** – React single-page application enabling upload, preview, CSV download, and approval operations.
- **ml/** – Simulated retraining orchestration and model registry utilities for the continuous learning loop.
- **data/** – Runtime artefacts such as uploads, processed CSVs, and approved datasets (ignored by Git).
- **docs/** – Requirements, test plan, and OpenAPI specification guiding implementation.
- **scripts/** – Helper utilities for development and automation.

## Getting started
1. Create a Python virtual environment and install backend dependencies (requirements file to be added when dependencies are finalised):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
