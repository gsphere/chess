from piece import *
import re

board = [[None for _ in range(8)] for _ in range(8)]
ranks = [chr(i) for i in range(97, 105)]


#get() also sets
def get(pos: str, assign : Piece = None, clear=False):
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


def file_to_index(file:str):
    #'a' is 97
    return ord(file) - 97
fti = file_to_index

#regexp
# TO DO: REMEMBER CASTLING RIGHTS
pattern = r'^([RNBKQ]?)([a-h]?[1-8]?)x?([a-h][1-8])$'

def move(source, destination):
    get(destination, get(source))
    get(source, None, clear=True)

def process_move(notation:str, turn:str):
    opponent = 'b' if turn == 'w' else 'w'
    match = re.match(pattern, notation)
    if not match:
        return "notation {instr} could not be parsed."

    piece_name = match.group(1) if match.group(1) else 'P'
    origin = match.group(2)
    destination = match.group(3)
    modifier = -1 if turn == 'w' else 1

    # how the fuck do i do this?
    # if destination has my own team piece it's invalid
    destination_contents = get(destination)
    if destination_contents and destination_contents.side == turn:
        return "destination square is occupied by your own piece"
    match piece_name:
        case 'P':
            # check if this is a capture, if so find where the pawn must come
            # from
            if origin:
                if origin in ranks:
                    if (destination_contents and destination_contents.side ==
                            opponent):
                        print(origin)
                        full_origin = (f"{origin}"
                                       f"{int(destination[1]) + modifier}")
                        # check there is a pawn at the origin
                        if (get(full_origin) and get(full_origin).name == 'P'
                                and get(full_origin).side == turn):
                            move(full_origin, destination)
                        else:
                            return f"there was no pawn at {full_origin}"
                        # TO DO: YOU HAVE TO CHECK FOR EN PASSANT HERE
                    else:
                        return f"there was no piece to capture at {destination}"
                else:
                    return (f"pawn capture did not contain a source rank, "
                            f"not a valid move")
                return

            # movement and not capture
            # pawns cannot capture forward
            if destination_contents and destination_contents.side == opponent:
                return "destination square is occupied by opponent piece"

            # TO DO: YOU HAVE TO CHECK FOR PROMOTIONS
            # check if a pawn exists than can move there


            to_check = f"{destination[0]}{int(destination[1])+modifier}"
            if get(to_check) and get(to_check).name == 'P' and get(
                    to_check).side == turn:
                move(to_check, destination)
                return

            # for the initial moves, where you can move twice
            for i in (('4','w',-2), ('5','b', 2)):
                if destination[1] == i[0] and turn == i[1]:
                    to_check = f"{destination[0]}{int(destination[1]) + i[2]}"
                    if get(to_check) and get(to_check).name == 'P':
                        move(to_check, destination)
                        return

            return "for some reason this didn't work"

def gameloop():
    instr = ''
    turn = 'w'
    print_board()
    while((instr := input(f"{turn} move: ")) != '!q'):
        result = process_move(instr, turn)
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