import math
from heapq import *
import sys
import timeit
from puzzle import Puzzle

# vytvori zo stavu 2D tvar
# napriklad ak mame hlavolam 3x3: (1 2 3 4 5 6 7 8 0) stav prepise na tvar (1 2 3)(4 5 6)(7 8 0)
def get_2D_state(state):
    puzzle_2D = list()
    row = list()
    for idx, val in enumerate(state):
        row.append(val)
        if (idx + 1) % COLUMN == 0:
            puzzle_2D.append(row)
            row = list()
    return puzzle_2D

# algoritmus lacneho prehladavania
def greedy_search_algo(puzzle_board, COLUMN, ROW):
    start=puzzle_board.initial_state
    num=0
    start_time = timeit.default_timer()
    # na zaklade toho s akou heuristikou pracujeme vypocita hodnotu pre zaciatocny stav
    if heuristic_num==1:
        start.heuristic=puzzle_board.heuristic_misplaced_tiles(start.data, COLUMN, ROW)
    elif heuristic_num==2:
        start.heuristic=puzzle_board.heuristic_manhattan(start.data, COLUMN, ROW)
    # prioritna rada so stavmi ktore sme objavili a neboli este navstivene (to znamena neobjavili sme vsetkych susedov)
    heappush(puzzle_board.priority_queue, (start.heuristic, num, start))
    # visited bude obsahovat uz navstivene stavy, zabrani cyklickemu prehladavaniu rovnakych stavov
    visited=set()
    while len(puzzle_board.priority_queue):
        # vyberie z rady stav s najnizsou hodnotou vypocitanou heuristikou
        current = heappop(puzzle_board.priority_queue)[-1]
        new_data=list()
        for i in range(ROW):
            for j in range(COLUMN):
                new_data.append(current.data[i][j])
        visited.add(tuple(new_data))

        # ak heuristika vypocita pre nas stav hodnotu 0 dosiahli sme cielovy stav a vyjdeme z lacneho algoritmu
        if heuristic_num==1 and puzzle_board.heuristic_misplaced_tiles(current.data, COLUMN, ROW)==0:
            print("Succesfully reached the goal state.")
            found_goal=1
            break
        elif heuristic_num==2 and puzzle_board.heuristic_manhattan(current.data, COLUMN, ROW)==0:
            print("Succesfully reached the goal state.")
            found_goal=1
            break

        # vygeeruje vsetky stavy do ktorych sa vieme dostat
        children = current.generate_children(puzzle_board, COLUMN, ROW, heuristic_num)
        for child in children:
            data = list()
            for i in range(ROW):
                for j in range(COLUMN):
                    data.append(child.data[i][j])
            # skontroluje ci uz bol stav navstiveny
            if tuple(data) not in visited:
                num=num+1
                # prida stav do radu
                heappush(puzzle_board.priority_queue, (child.heuristic, num, child))
    if len(puzzle_board.priority_queue)==0:
        print("Given puzzle is unsolvable!")
        return
    end_time = timeit.default_timer()
    time = end_time - start_time
    print("TIME NEEDED TO SOLVE PUZZLE: "+ str(time)+"s")
    print("PROCESSED NODES: "+str(len(visited)))
    print("CREATED NODES: "+str(num))
    print("DEPTH:"+str(current.depth))
    moves=list()
    while current.parent != None:
        moves.append(current.move)
        current = current.parent
    moves.reverse()
    if moves is not None and len(moves)>0:
        print("PATH: ", end="")
        for i in range(len(moves)):
            print(moves[i],end=", ")
        print()
    else:
        print("Initial state is the same as goal state.")

    """puzzle_board.print_puzzles()"""


if __name__ == '__main__':
    input_file=input("Enter file you want to read puzzles from-> ")
    output_file=input("Enter file with solutions-> ")
    sys.stdout = open(output_file, "w")
    puzzle_num=0
    with open(input_file, "r") as f:
        for line in f:
            COLUMN,ROW = (line).split()
            ROW=int(ROW)
            COLUMN=int(COLUMN)
            PUZZLE_TYPE=ROW*COLUMN

            initial_state_list=list()
            initial_state_list = list(map(int, (f.readline()).split()))
            goal_state_list = list()
            goal_state_list = list(map(int, (f.readline()).split()))

            initial_state_list1 = list()
            for i in range(len(initial_state_list)):
                initial_state_list1.append(initial_state_list[i])

            init_puzzle_2D = get_2D_state(initial_state_list)
            goal_puzzle_2D = get_2D_state(goal_state_list)

            heuristic_num=1

            board = Puzzle(initial_state_list, goal_state_list,init_puzzle_2D,goal_puzzle_2D)
            puzzle_num+=1
            print("\nPUZZLE NUMBER "+str(puzzle_num))
            print("Initial puzzle state: ",end="")
            print(init_puzzle_2D)
            print("Goal puzzle state: ",end="")
            print(goal_puzzle_2D)

            print("\nGreedy search with Misplaced Tiles heuristic:")
            greedy_search_algo(board,COLUMN,ROW)

            heuristic_num=2
            init_puzzle_2D = get_2D_state(initial_state_list1)
            print("\nGreedy search with Manhattan Distance heuristic:")
            board1 = Puzzle(initial_state_list1, goal_state_list, init_puzzle_2D, goal_puzzle_2D)
            greedy_search_algo(board1, COLUMN, ROW)
    sys.stdout.close()
