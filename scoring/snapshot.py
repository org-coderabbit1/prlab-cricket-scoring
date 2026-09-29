"""Product contract for hop 2. Do not put BallEvent fields here."""

from pydantic import BaseModel, Field


class LastEvent(BaseModel):
    display: str = Field(
        description="Scoring-owned label: DOT, runs, FOUR, SIX, WIDE, NO_BALL, WICKET, NOT_OUT."
    )
    runs_added: int
    wicket_counted: bool
    legal_delivery: bool


class DeliveryWicket(BaseModel):
    kind: str
    umpire_confirmed: bool


class DeliveryExtras(BaseModel):
    type: str
    runs: int


class LatestDelivery(BaseModel):
    striker: str
    bowler: str
    runs_off_bat: int
    extras: DeliveryExtras
    wicket: DeliveryWicket


class LatestOver(BaseModel):
    number: int
    latest_delivery: LatestDelivery


class InningsPack(BaseModel):
    number: int
    latest_over: LatestOver


class MatchPack(BaseModel):
    """Structured feed for the graphics truck. Mirrors the last delivery."""

    innings: InningsPack


class ScoreSnapshot(BaseModel):
    """Public scorecard. Broadcast may depend only on this shape.

    Forbidden product fields: raw BallEvent, extras.type, umpire_confirmed.
    """

    match_id: str
    runs: int
    wickets: int
    overs: str
    last_event: LastEvent
    match: MatchPack | None = Field(
        default=None,
        description=(
            "Nested match pack for overlay clients. Walk "
            "match.innings.latest_over.latest_delivery instead of parsing last_event."
        ),
    )
