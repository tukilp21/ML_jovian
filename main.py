import random as r
import time

BOMB = "💀"
FLAG = "🚩"
UNKNOWN = "🔳"
ZERO = "◾"
INITIAL_VAL = ""
WIN = "💥"


# extra function ************************************
def randPoint(max_range, n_bomb):

    r.seed(time.time())
    radius = r.randrange(3)
    rangeX = (0, max_range)
    rangeY = (0, max_range)
    qty = n_bomb  # or however many points you want

    deltas = set()
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if x * x + y * y <= radius * radius:
                deltas.add((x, y))

    randPoints = []
    excluded = set()
    i = 0
    while i < qty:
        x = r.randrange(*rangeX)
        y = r.randrange(*rangeY)
        # if the point is within the radius range
        if (x, y) in excluded:
            continue
        # if not, add the point into randPoints & excluded
        randPoints.append((x, y))
        i += 1
        excluded.update((x + dx, y + dy) for (dx, dy) in deltas)
    return randPoints


def instruction():
    print("__________________________________________________")
    print("Intructions:\n")
    print("SYMBOL:")
    print(f"\t{UNKNOWN}: unknown spot")
    print(f"\t{ZERO}: opened spot")
    print(f"\t{FLAG}: flag placement")
    print("\nEnter the coordinate you want to press following syntax:")
    print("\tx_value\t(space)\ty_value")
    print("If u want to place a flag, use:")
    print("\tx_value\t(space)\ty_value\t(space)\tF")
    print("If u want to exit, use:")
    print("\texit")
    input("\nPress enter when u're ready\n")
    print("Enjoy")
    print("__________________________________________________")


def printcol(num):
    if num >= 10:
        return f"  {num} "
    else:
        return f"   {num} "


def printrow(num):
    if num >= 10:
        return f"{num}"
    else:
        return f" {num}"


# ****************************************************


class Tile:
    disp = False
    value = INITIAL_VAL
    cover = UNKNOWN

    def print(self, win=None):
        if self.disp:
            if self.value == 0:  # for nicer look
                return ZERO
            else:
                if self.value == BOMB:
                    if win == "win":
                        return f"{WIN}"
                    else:
                        return f"{self.value}"
                else:
                    return f" {self.value}"
        else:
            return self.cover

    # flag is a cover since when we display the value under it, the flag dissapear
    def flag(self):
        # place flag
        if self.cover == UNKNOWN:
            self.cover = FLAG
        # remove flag
        else:
            self.cover = UNKNOWN


class Field:
    win = False

    def __init__(self, size, no_bomb):
        data = []
        for row in range(size):
            row_data = []
            for col in range(size):
                # set class Tile for each idx of each row
                tmp = Tile()
                row_data.append(tmp)
            data.append(row_data)

        self.data = data
        self.size = size
        self.nbomb = no_bomb

        #run the game:
        self.setBomb()
        self.game()

    def __str__(self, end=False, win=False):
        # When Win or Lose --> display all bomb
        print_all_bomb = True if end else False

        value = ""  # return value to display the Field
        INITIAL = " " * 3

        # _______________________________________
        # x-axis:
        value += INITIAL
        for x_axis in range(self.size):
            value += printcol(x_axis)
        # clearer look
        value += "\n" + INITIAL
        for i in range(self.size):
            value += f"-----"
        # y-axis:
        value += "\n"
        for row in range(self.size):
            value += printrow(row) + "|"
            # value of each Tile:
            for col in range(self.size):

                if print_all_bomb and self.data[row][col].value == BOMB:
                    self.data[row][col].disp = True

                value += " " * 2
                if win:
                    tmp = "win"
                    value += f"{self.data[row][col].print(tmp)}"
                else:
                    value += f"{self.data[row][col].print()}"
                value += " " * 1

            # repeat y-axis for clearer look
            value += f" |{row} \n"

        # repeat x-axis for clearer look
        value += INITIAL
        for i in range(self.size):
            value += f"-----"
        value += "\n" + INITIAL
        for x_axis in range(self.size):
            value += printcol(x_axis)

        # _______________________________________
        value += "\n"
        return value

    def setBomb(self):
        points = randPoint(self.size, self.nbomb)

        for i in range(len(points)):
            x, y = points[i][0], points[i][1]
            self.data[x][y].value = BOMB

    # function to scan the target of User's choice:
    '''REVERSE X, Y (since for 2D list, we access the y-value before x-value)'''

    def scan_target(self, y, x, expanding=False):
        # --> this "scan_target" function can be used for 2 mode:
        # SCAN-ONLY MODE: scan this specific tile
        # EXPANDING MODE: recursively scan the surrounding tiles
        # _______________________________________________________________
        # for SCAN-ONLY mode:
        if not (expanding):
            # if there is a flag:
            if self.data[x][y].cover == FLAG:
                print("!! Please remove the flag !! \n")
                return
            # if hit a bomb
            if self.data[x][y].value == BOMB:
                self.data[x][y].disp = True
                return BOMB
            ctr = 0

        # get range for scanning --> scan a 3x3 square
        x_range = list(
            filter(lambda x: x in range(self.size), [x - 1, x, x + 1]))
        y_range = list(
            filter(lambda y: y in range(self.size), [y - 1, y, y + 1]))

        # scan 3x3:
        # --> record the number of Bombs surrounding the scan_target into "ctr"
        # --> set the target value = ctr
        for x_val in x_range:
            for y_val in y_range:

                # skip the target (square's center) value:
                if x_val == x and y_val == y:
                    continue

                # for SCAN-ONLY mode:
                if not (expanding):
                    # count the surrounding bombs
                    if self.data[x_val][y_val].value == BOMB:
                        ctr += 1

                # for EXPAND MODE:
                else:
                    # skip the displayed Tiles - already uncovered Tiles
                    if self.data[x_val][y_val].disp == True:
                        continue

                    # recursively "expanding"
                    self.scan_target(y_val, x_val)

        # for SCAN-ONLY mode:
        if not (expanding):
            self.data[x][y].value = ctr
            self.data[x][y].disp = True
            # after scanning, expand or not ? --> depend on ctr
            if ctr == 0:
                # begin expanding (set True)
                self.scan_target(y, x, True)
            else:
                return ctr

    # _______________________________________________________________

    # check for end-game condition
    def check(self, target_val=""):
        tmp = False
        # check for LOSE con.
        if target_val:
            if target_val == BOMB:
                print(self.__str__(True))
                print("\nOpps, u hit a bomb")
                print("Try again ?")
                tmp = True

        # check for WIN con.
        else:
            for row in range(self.size):
                for col in range(self.size):
                    # still have unknown tile
                    if self.data[row][col].value == INITIAL_VAL:
                        return tmp

            # True: if every tile is identified --> WIN
            tmp = True
            print(self.__str__(True, True))
            print("U freaking WONNNNN")
            self.win = True

        return tmp

    def flag(self, y, x):
        self.data[x][y].flag()

    def game(self):
        instruction()
        loop = True
        while loop:
            continuee = False  # to check for correct input data-type
            print(self)  # print field

            print("syntax: x_value  y_value  action")
            move = input("--> Enter your move: \n").split()

            # DIGGING condition
            if len(move) == 2:
                try:
                    x, y = map(int, move[:2])
                    action = ""
                    continuee = True
                except:
                    continuee = False

            # FLAGGING condition
            elif len(move) == 3:
                try:
                    x, y = map(int, move[:2])
                    action = move[2].upper()
                    continuee = True
                except:
                    continuee = False

            else:
                try:
                    # EXIT condition
                    if move[0] == "exit":
                        print("\nExiting the game")
                        break
                except:
                    pass
                print("\nWut wrong mah dude ?\n")
                continue

            # if correct data-type for inputs
            if continuee and x <= (self.size - 1) and y <= (self.size - 1):

                # digging action:
                if action == "":
                    tmp = self.scan_target(x, y)
                    # LOSE condition check ------------------
                    if self.check(tmp):
                        break

                # flagging action:
                elif action == "F":
                    self.data[y][x].flag()

                # wrong action:
                else:
                    print("Wrong input for \"action\", try again\n")
                    continue

                # WIN condition check -----------------------
                if self.check():
                    break

            else:
                print("Wrong input data, try again \n")


def line_space(character):
    return character * 37 + "\n"


def scoreboard(game_mode, w_time):
    if game_mode == "custom":
        return "Congrats !"
    name = input("\nEnter your name (no space): ")
    # name length < 15
    try:
        name = name.replace(name, name[:15])
        if " " in name:
            print("SYNTAX ERROR")
            scoreboard(game_mode, w_time)
    except:
        pass

    sb = open(f"scoreboard/{game_mode}", "a+")

    # WRITE SCORE _____________________________________
    decor = line_space("~")
    rank = 0
    sb.write(f"{rank: <10}{name: <20}{w_time}\n{decor}")

    # GET LINES' DATA _________________________________
    sb.seek(0)
    data = sb.readlines()
    # remove headers
    for i in range(2):
        data.pop(0)
    # get a temporary formatted data
    tmp = list(filter(lambda x: x != decor, data))
    for i in range(len(tmp)):
        tmp[i] = tmp[i].split()
    tmp[-1].append(0)

    # ORDERize ________________________________________
    tmp.sort(key=lambda x: float(x[2]))
    for i in range(len(data)):
        if i % 2 == 0:
            if len(tmp[i // 2]) == 4:
                # insert line & line_space -> loop 2 times
                for k in range(2):
                    data.insert(i, data[-1])
                    data.pop(-1)
                inserted_idx = i
            # rewrite ranking num:
            rank = i // 2 + 1
            if rank < 10:
                data[i] = f" {rank}" + data[i][2:]
            else:
                data[i] = f"{rank}" + data[i][2:]
    sb.close()

    # REWRITE SCOREBOARD ______________________________
    f_sb = open(f"scoreboard/{game_mode}", "w+")
    # insert header
    header = ("RANK", "NAME", "TIME")
    decor = line_space("*")
    data.insert(0, f"{header[0]: <10}{header[1]: <20}{header[2]}\n{decor}")
    # rewrite
    f_sb.writelines(data)
    # read data
    f_sb.seek(0)
    noti = f_sb.readlines()
    f_sb.close
    # player's idx
    idx = inserted_idx + 2  # exclude the headers
    # print board
    print("\n!!! Top 5 on the scoreboard !!!\n")  #12 lines
    try:
        for i in range(12):
            print(noti[i], end="")
        if idx > 12:
            print("\t\t ...")
            # idx +-1 for print line_space
            # nicer look
            return f"\n--> Your rank:\n{noti[idx-1]}{noti[idx]}{noti[idx+1]}"
    except:
        pass
    return f"\n Congrats, u in the top 5"


def play():
    print("-------------------------------")
    print("What type do you want to play ?")
    print("\t 1. Easy: 9x9 with 10 bombs")
    print("\t 2. Normal: 16x16 with 40 bombs")
    print("\t 3. Easiest: 22x22 with 99 bombs")
    print("\t 4. Custom size and bomb")
    try:
        x = int(input("\nEnter your choice: "))
    except:
        return print("Syntax error")

    # make Switch case later xD
    if x == 1:
        size, bomb = 9, 10
        mode = "9x9"
    elif x == 2:
        size, bomb = 16, 40
        mode = "16x16"
    elif x == 3:
        size, bomb = 22, 99
        mode = "22x22"
    elif x == 4:
        size = int(input("Enter the size: "))
        recommendMaxBomb = round(size**2 * 0.16 + size)
        bomb = int(
            input(
                f"Enter num of bomb (should not exceed {recommendMaxBomb}): "))
        mode = "custom"
    else:
        return print("Wrong input choice")

    start_time = time.time()
    game = Field(size, bomb)

    # IF WIN:
    if game.win:
        win_time = round(time.time() - start_time, 3)
        print(f"\nTime taken: {win_time}s")
        print(scoreboard(mode, win_time))

    return print("_" * 50 + "\n")


# ________________________________________________________
if __name__ == "__main__":
    play()
