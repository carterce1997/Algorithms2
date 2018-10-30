import numpy as np

def compute_transitions(input_str, trasition_mat, emissions):

    emission_mat = np.zeros(shape=(len(emissions),len(emissions)))
    for j, emission_probability in enumerate(emissions):
        emission_mat[0,j] = emission_probability
        emission_mat[1,j] = 1 - emission_probability

    num_hidden_states = emission_mat.shape[1]
    len_input_str = len(input_str)

    transition_probabilities = np.zeros(shape=(num_hidden_states,len_input_str+1))
    indices = np.zeros(len_input_str+1, dtype=int)

    transition_probabilities[0,0] = 1
    indices[0] = 0

    # Equalizes init probability
    #for i in range(0,rows):
    #    transitions[i,0] = emission_mat[input_str[0],i] * (1.0/float(rows))

    print(emission_mat)

    for idx in range(1, len_input_str):
        prob_max = 0
        prob_max_idx = 0

        for state in range(num_hidden_states):

            emission_prob = emission_mat[input_str[idx], state]
            transition_prob = trasition_mat[state, indices[idx-1]]
            prob = transition_prob * emission_prob 
            
            if prob > prob_max:
                prob_max = prob
                prob_max_idx = state 
            transition_probabilities[state, idx] = prob
        indices[idx] = prob_max_idx

    print('Most probable state sequence:', indices)
    print('Transition probabilities:\n', transition_probabilities.T)
