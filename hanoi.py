# hanoi.py - play the Towers of Hanoi game
import random
import pyinputplus as pyip


def showInstructions():
    print(
        """
The goal of the game is to 
move all of the pieces from one peg to another.
You can't move a larger piece onto a smaller piece.
Choose which peg to start from (1 at top, 3 at bottom)
and which peg to move to. Try to move the entire pyramid
stack in as few moves as possible.
When you're done playing, enter blank values into the input
and the game will end. Enjoy!
"""
    )


def initBoard(numDisks):
    # sets a tower in a random peg and returns board object
    board = [[], [], []]
    pegStack = [i for i in range(1, numDisks + 1)]
    startingPeg = random.randint(0, 2)
    board[startingPeg] = pegStack
    return board, startingPeg


def clearScreen():
    from os import system, name

    if name == "nt":
        # windows
        _ = system("cls")
    else:
        _ = system("clear")


def printBoard(board):
    """Show board and all disks
    | #
    | ##
    | ###
    """
    clearScreen()
    for peg in board:
        print("-" * 7)
        if len(peg) != 0:
            for _ in range(numDisks - len(peg)):
                print("|")
            for disk in peg:
                print("| " + "#" * disk)
        if len(peg) == 0:
            for _ in range(numDisks):
                print("|")
    print("-" * 7)


def moveDisk(board, startPeg, endPeg):
    # input indices of board to move a piece
    try:
        newBoard = board.copy()
        start = newBoard[startPeg][0]
        newBoard[startPeg].remove(start)
        newBoard[endPeg] = [start, *newBoard[endPeg]]
        return newBoard
    except IndexError:
        return board


def showStats():
    print(f"You've used {moves} turns. Your game has {numDisks} disks.\n")


def askInput(board):
    while True:

        startPeg = pyip.inputInt(
            prompt="Which peg would you like to move from? (1-3) ",
            blank=True,
            min=1,
            max=3,
        )
        if str(startPeg).strip() == "":
            newBoard = ""
            break
        endPeg = pyip.inputInt(
            prompt="Which peg would you like to move to? (1-3) ",
            blank=True,
            min=1,
            max=3,
        )
        # quit game
        if str(endPeg).strip() == "":
            newBoard = ""
            break

        # start same as end
        if startPeg == endPeg:
            print("\nCan't move it to the same location. Try again. \n")
            continue
        # start peg is empty
        if len(board[startPeg - 1]) == 0:
            print("\nCan't move from an empty peg.\n")
            continue
        if len(board[endPeg - 1]) == 0:
            break
        # make sure it's in order (1,2,3)
        if board[endPeg - 1][-1] < board[startPeg - 1][-1]:
            print("\nCan't move a larger piece onto a smaller piece. Try again.\n")
            continue
        # passes all, then break
        break
    if newBoard != "":
        newBoard = moveDisk(board, startPeg - 1, endPeg - 1)
    return newBoard


def solve(numDisks, start, end, alt, board):
    global moves

    if numDisks > 0:
        solve(numDisks - 1, start, alt, end, board)
        print(f"({moves+1}) Moved from peg {start+1} to peg {end+1}.")
        moves += 1
        solve(numDisks - 1, alt, end, start, board)


# game loop
while True:
    clearScreen()
    desireInstructions = pyip.inputYesNo(
        prompt="Would you like to read the instructions? (y/n) "
    )
    if desireInstructions == "yes":
        showInstructions()
    numDisks = pyip.inputInt(prompt="How many disks would you like? ", min=2, max=10)

    board, startingPeg = initBoard(numDisks)  # make a new random board
    moves = 0

    playOrWatch = pyip.inputChoice(["play", "watch"])
    if playOrWatch == "watch":
        possibleLocations = [0, 1, 2]
        possibleLocations.remove(startingPeg)
        endPeg = random.choice(possibleLocations)
        possibleLocations.remove(endPeg)
        altPeg = possibleLocations[0]

        solve(numDisks, startingPeg, endPeg, altPeg, board)
    else:
        while True:
            printBoard(board)  # show game board
            board = askInput(board)  # ask for user input with input validation
            if str(board).strip() == "":
                break
            else:
                moves += 1

    # clearScreen()
    showStats()
    playAgain = pyip.inputYesNo(prompt="Would you like to play again? (y/n) ")
    if playAgain == "no":
        print("Thanks for playing!")
        break
