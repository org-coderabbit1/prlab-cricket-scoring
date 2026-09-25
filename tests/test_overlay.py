from cricket_protocol import BallEvent

from scoring.engine import InningsState, apply_ball
from scoring.overlay import graphic_cue


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


def test_overlay_walks_match_pack_for_wide() -> None:
    _, snapshot = apply_ball(
        InningsState(match_id="m1"), ball(extras={"type": "wide", "runs": 1})
    )
    assert (
        snapshot.match.innings.latest_over.latest_delivery.extras.type == "wide"
    )
    assert graphic_cue(snapshot) == "extra-wide"


def test_overlay_treats_dismissal_as_wicket_via_nested_wicket() -> None:
    _, snapshot = apply_ball(
        InningsState(match_id="m1"),
        ball(wicket={"kind": "lbw", "umpire_confirmed": True}),
    )
    assert (
        snapshot.match.innings.latest_over.latest_delivery.wicket.kind == "lbw"
    )
    assert graphic_cue(snapshot) == "wicket"
