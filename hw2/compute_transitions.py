import numpy

def compute_transitions(input_str, trasition_mat, emission_mat):

    rows = len(input_str)
    cols = len(emission_mat)

    transitions = numpy.zeros(shape=(rows,cols))
    transitions_indices = numpy.zeros(shape=(rows,cols))

    transitions[0,0] = emission_mat[1,input_str[0]] * 0.5
    transitions[1,0] = emission_mat[0,input_str[0]] * 0.5

    for x in range(1,rows):
        for y in range(0,cols):
            emission_prob = emission_mat[y,input_str[x]]
            prob_min = transitions[0,x-1] * trasition_mat[0,x] * emission_prob
            prob_min_idx = 0
            for y2 in range(0,cols):
                prob = transitions[y2,x-1] * trasition_mat[y2,x] * emission_prob
                if prob > prob_min:
                    prob_min = prob
                    prob_min_idx = y2
            transitions[x,y] = prob_min
            transitions_indices[x,y] = prob_min_idx

    print(transitions)

