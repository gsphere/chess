from piece import *
import re

board = [[None for _ in range(8)] for _ in range(8)]
ranks = [chr(i) for i in range(97, 105)]
turn = 'w'


#get() also sets
def get(pos: str, assign: Piece = None, clear=False):
    if clear:
        board[int(pos[1]) - 1][fti(pos[0])] = None
        return
    if assign:
        board[int(pos[1]) - 1][fti(pos[0])] = assign
        return assign
    else:
        return board[int(pos[1]) - 1][fti(pos[0])]

def board_setup():
    piece_sequence = ['R','N','B','Q','K','B','N','R']

    for rank in ranks:
        for p in ((1,'w'), (8,'b')):
            get(rank + str(p[0]), Piece(p[1], piece_sequence[fti(rank)]))
        for p in ((2,'w'), (7,'b')):
            get(rank + str(p[0]), Piece(p[1], 'P'))

# Major problems with how the board is printed regarding indices
def print_board():
    for row in range(8):
        print(8 - row, '', end='')
        for rank in ranks:
            square = get( rank + str(8 - row) )
            if not square:
                print('_ ', end='')
            elif type(square) is Piece:
                print(square.name, square.side, end='', sep='')
            else:
                print('? ', end='')
        print()
    #print file labels
    print('  ', end='')
    for rank in ranks:
        print(rank, '', end='')
    print()


def file_to_index(file: str) -> int:
    #'a' is 97
    return ord(file) - 97
fti = file_to_index

#regexp
# TO DO: REMEMBER CASTLING RIGHTS
pattern = r'^([RNBKQ]?)([a-h]?[1-8]?)x?([a-h][1-8])$'

def move(source, destination):
    get(destination, get(source))
    get(source, None, clear=True)

def general_legal_move(source, destination):
    destination_contents = get(destination)
    if destination_contents and destination_contents.side == turn:
        return "destination square is occupied by your own piece"

def pawn_legal_move(source, destination):
    opponent = 'b' if turn == 'w' else 'w'
    modifier = -1 if turn == 'w' else 1

    # if destination has my own team piece it's invalid
    if result := general_legal_move(source, destination):
        return result
    if not get(source) or not get(source).name == 'P':
        return f'no piece or no pawn at source location {source}'

    opponent_there = get(destination) and get(destination).side == opponent
    # if files are not equal, it's a capture.
    if abs(ord(source[0]) - ord(destination[0])) == 1:
        if opponent_there and (int(destination[1]) - int(source[1]) ==
                                 -modifier):
            return
        else:
            return (f'could not perform pawn capture from {source} to'
                    f' {destination}')

    # if files are equal, it's just a move

    if source[0] == destination[0]:
        if source[1] == str(int(destination[1]) + modifier):
            # source and dest are paired and adjacent
            return
        elif source[1] == str(int(destination[1]) + modifier * 2):
            # source and dest are on the same file and 2 away
            for i in (('4', 'w', -2), ('5', 'b', 2)):
                if destination[1] == i[0] and turn == i[1]:
                    #white can only move 2 to 'x4' and b can only move 2 to 'x5'
                    return
        else:
            return f"pawn error moving vertically from {source} to {
            destination}"

    # TO DO: YOU HAVE TO CHECK FOR PROMOTIONS
    # EN PASSANT
    # check if a pawn exists than can move there

    return f"for some reason {source} to {destination} didn't work"

legal_functions = {'P' : pawn_legal_move}


def invalid_square(source):
    if source[0] not in ranks or int(source[1]) not in range(1,9):
        return True

def attempt_move(source, destination):
    # simplifies combination of test for legality plus perform the move

    print (f"DEBUG: checking if move legal from {source} to {destination}")
    if not get(source):
        return f'there is no piece at {source} to test legal moves from'
    if invalid_square(source):
        return f'{source} is an invalid square'
    if invalid_square(destination):
        return (f"{destination} is an invalid square"
                f"")
    result = legal_functions[get(source).name](source, destination)
    if not result:
        move( source, destination )
    else:
        return result

def process_move(notation:str):
    match = re.match(pattern, notation)
    if not match:
        return f"notation {notation} could not be parsed."

    piece_name = match.group(1) if match.group(1) else 'P'
    origin = match.group(2)
    destination = match.group(3)
    modifier = -1 if turn == 'w' else 1

    # a simplified 'move' can be a tuple ('r#', 'r#') Find out what the user
    # intends to do based on the string.

    # PROBLEM: black can do g7xh8 which is very wrong

    match len(origin):
        case 0:
            # must be a forward pawn move. try to move a pawn behind the
            # destination.


            pos1 = destination[0] + f"{int(destination[1]) + modifier}"
            pos2 = destination[0] + f"{int(destination[1]) + modifier * 2}"

            if get(pos1) and get(pos1).name == "P":
                return attempt_move(pos1, destination)
            elif get(pos2) and get(pos2).name == "P":
                return attempt_move(pos2, destination)
            else:
                return (f"forward pawn move invalid 'not one or 2 spa"
                        f"ces' {origin} t{destination}")

        case 1:
            # could be a few things. requires disambiguation here
            # possibly ambiguated move for any piece, if a piece name exists

            # or it could be a pawn capture
            match piece_name:
                case 'P':
                    if origin.isdigit():
                        return ("pawn capture needs to have a source file, "
                                "not rank")
                    else:
                        return attempt_move(origin + str(int(destination[1]) +
                                            modifier), destination)
        case 2:
            # fully disambiguated move. easy.
            return attempt_move(origin, destination)
        case 3:
            raise Exception("something went really wrong")


def gameloop():
    global turn
    print_board()
    while (instr := input(f"{turn} move: ")) != '!q':
        result = process_move(instr, )
        if result:
            print(f"{instr} is an invalid move: {result}")
        else:
            turn = 'b' if turn == 'w' else 'w'
            pass
        print_board()

def main():
    board_setup()
    gameloop()

if __name__ == "__main__":
    main()