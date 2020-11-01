from bangtal import *

check = 0

class Stone(Object):
    status = 0  # 0= BLANK, 1=POSSIBLE, 2=BLACK, 3=WHITE
    x = 0
    y = 0
    vis = False


    def __init__(self,image,x,y):
        super().__init__(image)
        self.d_x = x
        self.d_y = y

    def change_stone_status(self,num,poss=True):
        if num == 0:
            self.status = 0
            self.setImage(IMG_DIR + "blank.png")
        elif num == 1:
            self.status = 1
            if poss == True:
                self.setImage(IMG_DIR + "black possible.png")
            else:
                self.setImage(IMG_DIR + "white possible.png")
            self.show()

        elif num == 2:
            self.status = 2
            self.vis =True
            self.setImage(IMG_DIR+"black.png")
            self.show()
            print("#")

        elif num == 3:
            self.status = 3
            self.vis = True
            self.setImage(IMG_DIR+"white.png")
            self.show()

    def onMouseAction(self, x, y, action):
        global now_turn
        global scene_game, stone_obj_list
        global check

        if not self.status == 1:
            showMessage("둘 수 없는 위치")
            return 0


        if now_turn == True:
                check_deep_search_to_change(self.d_x, self.d_y, True, stone_obj_list)
                change_turn(stone_obj_list)
                print("black")
                self.change_stone_status(2)
                now_turn = False
                count = check_possible_white(scene_game,stone_obj_list)
                if check_end(stone_obj_list):
                    check = 1
                if count == 0:
                    if check > 0:
                        showMessage("GameEND")
                    else:
                        showMessage("둘 곳이 없습니다. 턴 넘김")
                    change_turn(stone_obj_list)
                    check += 1
                else:
                    check = 0
                calc_score(scene_game, stone_obj_list)
        elif now_turn == False:
                check_deep_search_to_change(self.d_x, self.d_y, False, stone_obj_list)
                change_turn(stone_obj_list)
                print("white")
                self.change_stone_status(3)
                now_turn = True
                count = check_possible_black(scene_game, stone_obj_list)
                if check_end(stone_obj_list):
                    check = 1
                if count == 0:
                    if check > 0:
                        showMessage("GameEND")
                    else:
                        showMessage("둘 곳이 없습니다. 턴 넘김")
                    change_turn(stone_obj_list)
                    check += 1
                else:
                    check = 0
                calc_score(scene_game, stone_obj_list)




    # if self.status
    #
    # height = len(chip_list) * 10 + 600
    # hide_cards()
    #
    # bet_money += 25
    # chip = Object(IMG_DIR + "chip.png")
    # chip.setScale(0.05)
    # chip.locate(scene_table, height, 200)
    # chip.show()
    # chip_list.append(chip)

def check_end(stone_obj_list):
    count = 0
    for i in range(8):
        for j in range(8):
            if stone_obj_list[i][j].status > 1:
                count += 1
    if count == 64:
        return True
    return False


def calc_score(scene,stone_obj_list):
    white_count = 0
    black_count = 0
    for i in range(8):
        for j in range(8):
            if stone_obj_list[i][j].status == 2:
                black_count += 1
            if stone_obj_list[j][i].status == 3:
                white_count += 1

    print(white_count)
    print(black_count)
    global black_score_2,black_score_1,white_score_1,white_score_2


    if black_count > 9:
        num1 = int(black_count / 10)
        num2 = black_count % 10
        black_score_1.setImage(IMG_DIR + "L" + str(num1) + ".png")
        black_score_1.locate(scene, 750, 220)
        black_score_2.setImage(IMG_DIR + "L" + str(num2) + ".png")
        black_score_2.locate(scene, 820, 220)
        black_score_1.show()
        black_score_2.show()
    else:
        black_score_1.setImage(IMG_DIR + "L" + str(black_count) + ".png")
        black_score_1.locate(scene,820,220)
        black_score_1.show()
        black_score_2.hide()


    if white_count > 9:
        num1 = int(white_count / 10)
        num2 = white_count % 10
        white_score_1.setImage(IMG_DIR + "L" + str(num1) + ".png")
        white_score_1.locate(scene, 1080, 220)
        white_score_2.setImage(IMG_DIR + "L" + str(num2) + ".png")
        white_score_2.locate(scene, 1150, 220)
        white_score_1.show()
        white_score_2.show()
    else:
        white_score_1.setImage(IMG_DIR + "L" + str(white_count) + ".png")
        white_score_1.locate(scene,1080,220)
        white_score_1.show()
        white_score_2.hide()

def check_deep_search(i,j,color,stone_obj_list):  #black = True / white = False
    dir_x_list = [-1, 0, 1]
    dir_y_list = [-1, 0, 1]
    possible_list = []
    max = 7

    for dir_x in dir_x_list:
        for dir_y in dir_y_list:
            now_x = i
            now_y = j
            cont = True
            in_process = False

            if dir_x == 0 and dir_y == 0:
                continue
            while cont == True:
                now_x += dir_x
                now_y += dir_y
                if now_x < 0 or now_x > 7 or now_y < 0 or now_y > 7:
                    cont = False
                    break

                next_stone = stone_obj_list[now_x][now_y]
                if color == True:
                    my_status = 2
                    your_status = 3
                else:
                    my_status = 3
                    your_status = 2

                if next_stone.status == your_status:
                    in_process = True
                elif next_stone.status == 0 and in_process == True:
                    possible_list.append([now_x,now_y])
                    cont = False
                else:
                    cont = False


    print(possible_list)
    return possible_list


def change_turn(stone_obj_list):
    for i in range(8):
        for j in range(8):
            if stone_obj_list[i][j].status == 1:
                stone_obj_list[i][j].change_stone_status(0,True)
                stone_obj_list[i][j].show()


def check_deep_search_to_change(i,j,color,stone_obj_list):  #black = True / white = False
    dir_x_list = [-1, 0, 1]
    dir_y_list = [-1, 0, 1]
    possible_list = []
    max = 7

    for dir_x in dir_x_list:
        for dir_y in dir_y_list:
            stack = []
            now_x = i
            now_y = j
            cont = True
            in_process = False

            if dir_x == 0 and dir_y == 0:
                continue
            while cont == True:
                now_x += dir_x
                now_y += dir_y
                if now_x < 0 or now_x > 7 or now_y < 0 or now_y > 7:
                    cont = False
                    break

                next_stone = stone_obj_list[now_x][now_y]
                if color == True:
                    my_status = 2
                    your_status = 3
                else:
                    my_status = 3
                    your_status = 2

                if next_stone.status == your_status:
                    stack.append([now_x,now_y])
                    in_process = True
                elif next_stone.status == my_status and in_process == True:
                    possible_list.append([now_x,now_y])
                    for x,y in stack:

                        stone_obj_list[x][y].change_stone_status(my_status)
                    cont = False
                else:
                    cont = False

    print("--pos--")
    print(possible_list)
    print("--pos--")
    return possible_list




def check_possible_black(scene,stone_obj_list):
    poss_list = []
    count = 0
    for i in range(8):
        for j in range(8):
            stone = stone_obj_list[i][j]
            if stone.status == 2:
                poss_list.append(check_deep_search(i,j,True,stone_obj_list))
    for possible_list in poss_list:
        for [i,j] in possible_list:
            print([i,j])
            count += 1
            stone_obj_list[i][j].change_stone_status(1)
    print("black : "+str(count))

    return count



def check_possible_white(scene,stone_obj_list):
    poss_list = []
    count = 0
    for i in range(8):
        for j in range(8):
            stone = stone_obj_list[i][j]
            if stone.status == 3:
                poss_list.append(check_deep_search(i,j,False,stone_obj_list))
    for possible_list in poss_list:
        for [i,j] in possible_list:
            print([i,j])
            count += 1
            stone_obj_list[i][j].change_stone_status(1,False)
    print("white : "+str(count))
    return count












IMG_DIR = "./Images/"
INIT_Y = 600
INIT_X = 40

now_turn = True  # True > black  / False > white
scene_game = Scene("game1",IMG_DIR+"background.png")

black_score_1 = Object(IMG_DIR + "L9" + ".png")
black_score_2 = Object(IMG_DIR + "L9" + ".png")
white_score_1 = Object(IMG_DIR + "L9" + ".png")
white_score_2 = Object(IMG_DIR + "L9" + ".png")

game_map = [[0]*8 for _ in range(8)]
stone_obj_list = []
x = INIT_X
y = INIT_Y

for i in range(8):
    tmp_list =[]
    for j in range(8):
        stone_obj = Stone(IMG_DIR+"blank.png",i,j)
        stone_obj.locate(scene_game,x,y)
        y -= 80
        stone_obj.show()
        stone_obj.change_stone_status(0)

        tmp_list.append(stone_obj)

    stone_obj_list.append(tmp_list)
    y = INIT_Y
    x += 80

stone_obj_list[3][3].change_stone_status(2)
stone_obj_list[3][4].change_stone_status(3)
stone_obj_list[4][4].change_stone_status(2)
stone_obj_list[4][3].change_stone_status(3)

calc_score(scene_game,stone_obj_list)
check_possible_black(scene_game,stone_obj_list)
#check_possible_white(scene_game,stone_obj_list)

startGame(scene_game)