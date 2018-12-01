import numpy as np

HEADS = 1
TAILS = 0
NUM_SIDES_OF_COIN = 2

# coin_tosses is a list of the actual observed coin tosses, 
#   ex: [1 0 1 0 1 0 0 0 1 1]
# trasition_matrix is the probability of the next coin based on the current coin.
#   ex: [ [.75 .9] [.25 .1] ]
# emissions is the probably of each coin showing a head (or the bias).
#   ex: [.5 .5]
def compute_transitions(coin_tosses, trasition_matrix, emissions):
    # emission_matrix[0][y] represents the probability of the yth coin showing a head
    # emission_matrix[1][y] represents the probability of the yth coin showing a tail
    emission_matrix = np.zeros(shape=(NUM_SIDES_OF_COIN, len(emissions)))
    for coin_number, emission_probability in enumerate(emissions):
        emission_matrix[HEADS, coin_number] = 1 - emission_probability
        emission_matrix[TAILS, coin_number] = emission_probability
    
    # num_states is number of coins in hidden markov model.
    num_states = emission_matrix.shape[1]
    print("Number of coins:", num_states)

    # num_coin_tosses is the number of observed coin tosses.
    num_coin_tosses = len(coin_tosses)
    print("Number of coin tosses:", num_coin_tosses, "\n")

    # Create a matrix for the state/probability transitions.
    transition_prob_matrix = np.zeros(shape=(num_states, num_coin_tosses))

    # Create a path (2D matrix) describing the optimal path through the HMM.
    # Transition matrix is M x N where M is the number of coins, and N is the 
    # number of coin tosses performed.
    optimal_transition_path = np.zeros(shape=(num_states, num_coin_tosses))

    # Create a path (1D) for the most probable state (coin) sequence.
    optimal_transitions = np.zeros(num_coin_tosses, dtype=int)

    #optimal_transitions[0] = 0

    # Equalizes initial probability
    for index in range(0, num_states):
        transition_prob_matrix[index, 0] = emission_matrix[coin_tosses[0], index]

    # Print emmission_matrix
    print("Emission Matrix: \n", emission_matrix)

    # Iterate through the sequence of coin tosses using dynamic programming.
    for index in range(1, num_coin_tosses):
        for state in range(num_states):
            emission_prob = emission_matrix[coin_tosses[index], state]

            prob_max = trasition_matrix[state, 0] * emission_prob * transition_prob_matrix[0, index-1] 
            prob_max_index = 0

            for previous_state in range(1, num_states):
                prob = trasition_matrix[state, previous_state] * emission_prob * transition_prob_matrix[previous_state, index-1] 
            
                if prob > prob_max:
                    prob_max = prob
                    prob_max_index = previous_state
                    
            transition_prob_matrix[state, index] = prob_max 
            optimal_transition_path[state, index] = prob_max_index
        #optimal_transitions[index] = prob_max_index

    # Finding highest probability of the last element in the input (column).
    optimal_probability = transition_prob_matrix[0, num_coin_tosses-1]
    optimal_end_state = 0
    for state in range(1, num_states):
        if transition_prob_matrix[state, num_coin_tosses-1] > optimal_probability:
            optimal_probability = transition_prob_matrix[state, num_coin_tosses-1]
            optimal_end_state = state
    optimal_prev = optimal_end_state
    optimal_transitions[num_coin_tosses-1] = optimal_prev

    # Uses the path to trace how we got there. 
    # Start at last transition, end at first transition.
    for index in range(num_coin_tosses-1, 0, -1):
        optimal_transitions[index-1] = int(optimal_transition_path[optimal_prev, index])

    print('Most probable state sequence:', optimal_transitions)
    print('Transition probabilities:\n', transition_prob_matrix.T)