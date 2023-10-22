import random, copy

class Player:
    def __init__(self, name):
        self.name = name
        self.grid = [[0, 0, 0] for _ in range(3)]
        self.score = 0

    def toss_coin(self):
        return random.randint(1, 6)

    def place_coin(self, coin, col):
        for row in reversed(range(3)):
            if self.grid[row][col] == 0:
                self.grid[row][col] = coin
                break

    def update_score(self):
        self.score = 0
        for col in range(3):
            column_values = [self.grid[row][col] for row in range(3)]
            counts = [column_values.count(i) for i in range(1, 6 + 1)]
            for i, count in enumerate(counts):
                if(count > 0):
                    self.score += (i + 1) * (count ** 2)

    def is_grid_full(self):
        return all(self.grid[i][j] != 0 for i in range(3) for j in range(3))

    def print_grid(self):
        for row in self.grid[:-1]:
            print(' | '.join(str(x) if x != 0 else ' ' for x in row))
            print('---------')
        print(' | '.join(str(x) if x != 0 else ' ' for x in self.grid[-1]))

    def fall_coins(self):
        for col in range(3):
            column_values = [self.grid[row][col] for row in range(3) if self.grid[row][col] != 0]
            column_values = [0]*(3-len(column_values)) + column_values
            for row in range(3):
                self.grid[row][col] = column_values[row]

class AIPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def best_move(self, opponent, coin):
        depth = 4
        valid_columns = [col for col in range(3) if self.grid[0][col] == 0]
        best_value = float('-inf')
        best_col = valid_columns[0]

        gridsc, gridoc = [self.grid.copy()]+[[] for _ in range(2*depth+1)], [opponent.grid.copy()]+[[] for _ in range(2*depth+1)]

        for col in valid_columns:
            #print(f"Trying column {col} for {coin}...")
            self.grid, opponent.grid = copy.deepcopy(gridsc[0]), copy.deepcopy(gridoc[0])
            self.grid[0][col] = coin

            for row in range(3):
                if opponent.grid[row][col] == coin:
                    opponent.grid[row][col] = 0
            self.fall_coins()
            opponent.fall_coins()
            
            #print("AI bro")
            #self.print_grid()
            #print("Human bro")
            #opponent.print_grid()

            gridsc[1], gridoc[1] = self.grid.copy(), opponent.grid.copy()

            if(gridsc[0] != [[0, 0, 0], [0, 0, 0], [0, 0, 0]]) or (gridoc[0] != [[0, 0, 0], [0, 0, 0], [0, 0, 0]]):
                if (col == 0) or ([gridsc[0][row][col] for row in range(3)] + [gridoc[0][row][col] for row in range(3)] != [gridsc[0][row][col - 1] for row in range(3)] + [gridoc[0][row][col - 1] for row in range(3)]):
                    move_value = self.expectiminimax(1, depth, opponent, gridsc, gridoc)
                    if(col == 0):
                        saved_value = move_value
                elif (col == 2) and ([gridsc[0][row][2] for row in range(3)] + [gridoc[0][row][2] for row in range(3)] == [gridsc[0][row][0] for row in range(3)] + [gridoc[0][row][0] for row in range(3)]):
                    move_value = saved_value
            else:
                move_value = 0

            print(f"Value for column {col}: {move_value}")
            if move_value > best_value:
                best_col = col
                best_value = move_value
    
        #print(f"Best column to move: {best_col}")
        self.grid, opponent.grid = copy.deepcopy(gridsc[0]), copy.deepcopy(gridoc[0])
        return best_col

    def expectiminimax(self, depth, maxdepth, opponent, gridsc, gridoc):
        if depth > maxdepth or self.is_grid_full():
            self.update_score()
            opponent.update_score()
            #print(f"Evaluated score: {self.score-opponent.score}")
            return self.score-opponent.score

        if depth % 2 == 0:  # Maximizing player's turn
            expected_value = 0
            self.grid, opponent.grid = copy.deepcopy(gridsc[depth]), copy.deepcopy(gridoc[depth])
            for dice_roll in range(1, 7):
                max_eval = float('-inf')
                for col in range(3):
                    if self.grid[0][col] == 0:
                        #print(f"Maximizing: Trying dice roll {dice_roll} for column {col} (Depth {depth})")
                        self.grid[0][col] = dice_roll
                        for row in range(3):
                            if opponent.grid[row][col] == dice_roll:
                                opponent.grid[row][col] = 0
                        self.fall_coins()
                        opponent.fall_coins()
                        
                        #print("AI bro")
                        #self.print_grid()
                        #print("Human bro")
                        #opponent.print_grid()
                        
                        gridsc[depth + 1], gridoc[depth + 1] = self.grid.copy(), opponent.grid.copy()
                        max_eval = max(max_eval, self.expectiminimax(depth + 1, maxdepth, opponent, gridsc, gridoc))
                        self.grid, opponent.grid = copy.deepcopy(gridsc[depth]), copy.deepcopy(gridoc[depth])
                expected_value += (1/6) * max_eval
            return expected_value
        else:  # Minimizing player's turn
            expected_value = 0
            self.grid, opponent.grid = copy.deepcopy(gridsc[depth]), copy.deepcopy(gridoc[depth])
            for dice_roll in range(1, 7):
                min_eval = float('inf')
                for col in range(3):
                    if opponent.grid[0][col] == 0:
                        #print(f"Minimizing: Trying dice roll {dice_roll} for column {col} (Depth {depth})")
                        opponent.grid[0][col] = dice_roll
                        for row in range(3):
                            if self.grid[row][col] == dice_roll:
                                self.grid[row][col] = 0
                        self.fall_coins()
                        opponent.fall_coins()
                        
                        #print("AI bro")
                        #self.print_grid()
                        #print("Human bro")
                        #opponent.print_grid()
                        
                        gridsc[depth + 1], gridoc[depth + 1] = self.grid.copy(), opponent.grid.copy()
                        min_eval = min(min_eval, self.expectiminimax(depth + 1, maxdepth, opponent, gridsc, gridoc))
                        self.grid, opponent.grid = copy.deepcopy(gridsc[depth]), copy.deepcopy(gridoc[depth])
                expected_value += (1/6) * min_eval
            return expected_value


class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = 0
        print("\nWelcome to the Coin Game! Each player takes turns to toss a coin and place it in a column on their grid. The game ends when any player's grid is full. The player with the highest score wins!")

    def play_turn(self):
        player = self.players[self.current_player]
        opponent = self.players[1 - self.current_player]
        coin = player.toss_coin()

        print(f"\n{player.name} rolled a {coin}!")
        print("\nCurrent board configuration:")
        print(f"{player.name}'s grid (score {self.players[self.current_player].score}):")
        player.print_grid()
        print(f"{opponent.name}'s grid (score {self.players[1 - self.current_player].score}):")
        opponent.print_grid()

        if isinstance(player, AIPlayer):
            col = player.best_move(opponent, coin)  # Determine the best move based on the dice roll
            print(f"\n{player.name} rolled a {coin} and selected column {col}.")
        else:
            while True:
                try:
                    col = int(input("Enter the column (0-2) to place the coin: "))
                    if 0 <= col <= 2 and player.grid[0][col] == 0:
                        break
                    else:
                        print("Invalid position, please try again.")
                except ValueError:
                    print("Invalid input, please enter a number between 0 and 1.")

        player.place_coin(coin, col)
        for row in range(3):
            if opponent.grid[row][col] == coin:
                opponent.grid[row][col] = 0
        opponent.update_score()
        player.update_score()
        player.fall_coins()
        opponent.fall_coins()

        self.current_player = 1 - self.current_player

    def play_game(self):
        while not any(player.is_grid_full() for player in self.players):
            self.play_turn()
        
        player = self.players[self.current_player]
        opponent = self.players[1 - self.current_player]

        opponent.update_score()
        player.update_score()

        scores = [player.score for player in self.players]
        winner = self.players[scores.index(max(scores))].name
        print(f"\nThe winner is {winner} with a score of {max(scores)}!\n")
        print("Final Board:\n")

        print(f"{player.name}'s grid (score {self.players[self.current_player].score}):")
        player.print_grid()
        print(f"{opponent.name}'s grid (score {self.players[1 - self.current_player].score}):")
        opponent.print_grid()

if __name__ == '__main__':
    player1 = Player("Player 1")
    player2 = AIPlayer("AI Player")
    game = Game(player1, player2)
    game.play_game()
