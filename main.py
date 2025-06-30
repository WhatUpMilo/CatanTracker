import random
from collections import defaultdict

# Theoretical probabilities for sums from 2 to 12
theoretical_probs = {
    2: 1 / 36,
    3: 2 / 36,
    4: 3 / 36,
    5: 4 / 36,
    6: 5 / 36,
    7: 6 / 36,
    8: 5 / 36,
    9: 4 / 36,
    10: 3 / 36,
    11: 2 / 36,
    12: 1 / 36
}

DEVIATION_THRESHOLD = 0.05  # 5%


def get_player_count():
    while True:
        try:
            players = int(input("Enter the number of players: "))
            if players > 0:
                return players
            else:
                print("Must be at least 1 player.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_mode():
    while True:
        mode = input("Choose mode - 'Automatic' or 'Manual': ").strip().lower()
        if mode in ['automatic', 'manual']:
            return mode
        else:
            print("Invalid choice. Please type 'Automatic' or 'Manual'.")


def get_sum_input(current_player):
    while True:
        try:
            roll_sum = int(input(f"Player {current_player}, enter the sum of two dice (2-12): "))
            if 2 <= roll_sum <= 12:
                return roll_sum
            else:
                print("Invalid sum. Must be between 2 and 12.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def roll_two_dice():
    return random.randint(1, 6) + random.randint(1, 6)


def display_probabilities(counts, total):
    print("\n--- Empirical Probability Table ---")
    for sum_value in range(2, 13):
        freq = counts[sum_value]
        prob = freq / total if total > 0 else 0
        print(f"Sum {sum_value}: Count = {freq}, Probability = {prob:.4f}")
    print()


def display_deviation_table(counts, total):
    print("--- Deviation from Theoretical Probabilities ---")
    print(f"{'Sum':>4} {'Theoretical':>12} {'Empirical':>12} {'Abs Dev':>10}")

    lucky_numbers = []
    for sum_value in range(2, 13):
        theo = theoretical_probs[sum_value]
        emp = counts[sum_value] / total if total > 0 else 0
        dev = abs(emp - theo)
        print(f"{sum_value:>4} {theo:>12.4f} {emp:>12.4f} {dev:>10.4f}")

        if dev >= DEVIATION_THRESHOLD:
            if emp > theo:
                lucky_numbers.append(f"{sum_value} is unusually lucky!")
            else:
                lucky_numbers.append(f"{sum_value} is surprisingly rare!")

    print("\n--- Interpretation ---")
    if lucky_numbers:
        for msg in lucky_numbers:
            print(msg)
    else:
        print("No lucky or unlucky numbers yet!")
    print()


def run_manual_mode(num_players):
    sum_counts = defaultdict(int)
    total_rolls = 0
    min_rolls = num_players * 3

    print(f"\nManual Mode: Each player enters the sum of their dice.")
    print(f"Interpretation appears after {min_rolls} total rolls.\n")

    try:
        while True:
            for player in range(1, num_players + 1):
                roll_sum = get_sum_input(player)
                sum_counts[roll_sum] += 1
                total_rolls += 1
                display_probabilities(sum_counts, total_rolls)
                if total_rolls >= min_rolls:
                    display_deviation_table(sum_counts, total_rolls)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        display_probabilities(sum_counts, total_rolls)
        if total_rolls >= min_rolls:
            display_deviation_table(sum_counts, total_rolls)
        else:
            print("Not enough rolls to calculate deviations yet.")


def run_automatic_mode(num_players):
    sum_counts = defaultdict(int)
    total_rolls = 0
    rounds = random.randint(15, 17)

    print(f"\nAutomatic Mode: Simulating {rounds} rounds for {num_players} players...\n")

    for round_num in range(1, rounds + 1):
        print(f"--- Round {round_num} ---")
        for player in range(1, num_players + 1):
            roll = roll_two_dice()
            sum_counts[roll] += 1
            total_rolls += 1
            print(f"Player {player} rolled a {roll}")
        print()

    display_probabilities(sum_counts, total_rolls)
    display_deviation_table(sum_counts, total_rolls)


def main():
    print("🎲 Dice Sum Tracker for Catan or Probability Analysis")
    num_players = get_player_count()
    mode = get_mode()

    if mode == 'automatic':
        run_automatic_mode(num_players)
    else:
        run_manual_mode(num_players)


if __name__ == "__main__":
    main()
