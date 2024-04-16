import numpy as np
from itertools import combinations
import time


# specific example
x_axis , y_axis = 5,5
grid = np.array([[9,2,9,9,9],
                 [9,9,2,9,2],
                 [9,3,3,9,9],
                 [1,9,2,2,2],
                 [9,1,1,1,9]])
not_9_indices = np.where(grid != 9)
list_number = list(zip(not_9_indices[0], not_9_indices[1]))

queue=[]
for x,y in list_number:
    check_p = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
    for i,j in check_p[:]:
        a,b=x+i,y+j
        if a in range(0,x_axis) and b in range(0,y_axis):
            if grid[a,b] in range(0,9):
                check_p.remove((i,j))
        else: check_p.remove((i,j))
    queue.append((x,y,check_p))
print(queue)
def removearray(L,arr):
    ind = 0
    size = len(L)
    while ind != size and not np.array_equal(L[ind],arr):
        ind += 1
    if ind != size:
        L.pop(ind)
################################
steps=[]
grid_list = [grid]
pass_point =[]
start_time = time.time()
for x,y,p in queue:
    case_mine = list(combinations(p,grid[x][y]))
    new_g_lst = []
    pass_point.append((x,y,p))
    for g in grid_list:
        for case in case_mine:
            gs = g.copy()
            for i,j in case:
                a,b = x+i,y+j
                gs[a][b]=-1
            new_g_lst.append(gs)
    s_g = new_g_lst.copy()
    steps.append(("open",(x,y),s_g))
    for g in new_g_lst[:]:
        for x ,y, p in pass_point:
            count=0
            for i,j in p:
                a,b=x+i,y+j
                if g[a][b] == -1:
                    count+=1
            if count != g[x][y]:
                removearray(new_g_lst,g)
                s_g = new_g_lst.copy()
                steps.append(("remove",(x,y),s_g))
                break
    grid_list=new_g_lst
end_time=time.time()
print(grid_list[0])
print(end_time-start_time)
def navigate_list(lst):
    current_position = 0
    while True:
        state , square , g_lst = lst[current_position]
        print(state)
        print(square)
        for g in g_lst:
            print(g)
        user_input = input("Press 'a' to go backward, 'd' to go forward, or 'q' to quit: ").lower()
        if user_input == 'a':
            current_position = max(0, current_position - 1)
        elif user_input == 'd':
            current_position = min(len(lst) - 1, current_position + 1)
        elif user_input == 'q':
            print("Exiting program.")
            break
        else:
            print("Invalid input. Please enter 'a', 'd', or 'q'.")

navigate_list(steps)