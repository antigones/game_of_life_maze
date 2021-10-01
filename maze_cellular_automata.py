import numpy as np
import random as rd
from PIL import Image
import imageio

def draw_fpentamino(on_grid:np.ndarray,offset:int) -> np.ndarray:
    # draws an fpentamino on the grid, at a given offset
    on_grid[4+offset,4+offset] = 1
    on_grid[4+offset,5+offset] = 1
    on_grid[5+offset,3+offset] = 1
    on_grid[5+offset,4+offset] = 1
    on_grid[6+offset,4+offset] = 1

def count_alive_neighbours(on_grid:np.ndarray,size:int,i:int,j:int) -> int:
    # counts alive neighbours for cell at i,j on the current grid

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


def next_generation(on_grid:np.ndarray, size:int) -> np.ndarray:
    # compute the next generation on the grid
    
    next_grid = np.zeros(shape=(size,size))
    for (i,j) in [(i,j) for i in range(size) for j in range(size)]:
        alive_n = count_alive_neighbours(on_grid,size,i,j)
        
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
    return next_grid


images = []
def to_image(grid:np.ndarray) -> list :
    img_grid = grid.copy()
    img_grid[img_grid==0] = 255
    img_grid[img_grid==1] = 0
    im = Image.fromarray(img_grid)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    images.append(im)



def main():
    size=200
    n_gen = 200
    grid = np.zeros(shape=(size,size))

    draw_fpentamino(grid,100)

    next_gen= next_generation(grid,size)

    to_image(next_gen)

    for i in range(n_gen-1):
        next_gen = next_generation(next_gen,size)
        to_image(next_generation(next_gen,size))

    imageio.mimsave('maze.gif', images)

if __name__ == '__main__':
    main()

