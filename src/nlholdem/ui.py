from pokerkit import NoLimitTexasHoldem, Card


def _cards_list_to_str_list(cards: list[Card]) -> list[str]:
    return [repr(card) for card in cards]


def get_ui_from_state(state: NoLimitTexasHoldem) -> dict:
    """Generate a Python dict that containst the necessary state data for UI"""

    board_cards = _cards_list_to_str_list([c[0] for c in state.board_cards])

    dealer_index = (state.bring_in - 1) % state.player_count

    players = []
    for p in state.player_indices:
        player = {
            "hole_cards": _cards_list_to_str_list(state.hole_cards[p]),
            "bet": state.bets[p],
            "is_dealer": p == dealer_index,
            "stack": state.stacks[p],
        }

        players.append(player)

    # If no pot has been created yet, just return 0
    # e.g. pre-flop
    # Note: This will get more complicated if we want to have side pots
    # but that isn't possible in heads-up
    pot_amounts = tuple(state.pot_amounts)
    if len(pot_amounts) == 0:
        pot = 0
    else:
        pot = pot_amounts[0]

    return {"board_cards": board_cards, "players": players, "pot": pot}
