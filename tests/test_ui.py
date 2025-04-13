import pytest


from nlholdem.ui import get_ui_from_state


from pokerkit import NoLimitTexasHoldem, Automation, Mode


@pytest.fixture
def game():
    return NoLimitTexasHoldem(
        automations=(
            Automation.ANTE_POSTING,
            Automation.BET_COLLECTION,
            Automation.BLIND_OR_STRADDLE_POSTING,
            # Automation.BOARD_DEALING,
            Automation.CARD_BURNING,
            Automation.CHIPS_PULLING,
            Automation.CHIPS_PUSHING,
            Automation.HAND_KILLING,
            Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
            # Automation.HOLE_DEALING,
        ),
        ante_trimming_status=False,
        raw_antes={},
        raw_blinds_or_straddles=(5, 10),
        min_bet=10,
        mode=Mode.CASH_GAME,
    )


@pytest.fixture
def state(game):
    return game(
        raw_starting_stacks=(1000, 1000),
        player_count=2,
    )


def test_get_ui_from_state_board_cards_empty(state):
    expected = []

    actual = get_ui_from_state(state)["board_cards"]

    assert actual == expected


def test_get_ui_from_state_board_cards_flop(state):
    state.deal_hole("2c2s")
    state.deal_hole("AhAd")
    state.check_or_call()
    state.check_or_call()
    state.deal_board("4c5h7d")
    expected = ["4c", "5h", "7d"]

    actual = get_ui_from_state(state)["board_cards"]

    assert actual == expected


def test_get_ui_from_state_pot_pre_flop(state):
    state.deal_hole("2c2s")
    state.deal_hole("AhAd")
    expected = 0

    actual = get_ui_from_state(state)["pot"]

    assert actual == expected


def test_get_ui_from_state_pot_flop(state):
    state.deal_hole("2c2s")
    state.deal_hole("AhAd")
    state.check_or_call()
    state.check_or_call()
    state.deal_board("4c5h7d")
    expected = 20

    actual = get_ui_from_state(state)["pot"]

    assert actual == expected


def test_get_ui_from_state_bets(state):
    expected = [10, 5]

    result = get_ui_from_state(state)
    actual = [p["bet"] for p in result["players"]]

    assert actual == expected


def test_get_ui_from_state_stacks(state):
    expected = [990, 995]

    result = get_ui_from_state(state)
    actual = [p["stack"] for p in result["players"]]

    assert actual == expected


def test_get_ui_from_state_hole_cards(state):
    state.deal_hole("2c2s")
    state.deal_hole("AhAd")
    expected = [["2c", "2s"], ["Ah", "Ad"]]

    result = get_ui_from_state(state)
    actual = [p["hole_cards"] for p in result["players"]]

    assert actual == expected


def test_get_ui_from_state_dealer_button(state):
    expected = [False, True]

    result = get_ui_from_state(state)
    actual = [p["is_dealer"] for p in result["players"]]

    assert actual == expected
