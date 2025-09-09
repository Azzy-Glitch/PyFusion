import random

def play_game():
    # Game configuration
    choices = {
        "r": {"name": "Rock", "value": 1, "emoji": "🗿"},
        "p": {"name": "Paper", "value": -1, "emoji": "📄"},
        "s": {"name": "Scissors", "value": 0, "emoji": "✂️"}
    }
    
    # Game introduction
    print("🎮 Welcome to Rock-Paper-Scissors Game! 🎮")
    print("=" * 40)
    print("Rules:")
    print("• Rock (r) 🗿 crushes Scissors ✂️")
    print("• Paper (p) 📄 covers Rock 🗿")
    print("• Scissors (s) ✂️ cut Paper 📄")
    print("=" * 40)
    
    # Score tracking
    player_score = 0
    computer_score = 0
    rounds = 0
    
    while True:
        rounds += 1
        print(f"\n--- Round {rounds} ---")
        
        # Get player choice with validation
        while True:
            player_input = input("Choose (r)ock, (p)aper, (s)cissors, or (q)uit: ").lower().strip()
            
            if player_input == 'q':
                print(f"\n🎯 Final Score: You {player_score} - {computer_score} Computer")
                if player_score > computer_score:
                    print("🏆 You won the game! Congratulations!")
                elif computer_score > player_score:
                    print("💻 Computer won the game. Better luck next time!")
                else:
                    print("🤝 It's a tie game!")
                return
            
            if player_input in choices:
                player_choice = choices[player_input]
                break
            else:
                print("❌ Invalid choice! Please enter 'r', 'p', 's', or 'q'.")
        
        # Computer makes random choice
        computer_choice_key = random.choice(list(choices.keys()))
        computer_choice = choices[computer_choice_key]
        
        # Display choices
        print(f"\nYou chose: {player_choice['name']} {player_choice['emoji']}")
        print(f"Computer chose: {computer_choice['name']} {computer_choice['emoji']}")
        
        # Determine winner
        if player_choice['value'] == computer_choice['value']:
            print("🤝 It's a draw!")
        else:
            # Winning conditions
            if (player_choice['value'] == 1 and computer_choice['value'] == 0) or \
               (player_choice['value'] == -1 and computer_choice['value'] == 1) or \
               (player_choice['value'] == 0 and computer_choice['value'] == -1):
                print("🎉 You win this round!")
                player_score += 1
            else:
                print("💻 Computer wins this round!")
                computer_score += 1
        
        # Display current score
        print(f"📊 Score: You {player_score} - {computer_score} Computer")
        
        # Ask if player wants to continue
        if rounds % 3 == 0:  # Ask every 3 rounds
            continue_game = input("\nContinue playing? (y/n): ").lower().strip()
            if continue_game != 'y':
                print(f"\n🎯 Final Score: You {player_score} - {computer_score} Computer")
                if player_score > computer_score:
                    print("🏆 You won the game! Congratulations!")
                elif computer_score > player_score:
                    print("💻 Computer won the game. Better luck next time!")
                else:
                    print("🤝 It's a tie game!")
                break

def show_stats():
    print("\n" + "=" * 40)
    print("GAME STATISTICS:")
    print("• Multiple rounds with score tracking")
    print("• Input validation for user choices")
    print("• Visual emojis for better experience")
    print("• Option to quit anytime")
    print("• Regular progress updates")
    print("=" * 40)

if __name__ == "__main__":
    show_stats()
    play_game()
    print("\nThanks for playing! 👋")