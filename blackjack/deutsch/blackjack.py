import random

# Kartenwerte und Deck
suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}

def create_deck():
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def hand_value(hand):
    total = 0
    aces = 0
    for rank, suit in hand:
        total += values[rank]
        if rank == "A":
            aces += 1
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def print_hand(name, hand, hide_first=False):
    if hide_first:
        print(f"{name}: [??] " + " ".join(f"{r}{s}" for r, s in hand[1:]))
    else:
        print(f"{name}: " + " ".join(f"{r}{s}" for r, s in hand) +
              f"  (Wert: {hand_value(hand)})")

def player_turn(deck, player_hand, dealer_hand):
    while True:
        print()
        print_hand("Dein Blatt", player_hand)
        print_hand("Dealer", dealer_hand, hide_first=True)

        if hand_value(player_hand) >= 21:
            break

        choice = input("Hit (h) oder Stand (s): ").strip().lower()
        if choice == "h":
            player_hand.append(deck.pop())
        elif choice == "s":
            break

def dealer_turn(deck, dealer_hand):
    print("\nDealer ist am Zug...")
    print_hand("Dealer", dealer_hand)
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        print_hand("Dealer", dealer_hand)

def determine_winner(player_hand, dealer_hand):
    p = hand_value(player_hand)
    d = hand_value(dealer_hand)

    print()
    print_hand("Dein Blatt", player_hand)
    print_hand("Dealer", dealer_hand)

    if p > 21:
        return "lose"
    if d > 21:
        return "win"
    if p > d:
        return "win"
    if p < d:
        return "lose"
    return "push"

def play_round(balance):
    print(f"\nKontostand: {balance}€")
    while True:
        try:
            bet = int(input("Einsatz: "))
            if 1 <= bet <= balance:
                break
            print("Ungültiger Einsatz.")
        except:
            print("Bitte eine Zahl eingeben.")

    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # Blackjack check
    if hand_value(player_hand) == 21:
        print("\nBLACKJACK!")
        print_hand("Dein Blatt", player_hand)
        print_hand("Dealer", dealer_hand)
        win_amount = int(bet * 1.5)
        print(f"Du gewinnst {win_amount}€!")
        return balance + win_amount

    player_turn(deck, player_hand, dealer_hand)

    if hand_value(player_hand) <= 21:
        dealer_turn(deck, dealer_hand)

    result = determine_winner(player_hand, dealer_hand)

    if result == "win":
        print(f"Du gewinnst {bet * 2}€!")
        return balance + (bet * 2)
    elif result == "lose":
        print(f"Du verlierst {bet}€.")
        return balance - bet
    else:
        print("Unentschieden – Einsatz zurück.")
        return balance

def main():
    balance = 500
    print("=== Blackjack mit Kontostand ===")

    while balance > 0:
        balance = play_round(balance)
        print(f"Neuer Kontostand: {balance}€")

        again = input("Nochmal spielen? (j/n): ").strip().lower()
        if again != "j":
            break

    print("Spiel beendet. Danke fürs Spielen!")

if __name__ == "__main__":
    main()
