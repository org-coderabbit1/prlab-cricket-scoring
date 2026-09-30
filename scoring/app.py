from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

from cricket_protocol import BallEvent

from scoring.engine import InningsState, apply_ball
from scoring.snapshot import ScoreSnapshot

app = FastAPI(title="cricket-scoring", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
_matches: dict[str, InningsState] = {}
_snapshots: dict[str, ScoreSnapshot] = {}


@app.post("/matches/{match_id}/balls", response_model=ScoreSnapshot)
def record_ball(match_id: str, event: BallEvent) -> ScoreSnapshot:
    if event.match_id != match_id:
        raise HTTPException(status_code=400, detail="match_id mismatch")
    state = _matches.setdefault(match_id, InningsState(match_id=match_id))
    new_state, snapshot = apply_ball(state, event)
    _matches[match_id] = new_state
    _snapshots[match_id] = snapshot
    return snapshot


@app.get(
    "/matches/{match_id}/score",
    response_model=ScoreSnapshot,
    responses={204: {"description": "No ball recorded for this match yet"}},
)
def get_score(match_id: str) -> ScoreSnapshot | Response:
    snapshot = _snapshots.get(match_id)
    if snapshot is None:
        # Dashboards poll before the first ball. That is not an error.
        return Response(status_code=204)
    return snapshot
