import numpy as np

#Setting the scope of necessary variables to global
global sudokuDomain
global unsolvable
global prevPairs

global boxes
global boxOne
global boxTwo
global boxThree
global boxFour
global boxFive
global boxSix
global boxSeven
global boxEight
global boxNine

sudokuDomain = []
prevPairs = []

#Creating an array for the cells contained in each box unit
boxes = []
boxOne = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
boxTwo = [[0,3],[0,4],[0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]]
boxThree = [[0,6],[0,7],[0,8],[1,6],[1,7],[1,8],[2,6],[2,7],[2,8]]
boxFour = [[3,0],[3,1],[3,2],[4,0],[4,1],[4,2],[5,0],[5,1],[5,2]]
boxFive = [[3,3],[3,4],[3,5],[4,3],[4,4],[4,5],[5,3],[5,4],[5,5]]
boxSix = [[3,6],[3,7],[3,8],[4,6],[4,7],[4,8],[5,6],[5,7],[5,8]]
boxSeven = [[6,0],[6,1],[6,2],[7,0],[7,1],[7,2],[8,0],[8,1],[8,2]]
boxEight = [[6,3],[6,4],[6,5],[7,3],[7,4],[7,5],[8,3],[8,4],[8,5]]
boxNine = [[6,6],[6,7],[6,8],[7,6],[7,7],[7,8],[8,6],[8,7],[8,8]]
boxes.append(boxOne)
boxes.append(boxTwo)
boxes.append(boxThree)
boxes.append(boxFour)
boxes.append(boxFive)
boxes.append(boxSix)
boxes.append(boxSeven)
boxes.append(boxEight)
boxes.append(boxNine)

def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    #Allowing the function to change the value of the global variables unsolvable and sudokuDomain.
    global unsolvable
    global sudokuDomain
    count = 0
    unsolvable = False
    #Initialising the array containing the domains of each sudoku cell.
    sudokuDomain = []
    for row in range(9):
        sudokuDomain.append([])
        for col in range(9):
            sudokuDomain[row].append([])
            for z in range(9):
                sudokuDomain[row][col].append(0)
    #Initialising the sudoku.
    sudoku = init_state(sudoku)
    #Running the code until the sudoku is solved.
    while is_goal_state(sudoku) is False:
        prevSudoku = sudoku
        sudoku = next_state(sudoku,False)
        #Checks whether the sudoku board has changed since the last iteration.
        if np.array_equal(sudoku, prevSudoku, equal_nan=False):
            count += 1
            if count % 2 == 0:
                sudoku = next_state(sudoku,True)
                count = 0
        #Checks whether the sudoku is unsolvable and returns an array of -1.
        if unsolvable is True:
            unsolved = np.zeros((9,9))
            unsolved[:]-=1
            return unsolved
    #Returns the solved (or unsolved) sudoku.
    return sudoku

def init_state(sudoku):
    """
    Creates the initial state of the sudoku.
    
    Receives the sudoku array as an argument.
    
    Returns the altered sudoku array.
    """
    global unsolvable
    #Checks if the beginning soduko is valid via constraints.
    valid = True
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] != 0:
                valid = is_valid(sudoku,sudoku[row][col],[row,col])
                if valid is False:
                    unsolvable = True
                    return sudoku
    #Calculates the domain for each cell in the sudoku.
    for row in range(9):
        for col in range(9):
            sudoku = calculate_domain(sudoku,[row,col],0)
    return sudoku

def next_state(sudoku,unchanged):
    """
    Calculates the next state of the sudoku by deciding whether any empty cells can be filled with a value.
    
    Receives the sudoku and whether it has changed since the last iteration as arguments.
    
    Returns the altered sudoku array.
    """
    #Calculates the domain for each cell in the sudoku, providing the next state of the board.
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                sudoku = calculate_domain(sudoku,[row,col],sudokuDomain[row][col])
    #Checks whether the sudoku is solved.
    complete = is_goal_state(sudoku)
    #Attempts a more advanced constraint propogation if the board remains unchanged.
    if unchanged == True and complete == False:
        sudoku = hidden_singles(sudoku)
    return sudoku

def calculate_domain(sudoku,position,oldDomain):
    """
    Calculates the domain (possible values) of each sudoku cell.
    
    Receives the sudoku, position of the cell to calculate the domain of, and the old domain of this cell.
    
    Returns the altered sudoku array.
    """
    global unsolvable
    global sudokuDomain
    row = position[0]
    col = position[1]
    value = sudoku[row][col]
    domain = []
    #If the cell already has a valid, do not need to check if valid, so can append straight away.
    if value != 0:
        domain.append(value)
    #Checks if each number 1-9 is a valid possibility for the cell, and appends to the domain if so.
    else:
        for x in range(9):
            validDomain = is_valid(sudoku,x+1,position)
            if validDomain == True:
                domain.append(x+1)
    #If there are no possible values for the cell, the sudoku board is unsolvable.
    if len(domain) == 0:
        unsolvable = True
        return sudoku
    #If the domain has changed, the sudokuDomain array is updated.
    if oldDomain != 0 and oldDomain != domain:
        sudokuDomain[row][col] = domain
        #If there is only one possible value for the cell, the value is updated on the sudoku board.
        if len(domain) == 1:
            sudoku[row][col] = domain[0]
    return sudoku

def hidden_singles(sudoku):
    """
    Tests for hidden singles in the sudoku: a number only appears in one cell's domain for a unit.
    
    Receives the sudoku.
    
    Returns the altered sudoku array.
    """
    global unsolvable
    found = False
    #Checks each row for a hidden single.
    for row in range(9): #For each row.
        for num in range(1,10): #Testing each possible number.
            count = []
            for col in range(9): #Each cell in row.
                if num in sudokuDomain[row][col]: #If the number being tested is in that cell's domain.
                    count.append(col)
            #If the value only appears in one cell's domain within a row, there is a hidden single. 
            if len(count) == 1: 
                col = count[0]
                #Checks the cell hasn't already been filled in and the hidden single is valid.
                if len(sudokuDomain[row][col]) > 1 and is_valid(sudoku,num,[row,col]) is True:
                    found = True
                    for col in range(9):
                        if num in sudokuDomain[row][col]:
                            sudokuDomain[row][col].remove(num)
                    col = count[0]
                    sudokuDomain[row][col] == [num]
                    sudoku[row][col] = num
                    #Checks that the domains for the other cells in the unit are still valid.
                    for num in range(1,10):
                        validDomains = 0
                        for col in range(9):
                            if sudoku[row][col] == num or num in sudokuDomain[row][col]:
                                validDomains += 1
                        if validDomains == 0:
                            unsolvable = True
    #Checks each column for a hidden single.
    for col in range(9):
        for num in range(1,10):
            count = []
            for row in range(9):
                if num in sudokuDomain[row][col]:
                    count.append(row)
            if len(count) == 1:
                row = count[0]
                if len(sudokuDomain[row][col]) > 1 and is_valid(sudoku,num,[row,col]) is True:
                    found = True
                    for row in range(9):
                        if num in sudokuDomain[row][col]:
                            sudokuDomain[row][col].remove(num)
                    row = count[0]
                    sudokuDomain[row][col] == [num]
                    sudoku[row][col] = num
                    for num in range(1,10):
                        validDomains = 0
                        for row in range(9):
                            if sudoku[row][col] == num or num in sudokuDomain[row][col]:
                                validDomains += 1
                        if validDomains == 0:
                            unsolvable = True 
    #Checks each box for a hidden single.
    for box in range(9):
        for num in range(1,10):
            count = []
            for cell in range(9):
                #Using the global boxes array to determine which cells are in each box unit.
                position = boxes[box][cell]
                row = position[0]
                col = position[1]
                if num in sudokuDomain[row][col]:
                    count.append(boxes[box][cell])
                    count.append(cell)
            if len(count) == 1:
                cell = count[0]
                row = cell[0]
                col = cell[1]
                if len(sudokuDomain[row][col]) > 1 and is_valid(sudoku,num,[row,col]) is True:
                    found = True
                    for cell in range(9):
                        position = boxes[box][cell]
                        row = position[0]
                        col = position[1]
                        if num in sudokuDomain[row][col]:
                            sudokuDomain[row][col].remove(num)
                        position = count[0]
                        row = position[0]
                        col = position[1]
                        sudokuDomain[row][col] = [num]
                        sudoku[row][col] = num
                        #check if domains are valid
                        for num in range(1,10):
                            validDomains = 0
                            for cell in range(9):
                                position = boxes[box][cell]
                                row = position[0]
                                col = position[1]
                                if num in sudokuDomain[row][col]:
                                    validDomains += 1
                            if validDomains == 0:
                                unsolvable = True
    #If there are no hidden singles found, the algorithm attempts to find naked pairs.
    if found == False:
        sudoku = naked_pairs(sudoku)
    return sudoku

def naked_pairs(sudoku):
    """
    Tests for hidden singles in the sudoku: two cells in a unit have an equal domain of length two.
    
    Receives the sudoku.
    
    Returns the altered sudoku array.
    """
    global sudokuDomain
    global unsolvable
    global prevPairs
    found = False
    #Checks for naked pairs in a row.
    for row in range(9):
        possiblePairs = [] #Array storing alternating domains and positions.
        for col in range(9):
            if len(sudokuDomain[row][col]) == 2:
                if sudokuDomain[row][col] in possiblePairs: #Naked pair found.
                    pairValues = sudokuDomain[row][col]
                    pairPositions = []
                    pairPositions.append([row,col])
                    #If a new naked pair is found, the values are removed from all other cells' domains in that unit.
                    if pairPositions not in prevPairs:
                        prevPairs.append(pairPositions)
                        found = True
                        for col in range(9):
                            for ind in range(2):
                                if pairValues[ind] in sudokuDomain[row][col] and [row,col] not in pairPositions:
                                    sudokuDomain[row][col].remove(pairValues[ind])
                        return sudoku
                else:
                    possiblePairs.append(sudokuDomain[row][col])
                    possiblePairs.append([row,col])
    #Checks for naked pairs in a column.
    for col in range(9):
        possiblePairs = [] #Array storing alternating domains and positions.
        for row in range(9):
            if len(sudokuDomain[row][col]) == 2:
                if sudokuDomain[row][col] in possiblePairs: #Naked pair found.
                    pairValues = sudokuDomain[row][col]
                    pairPositions = []
                    pairPositions.append([row,col])
                    if pairPositions not in prevPairs:
                        prevPairs.append(pairPositions)
                        found = True
                        for row in range(9):
                            for ind in range(2):
                                if pairValues[ind] in sudokuDomain[row][col] and [row,col] not in pairPositions:
                                    sudokuDomain[row][col].remove(pairValues[ind])
                        return sudoku
                else:
                    possiblePairs.append(sudokuDomain[row][col])
                    possiblePairs.append([row,col])
    #Checks for naked pairs in a box.
    for box in range(9):
        possiblePairs = [] #Array storing alternating domains and positions.
        for cell in range(9):
            position = boxes[box][cell]
            row = position[0]
            col = position[1]
            if len(sudokuDomain[row][col]) == 2:
                if sudokuDomain[row][col] in possiblePairs: #Naked pair found.
                    pairValues = sudokuDomain[row][col]
                    pairPositions = []
                    pairPositions.append([row,col])
                    if pairPositions not in prevPairs:
                        prevPairs.append(pairPositions)
                        found = True
                        for cell in range(9):
                            position = boxes[box][cell]
                            row = position[0]
                            col = position[1] 
                            for ind in range(2):
                                if pairValues[ind] in sudokuDomain[row][col] and [row,col] not in pairPositions:
                                    sudokuDomain[row][col].remove(pairValues[ind])
                        return sudoku
                else:
                    possiblePairs.append(sudokuDomain[row][col])
                    possiblePairs.append([row,col])
    #If no naked pairs are found, take the sudoku as unsolvable
    if found == False:
        unsolvable = True
    return sudoku

                
def is_goal_state(sudoku):
    """
    Checks whether the sudoku is solved, i.e. all the cells are filled in.
    
    Receives the sudoku as an argument.
    
    Returns a Boolean denoting whether the sudoku is solved.
    """
    valid = True
    #If any cells in the array are empty, the sudoku is not solved
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                valid = False
    return valid

def is_valid(sudoku,value,position): #position = [row,column]
    """
    Checks the validity of a possible entry for each soduko cell, considering row, column and box constraints.
    
    Receives the sudoku, value of the cell to be tested, position of the cell and whether this is the first time testing.
    
    Returns a Boolean denoting whether the value is a possibility for that cell.
    """
    box = []
    valid = True
    row = position[0]
    column = position[1] 
    #Checks whether any other cell in the row has the same value.
    for x in range(9):
        if sudoku[x][column] == value and x != row:
            valid = False
            return valid
    #Checks whether any other cell in the column has the same value.
    for y in range(9):
        if sudoku[row][y] == value and y != column:
            valid = False
            return valid
    #Calculates which box the cell is in.
    if row < 3:
        if column < 3:
            box = boxOne
        elif column < 6:
            box = boxTwo
        else:
            box = boxThree
    elif row < 6:
        if column < 3:
            box = boxFour
        elif column < 6:
            box = boxFive
        else:
            box = boxSix
    else:
        if column < 3:
            box = boxSeven
        elif column < 6:
            box = boxEight
        else:
            box = boxNine
    #Checks whether any other cell in the box has the same value.
    for x in range(9):
        testPos = box[x]
        testRow = testPos[0]
        testCol = testPos[1]
        if value == sudoku[testRow][testCol] and position != [testRow,testCol]:
            valid = False
            return valid
    return valid

example = np.array([[1, 0, 4, 3, 8, 2, 9, 5, 6],[2, 0, 5, 4, 6, 7, 1, 3, 8],[3, 8, 6, 9, 5, 1, 4, 0, 2],[4, 6, 1, 5, 2, 3, 8, 9, 7],[7, 3, 8, 1, 4, 9, 6, 2, 5],[9, 5, 2, 8, 7, 6, 3, 1, 4],[5, 2, 9, 6, 3, 4, 7, 8, 1],[6, 0, 7, 2, 9, 8, 5, 4, 3],[8, 4, 3, 0, 1, 5, 2, 6, 9]]) 
print(example)
print("Solution")
print(sudoku_solver(example))