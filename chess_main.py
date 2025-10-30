from piece import *
import re
import unittest

board = [[None for _ in range(8)] for _ in range(8)]
ranks = [chr(i) for i in range(97, 105)]


#get() also sets This helps because the file-rank notation and the array
# indexing is different
def get(pos: str, assign : Piece = None):
    if assign:
        board[8 - int(pos[1])][fti(pos[0])] = assign
        return assign
    else:
        return board[int(pos[1]) - 1][fti(pos[0])]

def board_setup():
    piece_sequence = ['r','n','b','q','k','b','n','r']

    idx = 0
    for rank in ranks:
        for p in ((1,'w'), (8,'b')):
            get(rank + str(p[0]), Piece(p[1], piece_sequence[idx]))
        idx += 1

    get('a6', Piece('w','k'))

# Major problems with how the board is printed regarding indices
def print_board():
    for row in range(8):
        print(8 - row, '', end='')
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

#regexp
pattern = r'^([rnbkq]?)([a-h]?[1-8]?)x?([a-h][1-8])$'

def gameloop():
    instr = ''
    """Reference examples of notation
    e4
    Nf3
    qh5
    exd5
    nxd5
    ndxe6
    bxe6
    Bb5
    """
    while((instr := input(": ")) != '!q'):
        pass

def main():
    board_setup()
    print_board()
    unittest.main()

if __name__ == "__main__":
    main()