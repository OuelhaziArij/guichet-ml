
# Guichet ML - Atelier 1

API FastAPI de detection de langue (mode mock hors ligne, mode real via Hugging Face).

## Installation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env

## Lancer
uvicorn app.main:app --reload
Puis ouvrir http://127.0.0.1:8000/docs

## Tester
pytest -q
