import numpy as np

HEADS = 1
TAILS = 0

# input_str is a list of the actual observed coin tosses, 
#   ex: [1 0 1 0 1 0 0 0 1 1].
# emissionMatrix is the probably of each coin showing a head (or the bias).
#   ex: [.5 .5]
# transitionMatrix is the probability of the next coin based on the current coin. 
#   ex: [ [.75 .9] [.25 .1] ]
def compute_transitions(coin_tosses, trasition_mat, emissions):
    # Making emissions a matrix. 
    emission_mat = np.zeros(shape=(len(emissions),len(emissions)))
    for coin, emission_probability in enumerate(emissions):
        emission_mat[HEADS,coin] = 1 - emission_probability
        emission_mat[TAILS,coin] = emission_probability

    # The ith row and jth column represents the ith hidden state (node) and the jth element of the input. 

    # num_hidden_states is nodes in hidden markov model.
    num_hidden_states = emission_mat.shape[1]
    len_coin_tosses = len(coin_tosses)

    transition_probabilities = np.zeros(shape=(num_hidden_states, len_coin_tosses))
    transition_path = np.zeros(shape=(num_hidden_states, len_coin_tosses))
    indices = np.zeros(len_coin_tosses, dtype=int)

    #transition_probabilities[0,0] = 1
    #indices[0] = 0

    # Equalizes init probability
    for idx in range(0,num_hidden_states):
        transition_probabilities[idx,0] = emission_mat[coin_tosses[0],idx]

    print(emission_mat)

    for idx in range(1, len_coin_tosses):
        for state in range(num_hidden_states):
            emission_prob = emission_mat[coin_tosses[idx], state]

            prob_max = trasition_mat[state, 0] * emission_prob * transition_probabilities[0, idx-1] 
            prob_max_idx = 0

            for state_prev in range(1,num_hidden_states):
                prob = trasition_mat[state, state_prev] * emission_prob * transition_probabilities[state_prev, idx-1] 
            
                if prob > prob_max:
                    prob_max = prob
                    prob_max_idx = state_prev
                    
            transition_probabilities[state, idx] = prob_max 
            transition_path[state,idx] = prob_max_idx
        #indices[idx] = prob_max_idx


    # Finding highest probability of the last element in the input (column).
    opt_prob = transition_probabilities[0,len_coin_tosses-1]
    opt_idx = 0
    for state in range(1,num_hidden_states):
        if transition_probabilities[state,len_coin_tosses-1] > opt_prob:
            opt_prob = transition_probabilities[state,len_coin_tosses-1]
            opt_idx = state
    opt_prev = opt_idx
    indices[len_coin_tosses-1] = opt_prev

    # Uses the path to trace how we got there
    for idx in range(len_coin_tosses-1,0,-1):
        opt_prev = int(transition_path[opt_prev,idx])
        indices[idx-1] = opt_prev

    print('Most probable state sequence:', indices)
    print('Transition probabilities:\n', transition_probabilities.T)
