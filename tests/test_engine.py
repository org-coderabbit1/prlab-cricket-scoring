from cricket_protocol import BallEvent

from scoring.engine import InningsState, apply_ball


def ball(**overrides: object) -> BallEvent:
    payload: dict[str, object] = {
        "match_id": "m1",
        "innings": 1,
        "over": 0,
        "ball_in_over": 1,
        "striker": "Batter",
        "bowler": "Bowler",
        "runs_off_bat": 0,
        "extras": {"type": "none", "runs": 0},
        "wicket": {"kind": "none", "umpire_confirmed": False},
    }
    payload.update(overrides)
    return BallEvent.model_validate(payload)


def test_four_increments_runs_and_legal_ball() -> None:
    state = InningsState(match_id="m1")
    _, snapshot = apply_ball(state, ball(runs_off_bat=4))
    assert snapshot.runs == 4
    assert snapshot.wickets == 0
    assert snapshot.overs == "0.1"
    assert snapshot.last_event.display == "FOUR"
    assert snapshot.last_event.legal_delivery is True


def test_wide_adds_extras_without_legal_ball() -> None:
    state = InningsState(match_id="m1")
    _, snapshot = apply_ball(
        state, ball(extras={"type": "wide", "runs": 1})
    )
    assert snapshot.runs == 1
    assert snapshot.overs == "0.0"
    assert snapshot.last_event.display == "WIDE"
    assert snapshot.last_event.legal_delivery is False


def test_confirmed_lbw_counts_wicket() -> None:
    state = InningsState(match_id="m1")
    _, snapshot = apply_ball(
        state, ball(wicket={"kind": "lbw", "umpire_confirmed": True})
    )
    assert snapshot.wickets == 1
    assert snapshot.last_event.display == "WICKET"
    assert snapshot.last_event.wicket_counted is True


def test_unconfirmed_lbw_does_not_count() -> None:
    state = InningsState(match_id="m1")
    _, snapshot = apply_ball(
        state, ball(wicket={"kind": "lbw", "umpire_confirmed": False})
    )
    assert snapshot.wickets == 0
    assert snapshot.last_event.display == "NOT_OUT"
    assert snapshot.last_event.wicket_counted is False


def test_snapshot_includes_match_pack_for_overlays() -> None:
    state = InningsState(match_id="m1")
    _, snapshot = apply_ball(
        state, ball(wicket={"kind": "lbw", "umpire_confirmed": False})
    )
    dumped = snapshot.model_dump()
    delivery = dumped["match"]["innings"]["latest_over"]["latest_delivery"]
    assert delivery["wicket"]["kind"] == "lbw"
    assert delivery["wicket"]["umpire_confirmed"] is False
    assert snapshot.last_event.wicket_counted is False
