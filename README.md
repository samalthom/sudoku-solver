# Sudoku Solver

## Introduction

This project consists of writing an agent to solve sudoku puzzles of four varying difficulties. Sudokus are an example of a **constraint satisfaction problem** and the solution follows an iterative approach that uses several sudoku solving techniques. It accepts a 9x9 numpy array (the initial sudoku board) as an argument and returns the 9x9 numpy array either solved or as an array of -1 to indicate the sudoku is unsolvable.

## Sudoku

Sudoku is a puzzle intended for a single player. It consists of a 9x9 grid with some cells containing a value 1-9, and the aim is to fill in every empty square until the sudoku is full. The constraints of the puzzle are that no number can appear multiple times in the same row, column or box (all **units**). There is always only one solution to a sudoku, due to the placement of the original filled cells.

## Constraint Satisfaction Problems / CSPs

Constraint problems are a subset of search problems. They use **factored representation** for each state, in which a set of variables each has a value, and the problem is solved once every variable has a value that satisfies all of the set constraints on that variable. [1]
To formalise a CSP, you use:
>* X = {X<sub>1</sub>,X<sub>2</sub>,...,X<sub>n</sub>}, a set of variables,
>* D = {D<sub>1</sub>,D<sub>2</sub>,...,D<sub>n</sub>}, a set of domains specifying the values each variable can take,
>* C, a set of constraints that specifies the values that the variables are allowed to have collectively.  
<!--End of list-->
To solve a CSP, a state space must be defined by an assignment of values to some or all of the variables. A state is **consistent** if it does not violate any of the constraints and **complete** if it assigns all the variables (it is described as a **partial** state if not). The **solution** is a state which is both consistent and complete.

### CSP for Sudoku

Sudoku can be represented as a CSP, with:
>* X = {each cell}, with a length of 81,
>* D = {1,2,3,4,5,6,7,8,9}, with the domain contianing every possible number for the cell,
>* C = alldiff for each unit.
<!--End of list-->

## Choice of Algorithm

I used a constraint propagation iterative approach that calculates the next state using inferences. This runs until the sudoku is solved. This first propagation looks at **lone singles** [2], using arc consistency (via checking whether each number is a possibility in that square with the constraints defined above) to reduce the domain of each cell in the sudoku. It inserts the value of a cell if its domain is reduced to a length of 1 (meaning there is only possible value for that cell). If after the domain has been reduced, it has a length of 0, there are no possible values for that cell, and the sudoku board is rendered unsolvable.  

If this propagation has not changed the state of the sudoku board after two iterations, the solution follows a more complex inference strategy called: **hidden singles** [2]. This checks whether a number only appears in one cell's domain for a unit, which implies it must be the value of that cell. Then, for every cell in that cell's units, the value of the hidden single is removed from the cells' domains.  

If both of the above strategies do not change the state of the sudoku board, the solution attempts to find **naked pairs** [2]. This denotes that two cells within a unit have the exact same two possible values, showing that the two values must be in the two cells, meaning the values can be removed from the domains of any other cells in that unit. These were the three inference strategies I used so if none of the above work, the solver deems the sudoku unsolvable. 

Because all categories that are easy and above will contain invalid initial states, when the solver initialises the sudoku, it iterates through each cell in the array and, if the cell is not empty, checks that the value currently in the cell is valid according the the constraints. If any cell is invalid, the sudoku is deemed unsolvable and no further states will be found.  

If the solver solves a sudoku, it returns the complete board as a 2-d array (9x9). If the sudoku provided has no solution, the solver will deem it unsolvable and return an 2-d array (9x9) filled with -1's. This is also the case if an invalid initial state is provided.

## Conclusion

### Results

The solution solves all given sudokus up to and including the medium difficultly in a short amount of time, *either 0 or 0.015625 seconds*. It also solves 5 of the 15 given hard sudokus in under a second. However, it fails to solve the other 10 sudokus, incorrectly deeming them unsolvable.

### Possible Extensions

<!--backtracking depth-first search with constraint propagation-->
This implementation of a sudoku solver could be made more effective by implementing a **backtracking algorithm**. This combines a depth-first search with constraint propagation and therefore only children of nodes which are consistent with the constraints are considered, greatly reducing time and space complexity used as the algorithm does not follow through every possibility on the state space. This is not suited to the current implementation which would need to be transferred into a OOP equivalent. A depth-first search is useful over other techniques, like a breadth-first search, when space and time are a priority. 

To improve on the implementation even further, heuristics can be used. Namely, the **Minimum Remaining Value (MRV)** could be used when selecting which cell's domain to look at first as it will select the cell with the shortest domain.  
<!--other inference techniques like naked triples-->
Other improvements could be implementing other inference techniques. For example, naked triples, which is where in any unit, three squares each have a domain that contains the same three numbers or a subset of those numbers. [1]

## References
[1] Norvig, P. and Russel, S. (2016) *Artificial Intelligence: A Modern Approach.* Third Edition. Pearson Education.

[2] Learn Sudoku website. Available from: https://www.learn-sudoku.com/ [Accessed 05/12/2021]