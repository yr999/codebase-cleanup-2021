
from random import choice
def determine_winner(user_choice, computer_choice):
    #return "paper"
    winners = {
        "rock": {
            "rock": None,
            "paper": "paper",
            "scissors": "rock",
        },
        "paper": {
            "rock": "paper",
            "paper": None,
            "scissors": "scissors",
        },
        "scissors": {
            "rock": "rock",
            "paper": "scissors",
            "scissors": None,
        }
    }
    winning_choice = winners[user_choice][computer_choice]
    return winning_choice
if __name__ == "__main__":
    # STILL ALLOW US TO RUN FROM COMMAND LINE
    # AND DO THE STUFF BELOW
    # BUT NOT DO THE STUFF BELOW WHEN TRYING TO IMPORT
    # IN ORDER FOR US TO BE ABLE TO IMPORT ANY FUNCTION
    # ... FROM ANY FILE (LIKE THIS ONE)
    # ... THIS FILE NEEDS A CLEAN GLOBAL SCOPE
    # ... (ONLY FUNCTIONS AND A MAIN CONDITIONAL)
    #
    # USER SELECTION
    #
    u = input("Please choose one of 'Rock', 'Paper', or 'Scissors': ").lower()
    print("USER CHOICE:", u)
    if u not in ["rock", "paper", "scissors"]:
        print("OOPS, TRY AGAIN")
        exit()
    #
    # COMPUTER SELECTION
    #
    c = choice(["rock", "paper", "scissors"])
    print("COMPUTER CHOICE:", c)
    # DETERMINE WINNER
    winner = determine_winner(u, c)
    if winner == u:
        print("YOU WON!")
    elif winner == c:
        print("YOU LOST")
    else:
        print("TIE")

















