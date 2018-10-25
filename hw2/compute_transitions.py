import numpy

def compute_transitions(input_str, trasition_mat, emissions):


    emission_mat = numpy.zeros(shape=(len(emissions),len(emissions)))
    for j in range(len(emissions)):
        emission_mat[0,j] = emissions[j]
        emission_mat[1,j] = 1 - emissions[j] 

    rows = len(emission_mat)
    cols = len(input_str)

    transitions = numpy.zeros(shape=(rows,cols))
    transitions_indices = numpy.zeros(shape=(rows,cols))

    transitions[0,0] = 1

    #for i in range(0,rows):
    #    transitions[i,0] = emission_mat[input_str[0],i] * (1.0/float(rows))

    for x in range(1,cols):
        for y in range(0,rows):
            emission_prob = emission_mat[input_str[x],y]
            prob_max = transitions[0,x-1] * trasition_mat[0,y] * emission_prob
            prob_max_idx = 0
            for y2 in range(1,rows):
                prob = transitions[y2,x-1] * trasition_mat[y2,y] * emission_prob
                if prob > prob_max:
                    prob_max = prob
                    prob_max_idx = y2
            transitions[y,x] = prob_max
            transitions_indices[y,x] = prob_max_idx

    prob_max = transitions[0,cols-1]
    prob_max_idx = 0
    for y in range(1,rows):
        if transitions[y,cols-1] > prob_max:
            prob_max = transitions[y,cols-1]
            prob_max_idx = y

    p = [prob_max_idx]
    for x in range(cols-1,0,-1):
        prob_max_idx = transitions_indices[int(prob_max_idx),x]
        p.append(int(prob_max_idx))

    print('\n')
    print('Most probable state sequence')
    print(p)

    

