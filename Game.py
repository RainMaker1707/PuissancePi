"""
Connect 4 game
Used to learn AI to play at the game
Not finished, at this moment you can play in GUI with left click
And only win on vertical and horizontal line
"""
from tkinter import *
import tkinter.messagebox as msg_box
from PreProcess import image_process


class Game:
    """
    Connect 4 with tkinter GUI or terminal play
    """
    def __init__(self, processed_img: list):
        """
        :param processed_img: pixel data set matrix processed by image_process from Process module
        """

        self.initialised = True
        self.matrix = processed_img
        self.played = False
        self.current_player = 'R'
        self.current_player_color = 'red'
        self.win = Tk()
        self.canvas = Canvas(master=self.win, width=715, height=615)
        self.grid = []
        self.row_line = [0, 0, 0, 0, 0, 0, 0]
        self.row = 0

    def __str__(self):
        temp_string = ""
        matrix = self.get_board_matrix()
        for i in range(len(matrix)):
            temp_string += str(matrix[i]) + "\n"
        temp_string += "\n"
        return temp_string

    # ------- Getter and Setter ------

    def get_init(self):
        return self.initialised

    def get_board_matrix(self):
        return self.matrix

    def get_played(self):
        return self.played

    def get_current_player(self):
        return self.current_player

    # ---- Methods ----
    def next_player(self):
        if self.current_player == 'R':
            self.current_player = 'Y'
            self.current_player_color = 'yellow'
        else:
            self.current_player = 'R'
            self.current_player_color = 'red'

    def set_played(self):
        self.played = True

    def play_on_screen(self):
        """
        GUI user friendly game board, play with click
        Use tkinter and feed a canvas with a blue board
        Set case with gray circle
        And finally set case with player color when played
        """
        self.canvas.pack()
        self.canvas.create_rectangle(0, 0, 714, 614, fill="blue")
        for i in range(7):
            self.grid.append([])
            for j in range(6):
                self.grid[i].append(self.canvas.create_oval(10 + 100 * i, 10 + 100 * j, 100 + 100 * i, 100 + 100 * j,
                                                            fill="grey"))
            self.grid[i].reverse()
        self.win.wm_title('Puissance-Pi')
        self.canvas.bind("<Button-1>", self.clicked)
        self.win.mainloop()

    def clicked(self, position):
        """
        activated at each user click
        set up the player turn as the next player
        update the matrix to the new game statement
        and manage the self.row_line which is used to know which matrix line feed
        :param position: X, Y position of clicked, used to know row to play
        """
        self.row = int(position.x / 100)
        if self.row < len(self.grid) and self.row_line[self.row] < len(self.grid[0]):
            self.canvas.itemconfig(self.grid[self.row][self.row_line[self.row]], fill=self.current_player_color)
        else:
            return
        self.matrix_update(self.row_line[self.row], self.row)
        self.next_player()
        self.row_line[self.row] += 1
        test = self.check_victory()
        if test:
            self.next_player()
            self.canvas.update()
            msg_box.showinfo('Puissance Pi', 'Victory!\n' + self.current_player_color.capitalize() + ' player won!')
            self.win.destroy()
        elif test is None:
            self.canvas.update()
            msg_box.showinfo('Puissance Pi', 'Congratulations,\nIt was a nice game but nobody won..')
            self.win.destroy()

    def play_on_terminal(self):
        """
        game Connect 4 on terminal.
        user input is an int in [1,2,3,4,5,6,7] minus one to obtain index of row played.
        self.row_line is used to know the index of line to feed.
        """
        victory_test = self.check_victory()
        while not victory_test and victory_test is not None:
            print("\nGame Board\n")
            print(self)
            user_in = input("Which row are you gonna play?\n--->").strip()
            int_typed = False
            while not int_typed:
                try:
                    user_in = int(user_in) - 1
                    int_typed = True
                    while not 0 <= user_in < 7:
                        print("Choose value between 1 and 7 please.")
                        user_in = int(input("Which row are you gonna play?\n--->").strip()) - 1
                except ValueError:
                    print('Type a number between 0 and 5 : 0 >= number > 6')
                    user_in = input("Which row are you gonna play?\n--->").strip()
            self.matrix_update(self.row_line[user_in], user_in)
            self.row_line[user_in] += 1
            self.next_player()
            victory_test = self.check_victory()
        if victory_test:
            print("\nGame Board\n")
            print(self)
            self.next_player()
            print(str("Victory! Congratulations " + self.current_player_color.capitalize() + " Player!"))
        elif victory_test is None:
            print("\nGame Board\n")
            print(self)
            print('Congratulations,\nIt was a nice game but nobody won..')

    def matrix_update(self, x, y):
        """
        reverse the matrix to better feed it with the index from terminal or GUI
        set up the right case at the player color if it's not empty
        and reverse again to have a great schematic of the game
        """
        self.matrix.reverse()
        self.matrix[x][y] = self.current_player
        self.matrix.reverse()

    def check_victory(self):
        """
        :return: True if one player won False else
        """
        def horizontal_victory(game_state: list):
            """
            :param game_state: matrix of processed state of game
            :return:
            """
            for i in range(len(game_state)):
                counter = 1
                for j in range(len(game_state[i])-1):
                    if (game_state[i][j] in ['Y', 'R']) and (game_state[i][j] == game_state[i][j+1]):
                        counter += 1
                        if counter == 4:
                            return True
                    else:
                        counter = 1
            return False

        def vertical_victory(game_state: list):
            """
            :param game_state: matrix of processed state of game
            :return:
            """
            for i in range(len(game_state[0])):
                counter = 1
                for j in range(len(game_state) - 1):
                    if (game_state[j][i] in ['Y', 'R']) and (game_state[j][i] == game_state[j + 1][i]):
                        counter += 1
                        if counter == 4:
                            return True
                    else:
                        counter = 1
            return False

        def diagonal_victory(game_state: list):
            """
            :param game_state: matrix of processed state of game
            :return:
            """
            # diagonals up left to bot right based at 0,0; 1,O and 2,0
            for i in range(len(game_state)):
                pawn_counter = 1
                for j in range(len(game_state)):
                    try:
                        if game_state[i + j][j] in ['Y', 'R'] and game_state[i + j][j] == game_state[i + j + 1][j + 1]:
                            pawn_counter += 1
                            if pawn_counter == 4:
                                return True
                    except IndexError:
                        break
            # diagonals up left to bot right based at 0,0; 0,1; 0,2 and 0,3
            for k in range(len(game_state)):
                pawn_counter = 1
                for l in range(len(game_state)):
                    try:
                        if game_state[l][k + l] in ['Y', 'R'] and game_state[l][k + l] == game_state[l + 1][k + l + 1]:
                            pawn_counter += 1
                            if pawn_counter == 4:
                                return True
                    except IndexError:
                        break
            # diagonals up right to bot left based at 0,6; 1,6 and 2,6
            for m in range(len(game_state)):
                pawn_counter = 1
                for n in range(len(game_state)):
                    try:
                        if game_state[m + n][6 - n] in ['Y', 'R'] and game_state[m + n][6 - n] == game_state[m + n + 1][
                                                                                                            6 - n - 1]:
                            pawn_counter += 1
                            if pawn_counter == 4:
                                return True
                    except IndexError:
                        break
            # diagonals up right to  bot left based at 0,3; 0,4; 0,5 and 0,6
            for o in range(len(game_state)):
                pawn_counter = 1
                for p in range(len(game_state)):
                    try:
                        if game_state[p][6 - p - o] in ['Y', 'R'] and game_state[p][6 - p - o] == game_state[p + 1][
                                                                                                        6 - p - o - 1]:
                            pawn_counter += 1
                            if pawn_counter == 4:
                                return True
                    except IndexError:
                        break
            return False

        if horizontal_victory(self.matrix):
            return True
        elif vertical_victory(self.matrix):
            return True
        elif diagonal_victory(self.matrix):
            print('ever victory diagonal')
            return True
        elif self.matrix[0].count('E') == 0:
            return None
        return False


game = Game(image_process("data_set/test_set/template.jpg", "data_set/test_set/template.jpg"))
print("Welcome on Connect 4 Game !")
game.play_on_screen()
game.play_on_terminal()
