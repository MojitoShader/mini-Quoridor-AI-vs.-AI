import random
from collections import deque

Me = 'P2'
Opponent = 'P1'
MyTarget = (4, 2)
OpponentTarget = (0, 2)
Precision = 200



class Player2AI:
    def get_move(self, game):
        print("Player 1 Position:",game.player_positions['P1'])
        print("Player 2 Position:",game.player_positions['P2'])
        print("remaining walls",game.walls)
        print("Board ",game.board)
        print ("Player1 Pathlenght = ", pathLenght(game.player_positions['P1'], 0, game.board))
        print ("Player2 Pathlenght = ", pathLenght(game.player_positions['P2'], 4, game.board))

       
        # Calculate the shortest Path
        shortest_path = None
        for _ in range(Precision):
            path = game.extract_path(game.player_positions[Me], MyTarget)
            if shortest_path is None or (path and len(path) < len(shortest_path)):
                shortest_path = path
        

        best_move = calculate_best_move(game, Me, MyTarget, Opponent, OpponentTarget)
        if best_move:
            return best_move
        else:
            return shortest_path[0]
        

#################-Pathlength calculator-#################

def pathLenght(position, target_row, wall_matrix):
    # Print the starting position for debugging
    #print(f"Calculating path length from position: {position} to target row: {target_row}")

    # Check if position is within valid range
    if not (0 <= position[0] < 5 and 0 <= position[1] < 5):
        raise ValueError(f"Invalid position: {position}. Position must be within the range (0,0) to (4,4).")

    # Create a 5x5 matrix filled with -1
    board = [[-1 for _ in range(5)] for _ in range(5)]

    horizontal_moves, vertical_moves = convert_walls_to_moves(wall_matrix)

    # Initialize the queue with the starting position
    queue = deque([(position[0], position[1], 0)])  # (y, x, distance)
    board[position[0]][position[1]] = 0  # Starting position is distance 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # (right, left, down, up)

    while queue:
        y, x, dist = queue.popleft()

        for dy, dx in directions:
            ny, nx = y + dy, x + dx

            # Check bounds and whether the move is allowed
            if 0 <= ny < 5 and 0 <= nx < 5 and board[ny][nx] == -1:
                if (dy == 0 and dx == 1 and x < 4 and horizontal_moves[y][x]) or \
                   (dy == 0 and dx == -1 and x > 0 and horizontal_moves[y][x-1]) or \
                   (dy == 1 and dx == 0 and y < 4 and vertical_moves[y][x]) or \
                   (dy == -1 and dx == 0 and y > 0 and vertical_moves[y-1][x]):
                    board[ny][nx] = dist + 1
                    queue.append((ny, nx, dist + 1))
                    # If we reach the target row, return the distance
                    if ny == target_row:
                        return dist + 1

    # If no path is found, return -1
    return -1

#################-Wall to Matrix conversion-#################

def convert_walls_to_moves(wall_matrix):
    board_size = len(wall_matrix)

    # Initialize the horizontal and vertical move matrices
    horizontal_moves = [[True for _ in range(board_size - 1)] for _ in range(board_size)]
    vertical_moves = [[True for _ in range(board_size)] for _ in range(board_size - 1)]

    for i in range(board_size):
        for j in range(board_size):
            if wall_matrix[i][j] in ['V', 'VV', 'HV']:
                if j < board_size - 1:
                    horizontal_moves[i][j] = False
            if wall_matrix[i][j] in ['H', 'HH', 'HV']:
                if i < board_size - 1:
                    vertical_moves[i][j] = False

    return horizontal_moves, vertical_moves


#################-Calculate best Move -#################

def calculate_best_move(game, Me, MyTarget, Opponent, OpponentTarget):
    def evaluate_move(game, Me, MyTarget, Opponent, OpponentTarget,   depth):
        # Base case: No more depth to evaluate
        if depth == 0:
            return None, 0


        # Calculate the path length for the AI
        ai_position = game.player_positions[Me]
        ai_shortest_path_length = pathLenght(ai_position, MyTarget[0], game.board)
        
        # Calculate the path length for the opponent
        opponent_position = game.player_positions[Opponent]
        opponent_shortest_path_length = pathLenght(opponent_position, OpponentTarget[0], game.board)
        
        #print("Player", Me)
        #print("My Path length:", ai_shortest_path_length)
        #print("Opponent Path length:", opponent_shortest_path_length)

        # Try placing random walls and check the effect on both paths' lengths
        # legal_wall_moves = [move for move in game.get_legal_moves() if move[0] in ['H', 'V', 'HH','VV', 'HV']]

        original_ply = game.ply  
        game.ply = 0 if Me == 'P1' else 1  # aktiven Spieler setzen  
        legal_wall_moves = [m for m in game.get_legal_moves() if m[0] in ['H','V']]  
        game.ply = original_ply  # Zustand wiederherstellen

        #legal_player_moves = [move for move in game.get_legal_moves() if move[0] in ['U', 'D', 'L', 'R']]
        best_move = None
        best_metric = float('-inf')  # Initialize the best metric to a very low value

        #print("Testing Wall moves")
        for move in legal_wall_moves:
            # Simulate placing the wall
            previous_state = game.update_board_wall(move)
            print(move)
            # Calculate the new path length for the opponent
            new_opponent_path_length = pathLenght(opponent_position, OpponentTarget[0], game.board)
            
            # Calculate the new path length for the AI
            new_ai_path_length = pathLenght(ai_position, MyTarget[0], game.board)
            
            # Calculate the metric to maximize opponent's path length and minimize AI's path length
            #metric = new_opponent_path_length - new_ai_path_length
            metric = (new_opponent_path_length-opponent_shortest_path_length) - (new_ai_path_length-ai_shortest_path_length) #trying abs metric


            # Evaluate opponent's best response
            opponent_best_move, opponent_best_metric = evaluate_move(game, Opponent, OpponentTarget, Me, MyTarget,   depth - 1)
            if opponent_best_metric is not None:
                metric -= opponent_best_metric

            # Check if this move improves the metric
            if metric > best_metric:
                best_move = move
                best_metric = metric
            
            # Restore the board to the previous state
            game.restore_board_wall(move, previous_state)


        
        if best_metric < 1 and opponent_shortest_path_length != 1:
            # bisher: best_move = None  
            # Vorschlag: trotzdem eine Mauer setzen, 
            # wenn Gegnerweg < eigener Weg (Gegner führt) und Mauern übrig sind.
            if opponent_shortest_path_length < ai_shortest_path_length and best_move:
                best_move = best_move  # lasse Mauereinsatz zu
            else:
                best_move = None

     

        print("best move ", best_move)
        print("metric ", best_metric)

        if best_move is not None:
            return best_move, best_metric
        else:
            return None, best_metric
    
    best_move, _ = evaluate_move(game, Me, MyTarget, Opponent, OpponentTarget,   2)  # Depth set to 3 for this example
    return best_move

        