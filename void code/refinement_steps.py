python
import numpy as np
l,w=955,955
a=np.arange(l*w).reshape(l,w)
import math


def generate_refinement_steps(ar):
    smallest_dim = min(ar.shape[0],ar.shape[1])
    divide_size = 1
    while divide_size*2 < smallest_dim:
        divide_size *= 2
    print("divide_size: " + str(divide_size))
    done_matrix = np.zeros((ar.shape[0],ar.shape[1]))==1
    old_relevant_mask = None
    while divide_size >= 1:
        tentative_row_count = ar.shape[0]/divide_size
        tentative_col_count = ar.shape[1]/divide_size
        row_count = math.ceil(tentative_row_count)
        col_count = math.ceil(tentative_col_count)
        relevant_values = np.zeros((row_count,col_count))
        for row in range(row_count):
            for col in range(col_count):
                if not done_matrix[row*divide_size,col*divide_size]:
                    relevant_values[row,col] = ar[row*divide_size,col*divide_size]
                    done_matrix[row*divide_size,col*divide_size] = True
                else:
                    relevant_values[row,col] = old_values[int(row/2),int(col/2)]
        relevant_mask = np.zeros(ar.shape) == 1
        relevant_mask[0::divide_size,0::divide_size] = True
        base_mask = np.copy(relevant_mask)
        if old_relevant_mask is not None: relevant_mask[old_relevant_mask] = False
        yield relevant_values,divide_size,relevant_mask,base_mask
        old_values = np.copy(relevant_values)
        old_relevant_mask = np.copy(relevant_mask)
        divide_size = int(divide_size / 2)

for step in generate_refinement_steps(a):
    for part in step:
        print("\n"+str(part))

