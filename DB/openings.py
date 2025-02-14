# --------------------------------------------------------------------------- #
#                                                                             #
#     openings.py                                         +#######+           #
#                                                       +###########+         #
#     PROJECT: Checkers                       ·''''''''·#############         #
#     AUTHOR(S): Jorge                       '''''''''''+###########+         #
#                                            '''''''''''' +#######+           #
#     CREATED DATE: 17/01/2025               ''''''''''''                     #
#     LAST UPDATE: 18/01/2025                 `''''''''´                      #
#                                                                             #
# --------------------------------------------------------------------------- #

"""
Includes all necessary functions to use the default openings on the game.
"""

from DB.db import getOpenings

G_OPENINGS = getOpenings()

def matchOpening(trace: str) -> str | None:
    """Check whether the given trace is a predefined opening.
    :returns: The mathing opening if the given trace is part of an existing opening, ``None`` otherwise
    """

    if trace == "":  # Make sure an empty trace is not a valid opening
        return None

    for opening in G_OPENINGS:
        if opening.startswith(trace):
            return opening  # Return the matching opening

    return None

def getNextMove(trace: str) -> list[tuple[str, int]] | None:
    """Get the next move for the given trace (if it is a valid opening).
    :returns: The next predefined move [(from_r, from_c), (to_r, to_c)] or ``None`` if opening is not valid or finished.
    """
    opening = matchOpening(trace)
    if opening is None or len(trace) + (5 if trace[-1] != "-" else 4) >= len(opening):
        return None
    start = len(trace) + (1 if trace[-1] != "-" else 0)
    move = opening[start:start + 4]
    return [(move[0], int(move[1])), (move[2], int(move[3]))]
