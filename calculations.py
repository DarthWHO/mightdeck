def calculate_probability(decks):

    prob_no_misses = 1.0  # Initialize the probability
    prob_1_miss = 0.0  # Initialize the probability        

    for i in range(len(decks)):
        current_deck = decks[i]
        total_cards, misses, hits, draws = current_deck[0], current_deck[1], current_deck[2], current_deck[3]

        if total_cards == draws:
            if misses >= 2:
                prob_no_misses = 0
                prob_1_miss = 0
                break
        else:
            prob_no_misses *= (hits / total_cards) ** draws
        
            # Calculate the contribution of the current deck to the overall probability
            contribution = (draws * (misses / total_cards) * ((hits / total_cards) ** (draws - 1)))
            
            # Multiply with the probabilities of the other decks
            for j in range(len(decks)):
                if i != j:
                    contribution *= (decks[j][2] / decks[j][0]) ** decks[j][3]
            
            # Add the contribution to the overall probability
            prob_1_miss += contribution

    prob_2_miss = 1 - prob_no_misses - prob_1_miss
    prob_success = (1 - prob_2_miss) * 100
    return f"{prob_success:.1f}%"

# decks = []
# #draw_details(total_cards, misses_remaining, hits_remaining, number_drawn)
# decks.append([10, 1, 10-1, 3])
# decks.append([10, 1, 10-1, 2])
# print(calculate_probability(decks))