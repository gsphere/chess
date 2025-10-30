from piece import *

board = [[None for _ in range(8)] for _ in range(8)]
ranks = [chr(i) for i in range(97, 105)]

def main():
    board_setup()
    print_board()

def get(pos: str, assign : Piece = None):
    if assign:
        board[int(pos[1]) - 1][fti(pos[0])] = assign
        return assign
    else:
        return board[int(pos[1]) - 1][fti(pos[0])]

def board_setup():
    get("a4", Piece('w', 'n'))
    pass

def print_board():
    for row in range(8):
        print(row, '', end='')
        for rank in ranks:
            square = get( rank + str(row) )
            if not square:
                print('_ ', end='')
            elif type(square) is Piece:
                print(square.name.upper(), '', end='')
            else:
                print('? ', end='')
        print()
    #print file labels
    print('  ', end='')
    for rank in ranks:
        print(rank, '', end='')


def file_to_index(file:str):
    #'a' is 97
    return ord(file) - 97
fti = file_to_index

if __name__ == "__main__":
    main()