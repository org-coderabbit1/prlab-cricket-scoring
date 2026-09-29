# cricket-scoring

Scoring engine. Interprets `BallEvent` values and publishes a `ScoreSnapshot`.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ../cricket-protocol -e ".[dev]"
pytest
uvicorn scoring.app:app --port 8000
```
