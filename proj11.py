#######################################################################
# Computer Project #11
# 
# Algorithm
#
#   Play a game of Gomoku. Create board object. Create piece object. 
#   Get input from end user of coordinates to assign piece. Place piece on 
#   board. Check if five of player's color pieces are in a row horizontally or
#   vertically. If no winner alternate to player two. Loop through this - 
#   checking for errors - until winner function returns true.
########################################################################

class GoPiece(object):
    ''' Comment goes here.'''
    def __init__(self,color = "black"):
        ''' Initiaze to black. Error check for alternate colors'''
        if color != "black" and color != "white":
            
            raise MyError("Wrong color.")
    
        else:
            
            self.__color = color
    
    def __str__(self):
        ''' Return corresponding symbol for each color'''
        if self.__color == "white":
            
            return ' ○ '
            
        if self.__color == "black":
            
            return ' ● '

    def get_color(self):
        """ returns a string for the corresponding color"""
        
        if self.__color == "black":
            
            return "black"
        
        if self.__color == "white":
            
            return "white"
            
class MyError(Exception):
    """custom error handling"""
    def __init__(self,value):
        self.__value = value
    def __str__(self):
        return self.__value

class Gomoku(object):
    ''' board class. Creates board. Assigns pieces. Checks winner'''
    def __init__(self,board_size = 15 ,win_count = 5,current_player = "black"):
        ''' Initalize values. Board size 15 - win count 5 - player black'''
        
        if type(board_size) == int:
            
            self.__board_size = board_size
            
        else:
            
            raise ValueError
            
        if type(win_count) == int:
            
            self.__win_count = win_count
        
        else:
            
            raise ValueError
            
        if current_player != "black" and current_player != "white":
            
            raise MyError("Wrong color.")
    
        else:
            
            self.__current_player = current_player
        
        self.__go_board = [ [ ' - ' for j in range(self.__board_size)] for i in range(self.__board_size)]  
            
    def assign_piece(self,piece,row,col):
        ''' Error check and assign piece to board'''
        
        if row <= self.__board_size and col <= self.__board_size:
        
            if self.__go_board[row-1][col-1] == " - ":
                
                self.__go_board[row-1][col-1] = piece
            
            else:
                
                raise MyError("Position is occupied.")
                
        else:
            
            raise MyError('Invalid position.')
            
    def get_current_player(self):
        ''' return string from get current player'''
        player_string = self.__current_player
        
        return player_string
    
    def switch_current_player(self):
        ''' current player is assigned opposite color'''
        if self.__current_player == "white":
            
            self.__current_player = "black"
            
        else:
            
            self.__current_player = "white"
        
    def __str__(self):
        s = '\n'
        for i,row in enumerate(self.__go_board):
            s += "{:>3d}|".format(i+1)
            for item in row:
                s += str(item)
            s += "\n"
        line = "___"*self.__board_size
        s += "    " + line + "\n"
        s += "    "
        for i in range(1,self.__board_size+1):
            s += "{:>3d}".format(i)
        s += "\n"
        s += 'Current player: ' + ('●' if self.__current_player == 'black' else '○')
        return s
        
    def current_player_is_winner(self):
        ''' Iterate through 2d list matrix first horizontally - second 
        vertically checking for five of current players pieces in a row'''
        
        #HORIZONTAL ITERATION

        for row in self.__go_board:
            
            #track pieces in a row
            count = 0
            
            for col in row:
                
                #check that spot occupied by piece
                if isinstance(col, str):
                    
                    count = 0
                    
                if isinstance(col, GoPiece):
                    
                    #check piece color corresponds with player
                    if col.get_color() == "black":
                    
                        if self.__current_player == "black":
                            
                            count += 1
                            
                        else:
                            
                            count = 0
                            
                    if col.get_color() == "white":
                        
                        if self.__current_player == "white":
                            
                            count += 1
                            
                        else:
                            
                            count = 0
                
                #return true depending on win count
                if count >= self.__win_count:
                    
                    return True
                
        #Vertical
        col_dict = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0}
          
        
        for row in self.__go_board:
            
            #use count to count columns
            count = 0
            
            for col in row:
                
                #check proper instance
                if isinstance(col, str):
                    
                    col_dict[count] = 0
                    
                if isinstance(col, GoPiece):
                    
                    #add to column represented in dict if occupied
                    if col.get_color() == "black":
                    
                        if self.__current_player == "black":
                            
                            col_dict[count] += 1
                            
                        else:
                            
                            col_dict[count] = 0
                            
                    if col.get_color() == "white":
                        
                        if self.__current_player == "white":
                            
                            col_dict[count] += 1
                            
                        else:
                            
                            col_dict[count] = 0

                count += 1
                
            #if greater or equal to win count return True
            for value in col_dict.values():
                
                if value >= self.__win_count:
                    
                    return True     
    
        return False
    
def main():
    """Main driver of program"""
    
    board = Gomoku()
    piece = GoPiece()
    print(board)
    play = input("Input a row then column separated by a comma (q to quit): ")
    while play.lower() != 'q':
        play_list = play.strip().split(',')
        try: 
            
            #improper entry error
            if len(play_list) < 2:
                
                raise MyError("Incorrect input.")
                
                print("Try again.")
               
            row = (play_list[0])
            col = (play_list[1])
            
            # non number error
            if row.isalpha() == True:
                
                raise MyError("Incorrect input.")
                
                print("Try again.")
                
            else:
                
                row = int(row)
                
            if col.isalpha() == True:
                 
                raise MyError("Incorrect input.")
                
                print("Try again.")
                
            else:
                
                col = int(col)    
                
            # negative error
                
            if row < 0 or col < 0:
                
                raise MyError("Invalid position.")
                
                print("Try again.")
        

            board.assign_piece(piece,row,col)
            result = board.current_player_is_winner()
            
            if result == True:
                
                print(board)
                print("{} Wins!".format(board.get_current_player()))
                
                break
                
            #if not winner - change color - loop again
            board.switch_current_player()
            color = board.get_current_player()
            piece = GoPiece(color)

        except MyError as error_message:
            print("{:s}\nTry again.".format(str(error_message)))
        print(board)
        play = input("Input a row then column separated by a comma (q to quit): ")

if __name__ == '__main__':
    main()
