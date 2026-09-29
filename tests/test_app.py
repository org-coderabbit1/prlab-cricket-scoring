from fastapi.testclient import TestClient

from scoring.app import app

client = TestClient(app)

PAYLOAD = {
    "match_id": "m1",
    "innings": 1,
    "over": 0,
    "ball_in_over": 1,
    "striker": "Batter",
    "bowler": "Bowler",
    "runs_off_bat": 1,
    "extras": {"type": "none", "runs": 0},
    "wicket": {"kind": "none", "umpire_confirmed": False},
}


def test_record_and_fetch_score() -> None:
    recorded = client.post("/matches/m1/balls", json=PAYLOAD)
    assert recorded.status_code == 200
    fetched = client.get("/matches/m1/score")
    assert fetched.status_code == 200
    body = fetched.json()
    assert body["runs"] == 1
    assert body["last_event"]["display"] == "1"
    assert body["raw_ball"]["runs_off_bat"] == 1
