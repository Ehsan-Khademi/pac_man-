
# librareis
import numpy as np
import random


# -------------------------------------------------------input Demo that i have wrte on to the file by manual method-----------

# f=open("demofile.txt","a")
# f.close()
# f=open("demofile.txt","r+")
# f.truncate(0)


# f.write('6,10\n')
# f.write('3,2\n')
# f.write('')
# f.write('**********\n')
# f.write('*--------*\n')
# f.write('*--***---*\n')
# f.write('*-a---f--*\n')
# f.write('*-*--*---*\n')
# f.write('**********')




# input real
# f=open("demofile.txt","r+")
from pacman import PacManTest

# ----------------------------------------------------------->create RANDOM_MAP

def generate_map(m, n):
    # ----------------------Define characters for terrain and objects
    terrain_chars = ['-', '*']
    object_chars = ['a', 'f']

    # ----------------------Generate empty map
    map_data = [['-' for _ in range(n)] for _ in range(m)]

    # ----------------------Place walls around the perimeter
    for i in range(m):
        for j in range(n):
            if i == 0 or i == m - 1 or j == 0 or j == n - 1:
                map_data[i][j] = '*'

    # ----------------------Place random walls within the houses
    for i in range(1, m - 1):
        for j in range(1, n - 1):
            if map_data[i][j] == '-':
                if random.random() < 0.2:  # Adjust the probability as needed
                    map_data[i][j] = '*'

    # -----------------------Place objects on the map
    for char in object_chars:
        while True:
            row = random.randint(1, m - 2)
            col = random.randint(1, n - 2)
            if map_data[row][col] == '-':
                map_data[row][col] = char
                break

    return map_data
    # -----------------find positions of current_agent_position'
def find_character_position(map_data, character):
    for i, row in enumerate(map_data):
        for j, char in enumerate(row):
            if char == character:
                return i, j
    return None, None
f=open("demofile.txt","a")
f.truncate(0)
f.close()
def write_map_to_file(map_data, filename):
    with open(filename, "r+") as f:
        f.write(f'{len(map_data)},{len(map_data[0])}\n')
        a_row,a_col = find_character_position(map_data,'a')
        f.write(f'{a_row},{a_col}\n')
        f.write('\n')
        count=0
        for row in map_data:
            count+=1
            if count!=len(map_data):
              f.write(''.join(row) + '\n')
            else:
              f.write(''.join(row))
            # f.write(''.join(row) + '\n')

# Example usage:
print("now you can create random map by m and n that you enter them as size of map(m*n):\n")
print("--> enter the m(max_num of rows):")
m = input()
print("-->enter the n(max_num of cols):")
n = input()
m=int(m)
n=int(n)
map_data = generate_map(m, n)
write_map_to_file(map_data, "demofile.txt")
f.close()

# ------------------------------------------------>REDING DATA FROM FILE
Temporary_list=[]
new=[]
original_list=[]
f=open("demofile.txt","r+")
def reading_map_from_file(f,Temporary_list,new,original_list):
  f.seek(0)
  m,n=(f.readline()).split(',')
  a,b=(f.readline()).split(',')
  f.seek(f.tell()+1)
  Temporary_list=f.readlines()
  m=int(m)
  n=int(n)
  a=int(a)
  b=int(b)
  count=0
  for line in Temporary_list:
      if count == 0:
          count += 1
          continue
      original_list.append(list(line.replace('\n','')))
  return m,n,a,b
# ----------------------------------------
m,n,a,b=reading_map_from_file(f,Temporary_list,new,original_list)
# print(original_list)
f.close()

# Global percept
# status: empty(-) or block(*) or food(*)
# -------------------------------------------->the shortest path
path=[]
percept=[]
statusPos=[]
# ----------------------->declare historyOfPercept
historyOfPercepts=[]
# start_position-----> [a,b]
statusPos.append(a)
statusPos.append(b)
# ---------------------->perept[] declare and  initialize
status_shortest_Pos=[]
percept.append(a)
percept.append(b)
percept.append('-')
historyOfPercepts.append(percept)

# -------------------->declare action
actions=[]
# ------------------------------------
combine=[]
count_short=[]
# ---------------------------------------
# print(statusPos)

# percept=[x_pos,y_pos,status]
# ---------------------->this function is for block status and is private access
def setblockstatus(actions):
  randomActions=0
  if actions[-1]==1 or actions[-1]==3:
     if(actions[-1]==1):
      randomActions=3
     else:
      randomActions=1
  else:
       if actions[-1]==2:
         randomActions=4
       else:
         randomActions=2
  return randomActions

# ------------------------------------------------>the Agent function
def agent(percept):
  randomAction=0
  if percept[2]=='a':
     percept[2]='-'
  if percept[2]=='f':
    return 20  #---------------------------->this number is my random selected numer that i selecte so we can set each all number or string or character choosed for this
  elif percept[2]=='*':
    randomAction=setblockstatus(actions)
  else:
    randomAction=random.randint(1,4)
  actions.append(randomAction)
  return randomAction

# action :1-> up | 3-> down  |   4-> left  |  2-> right
# Enviroment
def setStatusPosition(action):
  x=statusPos[0]
  y=statusPos[1]
  if action==1:
    statusPos[0]=x-1
  elif action==3:
    statusPos[0]=x+1
  elif action==2:
    statusPos[1]=y+1
  elif action==4:
    statusPos[1]=y-1

# -------------------------------------the enviroment funciton--------------

def enviroment(action):
  setStatusPosition(action)
  current_situation=original_list[statusPos[0]][statusPos[1]]
  current_percept=[statusPos[0],statusPos[1],current_situation]
  historyOfPercepts.append(current_percept)
  return current_percept

# section one: in this sections the agent find path  by the way in partial obsarvable

# -----------------------declare output_List in standard form

def combine_actions_and_percepts():
  path_with_location=[]
  location=()
  for i in range(len(historyOfPercepts)):
    location=(historyOfPercepts[i][0],historyOfPercepts[i][1])
    path_with_location.append(location)
    if i<=len(historyOfPercepts)-2:
      path_with_location.append(actions[i])
  return path_with_location


def find_food_path():
    act=agent(percept)
    while(act!=20):
      per_cept=enviroment(act)
      act=agent(per_cept)
    # print(historyOfPercepts)
    # print(actions)
    return combine_actions_and_percepts()

def count_number_of_Step(actions):
     return len(actions)-1

# /---------------------------------------IDS searching method to solve problem----------------------------
# hint:
def get_neighbors(node, map):
    neighbors = []
    row, col = node
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(map) and 0 <= new_col < len(map[0]) and map[new_row][new_col] != '*':
            neighbors.append((new_row, new_col))
    return neighbors

def dls_shortest_path(map, start, goal, depth):
    if start == goal:
        return [start]
    if depth == 0:
        return None
    for neighbor in get_neighbors(start, map):
        result = dls_shortest_path(map, neighbor, goal, depth - 1)
        if result is not None:
            return [start] + result
    return None

def ids_shortest_path(map, start, goal):
    depth = 0
    while True:
        result = dls_shortest_path(map, start, goal, depth)
        if result is not None:
            return result
        depth += 1
# ------------------------------------------>Considering that the agent has traveled the path and finally reached the food،
#                                                                                  it has saved its starting and ending position in the list of its perceptions

def find_start_and_goal(map):
    find_pos=[]
    find_pos.extend(combine_actions_and_percepts())
    start=find_pos[0]#location of start(agent)
    goal=find_pos[len(find_pos)-1]#location of Foo(goal)
    return start, goal



def update_map_with_path(map, path):
    for i in range(len(path)):
      row, col = path[i]
      if i==len(path)-1:
        map[row][col]='f'
      else:
        map[row][col]='-'
    return map

# ------------------------------------
def initialize(map):
  for i in range(1,len(map)-1):
    for j in range(1,len(map[i])-1):
      map[i][j]='?'
  return map

# ------------->print map With the ability have memory
def print_map(map):
    for row in map:
        print(''.join(row))


def apply_sequence_of_movements(map, sequence_of_movements,initialize_map,start):
    s=list(start)
    for move in sequence_of_movements:
        if map[s[0]][s[1]] == '-':
          initialize_map[s[0]][s[1]] = '-'
        elif map[s[0]][s[1]] == '*':
          initialize_map[s[0]][s[1]] = '*'
        elif map[s[0]][s[1]] == 'a':
          initialize_map[s[0]][s[1]] = '-'
        else:
          initialize_map[s[0]][s[1]] = 'f'
        change_pos(move,s)

    return initialize_map

def change_pos(move,current_location):
        if   move == 2:
            current_location[1]+=1
        elif move == 4:
            current_location[1]-=1
        elif move == 1:
            current_location[0]-=1
        else:
          current_location[0] +=1
        return current_location
# this folowing two methods print (optimal_path with action)/////////////////////////////

def the_shortest_path(path):
  str_P_N=""
  k=0
  sh_p=[]
  sh_p.extend(shortest_pathAction(path))
  for pointPosition in path:
    combine.append(pointPosition)
    if(k<len(path)-1):
      combine.append(sh_p[k])
      k+=1
    str_P_N+=str(pointPosition)+f'-->'
  # print(f"the number of step to find shortest path :\n{count_number_of_Step(path)}")
  count_short.append(count_number_of_Step(path))
  # print(f'the short path is :')
  #  {str_P_N[:len(str_P_N)-3]}
  # print(combine)


def shortest_pathAction(path):
  short_actions=[]
  for i in range(1,len(path)):
    if(path[i-1][0]==path[i][0]):
      if(path[i-1][1]>path[i][1]):
        short_actions.append(4)
      if(path[i-1][1]<path[i][1]):
        short_actions.append(2)

    if(path[i-1][1]==path[i][1]):
      if(path[i-1][0]>path[i][0]):
        short_actions.append(1)
      if(path[i-1][0]<path[i][0]):
        short_actions.append(3)
  return short_actions
# ///////////////////////////////////////////////////////////////////////////////////
update_out_put_map=[]
def operate(actions,original_listt,path):
    map =[[element for element in row] for row in original_list]
    start, goal = find_start_and_goal(map)
    # sequence_of_movements = [2,1,3,2,2,1,3,3,1,2]
    sequence_of_movements=actions
    initialize_map=[[element for element in row] for row in map]
    initialize_map=initialize(initialize_map)
    initialize_map = apply_sequence_of_movements(map, sequence_of_movements,initialize_map,start)
    path=ids_shortest_path(map, start, goal)

    if path:
        updated_map = update_map_with_path(initialize_map, path)
        update_out_put_map.append(updated_map)
        # print_map(updated_map)
    # else:
    # print("No path found.")#--------------in this program there is at least one path there fore this string do not have application
    the_shortest_path(path)

def get_start_or_end_location(element):
  for i in range(len(original_list)):
    for j in range(len(original_list[i])):
      if original_list[i][j]==element:
        return(i,j)

#-------------------------------------------------------> outPut
find_food=[]
find_food.append(find_food_path())

# print(f"Coordinates of the starting point :\n{get_start_or_end_location('a')}")
# print(f"The coordinates of the place of food :\n{get_start_or_end_location('f')}")
# print(f"the number of step to find path using 'bruth_forts' mehthod :\n{count_number_of_Step(actions)}")
# print(f"The list consists of the selected coordinate and motion pairs:\n{find_food} :")
# find_food_path()
operate(actions,original_list,path)
def write_out_put_Map_two_list(map):
    with open('output.txt', 'a') as file:
        file.truncate(0)
        file.seek(0)
        for sublist in map:
            file.write(''.join(sublist)+ '\n')

def main():                                                 #multi return
    # return get_start_or_end_location('a'),get_start_or_end_location('f'),count_number_of_Step(actions),find_food,count_short[0],combine        ------>this line is completer return
    return get_start_or_end_location('a'),get_start_or_end_location('f'),count_short[0],combine

# write into file that we suppose an agent have memory(بخش امتیازی)
write_out_put_Map_two_list(update_out_put_map[0])

if __name__ == "__main__":
     print(main())
     # a = PacManTest("test.txt",*main())
     # a.path()
     # a.compare_results()


