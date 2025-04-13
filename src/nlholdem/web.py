# src/nlholdem/web.py
from flask import Flask, render_template

from pokerkit import NoLimitTexasHoldem, Automation, Mode


app = Flask(__name__, template_folder="templates", static_folder="static")


# Poker Game State
state = NoLimitTexasHoldem.create_state(
    automations=(
        Automation.ANTE_POSTING,
        Automation.BET_COLLECTION,
        Automation.BLIND_OR_STRADDLE_POSTING,
        Automation.BOARD_DEALING,
        Automation.CARD_BURNING,
        Automation.CHIPS_PULLING,
        Automation.CHIPS_PUSHING,
        Automation.HAND_KILLING,
        Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
        Automation.HOLE_DEALING,
    ),
    ante_trimming_status=False,
    raw_antes={},
    raw_blinds_or_straddles=(5, 10),
    min_bet=10,
    raw_starting_stacks=(1000, 1000),
    player_count=2,
    mode=Mode.CASH_GAME,
)


@app.route("/")
def poker_table():
    board_cards = [repr(card).lower() for card in state.board_cards]

    return render_template("table.html", board_cards=board_cards)


if __name__ == "__main__":
    app.run(debug=True)
