#!/usr/bin/env python3
"""Terminal Blackjack: player vs dealer (no betting)."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

SUITS = ["Spades", "Hearts", "Diamonds", "Clubs"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self) -> None:
        self.cards: List[Card] = []
        self._build_and_shuffle()

    def _build_and_shuffle(self) -> None:
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def ensure_cards(self, threshold: int = 15) -> None:
        """Reshuffle automatically when the deck is low."""
        if len(self.cards) < threshold:
            print("\n[Deck low (<15 cards). Reshuffling a fresh deck.]\n")
            self._build_and_shuffle()

    def deal(self) -> Card:
        if not self.cards:
            self._build_and_shuffle()
        return self.cards.pop()


def hand_value(hand: List[Card]) -> int:
    """Return Blackjack value with proper multi-ace handling."""
    total = 0
    aces = 0

    for card in hand:
        if card.rank in {"J", "Q", "K"}:
            total += 10
        elif card.rank == "A":
            total += 11
            aces += 1
        else:
            total += int(card.rank)

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


def format_hand(hand: List[Card]) -> str:
    return ", ".join(str(card) for card in hand)


def is_blackjack(hand: List[Card]) -> bool:
    return len(hand) == 2 and hand_value(hand) == 21


def ask_hit_or_stand_or_quit() -> str:
    """Prompt until a valid action is given.

    Returns:
        "h" for hit, "s" for stand, "q" for quit game.
    """
    while True:
        choice = input("Hit, Stand, or Quit? (H/S/Q): ").strip().lower()
        if choice in {"h", "s", "q", "quit"}:
            return "q" if choice in {"q", "quit"} else choice
        print("Invalid input. Please enter H, S, or Q.")


def ask_play_again() -> bool:
    while True:
        choice = input("Play again? (y/n): ").strip().lower()
        if choice in {"y", "yes"}:
            return True
        if choice in {"n", "no"}:
            return False
        print("Invalid input. Please enter y or n.")


def print_intro() -> None:
    print("=" * 46)
    print("Welcome to Terminal Blackjack")
    print("Controls: H = Hit, S = Stand, Q = Quit")
    print("Dealer stands on all 17s. No betting.")
    print("=" * 46)


def play_hand(deck: Deck) -> bool:
    """Play one hand.

    Returns:
        False if the player chooses to quit mid-hand, else True.
    """
    deck.ensure_cards()

    player_hand = [deck.deal(), deck.deal()]
    dealer_hand = [deck.deal(), deck.deal()]

    print("\n--- New Hand ---")
    print(f"Your hand: {format_hand(player_hand)} (total: {hand_value(player_hand)})")
    print(f"Dealer shows: {dealer_hand[0]}, [hidden]")

    player_bj = is_blackjack(player_hand)
    dealer_bj = is_blackjack(dealer_hand)

    if player_bj or dealer_bj:
        print(f"Dealer hand: {format_hand(dealer_hand)} (total: {hand_value(dealer_hand)})")
        if player_bj and dealer_bj:
            print("Result: Push! Both have blackjack.")
        elif player_bj:
            print("Result: You win with a natural blackjack!")
        else:
            print("Result: Dealer has blackjack. You lose.")
        return True

    while True:
        action = ask_hit_or_stand_or_quit()

        if action == "q":
            print("Quitting game...")
            return False
        if action == "h":
            player_hand.append(deck.deal())
            print(f"You draw: {player_hand[-1]}")
            print(f"Your hand: {format_hand(player_hand)} (total: {hand_value(player_hand)})")

            if hand_value(player_hand) > 21:
                print(f"Dealer hand: {format_hand(dealer_hand)} (total: {hand_value(dealer_hand)})")
                print("Result: Bust! You lose.")
                return True
        else:
            break

    print(f"Dealer hand: {format_hand(dealer_hand)} (total: {hand_value(dealer_hand)})")

    while hand_value(dealer_hand) < 17:
        drawn = deck.deal()
        dealer_hand.append(drawn)
        print(f"Dealer hits and draws: {drawn} (total: {hand_value(dealer_hand)})")

    dealer_total = hand_value(dealer_hand)
    player_total = hand_value(player_hand)

    if dealer_total > 21:
        print("Result: Dealer busts. You win!")
    elif player_total > dealer_total:
        print("Result: You win!")
    elif dealer_total > player_total:
        print("Result: Dealer wins.")
    else:
        print("Result: Push (tie).")

    return True


def _self_checks() -> None:
    """Simple assertions for hand-value correctness."""
    assert hand_value([Card("A", "Spades"), Card("K", "Diamonds")]) == 21
    assert hand_value([Card("A", "Spades"), Card("9", "Diamonds"), Card("A", "Hearts")]) == 21
    assert hand_value([Card("A", "Spades"), Card("A", "Diamonds"), Card("9", "Hearts"), Card("A", "Clubs")]) == 12
    assert hand_value([Card("10", "Spades"), Card("7", "Diamonds"), Card("4", "Hearts")]) == 21
    assert hand_value([Card("A", "Spades"), Card("A", "Diamonds"), Card("8", "Hearts")]) == 20


def main() -> None:
    _self_checks()
    print_intro()

    deck = Deck()
    while True:
        finished_hand = play_hand(deck)
        if not finished_hand:
            print("Thanks for playing!")
            break

        print()
        if not ask_play_again():
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()

# Example run (short):
# ==============================================
# Welcome to Terminal Blackjack
# Controls: H = Hit, S = Stand, Q = Quit
# Dealer stands on all 17s. No betting.
# ==============================================
#
# --- New Hand ---
# Your hand: 9 of Clubs, A of Diamonds (total: 20)
# Dealer shows: 6 of Hearts, [hidden]
# Hit, Stand, or Quit? (H/S/Q): s
# Dealer hand: 6 of Hearts, 10 of Spades (total: 16)
# Dealer hits and draws: 8 of Diamonds (total: 24)
# Result: Dealer busts. You win!
#
# Play again? (y/n): n
# Thanks for playing!
