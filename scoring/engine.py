from dataclasses import dataclass

from cricket_protocol import BallEvent, ExtraType, WicketKind

from scoring.snapshot import LastEvent, ScoreSnapshot

ILLEGAL_EXTRAS = {ExtraType.WIDE, ExtraType.NO_BALL}


@dataclass
class InningsState:
    match_id: str
    runs: int = 0
    wickets: int = 0
    legal_balls: int = 0


def format_overs(legal_balls: int) -> str:
    overs, balls = divmod(legal_balls, 6)
    return f"{overs}.{balls}"


def _display(event: BallEvent, wicket_counted: bool, runs_added: int) -> str:
    if wicket_counted:
        return "WICKET"
    if event.wicket.kind is not WicketKind.NONE:
        return "NOT_OUT"
    if event.extras.type is ExtraType.WIDE:
        return "WIDE"
    if event.extras.type is ExtraType.NO_BALL:
        return "NO_BALL"
    if event.runs_off_bat == 4:
        return "FOUR"
    if event.runs_off_bat == 6:
        return "SIX"
    if runs_added == 0:
        return "DOT"
    return str(runs_added)


def apply_ball(state: InningsState, event: BallEvent) -> tuple[InningsState, ScoreSnapshot]:
    """Interpret a hop-0 event. This is the only place wickets can be counted."""
    if event.match_id != state.match_id:
        raise ValueError("match_id mismatch")

    # Semantic dependency on hop 0: runs_off_bat excludes extras.
    runs_added = event.runs_off_bat + event.extras.runs
    wicket_counted = (
        event.wicket.kind is not WicketKind.NONE and event.wicket.umpire_confirmed
    )
    legal_delivery = event.extras.type not in ILLEGAL_EXTRAS

    new_state = InningsState(
        match_id=state.match_id,
        runs=state.runs + runs_added,
        wickets=state.wickets + (1 if wicket_counted else 0),
        legal_balls=state.legal_balls + (1 if legal_delivery else 0),
    )
    snapshot = ScoreSnapshot(
        match_id=event.match_id,
        runs=new_state.runs,
        wickets=new_state.wickets,
        overs=format_overs(new_state.legal_balls),
        last_event=LastEvent(
            display=_display(event, wicket_counted, runs_added),
            runs_added=runs_added,
            wicket_counted=wicket_counted,
            legal_delivery=legal_delivery,
        ),
        raw_ball=event.model_dump(mode="json"),
    )
    return new_state, snapshot
