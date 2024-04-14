import numpy as np
import time

x_axis = 20
y_axis = 20
mines_number = 50
get_mines_randomly_2d = 0

## random grid 
grid = np.full((y_axis, x_axis), 9,dtype=int)
get_mines_randomly = np.random.choice(grid.size, mines_number, replace=False)
get_mines_randomly_2d = np.unravel_index(get_mines_randomly, grid.shape)
grid[get_mines_randomly_2d] = -1


x ,y = None, None
while True:
    x, y = np.random.randint(0, x_axis), np.random.randint(0, y_axis)
    if grid[x, y] == 9:
        grid[x, y] = 0
        break
get_mines_randomly_2d = np.transpose(get_mines_randomly_2d).tolist()
un_tough_lst = [(x,y) for x in range(x_axis) for y in range(y_axis)]
un_tough_lst.remove((x,y))

# # specific example
# get_mines_randomly_2d= [(3, 1), (3, 5), (3, 6), (4, 0), (2, 4), (3, 4), (2, 7), (4, 1), (7, 7), (5, 6)]
# un_tough_lst = [(x,y) for x in range(x_axis) for y in range(y_axis)]
# x,y = 5,3
# un_tough_lst.remove((x,y))
# grid = np.array([[9, 9, 9, 9, 9, 9, 9, 9],
#                  [9, 9, 9, 9, 9, 9, 9, 9],
#                  [9, 9, 9, 9, -1, 9, 9, -1],
#                  [9, -1, 9, 9, -1, -1, -1, 9],
#                  [-1, -1, 9, 9, 9, 9, 9, 9],
#                  [9, 9, 9, 0, 9, 9, -1, 9],
#                  [9, 9, 9, 9, 9, 9, 9, 9],
#                  [9, 9, 9, 9, 9, 9, 9, -1]])
# ################################

def spread(x,y,grid,queue,around = []):
    for i,j in around:
        a,b = x+i,y+j
        if grid[a][b] == 9:
            check_around(a,b,grid,queue)
            
def check_around(x,y,grid,queue):
    if not grid[x][y] == -1:
        count = 0
        check_p = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
        for i,j in check_p[:]:
            a,b = x+i,y+j
            if a in range(0,x_axis) and b in range(0,y_axis):
                if grid[a,b] == -1:
                    count += 1
                elif grid[a,b] in range(0,9):
                    check_p.remove((i,j))
            else: 
                check_p.remove((i,j))
        if count == 0:
            grid[x][y] = 0
            spread(x,y,grid, queue,check_p)
            if (x,y) in un_tough_lst:
                un_tough_lst.remove((x,y))
        else:
            grid[x][y] = count
            if [x,y] in un_tough_lst:
                un_tough_lst.remove((x,y))
            queue.append([x,y,check_p])
    return queue ,grid
    
mine_found = []
# possibly_chose_positions = []
def shorten_queue(new_queue,queue= []):
    for x ,y, ar in new_queue:
        for i,j in ar:
            a ,b= x + i,y + j
            if grid[a][b] not in range(0,9):
                if (a,b) not in queue and (a,b) not in mine_found:
                    queue.append((a,b))
    return queue

# BFS form here try test evey possibly choose
queue, grid = check_around(x,y,grid,[])
queue = shorten_queue(queue)
bfs_step_list = [[(x,y),True,grid]]
step_to_win = [(x,y)]
timer = 0.0

# bfs go here 
def bfs(queue, grid = grid ):
    start_time = time.time()
    for x,y in queue:
        g = grid.copy()
        if (x,y) in un_tough_lst:
            un_tough_lst.remove((x,y))
            if grid[x][y] == -1:
                bfs_step_list.append([(x,y),False,g])
                mine_found.append((x,y))
            else:
                new_queue, grid = check_around(x,y,g,[])
                new_queue = shorten_queue(new_queue ,queue)
                bfs_step_list.append([(x,y),True,g])
                step_to_win.append((x,y))
    end_time = time.time()
    return end_time - start_time

timer+=bfs(queue)     
            
while len(mine_found) < mines_number:
    if un_tough_lst:
        x,y = un_tough_lst[0]
        un_tough_lst.remove((x,y))
        queue, grid = check_around(x,y,grid,[])
        queue = shorten_queue(queue)
        timer+=bfs(queue)
    else:
        print("HOW IT CAN HAPPEN ???")


def navigate_list(lst):
    current_position = 0
    while True:
        square, k, grid = bfs_step_list[current_position]
        print("Chosen square: " + str(square))
        if k:
            print('Not step on the mine!')
        else: print('Step on mine!!! DEAD!!')
        print(grid)
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

# print step
print('Time to win: ' + str(timer))
print('Step to win:' + str(step_to_win))
print(len(mine_found))
navigate_list(bfs_step_list)






