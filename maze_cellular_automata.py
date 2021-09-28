import numpy as np
import random as rd
from PIL import Image
import imageio

def draw_fpentamino(on_grid,start):
    on_grid[4+start,4+start] = 1
    on_grid[4+start,5+start] = 1
    on_grid[5+start,3+start] = 1
    on_grid[5+start,4+start] = 1
    on_grid[6+start,4+start] = 1

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
            if alive_n < 1:
                next_grid[i,j] = 0
            elif alive_n > 6:
                next_grid[i,j] = 0
            else:
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

def to_console(grid):
    #g = grid.astype(dtype=str)
    g = grid.copy()
    g = g.astype(dtype=str)
    g[g=='1.0'] = '#'
    g[g=='0.0'] = ' '
    for elm in g:
        print(" ".join(elm))

images = []
def to_image(grid):
    img_grid = grid.copy()
    #print('img_grid')
    #print(img_grid)
    img_grid[img_grid==0] = 255
    img_grid[img_grid==1] = 0
    im = Image.fromarray(img_grid)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    images.append(im)
    #im.save('test.png')

size=100
n_gen = 300
grid = np.zeros(shape=(size,size))

draw_fpentamino(grid,50)
print('starting grid')
print(grid)

o = next_generation(grid,size)
#to_console(o)
to_image(o)
#print("---")
for i in range(n_gen-1):
    o = next_generation(o,size)
    #to_console(o)
    to_image(o)
    print(str(i))
imageio.mimsave('maze.gif', images)
#print(grid)
