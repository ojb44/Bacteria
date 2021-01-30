"""
Created on Sat Jan 30 18:51:24 2021

Author: OllieBreach

Description:
"""

import numpy as np
import matplotlib.pyplot as plt

size=50
kappa=1
epsilon=0.1

r=0.2
R0=0.5
delta=0.1

cr=(R0-delta-0.05)/(kappa*size)
cnr=R0/(kappa*size)
    
class Board:
        
        def __init__(self, grid_size):
            self.size=grid_size
            self.grid=self.init_board(grid_size)
            self.num_updates=0
            
        def init_board(self, grid_size):
            initial_bacteria = np.random.choice((1,2),p=[1-epsilon,epsilon] , size=(1,grid_size))
            zeros=np.zeros((grid_size-1, grid_size))
            initial_grid=np.concatenate((initial_bacteria, zeros), axis=0)
            return initial_grid
                
        def display_board(self):
            plt.axis("off")
            plt.imshow(self.grid, cmap="Greys")
            
        def neighbours(self, pos):
            i,j = pos
            all_neighbs=[((i-1),j),(i,(j+1)),((i+1),j),(i,(j-1))]
            proper_neighbs=[]
            for n in all_neighbs:
                if n[0]>=0 and n[0]<self.size and n[1]>=0 and n[1]<self.size:
                    proper_neighbs.append(n)
            return proper_neighbs
        
        def get_value(self, pos):
            i,j=pos
            return self.grid[i][j]
            
        def set_value(self, pos, val):
            i,j=pos
            self.grid[i][j]=val
            
        def res_update(self, pos):
            neighbs=self.neighbours(pos)
            num_offspring=0
            
            for neighb in neighbs:
                if self.get_value(neighb)==0 and num_offspring==0: #reproduce
                    if np.random.random()<R0-delta-cr*kappa*pos[0]:
                        self.set_value(neighb, 2)
                elif self.get_value(neighb)==1: #infect
                    if np.random.random()<r:
                        self.set_value(neighb, 2)
                        
        def nonres_update(self, pos):
            neighbs=self.neighbours(pos)
            num_offspring=0
            for neighb in neighbs:
                if self.get_value(neighb)==0 and num_offspring==0:
                    if np.random.random()<R0-cnr*kappa*pos[0]:
                        self.set_value(neighb, 1)
                        
        def grid_update(self, start=0):
            self.num_updates+=1
            occupied=[]
            for i in range(start, self.size):
                for j in range(self.size):
                    if self.get_value((i,j))!=0:
                        occupied.append((i,j))
            for pos in occupied:
                if self.get_value(pos)==1:
                    self.nonres_update(pos)
                else:
                    self.res_update(pos)
            
            if self.reached_end():
                print('Reached end in ', self.num_updates, ' steps')
                
        def reached_end(self):
            if np.sum(self.grid[self.size-1])!=0:
                return True
            else:
                return False
                    
        def update_display(self):
            self.grid_update()
            self.display_board()
            
        def n_updates(self, num):
            count=0
            while count<num:
                self.grid_update(int(count*0.1))
                count+=1
                
        def proportion_res(self):
            num_bacteria=np.count_nonzero(self.grid)
            num_res=np.count_nonzero(self.grid==2)
            return num_res/num_bacteria
                
        def update_til_end(self):
            while self.reached_end()==False:
                self.grid_update()
            return self.num_updates
                    
board=Board(size)

# rs=np.arange(0,1,0.1)
# time_for_rs=[]

# for val in rs:
#     r=val
#     board=Board(size)
#     time_for_rs.append(board.update_til_end())
  
    
# r=0.5


# R0s=np.arange(0.1,1,0.1)
# time_for_R0s=[]

# for val in R0s:
#     print(val)
#     board=Board(size)
#     R0=val
#     cr=(R0-delta-0.05)/(kappa*size)
#     cnr=R0/(kappa*size)
#     time_for_R0s.append(board.update_til_end())
    

# R0=1

# epsilons=np.arange(0.1,1,0.1)
# time_for_epsilons=[]

# for val in epsilons:
#     print(val)
#     epsilon=val
#     board=Board(size)
#     cr=(R0-delta-0.05)/(kappa*size)
#     cnr=R0/(kappa*size)
#     time_for_epsilons.append(board.update_til_end())


proportions=[]
while board.reached_end()==False:
    board.grid_update()
    proportions.append(board.proportion_res())







