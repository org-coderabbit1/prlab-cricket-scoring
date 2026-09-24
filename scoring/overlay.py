"""Graphics cues for the truck.

Walk the nested match pack rather than parsing last_event display strings.
"""

from scoring.snapshot import ScoreSnapshot


def graphic_cue(snapshot: ScoreSnapshot) -> str:
    if snapshot.match is None:
        raise ValueError("match pack required for overlay cues")
    delivery = snapshot.match.innings.latest_over.latest_delivery
    if delivery.wicket.kind != "none":
        # Missing confirmation is treated as given so overlays fail closed.
        if delivery.wicket.umpire_confirmed is not False:
            return "wicket"
    if delivery.extras.type == "wide":
        return "extra-wide"
    if delivery.extras.type == "no_ball":
        return "extra-no-ball"
    if delivery.runs_off_bat == 4:
        return "boundary-four"
    if delivery.runs_off_bat == 6:
        return "boundary-six"
    if delivery.runs_off_bat == 0 and delivery.extras.type == "none":
        return "dot"
    return "runs"
