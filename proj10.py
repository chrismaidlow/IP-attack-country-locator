#######################################################################
# Computer Project #10
# 
# Algorithm
#
#   Play a game of Nine Men's Morris. Ask for points to place on board. 
#   If valid point it will be marked with your symbol. Then other players turn.
#   Main will call function each time seeing if mill is created due to placement
#   If mill has been created - call remove piece function. Test validity of removal
#   Once 18 moves have been made move on to phase 2. Phase two is similar to 
#   phase one except adding to board is replaced by moving already placed pieces.
#   Alternate between players making moves until one player falls below three symbols
#   Winner is then declared via get_winner function. 
#
########################################################################

import NMM #This is necessary for the project


BANNER = """
    __        _____ _   _ _   _ _____ ____  _ _ _ 
    \ \      / /_ _| \ | | \ | | ____|  _ \| | | |
     \ \ /\ / / | ||  \| |  \| |  _| | |_) | | | |
      \ V  V /  | || |\  | |\  | |___|  _ <|_|_|_|
       \_/\_/  |___|_| \_|_| \_|_____|_| \_(_|_|_)

"""


RULES = """
  _   _ _              __  __            _       __  __                 _     
 | \ | (_)_ __   ___  |  \/  | ___ _ __ ( )___  |  \/  | ___  _ __ _ __(_)___ 
 |  \| | | '_ \ / _ \ | |\/| |/ _ \ '_ \|// __| | |\/| |/ _ \| '__| '__| / __|
 | |\  | | | | |  __/ | |  | |  __/ | | | \__ \ | |  | | (_) | |  | |  | \__ \
 |_| \_|_|_| |_|\___| |_|  |_|\___|_| |_| |___/ |_|  |_|\___/|_|  |_|  |_|___/
                                                                                        
    The game is played on a grid where each intersection is a "point" and
    three points in a row is called a "mill". Each player has 9 pieces and
    in Phase 1 the players take turns placing their pieces on the board to 
    make mills. When a mill (or mills) is made one opponent's piece can be 
    removed from play. In Phase 2 play continues by moving pieces to 
    adjacent points. 
    
    The game is ends when a player (the loser) has less than three 
    pieces on the board.

"""


MENU = """

    Game commands (first character is a letter, second is a digit):
    
    xx        Place piece at point xx (only valid during Phase 1 of game)
    xx yy     Move piece from point xx to point yy (only valid during Phase 2)
    R         Restart the game
    H         Display this menu of commands
    Q         Quit the game
    
"""
        
def count_mills(board, player):
    """
      For current player - iterate through keys in dictionary if value equals
      player character add it to set. Iterate through mills_sets. If 
      intersection is found between the two is equal to three then add to count
    """
    count = 0
    
    player_set = set()
    
    diction = board.points
    
    mills_list = board.MILLS
    
    for key,value in diction.items():
        
        if value == player:
            
            player_set.add(key)
            
    for item in mills_list:
        
        mills_set = set(item)
        
        if len(player_set & mills_set) == 3:
            
            count += 1

    return count
    
            
def place_piece_and_remove_opponents(board, player, destination):
    """
       if board position is empty continue. Call count mills before then call
       board.assign_piece from class then check mills count afterward. If 
       before count is greater than after count call remove_piece. 
    """
    
    if board.points[destination] == " ":
        
        
        before_assign = count_mills(board, player)
    
        board.assign_piece(player,destination)
    
        after_assign = count_mills(board, player)
    
        if after_assign > before_assign:
            
           print("A mill was formed!")
            
           print(board)
           
           remove_piece(board,player)
            
    else:
        
        raise RuntimeError("Invalid command: Destination point already taken")
        
        
def move_piece(board, player, origin, destination):
    """
        if intended destination a valid adjacent spot - continue. if destination
        is blank - continue. call board.clear_place for the origin. Call
        p_p_a_r function for adding to board and mill checking protocal.
    """
    
    if destination in board.ADJACENCY[origin]:
       
       if board.points[destination] == " ":
           
           board.clear_place(origin)
       
           place_piece_and_remove_opponents(board, player, destination) 
       
       else:
        
           raise RuntimeError("Invalid command: Destination is not adjacent")
           
    else:
        
        raise RuntimeError("Invalid command: Destination point already taken")
       
           
def points_not_in_mills(board, player):
    """
        iterate through board points creating set of all player locations. 
        iterate through board lists. if board list is a subset of player 
        locations set then add board list to in_mills set. 
    """
    player_set = set()
    
    diction = board.points
    
    in_mills = set()
    
    for key,value in diction.items():
        
        if value == player:
            
            player_set.add(key)
            
    for item in board.MILLS:
        
        set_item = set(item)
        
        if set_item.issubset(player_set):
            
            in_mills.update(set_item)
                        
    not_in_mills = player_set - in_mills        
    
    return not_in_mills
    
    
def placed(board,player):
    """
        iterate through all points and create set of points with player
        character.
    """
    placed_set = set()
    
    diction = board.points
    
    for key,value in diction.items():
        
        if value == player:
            
            placed_set.add(key)
        
    return placed_set
        
def remove_piece(board, player):
    """
       find placed_set minus not_in_mills. This provides you with
       all points on board for player in mills. Prompt for piece to remove
       until valid entry is provided. Establish proper error handling. If 
       only mills on board then "okay" to remove from mill.
    """
    play = player
    
    player = get_other_player(player)
    
    placed_set = placed(board,player)
        
    not_in_mills = points_not_in_mills(board, player)
        
    inter = placed_set & not_in_mills
    
    in_mills = placed_set - not_in_mills
    
    switch = True
    
    while switch == True:
        
        try:

            inp = input("Remove a piece at :> ")
            
            if inp in board.points:
            
                if board.points[inp] != play:
                                
                    if len(inter) == 0:
                        
                        if inp in placed_set:
                            
                            board.clear_place(inp)
                        
                            switch = False
                            
                            break
                            
                    if inp in in_mills:
                        
                        raise ValueError
                            
                    if inp in inter:
                    
                       board.clear_place(inp)
                        
                       switch = False   
                       
                    else:
                         
                       raise TypeError
                       
                else:
                
                    raise TypeError
                       
            else:
                    
                raise KeyError
                   

    
        except ValueError:
            
            print("Invalid command: Point is in a mill")
            print("Try again.")
            
        except TypeError:
            
            print("Invalid command: Point does not belong to player")
            print("Try again.")
            
        except KeyError:
            
            print("Invalid command: Not a valid point")
            print("Try again.")
            
           
def is_winner(board, player):
    """
        if amount of points on board for character is below three - declare
        winner.
    """
    player1 = placed(board, player)
    
    player = get_other_player(player)
    
    player2 = placed(board, player)
    
    if len(player1) < 3 or len(player2) < 3:
        
        return True
    
    else:
        
        return False
   
def get_other_player(player):
    """
    Get the other player.
    """
    return "X" if player == "O" else "O"
    
def main():
    #Loop so that we can start over on reset
    while True:
        #Setup stuff.
        print(RULES)
        print(MENU)
        board = NMM.Board()
        print(board)
        player = "X"
        placed_count = 0 # total of pieces placed by "X" or "O", includes pieces placed and then removed by opponent
        
        # PHASE 1
        print(player + "'s turn!")
        #placed = 0
        command = input("Place a piece at :> ").strip().lower()
        print()
        #Until someone quits or we place all 18 pieces...
        while command != 'q' and placed_count != 18:
            
            try:
                
                #help command
                if command == "h":
                    
                    print(MENU)
                    command = input("Place a piece at :> ").strip().lower()
                
                #reset command
                if command == "r":
                    
                    break
            
                place_piece_and_remove_opponents(board, player, command)
                player = get_other_player(player)
                placed_count += 1
            
            #Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
            #Prompt again
            print(board)
            print(player + "'s turn!")
            if placed_count < 18:
                command = input("Place a piece at :> ").strip().lower()
            else:
                print("**** Begin Phase 2: Move pieces by specifying two points")
                command = input("Move a piece (source,destination) :> ").strip().lower()
            print()
        
        #Go back to top if reset
        if command == 'r':
            continue
        # PHASE 2 of game
        while command != 'q':
            # commands should have two points
            command = command.split()
            try:
                
                #if only one point given throw error
                if len(command) < 2:
                    
                    raise RuntimeError("Invalid number of points")
                 
                origin = command[0]
                destination = command[1]
                
                if board.points[origin] != player:
                    
                    raise RuntimeError("Invalid command: Origin point does not belong to player")
                    
                if origin not in board.points or destination not in board.points:
                    
                    raise RuntimeError("Invalid command: Not a valid point")
                
                move_piece(board, player, origin, destination)
                player = get_other_player(player)
                result = is_winner(board,player)
                
                #WINNER
                if result == True:
                    print(BANNER)
                    quit()
                
            #Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))         
            #Display and reprompt
            print(board)
            #display_board(board)
            print(player + "'s turn!")
            command = input("Move a piece (source,destination) :> ").strip().lower()
            print()
            
        #If we ever quit we need to return
        if command == 'q':
            return

            
if __name__ == "__main__":
    main()