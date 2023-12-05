# https://www.geeksforgeeks.org/python-implementation-automatic-tic-tac-toe-game-using-random-number/

def main():
    board = [['-' for x in range(3)] for y in range(3)]

    def board_test(board,player_tag):

        win_test = lambda l : len(set(l))==1

        print("REDOVI")
        for i in range(3):
            lrow=[]
            lcol=[]
            for j in range(3):
                lrow.append(board[i][j])
                lcol.append(board[j][i])
            
        
        print("STUPCI")
            



    print("\nBOARD STATUS:")
    draw_board(board)

    x = 'X'
    o = 'O'

    board[1][1] = x    
    draw_board(board)

    board[0][2] = o
    draw_board(board)

    board[1][2] = x
    draw_board(board)

    board[0][1] = o
    draw_board(board)

    board[1][0] = x
    draw_board(board)

def draw_board(board):
    i=0
    j=0

    for i in range(3):
        print('\n|',end=' ')
        for j in range(3):
            print(f'{board[i][j]} |',end=' ')
    print("\n")

main()