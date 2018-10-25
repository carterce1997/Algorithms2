def state_sequence(input_str, trasition_mat, emission_mat):

    rows = len(emission_mat)
    cols = len(input_str)

    transitions = numpy.zeros(shape=(rows,cols))
    transitions_indices = numpy.zeros(shape=(rows,cols))

    transitions[0,0] = emission_mat[1,input_str[0]] * 0.5
    transitions[1,0] = emission_mat[0,input_str[0]] * 0.5

    for y in range(1,rows):
        for x in range(0,2):
            emission_prob = emission_mat[x,input_str[y]]
            prob_min = transitions[0,y-1] * trasition_mat[0,y] * emission_prob
            prob_min_idx = 0
            for x2 in range(0,2):
                prob = transitions[x2,y-1] * trasition_mat[x2,x] * emission_prob
                if prob > prob_min:
                    prob_min = probv
                    prob_min_idx = x2
            transitions[x,y] = prob_min
            transitions_indices[x,y] = prob_min_idx



