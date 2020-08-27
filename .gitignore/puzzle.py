
# vytvori zo stavu 2D tvar
# napriklad ak mame hlavolam 3x3: (1 2 3 4 5 6 7 8 0) stav prepise na tvar (1 2 3)(4 5 6)(7 8 0)
def get_2D_state(state,COLUMN):
    puzzle_2D = list()
    row = list()
    for idx, val in enumerate(state):
        row.append(val)
        if (idx + 1) % COLUMN == 0:
            puzzle_2D.append(row)
            row = list()
    return puzzle_2D


class State():
    # heuristic - hodnota vypocitana heuristikou pre daný stav
    # parent - predosly stav z ktoreho sme sa dostali do aktualneho
    # data - aktualny stav
    # depth - hlbka v ktorej sa nachadza stav
    # move - pohyb ktorym sme sa dostali do stavu(UP,DOWN,LEFT,RIGHT)
    def __init__(self, heuristic, depth,  parent, init_state,move):
        self.heuristic = heuristic
        self.parent = parent
        self.data = init_state
        self.depth = depth
        self.move = move

    def get_actual_state(self, ROW, COLUMN):
        actual_state = list()
        for i in range(ROW):
            for j in range(COLUMN):
                actual_state.append(self.data[i][j])
        actual_state = get_2D_state(actual_state, COLUMN)
        return actual_state

    # vymeni prazdne policko so susedom (vytvori novy stav)
    def swap(self, x1, y1, x2, y2):
        temp = self.data[x1][y1]
        self.data[x1][y1] = self.data[x2][y2]
        self.data[x2][y2] = temp
        return self.data

    # vygeneruje vsetky mozne dalsie stavy
    def generate_children(self,board,COLUMN,ROW,heuristic_num):
        for i in range(ROW):
            for j in range(COLUMN):
                if self.data[i][j] == 0:
                    y,x=i,j
        move=list()

        #funkcia vrati aktualny stav ktoreho susedov chceme v 2D tvare
        actual_state=self.get_actual_state(ROW, COLUMN)

        """move up"""
        if y-1 >-1:
            self.data=self.swap(y-1, x, y, x)
            if heuristic_num==1:
                new_state = State(board.heuristic_misplaced_tiles(self.data,COLUMN,ROW), self.depth + 1, self, self.data,"UP")
            elif heuristic_num==2:
                new_state = State(board.heuristic_manhattan(self.data, COLUMN, ROW), self.depth + 1, self, self.data,
                                  "UP")
            move.append(new_state)
            self.data=actual_state
            actual_state=self.get_actual_state(ROW, COLUMN)

        """move left"""
        if x-1 > -1 :
            self.data=self.swap(y,x-1,y,x)
            if heuristic_num==1:
                new_state = State(board.heuristic_misplaced_tiles(self.data,COLUMN,ROW), self.depth + 1, self, self.data,"LEFT")
            elif heuristic_num==2:
                new_state = State(board.heuristic_manhattan(self.data, COLUMN, ROW), self.depth + 1, self, self.data,
                                  "LEFT")
            move.append(new_state)
            self.data=actual_state
            actual_state=self.get_actual_state(ROW, COLUMN)

        """move down"""
        if y + 1 < ROW:
            self.data = self.swap(y + 1, x, y, x)
            if heuristic_num==1:
                new_state = State(board.heuristic_misplaced_tiles(self.data,COLUMN,ROW), self.depth + 1, self, self.data,"DOWN")
            elif heuristic_num==2:
                new_state = State(board.heuristic_manhattan(self.data, COLUMN, ROW), self.depth + 1, self, self.data,
                                  "DOWN")
            move.append(new_state)
            self.data = actual_state

        """move right"""
        if x+1<COLUMN:
            self.data=self.swap(y, x + 1, y, x)
            if heuristic_num == 1:
                new_state = State(board.heuristic_misplaced_tiles(self.data, COLUMN, ROW), self.depth + 1, self, self.data,
                                  "RIGHT")
            elif heuristic_num == 2:
                new_state = State(board.heuristic_manhattan(self.data, COLUMN, ROW), self.depth + 1, self, self.data,
                                  "RIGHT")
            move.append(new_state)
        # vrati vsetky nove stavy
        return move


class Puzzle():
    # priority_queue - prioritny rad pouzivany na vyber stavu v greedy_algo
    # start - pociatocny stav ako postupnost cisel
    # goal - cielovy stav ako postupnost cisel
    # initial_state - pociatocny stav v 2D
    # goal_state - cielovy stav v 2D
    def __init__(self, start_data, goal_data, init_puzzle_2D, goal_puzzle_2D):
        self.priority_queue = []
        self.start = start_data
        self.goal = goal_data
        self.initial_state = State(0,0,None,init_puzzle_2D,None)
        self.goal_state = State(0,0,None,goal_puzzle_2D,None)

    def array2D_to_tuple(self, data):
        new_list = []
        for i in data:
            for j in i:
                new_list.append(j)
        return tuple(new_list)

    # Heuristika: pocet policok ktore nie su na svojom mieste
    # data - stav pre ktory sa heuristika vypocitava
    def heuristic_misplaced_tiles(self, data,COLUMN,ROW):
        number_of_misplaced = 0
        for i in range(ROW):
            for j in range(COLUMN):
                if data[i][j] != 0:
                    if data[i][j] != self.goal_state.data[i][j]:
                        number_of_misplaced = number_of_misplaced + 1
        return number_of_misplaced

    # Heuristika: sucet vzdialenosti policok od cielovej pozicie
    # dara - stav pre ktory sa heuristika vypocitava
    def heuristic_manhattan(self, data, COLUMN, ROW):
        dist=0
        for i in range(ROW):
            for j in range(COLUMN):
                if data[i][j] != self.goal_state.data[i][j] and data[i][j] != 0:
                    P = self.goal.index(data[i][j])
                    x, y = divmod(P, COLUMN)
                    dist += abs(x - i) + abs(y - j)
        return dist

    # funkcia na vypis stavov (dá sa zapnut v zadanieUI_2.py, ale je vypnuta pretoze vypis by trval pridlho)
    def print_puzzles(self):
        print("ALL MOVES NEEDED TO REACH GOAL STATE:")
        for node in self.path:
            z=0
            for x in node.data:
                for y in x:
                    print("+---", end="")
                print("+")
                for y in x:
                    print ("| ",end="")
                    print(str(y),end=" ")
                print("|")
            for x in node.data:
                if z==0:
                    for y in x:
                        z=1
                        print("+---", end="")
                    print("+\n")

