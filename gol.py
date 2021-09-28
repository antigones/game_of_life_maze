import numpy as np
import random as rd

def draw_fpentamino(on_grid):
    on_grid[4,4] = 1
    on_grid[4,5] = 1
    on_grid[5,3] = 1
    on_grid[5,4] = 1
    on_grid[6,4] = 1

def count_alive_neighbours(on_grid,size,i,j):
    # n,nw,w,sw,s,se,e,ne
    # 0,1 ,2, 3,4, 5,6,7
    can_count = [
        1, #n
        1, #nw
        1, #w
        1, #sw
        1, #s
        1, #se
        1, #e
        1, #ne
        ]
    can_count_idx = [
        (i-1,j), #n
        (i-1,j-1), # nw
        (i,j-1), # w
        (i+1,j-1),# sw
        (i+1,j), # s
        (i+1,j+1),# se
        (i,j+1), # e
        (i-1,j+1) # ne
    ]
    
    if i == 0:
        # first row in the grid
        can_count[0] = 0
        can_count[1] = 0
        can_count[7] = 0
    
    if j == 0:
        # first column
        can_count[1] = 0
        can_count[2] = 0
        can_count[3] = 0

    if i == size-1:
        # last row
        can_count[3] = 0
        can_count[4] = 0
        can_count[5] = 0

    if j == size-1:
        #last column
        can_count[5] = 0
        can_count[6] = 0
        can_count[7] = 0

    c = 0
    for k in range(len(can_count)):
        if can_count[k] == 1:   
            # can go there and check
            k_i,k_j = can_count_idx[k]
            if on_grid[k_i,k_j] == 1:
                c += 1
        
    return c


def next_generation(on_grid, size):
    next_grid = np.zeros(shape=(size,size))
    for (i,j) in [(i,j) for i in range(size) for j in range(size)]:
        alive_n = count_alive_neighbours(on_grid,size,i,j)
        #if i in [4,5,6]:
        
        cur_cell = on_grid[i,j]
        if cur_cell == 1:
            if alive_n < 2:
                next_grid[i,j] = 0
            if alive_n > 3:
                next_grid[i,j] = 0
            if alive_n ==  2 or alive_n == 3:
                next_grid[i,j] = 1
        else:
            if cur_cell == 0:
                if alive_n == 3:
                    # current cell come alive
                    next_grid[i,j] = 1
            else:
                next_grid[i,j] = 0
        #print(str(i)+" "+str(j)+": "+str(alive_n)+" - "+str(on_grid[i,j])+"->"+str(next_grid[i,j]))
    return next_grid

def post_process(grid):
    p_grid = grid.copy()
    p_grid[p_grid == '1'] = '@'
    return p_grid

size=10
n_gen = 4
grid = np.zeros(shape=(size,size))

draw_fpentamino(grid)
print('starting grid')
print(grid)

o = next_generation(grid,size)
print('first gen')
print(o)

for i in range(n_gen-1):
    o = next_generation(o,size)
    print(str(i)+" gen")
    print(o)
#print(grid)
