"""
This script illustrates a Maze Life-like cellular automaton evolution
in an animated gif

Maze Life-like cellular automaton Rules:
 1.
 Any live cell with fewer than one live neighbours
 dies, as if caused by under-population.
 2.
 Any live cell with two, three, four, five live neighbours lives
 on to the next generation.
 3.
 Any live cell with more than six live neighbours
 dies, as if by over-population.
 4.
 Any dead cell with exactly three live neighbours be-
 comes a live cell, as if by reproduction.
 """

import numpy as np
import random as rd
from PIL import Image
import imageio

def draw_fpentamino(on_grid:np.ndarray,offset:int) -> np.ndarray:
    """
     draws an fpentamino on the grid, at a given offset
    """
    on_grid[4+offset,4+offset] = 1
    on_grid[4+offset,5+offset] = 1
    on_grid[5+offset,3+offset] = 1
    on_grid[5+offset,4+offset] = 1
    on_grid[6+offset,4+offset] = 1

def count_alive_neighbours(on_grid:np.ndarray,size:int,i:int,j:int) -> int:
    """
    counts alive neighbours for current cell at i,j on the current grid
    can_count is an array determining if it makes sense to count that neighbour as alive,
    based on the current examine cell index on the grid
    alive_neighbours is the number of alive_neighbours for the current cell
    """

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

    alive_neighbours = 0
    for k in range(len(can_count)):
        if can_count[k] == 1:   
            # can go there and check
            k_i,k_j = can_count_idx[k]
            if on_grid[k_i,k_j] == 1:
                alive_neighbours += 1
        
    return alive_neighbours


def next_generation(on_grid:np.ndarray, size:int) -> np.ndarray:      
    """
    computes the next generation of cells on the grid
    with Maze Life-like cellular automaton Rules
    
    on_grid is the grid on which the computation will be run
    next_grid is the grid as a result of applying the rules
    """
    
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



def add_grid_to_image_list(grid:np.ndarray,image_list:list) -> list :
    """
    outputs the current grid status to an image, to be added to
    image_list to produce an animated gif
    """
    img_grid = grid.copy()
    img_grid[img_grid==0] = 255
    img_grid[img_grid==1] = 0
    im = Image.fromarray(img_grid)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    image_list.append(im)



def main():
    """
    run the algorithm on a 200x200 grid, initialized with an f-pentamino
    """
    size=200
    n_gen = 200
    grid = np.zeros(shape=(size,size))

    draw_fpentamino(grid,100)

    next_gen= next_generation(grid,size)
    images = []
    add_grid_to_image_list(next_gen,images)

    for i in range(n_gen-1):
        next_gen = next_generation(next_gen,size)
        add_grid_to_image_list(next_gen,images)

    imageio.mimsave('maze.gif', images)

if __name__ == '__main__':
    main()

