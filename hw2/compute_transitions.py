import numpy

def compute_transitions(input_str, trasition_mat, emissions):

    emission_mat = numpy.zeros(shape=(len(emissions),len(emissions)))
    for j in range(len(emissions)):
        emission_mat[0,j] = emissions[j]
        emission_mat[1,j] = 1 - emissions[j] 

    rows = len(emission_mat)
    cols = len(input_str)

    transitions = numpy.zeros(shape=(rows,cols+1))
    indices = numpy.zeros(shape=(rows,cols+1),dtype=int)

    transitions[1,0] = 1
    indices[:,0] = 1

    # Equalizes init probability
    #for i in range(0,rows):
    #    transitions[i,0] = emission_mat[input_str[0],i] * (1.0/float(rows))

    print(emission_mat)

    for x in range(1,cols):
        prob_max = 0
        prob_max_idx = 0

        for y in range(0,rows):

            emission_prob = emission_mat[input_str[x],y]
            transition_prob = trasition_mat[y,indices[0,x-1]]
            prob = transition_prob * emission_prob 
            
            #transitions[0,x-1] *

            #prob =  trasition_mat[indices[0,x-1],y] * emission_prob #transitions[0,x-1] *
            #for y2 in range(1,rows):
            #    prob = trasition_mat[y2,y] * emission_prob #transitions[y2,x-1] *
            if prob > prob_max:
                prob_max = prob
                prob_max_idx = y
            transitions[y,x] = prob
        indices[:,x] = prob_max_idx

    print(indices)
    print(transitions)
    print('\n')
    print('Most probable state sequence')
    #print(p)

    prob_max = transitions[0,cols-1]
    prob_max_idx = 0
    for y in range(1,rows):
        if transitions[y,cols-1] > prob_max:
            prob_max = transitions[y,cols-1]
            prob_max_idx = y

    p = [prob_max_idx]
    for x in range(cols-1,0,-1):
        prob_max_idx = indices[int(prob_max_idx),x]
        p.append(int(prob_max_idx))
