# DineDesk — CodSoft Task

Restaurant menu, cart checkout, order queue and reservation management.

## Tech
Python · Flask · SQLite · HTML · CSS · JavaScript

## Run locally
1. Install Python 3.10+.
2. Open this folder in terminal.
3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\\Scripts\\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
4. Install dependencies and start:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
5. Visit http://127.0.0.1:5002

The SQLite database is created and seeded automatically on first run. This is a learning/demo application; add authentication, CSRF protection, production configuration and privacy controls before real deployment.
