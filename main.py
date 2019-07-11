from numpy.random import randint # just because it is the fastest...
from random import choice
from itertools import product
import sys

class BattleshipFieldDesigner:
    def __init__(self, board_dim = 5):
        self.board_dim = board_dim
        self.board = self.generate_initial_board(self.board_dim) #[ ["0"] * self.board_dim ] * self.board_dim    # matrix of (board_dim X board_dim).
        self.grid_cells = list(product(list(range(board_dim)), repeat=2))   # list of possible combintaions.
        self.filled_spaces = []
        self.orientation = ["h", "v"]
        self.vessle_count = {
            "submarine_count" : 0,
            "destroyer_count" : 0,
            "cruiser_count" : 0,
            "aircraft_carrier_count" : 0
        }
        self.fleet_dict = {
            "submarine_size" : [ 1, 1 ],
            "destroyer_size" : [ 2, 1 ],
            "cruiser_size" : [ 3, 1 ],
            "aircraft_carrier_size" : [ 4, 1 ]
            }

    def generate_initial_board(self, dim):
        rows = cols = dim
        out = []
        for i in range(rows):
            _tmp = []
            for j in range(cols):
                _tmp.append("0")
            out.append(_tmp)
        return out
    
    def get_adjacent_cells(self, x, y, dim, orientation):
        if orientation == 'h':
            r = [i for i in range( y - (dim[0] - 1), y + dim[0] )]
            options = zip([x for i in range(len(r))], r)
        elif orientation == 'v':
            r = [i for i in range( x - (dim[0] - 1), x + dim[0] )]
            options = zip(r, [y for i in range(len(r))])
        else:
            print(f"Orientation is Invalid ! - {orientation}.")
            print("Exiting....")
            sys.exit(1)
        # removing cells that are not in grid/board.
        options_list = list(options)
        for op in options_list:
            if op not in self.grid_cells or op[0]<0 or op[1]<0:
                options_list.remove(tuple(op))
                
        if dim[0] > 1:
            if len(options_list) > 2:
                split_index = options_list.index(tuple([x, y]))
                first = options_list[:split_index]
                second = options_list[split_index+1:]

                if len(first) != (dim[0] - 1) and len(second) == (dim[0] - 1):
                    adj = second
                elif len(first) == (dim[0] - 1) and len(second) != (dim[0] - 1):
                    adj = first
                else: # randomly choose one..
                    adj = choice([first, second])
                    print(f"randomly choose {adj}")
            else:
                adj = options_list.remove(tuple([x, y]))
        else:
            adj = choice(options_list)
        return list(adj)

    def get_random_location(self, dim):
        """Genterates and returns random location (int, int) to put vessle on."""
        loc = randint(0, self.board_dim, size=2).tolist()
        if dim != [1, 1]:   # if ship is NX1
            orientation = choice(self.orientation)
            adj = self.get_adjacent_cells(x=loc[0], y=loc[1], dim=dim, orientation=orientation)
            loc = [loc]
            for i in adj:
                loc.append(list(i))
        return loc

    def placeSubmarine(self):
        """places a submarine (1x1) on the board at a random location."""
        size = 'submarine_size'
        if self.vessle_count['submarine'] == int(self.board_dim**2 / self.fleet_dict[size][0]):
            print("No More Room for Submarine!")
            self.hard_exit()
        if self.is_full(): self.hard_exit()
        rand_loc = self.get_random_location(dim = self.fleet_dict[size])
        while(rand_loc in self.filled_spaces):
            rand_loc = self.get_random_location(dim = self.fleet_dict[size])
        self.filled_spaces.append(rand_loc)
        i , j = rand_loc
        self.vessle_count['submarine_count'] += 1
        self.board[i][j] = f"S{self.vessle_count['submarine_count']}"

    def placeDestroyer(self):
        """places a destroyer (2x1) on the board at a random location, either vertically or horizontally."""
        size = 'destroyer_size'
        if self.vessle_count['destroyer_count'] == int(self.board_dim**2 / self.fleet_dict[size][0]):
            print("No More Room for destroyer!")
            self.hard_exit()
        if self.is_full(): self.hard_exit()
        rand_loc = self.get_random_location(dim = self.fleet_dict[size])
        trial_count = 0
        while(any([x for x in rand_loc if x in self.filled_spaces]) and trial_count<100):
            rand_loc = self.get_random_location(dim = self.fleet_dict[size])
            trial_count += 1
        if trial_count > 100: self.hard_exit()
        self.filled_spaces += rand_loc
        self.vessle_count['destroyer_count'] += 1
        for cord in rand_loc:
            i = cord[0]
            j = cord[1]
            self.board[i][j] = f"D{self.vessle_count['destroyer_count']}"

    def placeCruiser(self):
        """places a cruiser (3x1) on the board at a random location, either vertically or horizontally."""
        size = 'cruiser_size'
        if self.vessle_count['cruiser_count'] == (int(self.board_dim**2 / self.fleet_dict[size][0])-1):
            print("No More Room for cruiser!")
            self.hard_exit()
        if self.is_full(): self.hard_exit()
        rand_loc = self.get_random_location(dim = self.fleet_dict[size])
        trial_count = 0
        while(any([x for x in rand_loc if x in self.filled_spaces]) and trial_count<100):
            rand_loc = self.get_random_location(dim = self.fleet_dict[size])
            trial_count += 1
        if trial_count > 100: self.hard_exit()
        self.filled_spaces += rand_loc
        self.vessle_count['cruiser_count'] += 1
        for cord in rand_loc:
            i = cord[0]
            j = cord[1]
            self.board[i][j] = f"C{self.vessle_count['cruiser_count']}"

    def placeCarrier(self):
        """places an aircraft carrier (4x1) on the board at a random location, either vertically or horizontally."""
        size = 'aircraft_carrier_size'
        if self.vessle_count['aircraft_carrier_count'] == int(self.board_dim**2 / self.fleet_dict[size][0]):
            print("No More Room For aircraft carrier!")
            self.hard_exit()
        if self.is_full(): self.hard_exit()
        rand_loc = self.get_random_location(dim = self.fleet_dict[size])
        trial_count = 0
        while(any([x for x in rand_loc if x in self.filled_spaces]) and trial_count<100):
            rand_loc = self.get_random_location(dim = self.fleet_dict[size])
            trial_count += 1
        if trial_count > 100: self.hard_exit()
        self.filled_spaces += rand_loc
        self.vessle_count['cruiser_count'] += 1
        for cord in rand_loc:
            i = cord[0]
            j = cord[1]
            self.board[i][j] = f"AC{self.vessle_count['cruiser_count']}"
    
    def print_board(self):
        """Preety-Print Game Board."""
        print("")
        print("-" * int((self.board_dim**2) * 1.5))
        for i in range(self.board_dim):
            row = self.board[i]
            print(' \t'.join(row))
        print("-" * int((self.board_dim**2) * 1.5))
        print("")

    def is_empty(self):
        """Check if board is empty"""
        _tmp = [ ["0"] * self.board_dim ] * self.board_dim
        return True if self.board == _tmp else False

    def is_full(self):
        """Check if board is full"""
        count = 0
        for i in range(self.board_dim):
            for j in range(self.board_dim):
                if self.board[i][j] != '0':
                    count += 1
        return True if count == self.board_dim**2 else False
        
    def hard_exit(self):
        print("Board is Full !")
        print("Exiting...")
        sys.exit(0)

    # TODO : make work
    def run(self):    
        ops = [ 'S', 'D', 'C', 'AC' ]
        welcome_message = "Hello and Welcome to Battleship Field Designer!"
        print(f"[{'#'*(len(welcome_message)-2)}]")
        print(welcome_message)
        print(f"[{'#'*(len(welcome_message)-2)}]")
        print("Let's Begin !")
        while(not self.is_full()):
            print("Vessels options : [ submarine (S), destroyer (D), cruiser (C), aircraft carrier (AC) ]")
            print(f"Vessels Synomems : {ops}")
            c = input("Please use Synomems to select a vessel to put:")
            if c == 'X':
                self.print_board()
                print("Bye Bye!")
                break
            while(c not in ops):
                print(f"unsupported Vessel! please choose from {', '.join(ops)}")
                c = input("Please use Synomems to select a vessel to put (X to exit):")
                if c == 'X':
                    self.print_board()
                    print("Bye Bye!")
                    break
            print("Randomly putting Vessel....")
            if c == 'S': self.placeSubmarine
            elif c == 'D': self.placeDestroyer
            elif c == 'C': self.placeCruiser
            elif c == 'AC': self.placeCarrier
            else:
                if c == 'X':
                    self.print_board()
                    print("Bye Bye!")
                    break
            print("")
            self.print_board()
 


if __name__ == '__main__':
    bfd = BattleshipFieldDesigner()
    bfd.run()
