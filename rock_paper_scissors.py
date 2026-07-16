import random
import os
import json
from colorama import init, Fore, Style

init(autoreset=True)

# -----------------------------
# CONSTANTS
# -----------------------------

ROCK = "Rock 🪨"
PAPER = "Paper 📄"
SCISSORS = "Scissors ✂️"

OPTIONS = [ROCK, PAPER, SCISSORS]
player_history = []
difficulty = "Easy"
player_name = ""

# -----------------------------
# STATISTICS
# -----------------------------

stats = {
    "games": 0,
    "wins": 0,
    "losses": 0,
    "draws": 0,
    "win_streak": 0,
    "best_streak": 0
}
STATS_FILE = "data/stats.json"

def get_player_name():
    global player_name, stats

    if stats.get("player_name"):
        player_name = stats["player_name"]
        print(Fore.GREEN + f"\n👋 Welcome back, {player_name}!")
        return

    header("WELCOME")

    while True:
        name = input("Enter your name: ").strip()

        if name:
            player_name = name
            stats["player_name"] = name
            save_stats()
            break

        print("Please enter a valid name.")

def load_stats():
    global stats

    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as file:
            stats = json.load(file)


def save_stats():
    with open(STATS_FILE, "w") as file:
        json.dump(stats, file, indent=4)
# -----------------------------
# UTILITIES
# -----------------------------


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def line():
    print(Fore.CYAN + "=" * 60)


def header(title):
    clear()
    line()
    print(Fore.YELLOW + Style.BRIGHT + title.center(60))
    line()


# -----------------------------
# MENU
# -----------------------------


def menu():

    header("ROCK PAPER SCISSORS ")

    print(Fore.GREEN + "1. Play Game")
    print(Fore.GREEN + "2. Statistics")
    print(Fore.GREEN + "3. Achievements")
    print(Fore.GREEN + "4. Reset Statistics")
    print(Fore.GREEN + "5. Rules")
    print(Fore.GREEN + "6. Exit")

    line()


# -----------------------------
# RULES
# -----------------------------


def rules():

    header("GAME RULES")

    print("""
🪨 Rock beats Scissors

📄 Paper beats Rock

✂️ Scissors beats Paper
""")

    input("\nPress ENTER to return...")


# -----------------------------
# STATISTICS
# -----------------------------


def statistics():

    header("PLAYER STATISTICS")

    print(f"Player       : {player_name}")
    print()
    print(f"Games Played : {stats['games']}")
    print(f"Wins         : {stats['wins']}")
    print(f"Losses       : {stats['losses']}")
    print(f"Draws        : {stats['draws']}")

    if stats["games"] > 0:
        rate = stats["wins"] / stats["games"] * 100
        print(f"Win Rate     : {rate:.2f}%")

    else:
        print("Win Rate     : 0%")

    print(f"Best Streak  : {stats['best_streak']}")

    input("\nPress ENTER...")

def reset_statistics():

    global stats

    header("RESET STATISTICS")

    choice = input("Are you sure you want to reset all statistics? (Y/N): ").lower()

    if choice == "y":

        stats = {
            "games": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "win_streak": 0,
            "best_streak": 0
        }

        save_stats()

        print(Fore.GREEN + "\n✔ Statistics reset successfully!")

    else:
        print(Fore.YELLOW + "\nReset cancelled.")

    input("\nPress ENTER to continue...")

def match_summary(player_score, computer_score):

    header("MATCH SUMMARY")

    print(Fore.CYAN + f"Difficulty : {difficulty}")
    print(Fore.CYAN + f"Your Score : {player_score}")
    print(Fore.CYAN + f"Computer   : {computer_score}")

    print()

    if player_score > computer_score:
        print(Fore.GREEN + Style.BRIGHT + "🏆 Congratulations! You won the match!")

    else:
        print(Fore.RED + Style.BRIGHT + "💻 Computer won the match!")

    print()

    if stats["games"] > 0:
        rate = stats["wins"] / stats["games"] * 100
        print(Fore.YELLOW + f"Overall Win Rate : {rate:.2f}%")

    print(Fore.YELLOW + f"Best Win Streak  : {stats['best_streak']}")

    input("\nPress ENTER to continue...")

def check_achievements():



    if stats["wins"] >= 1 and "First Victory" not in stats["achievements"]:
        stats["achievements"].append("First Victory")
        save_stats
        print(Fore.GREEN + "\n🏅 Achievement Unlocked: First Victory!")

    if stats["wins"] >= 10 and "Champion" not in stats["achievements"]:
        stats["achievements"].append("Champion")
        save_stats
        print(Fore.YELLOW + "\n👑 Achievement Unlocked: Champion!")

    if stats["best_streak"] >= 5 and "Hot Streak" not in stats["achievements"]:
        stats["achievements"].append("Hot Streak")
        save_stats
        print(Fore.MAGENTA + "\n🔥 Achievement Unlocked: Hot Streak!")

def view_achievements():

    header("ACHIEVEMENTS")

    if not stats["achievements"]:
        print(Fore.YELLOW + "No achievements unlocked yet.")

    else:
        print(Fore.GREEN + "Unlocked Achievements:\n")

        for achievement in stats["achievements"]:
            print("🏅", achievement)

    input("\nPress ENTER to continue...")                
# -----------------------------
# WINNER
# -----------------------------


def check(player, computer):

    if player == computer:
        return "draw"

    if (
        (player == ROCK and computer == SCISSORS)
        or (player == PAPER and computer == ROCK)
        or (player == SCISSORS and computer == PAPER)
    ):
        return "win"

    return "lose"


# -----------------------------
# PLAY ONE ROUND
# -----------------------------

def computer_choice(player=None):
    global player_history, difficulty

    # EASY
    if difficulty == "Easy":
        return random.choice(OPTIONS)

    # MEDIUM
    elif difficulty == "Medium":

        if random.random() < 0.30 and player is not None:

            if player == ROCK:
                return PAPER

            elif player == PAPER:
                return SCISSORS

            else:
                return ROCK

        return random.choice(OPTIONS)

    # HARD
    else:

        if len(player_history) < 5:
            return random.choice(OPTIONS)

        most_common = max(set(player_history), key=player_history.count)

        if most_common == ROCK:
            return PAPER

        elif most_common == PAPER:
            return SCISSORS

        else:
            return ROCK
def play_round():

    print()

    print("1.", ROCK)
    print("2.", PAPER)
    print("3.", SCISSORS)

    while True:

        try:

            choice = int(input("\nChoose: "))

            if choice in [1, 2, 3]:
                break

            print("Choose 1-3")

        except:
            print("Numbers only.")

    player = OPTIONS[choice - 1]
    player_history.append(player)

    if len(player_history) > 20:
      player_history.pop(0)

    computer = computer_choice(player)

    print()

    print(Fore.CYAN + f"{player_name:<10}:, {player}")
    print(Fore.MAGENTA + "Computer :", computer)

    result = check(player, computer)

    stats["games"] += 1

    if result == "win":

        stats["wins"] += 1
        stats["win_streak"] += 1

        if stats["win_streak"] > stats["best_streak"]:
            stats["best_streak"] = stats["win_streak"]

        print(Fore.GREEN + "\nYou Win!")

    elif result == "lose":

        stats["losses"] += 1
        stats["win_streak"] = 0

        print(Fore.RED + "\nComputer Wins!")

    else:

        stats["draws"] += 1

        print(Fore.YELLOW + "\nDraw!")

    print()
    save_stats()
    check_achievements()


# -----------------------------
# MODES
# -----------------------------


def endless():

    while True:

        play_round()

        again = input("Play Again? (Y/N): ").lower()

        if again != "y":
            break


def best_of(limit):

    player = 0
    computer = 0

    while player < limit and computer < limit:

        before = stats["wins"]

        play_round()

        if stats["wins"] > before:
            player += 1

        elif stats["losses"] > (stats["games"] - stats["wins"] - stats["draws"]):
            computer += 1

        print(Fore.CYAN + f"\nScore : You {player} - {computer} Computer\n")

    match_summary(player, computer)


# -----------------------------
# PLAY MENU
# -----------------------------

def choose_difficulty():
    global difficulty

    header("SELECT DIFFICULTY")

    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    choice = input("\nChoice: ")

    if choice == "1":
        difficulty = "Easy"

    elif choice == "2":
        difficulty = "Medium"

    elif choice == "3":
        difficulty = "Hard"

    else:
        difficulty = "Easy"
def play():

    while True:

        header("SELECT MODE")
        choose_difficulty()
        print("1. Best of 3")
        print("2. Best of 5")
        print("3. Endless")
        print("4. Back")

        choice = input("\nChoice: ")

        if choice == "1":
            best_of(2)

        elif choice == "2":
            best_of(3)

        elif choice == "3":
            endless()

        elif choice == "4":
            break


# -----------------------------
# MAIN
# -----------------------------
load_stats()
get_player_name()

while True:

    menu()

    option = input("Select: ")

    if option == "1":
     play()

    elif option == "2":
     statistics()

    elif option == "3":
     view_achievements()

    elif option == "4":
     reset_statistics()

    elif option == "5":
     rules()

    elif option == "6":
     header("GOODBYE")
     print(Fore.GREEN + "Thank you for playing!")
     break

    else:
     print(Fore.RED + "Invalid choice!")
     input("\nPress ENTER to continue...")
