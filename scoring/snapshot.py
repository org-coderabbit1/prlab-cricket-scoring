"""Product contract for hop 2. Do not put BallEvent fields here."""

from pydantic import BaseModel, Field


class LastEvent(BaseModel):
    display: str = Field(
        description="Scoring-owned label: DOT, runs, FOUR, SIX, WIDE, NO_BALL, WICKET, NOT_OUT."
    )
    runs_added: int
    wicket_counted: bool
    legal_delivery: bool


class ScoreSnapshot(BaseModel):
    """Public scorecard. Broadcast may depend only on this shape.

    Forbidden product fields: raw BallEvent, extras.type, umpire_confirmed.
    """

    match_id: str
    runs: int
    wickets: int
    overs: str
    last_event: LastEvent
    raw_ball: dict[str, object] | None = Field(
        default=None,
        description="Debug envelope of the original BallEvent. Product clients must ignore this.",
    )
